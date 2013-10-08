#!/usr/bin/env python
import sys
import scipy
import math
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn import linear_model
from yhat import BaseModel
# from ckutil import transpose
# Refer to:
# [OneHotEncoder] http://bit.ly/11qcTn8
# [LabelEncoder]  http://bit.ly/YSeGCW
# [Ridge Regression Model] http://bit.ly/11rg4d7

class CKModel(BaseModel):
	def __init__(self, model, R2, encoder, encoder_onehot, feature_names, 
		n, p, sigma2_est, XtX_inv, conf_level, radius):
		self.model = model
		self.R2 = R2
		self.encoder = encoder
		self.encoder_onehot = encoder_onehot
		# maintaining a fixed order of features
		self.feature_names = feature_names
		self.feature_value_table = {}
		for feat in self.feature_names:
			self.feature_value_table[feat] = list(self.encoder[feat].classes_)
		self.n = n
		self.p = p
		self.sigma2_est = sigma2_est
		self.XtX_inv = XtX_inv
		self.conf_level = conf_level
		self.radius = radius

	# Get dummy data ready for analysis
	# Function required by Yhat
	def transform(self, raw_data):
		feature = raw_data
		coded_data = []
		if 'byear' in feature:
			feature['byear']='2012'
			#sys.stderr.write('Info: Forcing byear to be 2012.\n')
		for feat in self.feature_names:
			if not feat in feature:
				raise ValueError('The required feature "%s" is not provided.'%feat)
			if not feature[feat] in list(self.encoder[feat].classes_):
				raise ValueError('Unrecognizable value for feature "%s": "%s"'%(feat, feature[feat]))
			codes = self.encoder[feat].transform([feature[feat]])
			coded_data.append(list(codes))
		# coded_data_t = transpose(coded_data)
		coded_data_t = zip(*coded_data)
		feature_dummy = self.encoder_onehot.transform(coded_data_t)
		return feature_dummy

	# Predict the waiting time for a new case
	# Function required by Yhat
	# Parameters:
	# 	feature - a dictionary [feature]=value
	# Returns:
	#	a dictionary, with the following keys: "y", "conf_interval"
	def predict(self, data):
		x0 = data
		result = {}
		y0 = self.model.predict(x0)[0]
		x0 = x0.todense()
		n = self.n
		p = self.p
		var_y0 = self.sigma2_est * np.inner(np.dot(np.matrix(x0), self.XtX_inv), x0)
		radius = self.radius * np.sqrt(var_y0)
		result["y"] = y0
		result["interval_lower"] = y0 - radius[0][0]
		result["interval_upper"] = y0 + radius[0][0]
		return result

	# Get feature value table
	def get_valid_values(self):
		return self.feature_value_table

	# Print all required features and their valid values
	def print_feature_value_table(self):
		for feat in self.feature_names:
			print '\n[ %s ]'%feat
			for value in list(self.encoder[feat].classes_):
				print '\t%s'%value

class CKModelTrainer:
	def __init__(self, data_file):
		self.data_file = data_file

	def train_model(self, model=linear_model.Ridge):
		fin = open(self.data_file, 'r')
		datastr = fin.read()
		fin.close()

		uid = []
		wtime = []
		feature = {'vtype':[], 'ventry':[], 'loc':[], 'major':[], 
					'byear':[], 'bmonth':[], 'bday':[]}
		# feat_names = [x for x in feature]
		for line in datastr.split('\n'):
			line = line.strip()
			if len(line) == 0:
				continue
			(uid_,vtype_,ventry_,loc_,major_,stat_,byear_,
				bmonth_,bday_,eyear_,emonth_,eday_,wtime_) = line.split('\t')
			feature['vtype'].append(vtype_)
			feature['ventry'].append(ventry_)
			feature['loc'].append(loc_)
			feature['major'].append(major_)
			feature['byear'].append(byear_)
			feature['bmonth'].append(bmonth_)
			feature['bday'].append(bday_)
			uid.append(uid_)
			wtime.append(int(wtime_))

		encoder = {}
		enc_onehot = OneHotEncoder()
		coded_data = []
		for feat in feature.keys():
			encoder[feat] = preprocessing.LabelEncoder()
			codes = encoder[feat].fit_transform(feature[feat])
			coded_data.append(list(codes))

		# coded_data_t = transpose(coded_data)
		coded_data_t = zip(*coded_data)
		feature_dummy = enc_onehot.fit_transform(coded_data_t)
		X = feature_dummy
		y = wtime
		d_args = {}
		if model==linear_model.Ridge:
			d_args['alpha']=.5
		m1 = model(**d_args)
		m1.fit(X, y)
		R2 = m1.score(X,y)
		n,p = X.get_shape()
		y_est = m1.predict(X)
		SSE = np.sum([(y[i]-y_est[i])*(y[i]-y_est[i]) for i in range(n)])
		sigma2_est = SSE/(n-p)
		X_dense = X.todense()
		XtX_inv = np.linalg.inv(np.dot(np.transpose(X_dense), X_dense))
		conf_level = 0.95
		radius = scipy.stats.t.ppf(1-conf_level*0.5, n-p)
		ckmodel = CKModel(m1, R2, encoder, enc_onehot, feature.keys(), 
			n, p, sigma2_est, XtX_inv, conf_level, radius)
		ckmodel_wrapper = CKModelWrapper(ckmodel=ckmodel)
		#return ckmodel_wrapper
		return ckmodel

class CKModelWrapper(BaseModel):
	def transform(self, raw_data):
		return self.ckmodel.transform(raw_data)

	def predict(self, data):
		return self.ckmodel.predict(data)
