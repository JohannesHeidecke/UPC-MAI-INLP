import operator
from operator import itemgetter

import nltk
from nltk import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

import statistics
from statistics import mean, stdev

import warnings

def tokenCountsFromFile(filePath, 
tokenCounts = {}, 
onlyPurelyAlphabetic = False, 
charLevel = False, 
convertToLowerCase = False,
tokenizerKind = 'word_tokenize',
useStemming = False,
useLemmatization = False):
	# create tokenizer, stemming or lemmatization objects if needed:
	if not charLevel:
		if tokenizerKind == 'word_punct_tokenize':
			tokenizer = WordPunctTokenizer()
		if useStemming:
			stemmer = PorterStemmer()
		if useLemmatization:
			lemmatizer = WordNetLemmatizer()

	# if both stemming and lemmatizing are set to true, print a warning:
	if useStemming and useLemmatization:
		warnings.warn('The module is asked to use both stemming and lemmatizing. Only stemming will be used.')
	# if charLevel is wanted and stemming or lemmatizing is also wanted
	if charLevel and (useStemming or useLemmatization):
		warnings.warn('Char level is wanted. Stemming and lemmatizing will not be used')

	# open file to read:
	f = open(filePath, 'r')
	# loop over all lines of the file:
	for line in f:
		if charLevel:
			# if char level granularity is wanted, tokens are all characters of the read line:
			tokens = []
			for c in line:
				tokens.append(c)
		else:
			# if char level is not wanted, use a word tokenizer:
			# choose tokenizer according to argument tokenizerKind:
			if tokenizerKind == 'word_tokenize':
				tokens = word_tokenize(line) 
			elif tokenizerKind == 'word_punct_tokenize':
				tokens = tokenizer.tokenize(line)
		# loop over all tokens in the current line:
		for token in tokens:
			if onlyPurelyAlphabetic and not token.isalpha():
				# if purely alphabetic is wanted and a non-alphabetic char was found, skip to next token:
				continue;
			if convertToLowerCase:
				# if lower case is wanted, convert token to lower case:
				token = token.lower()
			if useStemming and not charLevel:
				# if stemming is wanted, use a nltk stemmer to stem the token
				token = stemmer.stem(token)
			elif useLemmatization and not charLevel:
				# if lemmatizing is wanted, use nltk lemmatizer with wordnet to stem. 
				# is not used, if stemming is also activated
				token = lemmatizer.lemmatize(token)
			# increase token count for this token or set to 1 if it doesn't exist yet:
			if token in tokenCounts:
				tokenCounts[token] += 1
			else:
				tokenCounts[token] = 1
	return tokenCounts

def createResultTuples(tokenCounts):
	# sort tokens descending by number of occurences:
	sortedTokenCounts = sorted(tokenCounts.items(),
		key = itemgetter(1),
		reverse=True)
	# calculate total number of tokens for frequency:
	totalNumberOfTokens = 0
	for token in tokenCounts:
		totalNumberOfTokens += tokenCounts[token]
	# create result tuples:
	result = []
	for idx, item in enumerate(sortedTokenCounts):
		rank = idx + 1
		token = item[0]
		occurences = item[1]
		frequency = occurences / totalNumberOfTokens
		k = rank * frequency
		result.append((rank, token, occurences, frequency, k))
	# return result:
	return result

def statisticalResultsK(resultTuples):
	# add all k values from resultTuples to a list
	ks = []
	for item in resultTuples:
		ks.append(item[4])
	# use statistics module to calculate mean and stdev and return results
	statisticalResults = {}
	statisticalResults['mean'] = mean(ks)
	statisticalResults['stdev'] = stdev(ks)
	return statisticalResults

def textualOutput(resultTuples, maxRows = 20):
	# avoid out of range errors:
	if len(resultTuples) < maxRows:
		maxRows = len(resultTuples)
	# print the first maxRows results:
	for i in range(0, maxRows):
		print(resultTuples[i])
	print('- ' * 40)
	# print statistical results for k:
	statisticalResults = statisticalResultsK(resultTuples)
	print('mean: ' + str(statisticalResults['mean']))
	print('stdev: ' + str(statisticalResults['stdev']))



tokenCounts = tokenCountsFromFile('corpus/en.txt', 
	onlyPurelyAlphabetic = True, 
	convertToLowerCase = True, 
	tokenizerKind = 'word_punct_tokenize',
	useLemmatization = True)
resultTuples = createResultTuples(tokenCounts)
textualOutput(resultTuples, maxRows = 20)





