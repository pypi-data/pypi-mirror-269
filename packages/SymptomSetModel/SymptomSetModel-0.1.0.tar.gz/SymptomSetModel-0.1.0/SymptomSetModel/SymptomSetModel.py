import pandas as pd 
import numpy as np
from scipy.special import expit,digamma,logsumexp,gammaln,betaln,expit
from scipy.stats import beta as beta_dist
from scipy.stats import dirichlet
from scipy import sparse
from scipy.optimize import fmin
from scipy.integrate import quad
import pickle
from collections.abc import Iterable
from vlpi.data.ClinicalDataset import ClinicalDataset
from .BackgroundModels import IndependentBackground,FullSetBackground,vLPIBackground
from .AffectedModel import IndependentAffectedModel
from .InferenceDataStruct import InferenceDataStruct





SMALL_FLOAT=np.finfo(np.float64).eps
MINLOG = -300.0

__version__ = "0.1.0"



class SymptomaticDiseaseModel:

	def _convert_bounds_to_beta_prior(self,lower_bound,upper_bound,CI=0.99,tol=1e-8):
		mean=lower_bound+(upper_bound-lower_bound)/2.0
		init_denom=(1.0/mean)*100
		log_a=np.log(init_denom*mean)
		log_b=np.log(init_denom-np.exp(log_a))

		f=lambda x: np.sqrt((upper_bound-beta_dist(np.exp(x[0]),np.exp(x[1])).ppf(1.0-(1.0-CI)/2.0))**2+(lower_bound-beta_dist(np.exp(x[0]),np.exp(x[1])).ppf((1.0-CI)/2.0))**2)
		output=fmin(f,np.array([log_a,log_b]),ftol=tol,disp=False)
		return np.exp(output)


	def _dirichlet_entropy(self,pvec):
		return dirichlet(pvec).entropy()

	def _beta_entropy(self,alpha,beta):
		return beta_dist(alpha,beta).entropy()
	
	def _dirichlet_log_like(self,log_prob_vec,param_vec):
		return np.sum((param_vec-1.0)*log_prob_vec)-self._multivariate_log_beta(param_vec)

	def _beta_log_like(self,log_prob_vec,param_vec):
		return np.sum((param_vec-1.0)*log_prob_vec)-betaln(*param_vec)

	def _multivariate_log_beta(self,alpha_vec):
		return np.sum(gammaln(alpha_vec))-gammaln(np.sum(alpha_vec))

	def _dirichlet_exp_logx(self,param_vec):
		return digamma(param_vec)-digamma(np.sum(param_vec))


	def __init__(self,SubjectIndex,SymptomColumns,SparseSymptomMatrix,FrequencyMinimum=None):
		"""
		A class that contains a simple model for estimating the likelihood ratio for a rare disease based on a subject's observed symptoms. This likelihood ratio can be converted into a probability by specifying a distribution/confidence interval over disease prevalence. The model generates a likelihood ratio by comparing the background symptom frequencies to the distribution of symptoms assuming that an individual is affected. This latter distribution can be derived from literature/database frequency estimates or directly estimated from a set of subjects who are highly likely to have the disease (but may not fully express due to incomplete penetrance/ascertainment errors). The class is initialized by creating a clinical dataset by passing an array of subject indices, an array of symptom columns, and a sparse binary matrix of diagnoses.
		
		Args:
		    SubjectIndex (array-like): Array of subject indices
		    SymptomColumns (array-like): Array of symptoms
		    SparseSymptomMatrix (sparse.csr_matrix): Sparse matrix of symptoms
		    FrequencyMinimum (None, optional float): Float to set the frequency minimum for the dataset. By default, 1/NumberOfSubjects is used if nothting is provided.
		
		
		"""
		assert isinstance(SparseSymptomMatrix,sparse.csr_matrix),"Symptom data matrix must be a scipy.sparse.csr_matrix."

		SymptomIndexMap=pd.Series(np.arange(SparseSymptomMatrix.shape[1]),index=SymptomColumns)
		SubjectIndex=np.array(SubjectIndex)
		assert len(set(SubjectIndex))==SubjectIndex.shape[0],"Patient indices contain duplicate columns."
		assert len(set(SymptomColumns))==SymptomColumns.shape[0],"Symptom array columns contain duplicate symptoms."


		self.clinical_dataset=ClinicalDataset(SymptomIndexMap.to_dict())
		self.clinical_dataset.LoadFromArrays(SparseSymptomMatrix,subjectIDs=SubjectIndex)
		if FrequencyMinimum is None:
			FrequencyMinimum=1.0/SubjectIndex.shape[0]
		assert (FrequencyMinimum>0.0) and (FrequencyMinimum<1.0),"Minimum dataset frequency must be between 0.0 and 1.0"
		self.DropLowFrequencySymptoms(FrequencyMinimum)
		self.CurrentBackgroundModel=None
		self.CurrentAffectedModel=None
		self.SymptomSetPosterior=None


	def DropLowFrequencySymptoms(self,min_freq):
		"""Drops all symptoms with prevelance less than min_freq from the dataset. The dataset is then re-indexed.
		
		Args:
		    min_freq (float): Minimum allowed prevalence for symptoms. 
		"""
		freqs=np.array(self.clinical_dataset.ReturnSparseDataMatrix().mean(axis=0)).ravel()
		dropped=np.where(freqs<min_freq)[0]
		allowed=np.where(freqs>=min_freq)[0]
		if dropped.shape[0]>0:
			print('{0:d} symptoms with prevalence < {1:f}. Dropping from dataset.'.format(dropped.shape[0],min_freq))
		self.clinical_dataset.ExcludeAll([self.clinical_dataset.dataIndexToDxCodeMap[s] for s in dropped])

	def BuildBackgroundModel(self,TargetSymptoms,BackgroundModelType,TrainingIndex=None,**kwargs):
		"""Builds a model for the background symptom frequencies. There are three options: 'Independent','vLPI', and 'FullSet.' They make increasingly relaxed assumptions about the correlation structure among the symptoms. Independent is simplest and likely most effective. vLPI takes the longest to build/train and is the least flexible in that it cannot be easily ported to new datasets. 
		
		Args:
		    TargetSymptoms (array-like): Array of symptoms used to build the background model. 
		    BackgroundModelType (str): Model type, must be in ['Independent','FullSet','vLPI']
		    TrainingIndex (None, optional): Index of subjects used to train the model. These can be a subset of the subjects in the dataset. If not provided, the default is to use the full set of subjects.
		    **kwargs: See BackgroundModels source code for details. Only vLPI has kwargs that can make a significant impact on model fitting. 
		"""
		assert BackgroundModelType in ['Independent','FullSet','vLPI'],"Specified Background model not allowed. Must be in ['Independent','FullSet','vLPI']."
		if len(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())):
			print('Symptoms: {0:s} are missing from ClinicalDataset. Dropping from backgound model.'.format(','.join(list(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())))))
			TargetSymptoms=list(set(TargetSymptoms).intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))

		if TrainingIndex is None:
			TrainingIndex=self.clinical_dataset.data.index
		else:
			assert len(set(TrainingIndex).difference(self.clinical_dataset.data.index))==0,"Training Index includes subjects that are missing from the dataset."

		if BackgroundModelType=='Independent':
			self.CurrentBackgroundModel = IndependentBackground(TargetSymptoms,ClinicalDataset=self.clinical_dataset,TrainingIndex=TrainingIndex,**kwargs)
		elif BackgroundModelType=='FullSet':
			self.CurrentBackgroundModel = FullSetBackground(TargetSymptoms,ClinicalDataset=self.clinical_dataset,TrainingIndex=TrainingIndex,**kwargs)
		else:
			self.CurrentBackgroundModel = vLPIBackground(TargetSymptoms,ClinicalDataset=self.clinical_dataset,TrainingIndex=TrainingIndex,**kwargs)


	def LoadBackgroundModel(self,TargetSymptoms,BackgroundModelType,FilePrefix):
		"""Loads a previously fit background model from disk. This is useful for porting models to new datasets. Note, TargetSymptoms must be a subset of the original symptoms used to fit the model for 'Independent' and 'FullSet.' For vLPI, TargetSymptoms and the original symptoms must be identical. 
		
		Args:
		    TargetSymptoms (array-like): Array of symptoms used to build the background model. 
		    BackgroundModelType (str): Model type, must be in ['Independent','FullSet','vLPI']
		    FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		assert BackgroundModelType in ['Independent','FullSet','vLPI'],"Specified Background model not allowed. Must be in ['Independent','FullSet','vLPI']."
		if len(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())):
			print('Symptoms: {0:s} are missing from ClinicalDataset. Dropping from backgound model.'.format(','.join(list(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())))))
			TargetSymptoms=list(set(TargetSymptoms).intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))
		if BackgroundModelType=='Independent':
			self.CurrentBackgroundModel = IndependentBackground(TargetSymptoms,FilePrefix=FilePrefix)
		elif BackgroundModelType=='FullSet':
			self.CurrentBackgroundModel = FullSetBackground(TargetSymptoms,FilePrefix=FilePrefix)
		else:
			self.CurrentBackgroundModel = vLPIBackground(TargetSymptoms,FilePrefix=FilePrefix)

	def SaveBackgroundModel(self,FilePrefix):
		"""Saves a background model to disk for future use. '.pth' is automatically added to the prefix. 
		
		Args:
		    FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		assert self.CurrentBackgroundModel is not None,"Must build or load a background model first."
		self.CurrentBackgroundModel.PackageModel(FilePrefix)


	def ComputeBackgroundScores(self,TargetIndex):
		"""Computes the -log(probability) of symptom diagnoses accoring to the background model. Only the index for the desired subjects needs to be provided. 
		
		Args:
		    TargetIndex (array-like): Subjects of interest
		
		Returns:
		    pd.Series: -log(probability) for the observed symptoms diagnosed in each subject. 
		"""

		assert self.CurrentBackgroundModel is not None,"Must build or load a background model first."

		assert len(set(TargetIndex).difference(self.clinical_dataset.data.index))==0,"Target Index includes subjects that are missing from the dataset."
		DxArray = self.clinical_dataset.ReturnSparseDataMatrix(index=TargetIndex).tocsr()[:,[self.clinical_dataset.dxCodeToDataIndexMap[s] for s in self.CurrentBackgroundModel.TargetSymptoms]]
		CurrentBackgroundScores=pd.Series(self.CurrentBackgroundModel.ComputeSurprisal(DxArray,self.CurrentBackgroundModel.TargetSymptoms),index=TargetIndex)
		return pd.Series(CurrentBackgroundScores,index=TargetIndex)

	def BuildAffectedModel(self,SymptomInfoTable,TrainingIndex=None):
		"""Builds a distribution over symptom sets based on frequencies reported in the literature and/or databases. This information is passed to model through SymptomInfoTable, a pandas dataframe with two columns. The first provides the probability that the symptom is correctly attributed to the disease, and the second provides disease-specific frequency information. The latter must either be a vector of length 5, which indicates the probability mass assigned to an ordinal set of frequecies ('VR', 'OC','F','VF', 'O'; see HPO for details), or a tuple containing the following information: (number of cases with symptom, total number of cases).
		
		Args:
		    SymptomInfoTable (pd.DataFrame): Disease-specific symptom frequency information. See above
		    TrainingIndex (None, optional): Index of subjects used to train the model. These can be a subset of the subjects in the dataset. If not provided, the default is to use the full set of subjects.
		"""
		if len(set(SymptomInfoTable.index).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())):
			print('Symptoms: {0:s} are missing from ClinicalDataset. Dropping from analysis.'.format(','.join(list(set(SymptomInfoTable.index).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())))))
			SymptomInfoTable=SymptomInfoTable.loc[list(set(SymptomInfoTable.index).intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))]
		if TrainingIndex is None:
			TrainingIndex=self.clinical_dataset.data.index
		else:
			assert len(set(TrainingIndex).difference(self.clinical_dataset.data.index))==0,"Training Index includes subjects that are missing from the dataset."		
		self.CurrentAffectedModel=IndependentAffectedModel(SymptomInfoTable,ClinicalDataset=self.clinical_dataset,BackgroundTrainingIndex=TrainingIndex)

	def SaveAffectedModel(self,FilePrefix):
		"""Saves an affected model to disk for future use. '.pth' is automatically added to the prefix. 
		
		Args:
		    FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		assert self.CurrentAffectedModel is not None,"Must build or load a background model first."
		self.CurrentAffectedModel.PackageModel(FilePrefix)

	def LoadAffectedModel(self,TargetSymptoms,FilePrefix):
		"""Loads a previously constructed affected model from disk. This is useful for porting models to new datasets. Note, TargetSymptoms must be a subset of the original symptoms used to build the model.
		
		Args:
		    TargetSymptoms (array-like): Array of symptoms used to build the background model. 
		    FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		if len(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())):
			print('Symptoms: {0:s} are missing from ClinicalDataset. Dropping from affected model.'.format(','.join(list(set(TargetSymptoms).difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())))))
			TargetSymptoms=list(set(TargetSymptoms).intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))
		self.CurrentAffectedModel=IndependentAffectedModel(pd.DataFrame([],columns=['A','B'],index=TargetSymptoms),FilePrefix=FilePrefix)
		

	def ComputeAffectedScores(self,TargetIndex):
		"""Computes the log(probability) of symptom diagnoses accoring to the affected model. Note, this is slightly different than what the Background models produce (-log[probability]) Only the index for the desired subjects needs to be provided. 
		
		Args:
		    TargetIndex (array-like): Subjects of interest
		
		Returns:
		    np.array: log(probability) for the observed symptoms diagnosed in each subject. 
		"""
		assert self.CurrentAffectedModel is not None,"Must build or load an affected model first."

		assert len(set(TargetIndex).difference(self.clinical_dataset.data.index))==0,"Target Index includes subjects that are missing from the dataset."	
		DxArray = self.clinical_dataset.ReturnSparseDataMatrix(index=TargetIndex).tocsr()[:,[self.clinical_dataset.dxCodeToDataIndexMap[s] for s in self.CurrentAffectedModel.SymptomInfoTable.index]]
		CurrentAffectedScores=pd.Series(self.CurrentAffectedModel.LogSetProbabilities(DxArray,self.CurrentAffectedModel.SymptomInfoTable.index),index=TargetIndex)
		return pd.Series(CurrentAffectedScores,index=TargetIndex)

	def ComputeSymptomaticDiseaseLogOdds(self,TargetIndex,usePenetranceModel=False):
		"""Computes the log-likelihood ratio of symptom set probabilities for a set of subjects defined by TargetIndex. There is an option to use a previously fit PenetranceModel to estimate these log-likelihood ratios.
		
		Args:
		   TargetIndex (array-like): Subjects of interest
		    usePenetranceModel (bool, optional): Indicates that a previously fit penetrance model should be used.
		
		Returns:
		    TYPE: Description
		"""
		assert (self.CurrentAffectedModel is not None) or (self.SymptomSetPosterior is not None),"Must use an affected model or a previously fit penetrance model..."
		assert self.CurrentBackgroundModel is not None,"Must build or load a background model first."
		if usePenetranceModel:
			assert self.SymptomSetPosterior is not None, "If using a penetrance model, it must be fit or loaded from disk."

		assert len(set(TargetIndex).difference(self.clinical_dataset.data.index))==0,"Target Index includes subjects that are missing from the dataset."	

		CurrentBackgroundScores = self.ComputeBackgroundScores(TargetIndex)

		if (usePenetranceModel==True):
			CurrentAffectedScores=self.ComputePenetranceScores(TargetIndex)
		else:
			CurrentAffectedScores = self.ComputeAffectedScores(TargetIndex)
		return CurrentAffectedScores.loc[TargetIndex]+CurrentBackgroundScores.loc[TargetIndex]


	def ComputePenetranceScores(self,TargetIndex):
		"""Given a previously fit penetrance model, computes the proability of penetrance for a set of subjects specfied by TargetIndex.
		
		Args:
		    TargetIndex (array-like): Subjects of interest
		
		Returns:
		    pd.Series: The penetrance proabilities. For asymptomatic subjects, these will essentially be zero. 
		"""
		assert (self.SymptomSetPosterior is not None),"Must fit a penetrance model first."
		assert len(set(TargetIndex).difference(self.clinical_dataset.data.index))==0,"Target Index includes subjects that are missing from the dataset."
		TargetSymptoms=set().union(*self.SymptomSetPosterior.index.drop('NEW'))


		target_dx_matrix = self.clinical_dataset.ReturnSparseDataMatrix(index=TargetIndex).tocsr()[:,[self.clinical_dataset.dxCodeToDataIndexMap[s] for s in TargetSymptoms]]
		inference_struct=InferenceDataStruct(target_dx_matrix,pd.Series(np.arange(len(TargetIndex)),index=TargetIndex), pd.Series(np.arange(len(TargetSymptoms)),index=TargetSymptoms))

		exp_log_set_probs=pd.Series(np.log(self.SymptomSetPosterior.values)-np.log(np.sum(self.SymptomSetPosterior.values)),index=self.SymptomSetPosterior.index)
		affected_scores = pd.Series(np.zeros(len(TargetIndex),dtype=np.float64),index=TargetIndex)
		symptomatic_targets= inference_struct.all_symptomatic_cases.index

		all_obs_sets = pd.Series([frozenset([inference_struct.oringal_index_map_to_dx[s] for s in x]) for x in  inference_struct.unique_symptom_sets[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets]]],index=symptomatic_targets)
		missing_sets=set(all_obs_sets.values).difference(exp_log_set_probs.index)
		for patient_id in all_obs_sets.index:
			if all_obs_sets.loc[patient_id] not in missing_sets:
				affected_scores.loc[patient_id]=exp_log_set_probs[all_obs_sets.loc[patient_id]]
			else:
				affected_scores.loc[patient_id]=exp_log_set_probs['NEW']

		asymptomatic_targets=inference_struct.all_asymptomatic_cases.index
		affected_scores.loc[asymptomatic_targets]=MINLOG
		return affected_scores





	def _update_penetrance_indicators(self,inference_struct,background_log_probs,penetrance_posterior,disease_set_posterior):
		exp_log_penetrance=self._dirichlet_exp_logx(penetrance_posterior)
		exp_log_set_probs=pd.Series(self._dirichlet_exp_logx(disease_set_posterior.values),index=disease_set_posterior.index)

		output_vector=pd.Series(np.zeros(len(background_log_probs),dtype=np.float64),index=background_log_probs.index)
		symptomatic_targets= inference_struct.all_symptomatic_cases.index


		symptomatic_log_prob_penetrant=pd.Series(np.array([exp_log_set_probs[frozenset(x)] for x in inference_struct.unique_symptom_sets[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets]]]),index=symptomatic_targets)+exp_log_penetrance[0]
		symptomatic_log_prob_nonpenetrant=pd.Series(background_log_probs.loc[symptomatic_targets].values,index=symptomatic_targets)+exp_log_penetrance[1]
		norm_consts=logsumexp(np.hstack((symptomatic_log_prob_penetrant.values.reshape(-1,1),symptomatic_log_prob_nonpenetrant.values.reshape(-1,1))),axis=-1)

		output_vector.loc[symptomatic_targets]=pd.Series(np.exp(symptomatic_log_prob_penetrant.loc[symptomatic_targets].values-norm_consts),index=symptomatic_targets)
		return output_vector		

	def _update_penetrance_posterior(self,penetrance_indicators,penetrance_prior):
		penetrance_posterior=np.zeros(2,dtype=np.float64)
		penetrance_posterior[0]+=penetrance_indicators.sum()+float(penetrance_prior[0])
		penetrance_posterior[1]+=float(penetrance_indicators.shape[0])-penetrance_indicators.sum()+float(penetrance_prior[1])
		return penetrance_posterior

	def _update_disease_set_posterior(self,penetrance_indicators,inference_struct,disease_set_prior):
		set_freq_counts=inference_struct._compute_set_based_counts(penetrance_indicators.loc[inference_struct.all_subjects]).drop('NULL')
		disease_set_posterior = pd.Series(np.zeros(len(disease_set_prior),dtype=np.float64),index=disease_set_prior.index)
		for set_indicator in set_freq_counts.index:
			disease_set_posterior[frozenset(inference_struct.unique_symptom_sets.loc[set_indicator])]=set_freq_counts.loc[set_indicator]+disease_set_prior[frozenset(inference_struct.unique_symptom_sets.loc[set_indicator])]
		disease_set_posterior.loc['NEW']=disease_set_prior.loc['NEW']
		return disease_set_posterior


	def _penetrance_model_marg_like(self,inference_struct,penetrance_indicators,background_log_probs,disease_set_posterior,penetrance_posterior,disease_set_prior,penetrance_prior):
		exp_log_penetrance=self._dirichlet_exp_logx(penetrance_posterior)
		exp_log_set_probs=pd.Series(self._dirichlet_exp_logx(disease_set_posterior.values),index=disease_set_posterior.index)

		symptomatic_targets= inference_struct.all_symptomatic_cases.index
		symptomatic_log_prob_penetrant=pd.Series(np.array([exp_log_set_probs[frozenset(x)] for x in inference_struct.unique_symptom_sets[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets]]]),index=symptomatic_targets)+exp_log_penetrance[0]
		symptomatic_log_prob_nonpenetrant=pd.Series(background_log_probs.loc[symptomatic_targets].values,index=symptomatic_targets)+exp_log_penetrance[1]

		elbo=np.sum(penetrance_indicators.loc[symptomatic_targets]*symptomatic_log_prob_penetrant.loc[symptomatic_targets]+(1.0-penetrance_indicators.loc[symptomatic_targets])*symptomatic_log_prob_nonpenetrant.loc[symptomatic_targets])

		asymptomatic_targets=inference_struct.all_asymptomatic_cases.index
		elbo+=float(len(asymptomatic_targets))*exp_log_penetrance[1]



		elbo+=self._beta_log_like(exp_log_penetrance,penetrance_prior)
		elbo+=self._dirichlet_log_like(exp_log_set_probs.values,disease_set_prior)

		elbo+=-1.0*np.sum(penetrance_indicators.loc[symptomatic_targets]*np.log(penetrance_indicators.loc[symptomatic_targets])+(1.0-penetrance_indicators.loc[symptomatic_targets])*np.log(1.0-penetrance_indicators.loc[symptomatic_targets]))
		elbo+=self._beta_entropy(penetrance_posterior[0],penetrance_posterior[1])
		elbo+=self._dirichlet_entropy(disease_set_posterior)

		return elbo



	def FitPenetranceModel(self,TargetIndex,PentrancePriorParameters=[1.0,1.0],error_tol=1e-8,max_iter=200,disease_set_contration_prior=1.0):
		"""Using a set of subjects with a high-likelihood for being affected by a rare diseae (provided by TargetIndex), this function fits a statistic model that predicts the probability that each subject's symptoms were generated by the disease of interest, rather than simple background noise. As a by-product, two distributions are inferred: 1) a beta distribution over the probability that a subject in this target set is affected with the disease (penetrnace posterior), and 2) a dirichlet distribution over the sets of observed symptoms (previously unseen symptoms fall under the set labeled 'NEW'). This latter distributions, when combined with a background model, can be used to predict the probability that a subject is affected by a disease. When using pathogenic variant carriers to fit this model, the estimates produced represent penetrance, and fitting this function can be viewed as optimizing the penetrance for a set of rare variant carriers. The model is fit using a Variational Bayes inference strategy. 
		
		Args:
		    TargetIndex (array-like): Subjects of interest. These should have a very high probability of actually having the disease in order for the model to be useful. 
		    PentrancePriorParameters (list, optional): Parameters specifying a beta prior over penetrance. Default is uniform: [1.0,1.0]
		    error_tol (float, optional): Error threshold in the likelihood used to determine convergence. Default is 1e-8
		    max_iter (int, optional): Maximum number of iteractions for fitting. Convergence usually happens within 10-20 iterations. 
		    disease_set_contration_prior (float, optional): Default is 1.0, meaning that by default a uniform distribution is assumed over observed symptom sets. Without any additional information, a simple independent background model is recovered.
		
		Returns:
		    (pd.Series, np.array): Returns tuple that contains: 1) the affected-status probabilties for the TargetSubjects (penetrance) and 2) the posterior distribution over the prior probability of being affected. Note, the symptom set probabilities are stored within the class as self.SymptomSetPosterior.
		"""
		assert isinstance(PentrancePriorParameters,Iterable),"PentrancePriorParameters must be a list-like structure of length 2"
		assert len(PentrancePriorParameters)==2,"PentrancePriorParameters must be a list-like structure of length 2"


		assert self.CurrentBackgroundModel is not None,"Must build or load a background model first."


		background_log_probs = -1.0*self.ComputeBackgroundScores(TargetIndex)

		target_dx_matrix = self.clinical_dataset.ReturnSparseDataMatrix(index=TargetIndex).tocsr()[:,[self.clinical_dataset.dxCodeToDataIndexMap[s] for s in self.CurrentBackgroundModel.TargetSymptoms]]

		set_based_inference_struct=InferenceDataStruct(target_dx_matrix,pd.Series(np.arange(len(TargetIndex)),index=TargetIndex), pd.Series(np.arange(len(self.CurrentBackgroundModel.TargetSymptoms)),index=self.CurrentBackgroundModel.TargetSymptoms))

		penetrance_prior=np.array(PentrancePriorParameters,dtype=np.float64)

		penetrance_posterior=np.zeros(2,dtype=np.float64)
		penetrance_posterior[:]=penetrance_prior[:]

		disease_set_prior = pd.Series(np.ones(len(set_based_inference_struct.unique_symptom_sets)+1,dtype=np.float64)*disease_set_contration_prior,index=[frozenset(x) for x in set_based_inference_struct.unique_symptom_sets.values]+['NEW'])

		disease_set_posterior = pd.Series(np.ones(len(set_based_inference_struct.unique_symptom_sets)+1,dtype=np.float64)*disease_set_contration_prior,index=[frozenset(x) for x in set_based_inference_struct.unique_symptom_sets.values]+['NEW'])

		penetrance_indicators = self._update_penetrance_indicators(set_based_inference_struct,background_log_probs,penetrance_posterior,disease_set_posterior)
		penetrance_posterior=self._update_penetrance_posterior(penetrance_indicators,penetrance_prior)
		disease_set_posterior=self._update_disease_set_posterior(penetrance_indicators,set_based_inference_struct,disease_set_prior)

		elbo=self._penetrance_model_marg_like(set_based_inference_struct,penetrance_indicators,background_log_probs,disease_set_posterior,penetrance_posterior,disease_set_prior,penetrance_prior)

		prev_elbo=elbo
		for fit_iter in range(1,max_iter):
			penetrance_indicators = self._update_penetrance_indicators(set_based_inference_struct,background_log_probs,penetrance_posterior,disease_set_posterior)
			penetrance_posterior=self._update_penetrance_posterior(penetrance_indicators,penetrance_prior)
			disease_set_posterior=self._update_disease_set_posterior(penetrance_indicators,set_based_inference_struct,disease_set_prior)

			elbo=self._penetrance_model_marg_like(set_based_inference_struct,penetrance_indicators,background_log_probs,disease_set_posterior,penetrance_posterior,disease_set_prior,penetrance_prior)


			error=(elbo-prev_elbo)/np.abs(elbo)
			if error<=error_tol:
				print('Inference complete. Final ELBO (Error): {0:f} ({1:e}).'.format(elbo,error))
				break
			else:
				prev_elbo=elbo
				print('Completed {0:d} iterations. Current ELBO (Error): {1:f} ({2:e})'.format(fit_iter+1,elbo,error))	

		self.SymptomSetPosterior=pd.Series(disease_set_posterior.values,index=[frozenset([set_based_inference_struct.oringal_index_map_to_dx[x] for x in set_index]) if set_index!='NEW' else 'NEW' for set_index in disease_set_posterior.index])

		return penetrance_indicators,penetrance_posterior


	def SavePenetranceModel(self,FilePrefix):

		"""Writes the penetrance model to disk using pickle.
		
		Args:
		     FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		model_dict={'SymptomSetPosterior':self.SymptomSetPosterior}
		with open(FilePrefix+'.pth','wb') as f:
			pickle.dump(model_dict,f)

	def LoadPenetranceModel(self,FilePrefix):
		"""Loads a previously fit penetrance model from disk.
		
		Args:
		    FilePrefix (str): Path to the stored model. Note, '.pth' is automatically added (hence prefix)
		"""
		with open(FilePrefix+'.pth','rb') as f:
			model_dict=pickle.load(f)
		self.SymptomSetPosterior=model_dict['SymptomSetPosterior']
		model_symptoms=set().union(*self.SymptomSetPosterior.index.drop('NEW'))
		assert len(set(model_symptoms).intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))>0,"There must be some overlap between SymptomSetPosterior and the diagnostic codes in the clinical dataset."

		missing_symptoms = model_symptoms.difference(self.clinical_dataset.dxCodeToDataIndexMap.keys())

		if len(missing_symptoms)>0:
			TargetSymptoms=list(model_symptoms.intersection(self.clinical_dataset.dxCodeToDataIndexMap.keys()))
			new_index=set([x.intersection(TargetSymptoms) for x in self.SymptomSetPosterior.index.drop('NEW')])
			if frozenset([]) in new_index:
				new_index.remove(frozenset([]))
			new_index = list(new_index)+['NEW']
			modified_symptom_set=pd.Series(np.zeros(len(new_index),dtype=np.float64),index=new_index)
			for sset in self.SymptomSetPosterior.index:
				if sset!='NEW':
					new_sset = frozenset(sset.intersection(TargetSymptoms))
					if len(new_sset)>0:
						modified_symptom_set[new_sset]+=self.SymptomSetPosterior[sset]
				else:
					modified_symptom_set[sset]+=self.SymptomSetPosterior[sset]
			self.SymptomSetPosterior=modified_symptom_set.copy()



	def _predict_affected_indicators(self,log_odds,freq_dist_params):
		indicators = pd.Series(np.zeros(log_odds.shape[0]),index=log_odds.index)
		for p_id in log_odds.index:
			if log_odds.loc[p_id]>np.log(SMALL_FLOAT):
				prob_func=lambda x: expit(np.log(x)-np.log(1.0-x)+log_odds.loc[p_id])*beta_dist(*freq_dist_params).pdf(x)
				int_output=quad(prob_func,0.0,1.0,epsabs=1e-8)
				indicators.loc[p_id]=int_output[0]
		return indicators


	def PredictAffectedStatus(self,TargetIndex,PrevalencePriorCI=None,PrevalenceDistributionParameters=None,usePenetranceModel=False,CI=0.99):
		"""Summary
		
		Args:
		    TargetIndex (array-like): Subjects of interest. 
		    PrevalencePriorCI (None, array-like of length 2): Tuple that specifies the upper and lower bound for the confidence interval over prevalance.  
		    PrevalenceDistributionParameters (None, array-like of length 2): Instead of specifying the confidence interval, a beta distribution over prevalence can instead be specified. This is useful for debugging but not practically useful.
		    usePenetranceModel (bool, optional): Indicates whether to use a previously fit penentrance model or a simple affected model based on literature-reported frequencies. 
		    CI (float, optional): Size of the confidence interval. Default is 99% (0.99)
		
		Returns:
		    pd.Series: Array of probabilites indicating affected status. 
		"""
		assert (PrevalenceDistributionParameters is not None) or (PrevalencePriorCI is not None), "Must provide either posterior distribution parameters for prevalence, or a confidence interval for the range of prevalence values"

		if PrevalencePriorCI is not None:
			assert isinstance(PrevalencePriorCI,Iterable),"PrevalencePriorCI must be a list-like structure of length 2"
			assert len(PrevalencePriorCI)==2,"PrevalencePriorCI must be a list-like structure of length 2"
			assert (CI>0.0) and CI<(1.0), "Bounds for prior CI must be between 0 and 1"	
			assert (PrevalencePriorCI[0]>0.0) and (PrevalencePriorCI[1]<1.0) and (PrevalencePriorCI[1]>PrevalencePriorCI[0]),"PrevalencePriorCI must define an interval in (0,1)"
			PrevalenceDistributionParameters=self._convert_bounds_to_beta_prior(PrevalencePriorCI[0],PrevalencePriorCI[1],CI=CI)
		else:
			assert isinstance(PrevalenceDistributionParameters,Iterable),"PrevalencePosterior must be a list-like structure of length 2"
			assert (PrevalenceDistributionParameters[0]>0.0) and (PrevalenceDistributionParameters[1]>0.0),"PrevalencePosterior parameters must be > 0"

		assert self.CurrentBackgroundModel is not None,"Must build or load a background model first."
		assert (self.CurrentAffectedModel is not None) or (self.SymptomSetPosterior is not None),"Must use an affected model or a previously fit penetrance model..."

		if usePenetranceModel==True:
			assert (self.SymptomSetPosterior is not None),"Must fit a penetrance model first."
			print("Predicting affected status using a previously fit penetrance model...")	
			symptomatic_log_odds = self.ComputeSymptomaticDiseaseLogOdds(TargetIndex,usePenetranceModel=usePenetranceModel)

		else:
			print("Predicting affected status using a literature derived symptom frequencies...")
			symptomatic_log_odds = self.ComputeSymptomaticDiseaseLogOdds(TargetIndex,usePenetranceModel=usePenetranceModel)

		return self._predict_affected_indicators(symptomatic_log_odds,PrevalenceDistributionParameters)


