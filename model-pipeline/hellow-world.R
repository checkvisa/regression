#!/usr/bin/Rscript

library(yhatr)

model.transform  <- function(request) {
  me <- request$name
  paste ("Hello", me, "!")
}
model.predict <- function(greeting) {
  data.frame(greeting=greeting)
}

yhat.config <- c(username="rongxin1989@gmail.com",
                 apikey="HaDobDyJtFoQQPZ9xRkCJrI44OB6EW8hC6IfUMsGzo8",
                 env="http://cloud.yhathq.com/")  
yhat.deploy ("HelloWorld")