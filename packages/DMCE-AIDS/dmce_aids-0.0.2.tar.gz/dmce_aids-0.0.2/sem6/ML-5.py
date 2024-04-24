import pandas as pd
def hebbian(z,gate):
  # print input array
  gate = df = pd.DataFrame(columns=['X1','X2','Y','delw1','delw2','w1','w2','b','y_new'])
  print("w1 w2 b")
  b = w1 = w2 = 0
  for x1 , x2 , y in z :
      w1=w1+x1*y
      w2=w2+x2*y
      b=b+y
      print(w1,w2,b)
      ynew = w1*x1 + w2*x2 + b
      gate.loc[len(gate.index)] = [x1, x2, y,x1*y,x2*y,w1,w2,b,ynew]
  return gate

#OR GATE
input_array = [
    [-1,-1,-1],
    [-1,1,1],
    [1,-1,1],
    [1,1,1]
];
gate = hebbian(input_array,'and')
#Output 1

print(gate)
#Output 2