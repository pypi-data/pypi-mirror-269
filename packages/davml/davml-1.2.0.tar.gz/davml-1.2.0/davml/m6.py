import numpy as np

while True :
  x1 = np.array([0, 0, 1, 1])
  x2 = np.array([0,  1, 0, 1])
  t = np.array([0,1,1,1])
  w1 = float(input("Enter W1 Weight Value: "))
  w2 = float(input("Enter W2 Weight Value: "))
  T = float(input("Enter Threshold Value: "))


  yin = w1 * x1 + w2 * x2

  print("Yin:")
  print(yin)

  y = np.zeros_like(t) #to make 0 for -ve values

  for i in range(len(yin)):
     if yin[i] >= T:
         y[i] = 1

  print("")

  print("Target O/P", t)
  print("Calculated O/P", y)
  print("")

  if np.array_equal(y, t):
    print("Correct Weight And Threshold Values")
    break
  else:
    print("Incorrect Weights, Re-running Code")
    print("\n")