import pandas as pd 
import numpy as np
from scipy import sparse
from .InferenceDataStruct import InferenceDataStruct
from vlpi.data.ClinicalDataset import ClinicalDatasetSampler,ClinicalDataset
from vlpi.vLPI import vLPI
import pickle
import copy

class IndependentBackground:

	def __init__(self,TargetSymptoms,FilePrefix=None,ClinicalDataset=None,TrainingIndex=None,**kwargs):


		"""Initiates and fits the PheRS Background model, which computes symptom set log-probabilities assuming that all symptoms occur independently. 
		
		Args:
		    TargetSymptoms (1-d iterable): List of symptoms for model. 
		    FilePrefix (None, optional str): Path to file storing previously fit model. Note, model will be adjusted based on the TargetSymptoms provided.
		    ClinicalDataset (None, vlpi.data.ClinicalDataset): ClinicalDataset that stores the diagnositic information. Only requred if building a new model.
		    TrainingIndex (None, 1-d iterable): List/array of subject indices to use for training. Only required if building a new model.
		    **kwargs: 
		    	CountPrior: Smoothing count for symptom frequencies. Defaul is 1.0
		"""
		self.TargetSymptoms=np.array(TargetSymptoms)
		assert (ClinicalDataset is not None) or (FilePrefix is not None), "Must provide either file path for model or a ClinicalDatset. Note, if fitting model from new ClinicalDataset, a TrainingIndex must be used."
		if (ClinicalDataset is not None):
			assert (TrainingIndex is not None), "Must provide a TrainingIndex if fitting a new model."
			if 'CountPrior' in kwargs.keys():
				self.CountPrior=kwargs['CountPrior']
			else:
				self.CountPrior=1.0

			training_dx_matrix = ClinicalDataset.ReturnSparseDataMatrix(index=TrainingIndex).tocsr()[:,[ClinicalDataset.dxCodeToDataIndexMap[s] for s in TargetSymptoms]].toarray()
			self.SymptomPresentWeights = -np.log((training_dx_matrix.sum(axis=0).ravel()+self.CountPrior)/(training_dx_matrix.shape[0]+self.CountPrior*2))
			self.SymptomPresentWeights = pd.Series(self.SymptomPresentWeights,index=TargetSymptoms)

			self.SymptomAbsentWeights = -np.log(((1.0-training_dx_matrix).sum(axis=0).ravel()+self.CountPrior)/(training_dx_matrix.shape[0]+self.CountPrior*2))
			self.SymptomAbsentWeights = pd.Series(self.SymptomAbsentWeights,index=TargetSymptoms)

		else:
			self.LoadModel(FilePrefix, self.TargetSymptoms)


	def ComputeSurprisal(self,DxArray,SymptomColumns):
		"""Computes the surprisals (-1*log[prob]) for a binary array of diagnoses.
		
		Args:
		    DxArray (np.array or sparse.csr_matrix): Binary array of diagnoses.
		    SymptomColumns (optional, 1-d iterable): List/array of symptom labels for columns of DxArray. This is provided in case the model is being applied to dataset with different symptoms/column ordering. 
	
		
		Returns:
		    np.array: Array of suprisals for DxArray
		"""
		if len(DxArray.shape)==1:
			DxArray=DxArray.reshape(1,-1)

		assert len(set(SymptomColumns).intersection(self.SymptomPresentWeights.index))>0,"DxArray must contain some symptom overlap with IndependentBackground model."
		SymptomColumns=list(SymptomColumns)
		new_symptom_columns = list(set(SymptomColumns).intersection(self.SymptomPresentWeights.index))
		new_dx_array = DxArray[:,[SymptomColumns.index(s) for s in new_symptom_columns]]

		if isinstance(new_dx_array,sparse.csr_matrix):
			new_dx_array=new_dx_array.toarray()

		pos_weight_vec = np.array([self.SymptomPresentWeights[s] for s in new_symptom_columns])
		neg_weight_vec = np.array([self.SymptomAbsentWeights[s] for s in new_symptom_columns])

		pos_component = (pos_weight_vec*new_dx_array).sum(axis=1)
		neg_component = (neg_weight_vec*(1-new_dx_array)).sum(axis=1)
		return pos_component+neg_component

	def PackageModel(self,FilePrefix):
		"""Writes model to disk using pickle.
		
		Args:
		     (str): Path for model file. 
		"""
		model_dict={'SymptomPresentWeights':self.SymptomPresentWeights,'SymptomAbsentWeights':self.SymptomAbsentWeights,'CountPrior':self.CountPrior}
		with open(FilePrefix+'.pth','wb') as f:
			pickle.dump(model_dict,f)

	def LoadModel(self,FilePrefix,TargetSymptoms):
		"""Loads a previously fit model. Only the intersection of the TargetSymptoms and stored symptoms are loaded.
		
		Args:
		    FilePrefix (str): Path to model fil. 
		"""
		with open(FilePrefix+'.pth','rb') as f:
			model_dict=pickle.load(f)
		self.SymptomPresentWeights=model_dict['SymptomPresentWeights']
		self.SymptomAbsentWeights=model_dict['SymptomAbsentWeights']
		self.CountPrior=model_dict['CountPrior']

		self.SymptomPresentWeights=self.SymptomPresentWeights.loc[self.SymptomPresentWeights.index.intersection(TargetSymptoms)]
		self.SymptomAbsentWeights=self.SymptomAbsentWeights.loc[self.SymptomAbsentWeights.index.intersection(TargetSymptoms)]


