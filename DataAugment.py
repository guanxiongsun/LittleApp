# import packages
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import os
import glob

datagen = ImageDataGenerator(
        rotation_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

#pic_path = input('input source Path of pictures, eg: /home/sgx/1:\n')

#aug_path = input('input target Path of Augmentation, eg: /home/sgx/2:\n')

pic_path = '/home/sgx/images/Picture_test_copy'

aug_path = '/home/sgx/Pic_Augment'

files = glob.glob(os.path.join(pic_path,  '*/*.*'))

for f in files:
	(file_path, pic_name) = os.path.split(f)
	(file_path, class_num) = os.path.split(file_path)
	
	pic_name = pic_name.split('.')[0]

	img = load_img(f)  # this is a PIL image, please replace to your own file path
	x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
	x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

	# the .flow() command below generates batches of randomly transformed images
	# and saves the results to the `preview/` directory
	
	target_path = os.path.join(aug_path, class_num)

	if not os.path.exists(target_path):
		os.makedirs(target_path)

	i = 0
	for batch in datagen.flow(x, 
		                  batch_size=1,
		                  save_to_dir= os.path.join(aug_path, class_num),  
		                  save_prefix= pic_name, 
		                  save_format='jpg'):
	    i += 1
	    if i > 20:
		break  # otherwise the generator would loop indefinitely
