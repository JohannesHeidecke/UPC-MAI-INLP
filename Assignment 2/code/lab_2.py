from functions_lab_2 import *
from auxiliar import *
from math import log


taggedBrown = 'corpus/taggedBrown.txt'
enCorpus = 'corpus/en.txt'

# importingBrownCorpusFromNLTK(taggedBrown)

wordList = getWordsFromFile(enCorpus)

print wordList[:10]


ubtGrams = countNgrams(wordList, 0)
# ubtGrams[0] = dictionary of unigrams & frequency
# ubtGrams[1] = dictionary of bigrams & frequency
# ubtGrams[2] = dictionary of trigrams & frequency

nUni = len(ubtGrams[0])
nBi = len(ubtGrams[1])
nTri = len(ubtGrams[2])

Huni = 0
for uni in ubtGrams[0]:
	p_x = float(ubtGrams[0][uni]) / nUni
	Huni += -(p_x * log(p_x, 2))

print Huni