class vLPIBackground:

	def __init__(self,TargetSymptoms,FilePrefix=None,ClinicalDataset=None,TrainingIndex=None,**kwargs):

		"""
		Initiates and fits the VAE Background model, which uses a variational autoencoder to compute the symptom set probabilities for symptomatic cases. Note, this model is much more complicated and less flexible than the other models. 

		Args:
		    TargetSymptoms (1-d iterable): List of symptoms for model. 
		    FilePrefix (None, optional str): Path to file storing previously fit model. 
		    ClinicalDataset (None, vlpi.data.ClinicalDataset): ClinicalDataset that stores the diagnositic information. Only requred if building a new model.
		    TrainingIndex (None, 1-d iterable): List/array of subject indices to use for training. Only required if building a new model.
		   	**kwargs: 
				TrainingFraction: float, optional
					Fraction of dataset to use for training. Must be between 0 and 1. The remainder is used for validation. Default is 0.75.

				nLatentDim: int, optional
					Specifies the number of latent dimesions for the VAE model. Default is 10. 
	
				batch_size: int, optional
					Number of samples included in each batch during stochastic inference. Default is 1024. 

			    maxLearningRate: float, optional
		            Specifies the maximum learning rate used during inference. Default is 0.04

		        errorTol: float, optional
		            Error tolerance in ELBO (computed on held out validation data) to determine convergence. Default is 0.5/# of training samples. 

		        numParticles: int, optional
		            Number of particles (ie random samples) used to approximate gradient. Default is 1. Computational cost increases linearly with value.

		        maxEpochs: int, optional
		            Maximum number of epochs (passes through training data) for inference. Note, because annealing and learning rate updates depend on maxEpochs, this offers a simple way to adjust the speed at which these values change. Default is 500. 

		        computeDevice: int or None, optional
		            Specifies compute device for inference. Default is None, which instructs algorithm to use cpu. If integer is provided, then algorithm will be assigned to that integer valued gpu.

		        numDataLoaders: int
		            Specifies the number of threads used to process data and prepare for upload into the gpu. Note, due to the speed of gpu, inference can become limited by data transfer speed, hence the use of multiple DataLoaders to improve this bottleneck. Default is 0, meaning just the dedicated cpu performs data transfer.

		        OneCycleParams: dict with keys 'pctCycleIncrease','initLRDivisionFactor','finalLRDivisionFactor'
		            Parameters specifying the One-Cycle learning rate adjustment strategy, which helps to enable good anytime performance.
		            pctCycleIncrease--fraction of inference epochs used for increasing learning rate. Default: 0.1
		            initLRDivisionFactor--initial learning rate acheived by dividing maxLearningRate by this value. Default: 25.0
		            finalLRDivisionFactor--final learning rate acheived by dividing maxLearningRate by this value. Default: 1e4


		        KLAnnealingParams: dict with keys 'initialTemp','maxTemp','fractionalDuration','schedule'
		            Parameters that define KL-Annealing strategy used during inference, important for avoiding local optima. Note, annealing is only used for computation of ELBO and gradients on training data. Validation data ELBO evaluation, used to monitor convergence, is performed at the maximum desired temperature (typically 1.0, equivalent to standard variational inference). Therefore, it is possible for the model to converge even when the temperature hasn't reached it's final value. It's possible that further cooling would find a better optimum, but this is highly unlikely in practice.
		            initialTemp--initial temperature during inference. Default: 0.0
		            maxTemp--final temperature obtained during inference. Default: 1.0 (standard variational inference)
		            fractionalDuration--fraction of inference epochs used for annealing. Default is 0.25
		            schedule--function used to change temperature during inference. Defualt is 'cosine'. Options: 'cosine','linear'

		        'OpimizationStrategy': str, optional
		            Specifies a strategry for optimization. Options include: 'Full','DecoderOnly','EncoderOnly'. Useful for debugging. Default is 'Full'
		
		"""
		self.TargetSymptoms=np.array(TargetSymptoms)
		assert (ClinicalDataset is not None) or (FilePrefix is not None), "Must provide either file path for model or a ClinicalDatset. Note, if fitting model from new ClinicalDataset, a TrainingIndex must be used."

		if 'TrainingFraction' in kwargs.keys():
			self.TrainingFraction=kwargs['TrainingFraction']
			del kwargs['TrainingFraction']
		else:
			self.TrainingFraction=0.75

		if (ClinicalDataset is not None):

			assert (TrainingIndex is not None), "Must provide a TrainingIndex if fitting a new model."


			if 'nLatentDim' in kwargs.keys():
				self.nLatentDim=kwargs['nLatentDim']
				del kwargs['nLatentDim']
			else:
				self.nLatentDim=10
				

			if 'batch_size' in kwargs.keys():
				batch_size=kwargs['batch_size']
				del kwargs['batch_size']
			else:
				batch_size=1024
				

			if 'verbose' in kwargs.keys():
				verbose=kwargs['verbose']
				del kwargs['verbose']
			else:
				verbose=True
				


			self.local_clinical_dataset=copy.deepcopy(ClinicalDataset)
			self.local_clinical_dataset.IncludeOnly(TargetSymptoms)
			self.local_clinical_dataset.data.drop(self.local_clinical_dataset.data.index.difference(TrainingIndex),inplace=True)

			if 'errorTol' not in kwargs.keys():
				kwargs['errorTol']=0.5/len(TrainingIndex)

			if 'maxEpochs' not in kwargs.keys():
				kwargs['maxEpochs']=500


			self.sampler = ClinicalDatasetSampler(self.local_clinical_dataset,self.TrainingFraction,returnArrays='Torch')
			self.vlpiModel= vLPI(self.sampler,self.nLatentDim)
			self.InferenceOutput = self.vlpiModel.FitModel(batch_size=batch_size,verbose=verbose,**kwargs)
		else:
			self.LoadModel(FilePrefix)

	def ComputeSurprisal(self,DxArray,SymptomColumns,numParticles=50):
		"""Computes the surprisals (-1*log[prob]) for a binary array of diagnoses. Unlike the other models, the SymptomColumns provided and the TargetSymptoms used to fit the model must match exactly. This makes the model much less flexible. 
		
		Args:
		    DxArray (np.array or sparse.csr_matrix): Binary array of diagnoses.
		    SymptomColumns  (1-d iterable): List/array of symptom labels for columns of DxArray. Provided in case model is being applied to dataset with different column ordering. 
		
		Returns:
		    np.array: Array of suprisals for DxArray
		"""		
		if len(DxArray.shape)==1:
			DxArray=DxArray.reshape(1,-1)
		assert DxArray.shape[1]==self.local_clinical_dataset.numDxCodes,"Diagnostic array has a different number of symptoms than the vLPIBackground model. Unable to use."
		assert lent(set(SymptomColumns).symmetric_difference(self.local_clinical_dataset.dxCodeToDataIndexMap.keys()))==0,"Data array and vLPIBackground model must contain identical symptoms."

		if isinstance(DxArray,sparse.csr_matrix):
			DxArray=DxArray.toarray()

		SymptomColumns=list(SymptomColumns)
		output=np.zeros(DxArray.shape[0])
		input_arrays = (DxArray[:,[SymptomColumns.index(s) for s in self.local_clinical_dataset.dxCodeToDataIndexMap.keys()]],[])

		symptomatic_set_surpisal=self.vlpiModel.ComputeSurprisal(dataArrays=input_arrays,numParticles=numParticles).ravel()
		return symptomatic_set_surpisal



	def PackageModel(self,FilePrefix):
		"""Writes model to disk using pickle. Note, multiple files are created to store the required information. 
		
		Args:
		    FilePrefix (str): Prefix for model files.  
		"""	
		self.local_clinical_dataset.WriteToDisk(FilePrefix+'_ClinicalDataset.pth')
		self.sampler.WriteToDisk(FilePrefix+'_ClinicalSampler.pth')
		self.vlpiModel.PackageModel(fName=FilePrefix+'_FittedModel.pth')
		aux_model_dict={}
		aux_model_dict['nLatentDim']=self.nLatentDim
		aux_model_dict['TrainingFraction']=self.TrainingFraction
		aux_model_dict['InferenceOutput']=self.InferenceOutput
		with open(FilePrefix+'_AuxInfo.pth','wb') as f:
			pickle.dump(aux_model_dict,f)	

	def LoadModel(self,FilePrefix):
		"""Loads a previously fit model. 
		
		Args:
		    FilePrefix (str): Prefix for paths to model file. 
		"""
		with open(FilePrefix+'_AuxInfo.pth','rb') as f:
			aux_model_dict=pickle.load(f)
		self.nLatentDim=aux_model_dict['nLatentDim']
		self.TrainingFraction=aux_model_dict['TrainingFraction']
		self.InferenceOutput=aux_model_dict['InferenceOutput']

		self.local_clinical_dataset=ClinicalDataset(dict(zip(self.TargetSymptoms,np.arange(0,self.TargetSymptoms.shape[0]))))
		self.local_clinical_dataset.ReadFromDisk(FilePrefix+'_ClinicalDataset.pth')
		self.sampler=ClinicalDatasetSampler(self.local_clinical_dataset,self.TrainingFraction)
		self.sampler.ReadFromDisk(FilePrefix+'_ClinicalSampler.pth')
		self.vlpiModel= vLPI(self.sampler,self.nLatentDim)
		self.vlpiModel.LoadModel(FilePrefix+'_FittedModel.pth')


