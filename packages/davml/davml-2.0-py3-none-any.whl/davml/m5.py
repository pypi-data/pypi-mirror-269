def heb_learning(samples):
  print(f'{"Input" : ^8}{"Target" : ^16}{"Weight changes" : ^15}{"Weight" : ^28}')
  w1 , w2 , b = 0 , 0 , 0
  print(' ' * 48 , f'({w1:2} , {w2:2} , {b:2})')
  for x1,x2,y in samples:
    w1 = w1 + x1 * y
    w2 = w2 + x2 * y
    b=b+y
    print(f'({x1:2} , {x2:2})\t {y:2}\t ({x1*y:2},{x2*y:2},{y:2})\t\t ({w1:2} , {w2:2} , {b:2})')

OR_samples = {
    'bipolar_input_bipolar_output' : [
        [1,1,1],
        [1,-1,1],
        [-1,1,1],
        [-1,-1,-1]
    ]
}

print('-'*20,'Hebbian Learning','-'*20)

print('OR with bipolar input and bipoloar output')
heb_learning(OR_samples['bipolar_input_bipolar_output'])

def heb_learnings(samples):
  print(f'{"Input" : ^6}{"Target" : ^12}{"Changes" : ^12}{"Initial" : ^12}')
  w1=0
  w2=0
  b=0
  print(' '*32, f'{w1:2}{w2:2}{b:2}')
  for x1,x2,y in samples:
    w1 = w1 + x1*y
    w2 = w2 + x2*y
    b = b+y
    print(f'{x1:2}{x2:2}\t {y:2}\t {x1*y:2}{x2*y:2}{y:2}\t\t {w1:2}{w2:2}{b:2}')

AND_samples = {

    'bipolar_input_bipolar_output' : [

          [1,1,1],
          [1,-1,-1],
          [-1,1,-1],
          [-1,-1,-1]
    ]
}

print("AND gate hebbian Learning\n")
heb_learnings(AND_samples['bipolar_input_bipolar_output'])