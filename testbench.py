import theano
import theano.tensor
import numpy as np
import cPickle

from ModelFactory import *
from output48_39 import *

parameter = open('parameter.txt','w')

def float_convert(i):
	try: 
		return float(i)
	except ValueError :
		return i

train_data = open('train.ark','r')
ans_data = open('answer_map.txt','r')

train = []
ans = []

for line in train_data:
	input_x = line.split()
	input_x = [float_convert(i) for i in input_x]
	train.append(input_x)
for line in ans_data:
	ans_x = line.split(',')
	ans.append(ans_x)

'''
train = train_data.readline()
ans = ans_data.readline()



train= train.split()
train = [float_convert(i) for i in train]
ans = ans.split(',')
'''
anstype = ["aa", "ae", "ah", "ao", "aw", "ax", "ay", "b", "ch", "cl", "d", "dh", "dx", "eh", "el"
               , "en", "epi", "er", "ey", "f", "g", "hh", "ih", "ix", "iy", "jh", "k", "l", "m", "ng"
               , "n", "ow", "oy", "p", "r", "sh", "sil", "s", "th", "t", "uh", "uw", "vcl", "v", "w"
               , "y", "zh", "z"]

W_number_list = [128,128]
layer_number = 1  # Number of layers in this model
input_dimension = 69  # Dimension of input vector
output_dimension = 48  # Dimension of output vector
batch_number = 1 # Number of batch size
LR = 0.001

test = ModelFactory(input_dimension, output_dimension, W_number_list, batch_number, LR)
X = None
Y = None
i=0
ACC = 0.0
W_new = []
B_new = [] 
c = MAP()
try:
	while True:
		X = []
		yy= []
		for k in range(batch_number):
			if i>=1000000:#i>=1124823:
				i=0
				err=0.0
				for m in range(124823):
					Ya= test.y_evaluated_function([train[1000000+m][1:70]], Y)[0]
					if [c.map(Ya)]!=[str(ans[1000000+m][1].split('\n')[0])]:
						err = err+1
					#print [c.map(Ya)]
					#print [str(ans[m][1].split('\n')[0])]
				ACC = 1.0-err/124823.0
				#print err
				print ACC
			typeidx = anstype.index(str(ans[i][1].split('\n')[0]))
			y=[0]*48
			y[typeidx]=1
			yy.append(y)
			X.append(train[i][1:70])
			i=i+1
		Y=yy
		if i%10000==0:
			print i
			print test.y_evaluated_function(X,Y)
			#print [test.W_array[0].get_value(),test.W_array[1].get_value()] 
		test.train_one(X,Y)


except KeyboardInterrupt:
	pass

f = file('parameter_W.txt', 'wb')
cPickle.dump(test.W_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('parameter_B.txt', 'wb')
cPickle.dump(test.B_array, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()


'''
ff= file('parameter.txt', 'rb')
xxx = cPickle.load(ff)
print xxx[0].get_value()
for data_slice in test.W_array[0]:
        np.savetxt(parameter, data_slice, fmt='%-7.10f')
        parameter.write('# New slice\n') 
'''
#np.savetxt('test.txt',test.W_array)
#parameter.write(test.W_array)
#parameter.write(test.B_array)



'''
c = MAP()
for i in range(400):
	#print [train[i][1:70]]
	Ya = test.y_evaluated_function([train[i][1:70]], Y)[0]
	print c.map(Ya)
'''

#print test.train_one(X, Y)
