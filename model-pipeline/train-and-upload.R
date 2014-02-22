#!/usr/bin/Rscript

cat("Running RScript.\n")

########################################################################
# Read data from dat.tsv
dat <- read.delim("dat.tsv", header=FALSE)
colnames(dat) <- c("uid", "type", "entry", "city", "major", "status", 
                   "byear", "bmonth", "bday", "eyear", "emonth", "eday",
                   "wt")

#######################################################################
# Train model for uploading to Yhat

# Factorize feature columns
# URL for reference: http://www.stat.berkeley.edu/classes/s133/factors.html
dat$vtype <- factor(dat$type)
dat$ventry <- factor(dat$entry)
dat$loc <- factor(dat$city)
dat$major <- factor(dat$major)
dat$bmonth <- factor(dat$bmonth)
dat$bday <- factor(dat$bday)
feature_columns <- c("vtype","ventry","loc","major", "bmonth","bday")
dat1 <- dat[,c(feature_columns,"wt")]
summary(dat1)

# Ridge Regression #
library(MASS)
m1 <- lm.ridge(wt~., dat1)
summary(m1)

# Not Sure How to Make a prediction with this !! #

# Linear regression 
m2 <- lm(wt~., dat1)
summary(m2)

# Make prediction of a data point with the linear model
pred <- predict(m2, dat1[1,-7], interval="confidence")

#######################################################################
# Compose YHat model

# model.require(...) # include any package dependency you are using
model.transform <- function(df) {
	# TODO: Factorize this incoming sample!
	df <- df[, feature_columns]
	for (feat in feature_columns) {
		df[,feat] <- factor(df[,feat], levels(dat1[,feat]))
	}
	if (is.na(df[1,"major"])) {
		df[1,"major"] <- "N/A"
		df[,"major"] <- factor(df[,"major"], levels(dat1[,"major"]))
	}
	df
}
model.predict <- function(df) {
	# yhatr will automatically load any data dependencies in your model
	# Therefore, m2 will be automatically uploaded, too
	pred <- predict(m2, df, interval="confidence")
	pred <- as.data.frame(pred)
	result <- NULL
	y <- c(pred$fit)
	interval_lower <- c(pred$lwr)
	interval_upper <- c(pred$upr)
	result <- cbind(y, interval_lower, interval_upper)
	result <- as.data.frame(result)
	result
}

#######################################################################
# Local Test
new_input <- c("F1", "New", "BeiJing", "Chemistry", "9", "15")
new_input <- rbind(new_input)
colnames(new_input) <- feature_columns
new_input <- as.data.frame(new_input)
new_input
trans <- model.transform(new_input)
trans
pred <- model.predict(trans)
pred

# Test Bad Major Name
input2 <- c("F1", "New", "BeiJing", "Some Bad Major Name", "9", "15")
input2 <- rbind(input2)
colnames(input2) <- feature_columns
input2 <- as.data.frame(input2)
input2
trans <- model.transform(input2)
trans
pred <- model.predict(trans)
pred


#######################################################################
# Upload yhat model
#install.packages("yhatr")
library(yhatr)
library(RCurl)
yhat.config <- c(username="rongxin1989@gmail.com",
                 apikey="HaDobDyJtFoQQPZ9xRkCJrI44OB6EW8hC6IfUMsGzo8",
                 env="http://cloud.yhathq.com/")  
yhat.deploy("Checkoo R Linear Regression")
yhat.show_models()

cat("Finished running RScript.\n")
