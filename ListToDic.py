import os
path = '/home/sgx/PicOrigin'

lst = os.listdir(path)
dic = {}

for folder in lst:
	dic[folder] = str(lst.index(folder))
