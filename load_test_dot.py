import gc
from scipy import sparse

from config import TEST_FILE_PATH
import pickle
from sklearn.preprocessing import normalize


'''
The data files for all the datasets are in the following sparse representation format:
Header Line: Total_Points Num_Features Num_Labels
1 line per datapoint : label1,label2,...labelk ft1:ft1_val ft2:ft2_val ft3:ft3_val .. ftd:ftd_valsour
'''

test_specs = {}



# READ TEST FILE
f = open(TEST_FILE_PATH)
size = f.readline()
nrows, nfeature, nlabel = [int(s) for s in size.split()]
test_specs['test_length'] = nrows
x_m = [[] for i in range(nrows)]
pos = [[] for i in range(nrows)]
y_m = [[] for i in range(nrows)]
for i in range(nrows):
	line = f.readline()
	temp=[s for s in line.split(sep=' ')]
	pos[i]=[int(s.split(':')[0]) for s in temp[1:]]
	x_m[i]=[float(s.split(':')[1]) for s in temp[1:]]
	for s in temp[0].split(','):
		try:
			int(s)
			y_m[i]=[ int(s) for s in temp[0].split(',')]
		except:
			y_m[i]=[]

x_test=sparse.lil_matrix((nrows,nfeature))
for i in range(nrows):
	for j in range(len(pos[i])):
		x_test[i,pos[i][j]]=x_m[i][j]

del x_m, pos
gc.collect()

y_test=sparse.lil_matrix((nrows,nlabel))
for i in range(nrows):
	for j in y_m[i]:
		y_test[i,j]=1

del y_m
gc.collect()
f.close()

with open('nozero_col.pkl','rb') as f:
    nonzeroColindices = pickle.load(f)
print("test",len(nonzeroColindices))
y_test = y_test[:,nonzeroColindices]
x_test = normalize(x_test,norm = 'l2',axis =1,copy=False)

test_specs = {
	'test_length' : x_test.shape[0],
}

print("Testing data is created ")