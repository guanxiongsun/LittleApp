import shutil
import os

percent = input('Input the percent of trainning using 0< float <1,:\n')

pic_path = '/home/sgx/Pic_Augment'

train_pic_path = os.path.join(pic_path, 'train_pic')
test_pic_path = os.path.join(pic_path, 'test_pic')

for folder in os.listdir(pic_path):
	pic_in_this = os.listdir(os.path.join(pic_path, folder))
	pic_num = len(pic_in_this)
	divider = int(pic_num*percent)
	pic_train = pic_in_this[0:divider]
	pic_test = pic_in_this[divider:]
	if not os.path.exists(train_pic_path):
		os.makedirs(train_pic_path)
	if not os.path.exists(test_pic_path):
		os.makedirs(test_pic_path)

	if not os.path.exists(os.path.join(train_pic_path, folder)):
		os.makedirs(os.path.join(train_pic_path, folder))
	if not os.path.exists(os.path.join(test_pic_path, folder)):
		os.makedirs(os.path.join(test_pic_path, folder))
	
	for train_files in pic_train:
		shutil.copy(os.path.join(pic_path, folder, train_files), os.path.join(train_pic_path, folder))
	for test_files in pic_test:
		shutil.copy(os.path.join(pic_path, folder, test_files), os.path.join(test_pic_path, folder))
