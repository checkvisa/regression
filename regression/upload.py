#!/usr/bin/env python
import sklearn
from ckreg import *
from yhat import Yhat, BaseModel

trainer = CKModelTrainer(data_file='./dat.txt')
ckmodel = trainer.train_model(model=sklearn.linear_model.Ridge)
#yh = Yhat("richeliteys@gmail.com", "RoVGt5VDZfHkdBLx2rre76sg998cD4IuJiYzzNmNp48")
yh = Yhat("rongxin1989@gmail.com", "HaDobDyJtFoQQPZ9xRkCJrI44OB6EW8hC6IfUMsGzo8")
print yh.upload("CKModel", ckmodel)