import gc
from scipy import sparse
import pickle
from sklearn.preprocessing import normalize
from config import TRAIN_FILE_PATH


'''
The data files for all the datasets are in the following sparse representation format:
Header Line: Total_Points Num_Features Num_Labels
1 line per datapoint : label1,label2,...labelk ft1:ft1_val ft2:ft2_val ft3:ft3_val .. ftd:ftd_valsour
'''

train_specs = {}


# READ TRAINING FILE
f = open(TRAIN_FILE_PATH)
size = f.readline()
nrows, nfeature,nlabel = [int(s) for s in size.split()]
# train_specs['train_length'] = nrows
# train_specs['num_features'] = nfeature
# train_specs['num_labels'] = nlabel
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

x_train=sparse.lil_matrix((nrows,nfeature))
for i in range(nrows):
	for j in range(len(pos[i])):
		x_train[i,pos[i][j]]=x_m[i][j]

del x_m, pos
gc.collect()

y_train=sparse.lil_matrix((nrows,nlabel))
for i in range(nrows):
	for j in y_m[i]:
		y_train[i,j]=1

del y_m
gc.collect()
f.close()

nonzeroColindices = sorted(list(set(y_train.nonzero()[1])))
with open('nozero_col.pkl','wb') as p:
    pickle.dump(nonzeroColindices, p)
print("train",len(nonzeroColindices))
y_train = y_train[:,nonzeroColindices]
x_train = normalize(x_train,norm = 'l2',axis =1,copy=False)

train_specs = {
	'train_length' : x_train.shape[0],
	'num_features' : x_train.shape[1],
	'num_labels' : y_train.shape[1]
}

print("Training dataset is created")