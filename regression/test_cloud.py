#!/usr/bin/env python
from yhat import Yhat
#yh = Yhat("richeliteys@gmail.com", "RoVGt5VDZfHkdBLx2rre76sg998cD4IuJiYzzNmNp48")
yh = Yhat("rongxin1989@gmail.com", "HaDobDyJtFoQQPZ9xRkCJrI44OB6EW8hC6IfUMsGzo8")
checkoo_models = yh.show_models()
for model in checkoo_models['models']:
	print model

newcase = {
	'loc':'BeiJing', 
	'major':'Computer Science/Engineering', 
	'vtype':'F1', 
	'ventry':'New',
	'byear':'2013',
	'bmonth':'7',
	'bday':'20'
}
checkoo_version = 14
print yh.predict('CKModel',checkoo_version,newcase)
