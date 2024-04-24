import pandas as pd 
import numpy as np
from scipy import sparse
from scipy.special import gammaln,betaln,expit,digamma
from vlpi.data.ClinicalDataset import ClinicalDataset
import pickle

class InferenceDataStruct:

	def __init__(self,sparse_data_array,subject_index,target_dx_to_index_map):
		"""This class constructs a series of data structures that simplify the inference/application of the SymptomSetModel. 
		
		Args:
		    sparse_data_array (sparse.csr_matrix): sparse.csr_matrix of binary indicators, which represent the set of symptoms (columns) diagnosed in each subject (rows).
		    subject_index (pandas.Series): Subject ID-to-array rows, provided using a pd.Series data structure 
		    target_dx_to_index_map (pandas.Series): HPO ID-to-array columns, provided using a pd.Series data structure 
		"""
		self.all_subjects=subject_index.index
		self.target_dx_to_oringal_index_map=target_dx_to_index_map
		self.oringal_index_map_to_dx=pd.Series(target_dx_to_index_map.index,target_dx_to_index_map.values)
		self.new_index_to_original_index_map=pd.Series(target_dx_to_index_map.values,index=np.arange(len(target_dx_to_index_map)))
		self.orignal_index_to_new_index_map=pd.Series(np.arange(len(target_dx_to_index_map)),index=target_dx_to_index_map.values)

		symptom_counts=np.array(sparse_data_array[:,self.target_dx_to_oringal_index_map.values].sum(axis=1)).ravel()

		no_symptoms=np.where(symptom_counts==0)[0]
		at_least_one_symptom=np.where(symptom_counts>0)[0]

		self.all_asymptomatic_cases=pd.Series(no_symptoms,index=subject_index.index[no_symptoms])
		self.all_symptomatic_cases=pd.Series(at_least_one_symptom,index=subject_index.index[at_least_one_symptom])


		#Find all of the unique symptom sets and where they occur. 
		symptomatic_lil_array=sparse.lil_matrix(sparse_data_array[self.all_symptomatic_cases.values][:,self.target_dx_to_oringal_index_map.values])
		unique_symptom_sets,array_of_unique_indices=np.unique(symptomatic_lil_array.rows,return_inverse=True)

		self.unique_symptom_sets=pd.Series([self.new_index_to_original_index_map.loc[x].values for x in unique_symptom_sets],index=map(str,np.arange(len(unique_symptom_sets))))
		self.symptom_sets_to_index = pd.Series(np.array(self.unique_symptom_sets.index),index=[frozenset(x) for x in self.unique_symptom_sets.values])
		self.symptomatic_patients_to_unique_sets=pd.Series(map(str,array_of_unique_indices),index=self.all_symptomatic_cases.index)

		self.symptoms_to_unique_sets={}
		for u_id,symptom_array in self.unique_symptom_sets.items():
			for symp in symptom_array:
				try:
					self.symptoms_to_unique_sets[self.oringal_index_map_to_dx[symp]]+=[u_id]
				except KeyError:
					self.symptoms_to_unique_sets[self.oringal_index_map_to_dx[symp]]=[u_id]
		self.symptoms_to_unique_sets=pd.DataFrame({'HPO':list(self.symptoms_to_unique_sets.keys()),'SET_ID':list(self.symptoms_to_unique_sets.values())})
		self.symptoms_to_unique_sets.set_index('HPO',inplace=True)


		self.unique_sets_to_patient_map={}
		for p_id,u_id in self.symptomatic_patients_to_unique_sets.items():
			try:
				self.unique_sets_to_patient_map[u_id]+=[p_id]
			except KeyError:
				self.unique_sets_to_patient_map[u_id]=[p_id]
		self.unique_sets_to_patient_map=pd.DataFrame({'SET_ID':list(self.unique_sets_to_patient_map.keys()),'SUBJECT_ID':list(self.unique_sets_to_patient_map.values())})
		self.unique_sets_to_patient_map.set_index('SET_ID',inplace=True)

		self.num_unique_sets_total=self.unique_symptom_sets.shape[0]


	def _compute_independent_counts(self,independence_indicator_weights):
		independent_counts=np.zeros((len(self.target_dx_to_oringal_index_map),2),dtype=np.float64)
		for u_idx,p_id in self.unique_sets_to_patient_map.iterrows():
			independent_counts[[self.orignal_index_to_new_index_map[orig_index] for orig_index in self.unique_symptom_sets[u_idx]],0]+=np.sum(independence_indicator_weights.loc[p_id.SUBJECT_ID])
		independent_counts[:,1]=independence_indicator_weights.sum()-independent_counts[:,0]
		return pd.DataFrame(independent_counts,index=self.target_dx_to_oringal_index_map.index,columns=['Present','Absent'])


	def _compute_set_based_counts(self, set_indicator_weights):
		target_count_vec=pd.Series(np.zeros(self.num_unique_sets_total+1,dtype=np.float64),index=np.concatenate([self.unique_symptom_sets.index,np.array(['NULL'])]))
		for u_idx,p_id in self.unique_sets_to_patient_map.iterrows():
			target_count_vec.loc[u_idx]+=np.sum(set_indicator_weights.loc[p_id.SUBJECT_ID])
		target_count_vec.loc['NULL']+=np.sum(set_indicator_weights.loc[self.all_asymptomatic_cases.index])
		return target_count_vec