class FullSetBackground:

	def __init__(self,TargetSymptoms,FilePrefix=None,ClinicalDataset=None,TrainingIndex=None,**kwargs):
		"""Initiates and fits the FullSet Background model, which simply creates a multinomial distribution over all observed sets. 
		
		
		Args:
		    TargetSymptoms (1-d iterable): List of symptoms for model. 
		    FilePrefix (None, optional str): Path to file storing previously fit model. Note, model will be adjusted based on the TargetSymptoms provided.
		    ClinicalDataset (None, vlpi.data.ClinicalDataset): ClinicalDataset that stores the diagnositic information. Only requred if building a new model.
		    TrainingIndex (None, 1-d iterable): List/array of subject indices to use for training. Only required if building a new model.
		    **kwargs: 
				SetCountPrior: Smoothing count for symptom frequencies. Default is 1.0. Note, model is parameterized as a dirirchlet distribution with concerntration parameter SetCountPrior/(# of set counts)
		"""
		self.TargetSymptoms=np.array(TargetSymptoms)
		assert (ClinicalDataset is not None) or (FilePrefix is not None), "Must provide either file path for model or a ClinicalDatset. Note, if fitting model from new ClinicalDataset, a TrainingIndex must be used."
		if (ClinicalDataset is not None):
			assert (TrainingIndex is not None), "Must provide a TrainingIndex if fitting a new model."
			if 'SetCountPrior' in kwargs.keys():
				self.SetCountPrior=kwargs['SetCountPrior']
			else:
				self.SetCountPrior=1.0

			training_dx_matrix = ClinicalDataset.ReturnSparseDataMatrix(index=TrainingIndex).tocsr()[:,[ClinicalDataset.dxCodeToDataIndexMap[s] for s in TargetSymptoms]]
			

			set_based_inference_struct=InferenceDataStruct(training_dx_matrix,pd.Series(np.arange(len(TrainingIndex)),index=TrainingIndex), pd.Series(np.arange(len(TargetSymptoms)),index=TargetSymptoms))


			set_counts=set_based_inference_struct._compute_set_based_counts(pd.Series(np.ones(len(TrainingIndex)),index=TrainingIndex))
			set_counts_no_null=set_counts.drop('NULL')
			null_counts = set_counts['NULL']


			self.SetCounts=pd.Series(set_counts_no_null.values,index=[frozenset([set_based_inference_struct.oringal_index_map_to_dx[x] for x in set_based_inference_struct.unique_symptom_sets.loc[set_index]]) for set_index in set_counts_no_null.index])
			self.SetCounts=pd.concat([self.SetCounts,pd.Series([null_counts],index=['NULL'])])
			self.SetCounts=pd.concat([self.SetCounts,pd.Series([0.0],index=['NEW'])])

		else:
			self.LoadModel(FilePrefix,self.TargetSymptoms)



	def ComputeSurprisal(self,DxArray,SymptomColumns):
		"""Computes the surprisals (-1*log[prob]) for a binary array of diagnoses.
		
		Args:
		    DxArray (np.array or sparse.csr_matrix): Binary array of diagnoses.
		   	SymptomColumns (optional, 1-d iterable): List/array of symptom labels for columns of DxArray. This is provided in case the model is being applied to dataset with different symptoms/column ordering. 
		
		Returns:
		    np.array: Array of suprisals for DxArray
		"""		

		#create set of all symptomms in current model
		current_model_symptoms=set().union(*self.SetCounts.index.drop(['NEW','NULL']))
		assert len(set(SymptomColumns).intersection(current_model_symptoms))>0, "There must be some overlap between FullSetBackground model and the provided symptoms."
		target_symptoms = list(set(SymptomColumns).intersection(current_model_symptoms))
		missing_symptoms = current_model_symptoms.difference(target_symptoms)


		if len(missing_symptoms)>0:
			new_index=set([x.intersection(target_symptoms) for x in self.SetCounts.index.drop(['NEW','NULL'])])
			if frozenset([]) in new_index:
				new_index.remove(frozenset([]))
			new_index = list(new_index)+['NEW','NULL']
			modified_symptom_set=pd.Series(np.zeros(len(new_index),dtype=np.float64),index=new_index)
			for sset in self.SetCounts.index:
				if sset not in set(['NEW','NULL']):
					new_sset = frozenset(sset.intersection(target_symptoms))
					if len(new_sset)>0:
						modified_symptom_set[new_sset]+=self.SetCounts[sset]
					else:
						modified_symptom_set['NULL']+=self.SetCounts[sset]
				else:
					modified_symptom_set[sset]+=self.SetCounts[sset]
		else:
			modified_symptom_set=self.SetCounts.copy()



		if len(DxArray.shape)==1:
			DxArray=DxArray.reshape(1,-1)

		SymptomColumns=list(SymptomColumns)
		new_dx_array = sparse.csr_matrix(DxArray[:,[SymptomColumns.index(s) for s in target_symptoms]])

		inference_struct=InferenceDataStruct(new_dx_array,pd.Series(np.arange(DxArray.shape[0]),index=np.arange(DxArray.shape[0])), pd.Series(np.arange(len(target_symptoms)),index=target_symptoms))

		set_log_probs = np.log(modified_symptom_set+self.SetCountPrior)-np.log((self.SetCounts+self.SetCountPrior).sum())

		scores = pd.Series(np.zeros(DxArray.shape[0],dtype=np.float64),index=np.arange(DxArray.shape[0]))
		symptomatic_targets= inference_struct.all_symptomatic_cases.index

		all_obs_sets = pd.Series([frozenset([inference_struct.oringal_index_map_to_dx[s] for s in x]) for x in  inference_struct.unique_symptom_sets[inference_struct.symptomatic_patients_to_unique_sets[symptomatic_targets]]],index=symptomatic_targets)

		missing_sets=set(all_obs_sets.values).difference(set_log_probs.index)

		for patient_id in all_obs_sets.index:
			if all_obs_sets.loc[patient_id] not in missing_sets:
				scores.loc[patient_id]=set_log_probs[all_obs_sets.loc[patient_id]]
			else:
				scores.loc[patient_id]=set_log_probs['NEW']
		asymptomatic_targets=inference_struct.all_asymptomatic_cases.index
		scores.loc[asymptomatic_targets]=set_log_probs['NULL']
		return -1.0*np.array(scores.values,dtype=np.float64)


	def PackageModel(self,FilePrefix):
		"""Writes model to disk using pickle.
		
		Args:
		    FilePrefix (str): Path for model file. 
		"""		
		model_dict={'SetCounts':self.SetCounts,'SetCountPrior':self.SetCountPrior}
		with open(FilePrefix+'.pth','wb') as f:
			pickle.dump(model_dict,f)		

	def LoadModel(self,FilePrefix,TargetSymptoms):
		"""Loads a previously fit model and removes symptoms missing from the target set as needed. 
		
		Args:
		    FilePrefix (str): Path to model fil. 
		"""
		with open(FilePrefix+'.pth','rb') as f:
			model_dict=pickle.load(f)
		self.SetCounts=model_dict['SetCounts']
		self.SetCountPrior=model_dict['SetCountPrior']

		current_model_symptoms=set().union(*self.SetCounts.index.drop(['NEW','NULL']))
		assert len(set(TargetSymptoms).intersection(current_model_symptoms))>0, "There must be some overlap between FullSetBackground model and the provided symptoms."
		target_symptoms = list(set(TargetSymptoms).intersection(current_model_symptoms))
		missing_symptoms = current_model_symptoms.difference(target_symptoms)


		if len(missing_symptoms)>0:
			new_index=set([x.intersection(target_symptoms) for x in self.SetCounts.index.drop(['NEW','NULL'])])
			if frozenset([]) in new_index:
				new_index.remove(frozenset([]))
			new_index = list(new_index)+['NEW','NULL']
			modified_symptom_set=pd.Series(np.zeros(len(new_index),dtype=np.float64),index=new_index)
			for sset in self.SetCounts.index:
				if sset not in set(['NEW','NULL']):
					new_sset = frozenset(sset.intersection(target_symptoms))
					if len(new_sset)>0:
						modified_symptom_set[new_sset]+=self.SetCounts[sset]
					else:
						modified_symptom_set['NULL']+=self.SetCounts[sset]
				else:
					modified_symptom_set[sset]+=self.SetCounts[sset]
			self.SetCounts=modified_symptom_set.copy()



		
		
	
