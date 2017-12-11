import cv2
import numpy as np
from PIL import ImageGrab
import lane_detection as ld
import game_controller as gc
import image_processing as ip


MAX_CRASH_COUNT = 200

def process_image(image, colour=[0,255,0], thickness=30):
	original_image = image
	processed_image = ld.detect_yellow(image)
	processed_image = ip.grayscale(processed_image)
	processed_image = ip.gaussian_blur(processed_image)
	processed_image = ip.canny_transform(processed_image)
	processed_image = ip.view_region(processed_image)
	lines = ld.hough_lines(processed_image)
	original_image, error = ld.draw_lane_lines(original_image, ld.lane_lines(image, lines))
	return processed_image, original_image, error

def main():
	crash = 0
	while True:
		screen_image = ImageGrab.grab(bbox=(0,40,800,640))
		screen = np.array(screen_image)
		new_screen, original_image, error = process_image(screen)
		if error:
			crash += 1
		if new_screen is not None and original_image is not None:
			if crash == MAX_CRASH_COUNT:
				gc.restart_game()
			# cv2.imshow('Car View', new_screen)
			cv2.imshow('Lane Lines', cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break

if __name__ == "__main__":
	main()
