import cv2
import os
import copy
import numpy as np

target_dir = 'testimages'
pro_sample_dir = 'pos'
neg_sample_dir = 'neg'
current_img = ''

roi = np.array([])
refPt = []
cropping = False



def click_and_crop(event, x, y, flags, param):
	global refPt, cropping, img, roi

	if len(refPt) == 1:
		img = copy.copy(clone)
		cv2.rectangle(img, refPt[0], (x,y), (0, 255, 0), 2)


	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
	elif event == cv2.EVENT_LBUTTONUP:
		refPt.append((x, y))
		img = copy.copy(clone)

		cropping = False

		#dragged from right to left
		left = min(refPt[0][0], refPt[1][0])
		right = max(refPt[0][0], refPt[1][0])
		top = min(refPt[0][1], refPt[1][1])
		bottom = max(refPt[0][1], refPt[1][1])

		refPt = [(left, top), (right, bottom)]
		cv2.rectangle(img, refPt[0], refPt[1], (0, 255, 0), 2)
		roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]



def reset():
	global roi, refPt, img
	refPt = []
	roi = clone.copy()
	img = clone.copy()

def create_list(dir_name):
	txt_file = open( dir_name + '_data.txt' , 'b')
	for file in os.listdir(target_dir):
		if file.endswith('.jpg'):
			txt_file.write(dir_name + '/' + file + '\n')
	txt_file.close()

for file in os.listdir(target_dir):
	if file.endswith('.jpg'):
		current_img = target_dir + '/' + file
		img = cv2.imread(current_img,0)
		clone = copy.copy(img)
		cv2.namedWindow(current_img)
		cv2.setMouseCallback(current_img, click_and_crop)
		reset()
		while True:
			cv2.putText(img,"r reset, c continue, a ok", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
			cv2.imshow(current_img, img)
			key = cv2.waitKey(1) & 0xFF

			if key == ord("r"):
				reset()
			elif key == ord("a"):
				break

		if roi.size < img.size:
			sample_dir = pro_sample_dir
			img_to_save = roi
		else:
			sample_dir = neg_sample_dir
			img_to_save = clone

		if not os.path.exists(sample_dir):
			os.makedirs(sample_dir)

		cv2.imwrite(sample_dir + '/' + str(len(os.listdir(sample_dir)) + 1) + '.jpg', img_to_save)
		cv2.destroyAllWindows()
		reset()

# close all open windows
cv2.destroyAllWindows()

create_list(pro_sample_dir)
create_list(neg_sample_dir)
