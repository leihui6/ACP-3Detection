
import sys
import numpy as np

if __name__ == '__main__':
	filename = sys.argv[1]
	filename_without_postfix = filename[:filename.find('.')]
	points=[]
	with open(filename) as f:
		data =f.readlines()
		for l in data:
			point = l.strip().split()
			points.append(point)
	float_points = np.array(points).astype(float).round(8)
	print(float_points.shape)
	save_filename = filename_without_postfix+"_test.bin"
	print('write into ', save_filename)
	float_points.astype(np.float32).tofile(save_filename)
