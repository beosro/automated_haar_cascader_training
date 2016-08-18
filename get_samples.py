import cv2
import os
import time

is_recording = False
time_last_img_saved = time.time()
is_running = True
target_dir = 'testimages'

if not os.path.exists(target_dir):
	os.makedirs(target_dir)


cap = cv2.VideoCapture(1)

def save_images(img):
	global time_last_img_saved
	if (time_last_img_saved) + 1 < time.time():
		cv2.imwrite(target_dir + '/' + str(len(os.listdir(target_dir)) + 1) + '.jpg', img)
		print str(len(os.listdir(target_dir))) + ' files saved'
		time_last_img_saved = time.time()

def look_if_a_key_is_pressed():
	global is_recording, is_running
	k = cv2.waitKey(30) & 0xff
	#print k
	if k == 113:
		is_running = False
	if k == 114:
		is_recording = True

def main():
	while is_running:
		ret, img = cap.read()
		look_if_a_key_is_pressed()

		if is_recording:
			save_images(img)
			cv2.putText(img,"recording, press q for quit", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
		else:
			cv2.putText(img,"press r for record", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

		cv2.imshow('img',img)

	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
