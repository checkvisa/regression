#!/usr/bin/env python
# This script tests the functionality of ckreg.
# It shows how to generate and use CKModel.
import sklearn
from ckreg import *

# First, create a trainer object by assigning the training data file.
# The format should be the same as that of checkoo/Regression/dat.txt
trainer = CKModelTrainer(data_file='./dat.txt')

# Second, use the trainer to generate a CKModel object.
# After training, push this model to the server.
# This CKModel is the only object that you need to push to the server.
ckmodel = trainer.train_model(model=sklearn.linear_model.Ridge)

# The following codes are for the server-side
# Use the following statement to get a list of all supported values for each feature
# You will get a dictionary, key is feature name, 
# and value is a list of all supported values for the feture.
feature_value_table = ckmodel.get_valid_values()

# You can print out all the supported values
# for feature in feature_value_table:
# 	print '[ %s ]'%feature
# 	print '\n'.join('\t'+x for x in feature_value_table[feature])
# 	print '\n'

# When the user submits a query, you need to make all the feature-value pairs into
# a dictionary like the following one.
newcase = {
	'loc':'BeiJing', 
	'major':'Computer Science/Engineering', 
	'vtype':'F1', 
	'ventry':'Renewal',
	'byear':'2013',
	'bmonth':'7',
	'bday':'20'
	}

# Then use the predict function of the CKModel object to get predicted waiting time.
dummy_data = ckmodel.transform(newcase)
result = ckmodel.predict(dummy_data)
waiting_time = result["y"]
interval_lower = result["interval_lower"]
interval_upper = result["interval_upper"]

# You can print out the predicted waiting time.
print 'Result: Estimated waiting time for this case is: %d days'%waiting_time
print '        Estimated waiting time range: %s ~ %s days'%(interval_lower, interval_upper)