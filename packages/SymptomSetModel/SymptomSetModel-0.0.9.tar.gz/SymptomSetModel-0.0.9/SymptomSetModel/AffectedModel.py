import pandas as pd 
import numpy as np
from scipy import sparse
from scipy.special import betaln,logsumexp,gammaln,logsumexp,comb
from .BackgroundModels import IndependentBackground
from PiecewiseBeta.PiecewiseBeta import PiecewiseBeta
from collections.abc import Iterable
import pickle
import copy

SMALL_FLOAT=np.finfo(np.float64).eps
MINLOG = np.log(SMALL_FLOAT)

class IndependentAffectedModel:

	def _multivariate_log_beta(self,alpha_vec):
		return np.sum(gammaln(alpha_vec))-gammaln(np.sum(alpha_vec))


	def _simple_beta_marg_like(self,a,b,successes,failures):
		return betaln(a+successes,b+failures)-betaln(a,b)
	
	def _dirichlet_marg_like(self,obs_vec,pvec):
		prior_norm_const=self._multivariate_log_beta(pvec)
		posterior_norm_const=np.sum(gammaln(pvec+obs_vec))-gammaln(np.sum(pvec+obs_vec))
		return posterior_norm_const-prior_norm_const

	def _symptom_log_marginals_beta_pieces(self,segment_probs):

		segment_probs=np.array(segment_probs)
		segment_probs/=segment_probs.sum()

		pbeta=PiecewiseBeta(self.piecewise_beta_cut_points,self.symptom_frequency_prior_params[0],self.symptom_frequency_prior_params[1])

		log_symptom_freq=pbeta.MarginalLogLikelihood(segment_probs,1,1)
		
		return np.exp(log_symptom_freq)

	def _symptom_log_marginals_counts(self,successes, total):

		log_symptom_freq=self._simple_beta_marg_like(self.symptom_frequency_prior_params[0]+successes,self.symptom_frequency_prior_params[1]+total-successes,1,0)

		return np.exp(log_symptom_freq)

	def _process_freq_info(self,dx,freq_info):

		if isinstance(freq_info,tuple):
			assert len(freq_info)==2,"Frequency information for HPO {0:s} data type 'tuple' does not match expectations. Must have two entries.".format(dx)
			assert freq_info[1]>=freq_info[0],"Frequency counts for HPO {0:s} are improper. Must be in (successes, total) format."
			return self._symptom_log_marginals_counts(freq_info[0],freq_info[1]),False
		elif isinstance(freq_info,Iterable):
			freq_info=np.array(freq_info)
			assert len(freq_info)==(self.piecewise_beta_cut_points.shape[0]-1),"Frequency information for Symptom {0:s} data type 'frequency classes' does not match expectations. Number of entries must match provided beta distribution cut points".format(dx)
			return self._symptom_log_marginals_beta_pieces(freq_info),True
		else: 
			raise ValueError("Error in frequency informaton for HPO {0:s}. Frequency information must either be a tuple of length 2 or a vector of frequency classes.".format(dx))

	def __init__(self,AnnotatedSymptomInformation,FilePrefix=None, ClinicalDataset=None,BackgroundTrainingIndex=None,verbose=False,symptom_frequency_prior_params=[0.5,0.5],piecewise_beta_cut_points=[0.0,0.04,0.3,0.8,0.99,1.0]):
		"""
		Uses literature/database-derived symptom frequency estimates to produce a distribution over symptom-set frequencies among affected individuals. To do so, it makes the strong (and false) assumption that symptoms occur independently.

		Args:
		    AnnotatedSymptomInformation (pd.DataFrame): A pandas.DataFrame with two columns and S rows, where S denotes the number of symptoms annotated to the disease. The two columns contain: 1) the annotation probability and 2) the symptom-set frequency information. The latter must either be a vector of length 5, which indicates the probability mass assigned to an ordinal set of frequecies ('VR', 'OC','F','VF', 'O'; see HPO for details), or a tuple containing the following information (number of cases with symptom, total number of cases).
		    FilePrefix (None, optional): FilePrefix to load previously contructed model.
		    ClinicalDataset (vlpi.data.ClinicalDataset): ClinicalDataset that stores diagnositic information. Only requred if building a new model (used to fit background symptom frequencies).
		    BackgroundTrainingIndex (None, 1-d iterable): Index of patients used to build the background frequencies. Must overlap with the subject index in ClinicalDataset.
		    symptom_frequency_prior_params (list, optional): Parameters of beta prior distribution used to compute the expected symptom frequency from the literature/database data. Has minimal impact on model unless very strong prior is provided. Default is (alpha=0.5, beta=0.5). 
		    piecewise_beta_cut_points (list, optional): Cut-points for a piecewise distribution over symptom frequency. The default cut-points match those defined in the HPO. This should not generally be modifed. 
		
		Raises:
		    ValueError: See source code.

		
		"""
		assert (ClinicalDataset is not None) or (FilePrefix is not None), "Must provide either file path for model or a ClinicalDatset. Note, if fitting model from new ClinicalDataset, a TrainingIndex must be used."
		if (ClinicalDataset is not None):
			assert (BackgroundTrainingIndex is not None), "Must provide a TrainingIndex if fitting a new model."
			assert isinstance(AnnotatedSymptomInformation, pd.DataFrame),"Annotated symptom information must be a pandas.DataFrame."
			assert len(AnnotatedSymptomInformation.columns)==2,"AnnotatedSymptomInformation must contain at least two columns. The first must contain the probability that the symptom is correctly annotated, and the second should specify a prior distribution over symptom frequency."

			if len(AnnotatedSymptomInformation.index.difference(ClinicalDataset.dxCodeToDataIndexMap.keys())):
				print("Symptoms {0:s} were not observed in the dataset. Dropping them from the IndependentAffectedModel.".format(','.join(AnnotatedSymptomInformation.index.difference(ClinicalDataset.dxCodeToDataIndexMap.keys()))))
				observed_symptoms=list(set(ClinicalDataset.dxCodeToDataIndexMap.keys()).intersection(AnnotatedSymptomInformation.index))
				if len(observed_symptoms):
					AnnotatedSymptomInformation=AnnotatedSymptomInformation.loc[observed_symptoms]
				else:
					raise ValueError("No rare disease symptoms were observed in the dataset. Unable to build model.")

			self.SymptomInfoTable=pd.DataFrame([],columns=['AnnotProb','IsPiecewise','FreqPrior','SymptomFreq'],index=AnnotatedSymptomInformation.index)
			self.SymptomInfoTable=self.SymptomInfoTable.astype({"AnnotProb": float, "IsPiecewise": bool,'SymptomFreq':float})
			self.symptom_frequency_prior_params=symptom_frequency_prior_params
			self.piecewise_beta_cut_points=np.array(piecewise_beta_cut_points)

			for dx,annot_info in AnnotatedSymptomInformation.iterrows():
				rate=annot_info.iloc[0]
				freq_prior=annot_info.iloc[1]
				output=self._process_freq_info(dx,freq_prior)
				self.SymptomInfoTable.at[dx,'FreqPrior']=freq_prior
				self.SymptomInfoTable.loc[dx,'AnnotProb']=rate
				self.SymptomInfoTable.loc[dx,'IsPiecewise']=output[1]			
				self.SymptomInfoTable.loc[dx,'SymptomFreq']=output[0]

			BackgroundFrequencies=IndependentBackground(self.SymptomInfoTable.index,ClinicalDataset=ClinicalDataset,TrainingIndex=BackgroundTrainingIndex)
			annot_prob_vec = np.exp(np.array([np.log(self.SymptomInfoTable.loc[x,'AnnotProb']) for x in self.SymptomInfoTable.index]))
			associated_symptom_freq = np.array([self.SymptomInfoTable.loc[x,'SymptomFreq'] for x in self.SymptomInfoTable.index])
			background_symptom_freq = np.exp(np.array([-BackgroundFrequencies.SymptomPresentWeights.loc[x] for x in self.SymptomInfoTable.index]))

			self.SymptomPresentLogProbs = pd.Series(np.log(annot_prob_vec*(associated_symptom_freq)+(1.0-annot_prob_vec)*background_symptom_freq),index=self.SymptomInfoTable.index)
			self.SymptomAbsentLogProbs = pd.Series(np.log(1.0-np.exp(self.SymptomPresentLogProbs.values)),index=self.SymptomInfoTable.index)
		else:
			self.LoadModel(FilePrefix,AnnotatedSymptomInformation.index)

	def LogSetProbabilities(self,DxArray,SymptomColumns):
		"""Given a binary array of diagnoses and a 1-d iterable of SymptomColumns, produces a per-subject log-likelihood estimate for the symptoms. 
		
		Args:
		    DxArray (np.array or sparse.csr_matrix): Binary array of diagnoses.
		    SymptomColumns  (1-d iterable): List/array of symptom labels for columns of DxArray. Provided in case model is being applied to dataset with different column ordering. 
		
		Returns:
		    np.array: Array of log-likelihoods for DxArray
		"""

		if len(DxArray.shape)==1:
			DxArray=DxArray.reshape(1,-1)

		assert len(set(SymptomColumns).intersection(self.SymptomPresentLogProbs.index))>0,"DxArray must contain some symptom overlap with IndependentBackground model."
		SymptomColumns=list(SymptomColumns)
		new_symptom_columns = list(set(SymptomColumns).intersection(self.SymptomPresentLogProbs.index))
		new_dx_array = DxArray[:,[SymptomColumns.index(s) for s in new_symptom_columns]]


		if isinstance(DxArray,sparse.csr_matrix):
			DxArray=DxArray.toarray()

		pos_weight_vec = np.array([self.SymptomPresentLogProbs[s] for s in SymptomColumns])
		neg_weight_vec = np.array([self.SymptomAbsentLogProbs[s] for s in SymptomColumns])

		pos_component = (pos_weight_vec*DxArray).sum(axis=1)
		neg_component = (neg_weight_vec*(1-DxArray)).sum(axis=1)
		return pos_component+neg_component

	def PackageModel(self,FilePrefix):
		"""Writes model to disk using pickle.
		
		Args:
		     (str): Path for model file. 
		"""
		model_dict={'SymptomPresentLogProbs':self.SymptomPresentLogProbs,'SymptomAbsentLogProbs':self.SymptomAbsentLogProbs,'SymptomInfoTable':self.SymptomInfoTable,'symptom_frequency_prior_params':self.symptom_frequency_prior_params,'piecewise_beta_cut_points':self.piecewise_beta_cut_points}
		with open(FilePrefix+'.pth','wb') as f:
			pickle.dump(model_dict,f)

	def LoadModel(self,FilePrefix,TargetSymptoms):
		"""Loads a previously fit model. 
		
		Args:
		    FilePrefix (str): Path to model fil. 
		"""
		with open(FilePrefix+'.pth','rb') as f:
			model_dict=pickle.load(f)

		self.SymptomPresentLogProbs=model_dict['SymptomPresentLogProbs']
		self.SymptomAbsentLogProbs=model_dict['SymptomAbsentLogProbs']
		self.SymptomInfoTable=model_dict['SymptomInfoTable']
		self.symptom_frequency_prior_params=model_dict['symptom_frequency_prior_params']
		self.piecewise_beta_cut_points=model_dict['piecewise_beta_cut_points']		

		self.SymptomPresentLogProbs=self.SymptomPresentLogProbs.loc[self.SymptomPresentLogProbs.index.intersection(TargetSymptoms)]
		self.SymptomAbsentLogProbs=self.SymptomAbsentLogProbs.loc[self.SymptomAbsentLogProbs.index.intersection(TargetSymptoms)]
		self.SymptomInfoTable=self.SymptomInfoTable.loc[self.SymptomInfoTable.index.intersection(TargetSymptoms)]



