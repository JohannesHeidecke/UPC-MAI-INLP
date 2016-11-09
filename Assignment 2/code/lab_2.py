from functions_lab_2 import *
from auxiliar import *
from math import log
from tqdm import tqdm


taggedBrown = 'corpus/taggedBrown.txt'
enCorpus = 'corpus/en.txt'
small = 'corpus/small.txt'

# importingBrownCorpusFromNLTK(taggedBrown)

wordList = getWordsFromFile(enCorpus)

ubtGrams = countNgrams(wordList, 0)
# ubtGrams[0] = dictionary of unigrams & frequency
# ubtGrams[1] = dictionary of bigrams & frequency
# ubtGrams[2] = dictionary of trigrams & frequency

# print ubtGrams[0]['parched']

nOWords = len(wordList)

Huni = 0
for uni in tqdm(ubtGrams[0]):
	pX = float(ubtGrams[0][uni]) / nOWords
	Huni += -(pX * log(pX, 2))
print len(ubtGrams[0]), 'single words.'
print 'H unigrams: ', Huni
print 'Perplexity unigrams: ', 2 ** Huni

Hbi = 0
for bi in tqdm(ubtGrams[1]):
	x = bi[0]
	y = bi[1]
	pX = float(ubtGrams[0][x]) / nOWords
	pYGivenX = float(ubtGrams[1][(x, y)]) / ubtGrams[0][x]
	Hbi += - (pX * pYGivenX * log(pYGivenX, 2))
print len(ubtGrams[1]), 'bigrams.'
print 'H bigrams: ', Hbi
print 'Perplexity bigrams: ', 2 ** Hbi

Htri = 0
for tri in tqdm(ubtGrams[2]):
	x = tri[0]
	y = tri[1]
	z = tri[2]
	pX = float(ubtGrams[0][x]) / nOWords
	pYGivenX = float(ubtGrams[1][(x, y)]) / ubtGrams[0][x]
	pZGivenXY = float(ubtGrams[2][(x, y, z)]) / ubtGrams[1][(x, y)]
	Htri += - (pX * pYGivenX * pZGivenXY * log(pZGivenXY, 2))
print len(ubtGrams[2]), 'trigrams.'
print 'H trigrams: ', Htri
print 'Perplexity trigrams: ', 2 ** Htri















