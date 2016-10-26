'''
These are the functions used by zipfs.py
UPC MAI 
INLP 2016/2017
Assignment 1 - Zipf's Law
'''

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
import numpy as np
from operator import itemgetter
from statistics import mean, stdev
import sys



def corpusToTokenFrequencies(corpusLocation, caseSensitive=True, useStemming = False, charLevel=False):
	''' This function reads a corpus from a file and returns the list of tokens and their respective frequency.

	Args:
		corpusLocation (str): the file path of the corpus
		caseSensitive (boolean): tokens are considered in a case sensitive way. Default is True.
		useStemming (boolean): tokens are mapped to their word stem. Default is False.
		charLevel (boolean): consider every single char a token. Default is False.

	Returns:
		(list of (str, int)): the list of tokens and their frequencys, ordered descending by frequency
	'''

	# Open file and read text data:
	file = open(corpusLocation)
	rawText = file.read()

	# if charLevel is False, tokenize words:
	if charLevel:
		tokens = rawText
	else:
		# Tokenize the text using NLTK WordPunctTokenizer:
		tokenizer = WordPunctTokenizer()
		tokens = tokenizer.tokenize(rawText)

	if useStemming:
		stemmer = PorterStemmer()

	# Count the number of occurences (frequency) of each token:
	tokenCounts = {}
	for token in tokens:
		
		# Use stemming if wanted:
		if useStemming:
			token = stemmer.stem(token)
		# Convert tokens to lower case if case sensitive is not wanted:
		if not caseSensitive:
			token = token.lower()

		# Update frequency counts:
		if token in tokenCounts:
			tokenCounts[token] += 1
		else:
			tokenCounts[token] = 1

	# Sort tokens descending by their frequency:
	sortedTokenCounts = sorted(tokenCounts.items(),
		key = itemgetter(1),
		reverse=True)
	
	# Return sorted token frequencies:
	return sortedTokenCounts

def kValuesFromTokenFrequencies(tokenFrequencies):
	''' This function calculates the k values for tokens and their frequencies.

	Args:
		tokenFrequencies (list of (str, int)): the list of tokens and their frequencys

	Returns:
		(list of float): the list of calculated Ks, corresponding to the order of the tokenFrequencies list
	'''

	# Calculate K values, based on rank r and frequency f: K = f * r
	result = []
	rank = 1
	for tokenFrequency in tokenFrequencies:
		result.append(tokenFrequency[1] * rank)
		rank += 1

	# Return the list of calculated Ks:
	return result

def kValuesReport(tokenFrequenciesCollection, plot=False):
	''' This function prints mean, standard deviation and CV of K values for all provided tokenFrequencies
	
	Args:
		tokenFrequenciesCollection: the list of tokens and their frequencys for one or more corpi
		plot (boolean): determines if kValues get plotted in a histogram. Default: False

	Returns:
		() void
	'''
	kValuesCollection = {}
	kMeanCollection = {}
	kStDevCollection = {}
	# calculate statistical data:
	for corpus in tokenFrequenciesCollection:
		kValuesCollection[corpus] = kValuesFromTokenFrequencies(tokenFrequenciesCollection[corpus])
		kMeanCollection[corpus] = mean(kValuesCollection[corpus])
		kStDevCollection[corpus] = stdev(kValuesCollection[corpus])
		if plot:
			plotKHistogram(kValuesCollection[corpus])

	# print results for mean, standard deviation and CV:
	for corpus in tokenFrequenciesCollection:
		m = kMeanCollection[corpus]
		sd = kStDevCollection[corpus]
		print('K distribution for ' + corpus + 
			': mean: ' + str(round(m,2)) + 
			', stdev: ' + str(round(sd,2)) +
			', CV: ' + str(round(sd/m,4))
			)

def filterTokenFrequencies(tokenFrequencies, allowNumbers=False):
	''' Filter out tokens containing non-alphabetical tokens.

	Args:
		tokenFrequencies: The frequencies that should be filtered
		allowNumbers (boolean): Set true to allow numbers

	Returns:
		tokenFrequencies minus the filtered elements

	'''
	result = []

	# Loop over each token:
	for tokenFrequency in tokenFrequencies:
		filteredOut = False
		
		# Check if token is only alphabetic or aplhanumeric:
		if allowNumbers:
			if not tokenFrequency[0].isalnum():
				filteredOut = True
		else:
			if not tokenFrequency[0].isalpha():
				filteredOut = True

		# Filter:
		if not filteredOut:
			result.append(tokenFrequency)

	return result

def plotFrequencies(tokenFrequencies, first=1, last=False):
	''' Plot the frequencies on a double-log scale

	Args:
		first (int): The rank of the first element of tokenFrequencies to plot. Default: 1
		last (int): The rank of the last element to plot. Default: size of tokenFrequencies
	Returns:
		() void

	'''
	if not last:
		last = len(tokenFrequencies)

	# prepare the data:
	frequencies = [tupl[1] for tupl in tokenFrequencies[first-1:last]]
	ranks = list(range(first, last+1))
	
	# plot the data:
	fig = plt.figure()
	ax = plt.gca()
	ax.plot(ranks, frequencies)
	ax.set_yscale('log')
	ax.set_xscale('log')
	plt.show()

def plotKHistogram(kValues):
	''' Auxiliary function to plot data in a histogram

	Args:
		data (list of int or float): the data to be plotted

	Returns:
		() void

	'''

	n, bins = np.histogram(kValues, 50)
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
