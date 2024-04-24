import pandas as p
from sklearn.linear_model import LinearRegression
import numpy as n
import matplotlib.pyplot as mtp

data = p.read_csv("Your_dataset.csv")


X = data.iloc[:,0]

y= data.iloc[:,1]
xy = X*y

x_squared = X**2

n = len(data)

sum_y = sum(y)
sum_y


sum_x = sum(X)
sum_x

sum_x_squared = sum(x_squared)

sum_xy = sum(xy)

a = ((sum_y*sum_x_squared)-(sum_x*sum_xy))/((n*sum_x_squared)-sum_x**2)


b = ((n*sum_xy)-(sum_x*sum_y))/((n*sum_x_squared)-sum_x**2)


y = a+b*1.7

x_test = [1.7,2.5,6.5,1,2.2]
y_pred = []
for i in range(len(x_test)):
   y_pred.append(a + b* x_test[i])


l = LinearRegression()
x_reshaped = n.reshape(X,(-1,1))
print(l.fit(x_reshaped,y))

 
prediction = l.predict(x_reshaped)

mtp.plot(x_reshaped,prediction)
mtp.scatter(x_test,y_pred,color="red")
mtp.scatter(X,y,color="orange")

