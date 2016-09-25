import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path

def plotHistogram(data):
	n, bins = np.histogram(data, 50)
	fig, ax = plt.subplots()

	# get the corners of the rectangles for the histogram
	left = np.array(bins[:-1])
	right = np.array(bins[1:])
	bottom = np.zeros(len(left))
	top = bottom + n


	# we need a (numrects x numsides x 2) numpy array for the path helper
	# function to build a compound path
	XY = np.array([[left, left, right, right], [bottom, top, top, bottom]]).T

	# get the Path object
	barpath = path.Path.make_compound_path_from_polys(XY)

	# make a patch out of it
	patch = patches.PathPatch(
	    barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
	ax.add_patch(patch)

	# update the view limits
	ax.set_xlim(left[0], right[-1])
	ax.set_ylim(bottom.min(), top.max())

	plt.show()

def plotScatter(data):

	x = list(range(1, len(data)+1))
	y = data
	area = np.pi # radius 1pt
	plt.scatter(x, y, s=area)

	plt.show()

