from skimage import transform,io
import os

def scale(picture_path, target_path, pic_name):
	img = io.imread(picture_path)
	#a is the shorter edge pixels number
	a = min(img.shape[0:2])
	b = 227
	a = float(a)
	b = float(b)
	img_resize = transform.resize(img, (500,500))
	img_center = img_resize[137:364,137:364]
	io.imsave(os.path.join(target_path, 'c' + pic_name), img_center)	
	
	#s,l represent short,long = (0,1)	
	#s = shape.index(227)
	#l = 1 - s
	#if s == 0:
		#for x in xrange(3):
			#if x == 0:			
			#	io.imsave(os.path.join(target_path, str(x) + pic_name), img_scale[:,0:227])
			#elif x == 1:
			#	mid = shape[l]/2
			#	io.imsave(os.path.join(target_path, 'x' + pic_name), img_scale[:,mid-113:mid+114])
			#else:
			#	io.imsave(os.path.join(target_path, str(x) + pic_name), img_scale[:,-227:])
	#else:
		#for x in xrange(3):
		#	if x == 0:			
		#		io.imsave(os.path.join(target_path, str(x) + pic_name), img_scale[0:227,:])
		#	elif x == 1:
		#		mid = shape[l]/2
		#		io.imsave(os.path.join(target_path, 'x' + pic_name), img_scale[mid-113:mid+114,:])
		#	else:
		#		io.imsave(os.path.join(target_path, str(x) + pic_name), img_scale[-227:,:])

#Origin pic path
pic_path = '/home/sgx/groundtrue'

#Precessed pic path
pic_target = '/home/sgx/groundtruecenter'

if not os.path.exists(pic_target):
	os.makedirs(pic_target)

for folder in os.listdir(pic_path):
	pic_in_this = os.listdir(os.path.join(pic_path, folder))
	for picture in pic_in_this:
		if not os.path.exists(os.path.join(pic_target, folder)):
			os.makedirs(os.path.join(pic_target, folder))
		scale(os.path.join(pic_path, folder, picture), os.path.join(pic_target, folder), picture)

