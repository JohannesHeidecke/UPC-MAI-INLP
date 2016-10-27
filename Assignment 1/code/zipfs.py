'''
This script implements the required code for the following assignment:
UPC MAI 
INLP 2016/2017
Assignment 1 - Zipf's Law
'''

from zipfs_functions import *

'''
1) Use the text files corpus/en.txt and corpus/es.txt
'''

corpi = {
#	'en': 'corpus/en.txt',
#	'es': 'corpus/es.txt',
#	'de': 'corpus/de-large.txt',
	'test': 'corpus/test.txt'
}

'''
2) Write a program to read the corpus. 
Tokenize it using whatever tokenizer from NLTK or write your own tokenizer.
3) Write a program to check Zipf's first law f = K/r on this corpus:
Count word frequencies, sort them by rank and plot the curve
'''
tokenFrequenciesCollection = {}

print('Calculate token frequencies with simple tokenization:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = corpusToTokenFrequencies(corpi[corpus])
	plotFrequencies(tokenFrequenciesCollection[corpus])
print(tokenFrequenciesCollection['test'][:10])
'''
4) Compute the proportionality constant K between rank and frequency for each word.
Compute its average and deviation.
'''

kValuesReport(tokenFrequenciesCollection, plot = True);

'''
5) Fix issues with tokenization (word case, punctuation marks, numbers, etc).
Repeat steps 3) and 4)
'''

print('\nCacluclate token frequencies case insensitive:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = corpusToTokenFrequencies(corpi[corpus], caseSensitive=False)
kValuesReport(tokenFrequenciesCollection);

print('\nCase insensitive and ignore punctuation and numbers:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = filterTokenFrequencies(tokenFrequenciesCollection[corpus])
kValuesReport(tokenFrequenciesCollection);

print('\nUse Stemming, case insensitive and ignore puncuation and numbers:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = corpusToTokenFrequencies(corpi[corpus], caseSensitive=False, useStemming=True)
	tokenFrequenciesCollection[corpus] = filterTokenFrequencies(tokenFrequenciesCollection[corpus])
	plotFrequencies(tokenFrequenciesCollection[corpus])
kValuesReport(tokenFrequenciesCollection, plot = True);
print(tokenFrequenciesCollection['test'][:10])

'''
6) Move to the char level 
'''

print('\nMove to char level:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = corpusToTokenFrequencies(corpi[corpus], charLevel=True)
kValuesReport(tokenFrequenciesCollection)

print('\nChar level, case insensitive and ignore punctuation and numbers:')
for corpus in corpi:
	tokenFrequenciesCollection[corpus] = corpusToTokenFrequencies(corpi[corpus], charLevel=True, caseSensitive=False)
	tokenFrequenciesCollection[corpus] = filterTokenFrequencies(tokenFrequenciesCollection[corpus])
	plotFrequencies(tokenFrequenciesCollection[corpus])
kValuesReport(tokenFrequenciesCollection, plot = True);
