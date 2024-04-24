import pandas as pd 
import numpy as np
def mcculloch_pitt(x1 , x2 , y ,w1 , w2 ,t ):
    d = []
    y_in_list = []
    for i in range(len(y)):
        y_in = w1 * x1[i] + w2 * x2[i]
        if y_in >= t :    
            y_in_list.append(1)
        else :
            y_in_list.append(0)
        d.append([x1[i], x2[i] , y[i] , y_in])
    df = pd.DataFrame(d , columns = ['x1' , 'x2' , 'y' , 'y_in'])
    print(df)

    if np.equal(y_in_list,y).all() :
        print("Correct")
    else : 
        print("Wrong , re run the code ")
w1 = int(input("Enter the value of weight 1 "))
w2 = int(input("Enter the value of weight 2 "))
t = int(input("Enter the value of threshold "))
mcculloch_pitt([0,0,1,1],[0,1,0,1],[0,1,1,1],w1 , w2 ,t)