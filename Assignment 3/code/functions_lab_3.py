from nltk.corpus import treebank
from nltk.tree import Tree
from nltk.tree import ParentedTree
from collections import Counter
import numpy as np
from tqdm import tqdm

def getFileIds(trainProportion=0.9):
	fileIds = treebank.fileids()
	cutPointTestData = int(len(fileIds) * trainProportion)
	return (fileIds[:cutPointTestData], fileIds[cutPointTestData:])

def getSecondLevelPosTrees(fileIds):
	secondLevelPosTrees = []
	for fileId in tqdm(fileIds):
		tree = treebank.parsed_sents(fileId)[0]
		tree = ParentedTree.fromstring(str(tree))
		for subtree in tree.subtrees():
			if getMinTreeDepth(subtree) == 3:
				secondLevelPosTrees.append(subtree)
	return secondLevelPosTrees

def getMinTreeDepth(tree):
	leaves = tree.leaves()
	depths = []
	for leaf in leaves:
		leafIndex = leaves.index(leaf)
		treeLocation = tree.leaf_treeposition(leafIndex)
		leafDepth = len(treeLocation) + 1
		depths.append(leafDepth)		
	return np.min(depths)

def getMaxTreeDepth(tree):
	leaves = tree.leaves()
	depths = []
	for leaf in leaves:
		leafIndex = leaves.index(leaf)
		treeLocation = tree.leaf_treeposition(leafIndex)
		leafDepth = len(treeLocation) + 1
		depths.append(leafDepth)		
	return np.max(depths)

def getPosSequenceCounters(secondLevelPosTrees):
	npPosSequences = []
	otherPosSequences = []
	for secondLevelPosTree in tqdm(secondLevelPosTrees):
		label = secondLevelPosTree.label()
		leaves = secondLevelPosTree.leaves()
		posSequence = leavesToPosSequence(leaves, secondLevelPosTree)
		if label.startswith('NP'):
			npPosSequences.append(posSequence)
		else:
			otherPosSequences.append(posSequence)
	npPosSequenceCounter = Counter(npPosSequences)
	otherPosSequenceCounter = Counter(otherPosSequences)
	return (npPosSequenceCounter, otherPosSequenceCounter)

def leavesToPosSequence(leaves, tree):
	poss = leavesToPosList(leaves, tree)
	return posListToSequence(poss)

def leavesToPosList(leaves, tree):
	poss = []
	for leaf in leaves:
		leafIndex = leaves.index(leaf)
		treeLocation = tree.leaf_treeposition(leafIndex)
		leaveParent = str(tree[treeLocation[:-1]]).split(" ")
		pos = leaveParent[0][1:]
		poss.append(pos)
	return poss

def posListToSequence(poss):
	sequence = '(' + poss[0]
	if len(poss) == 1:
		sequence = sequence + ','
	for seqPos in range(1, len(poss)):
		sequence = sequence + ', ' + poss[seqPos]
	sequence = sequence + ')'
	return sequence

def getLongestSequenceLength(posSequenceCounter):
	maxSequenceLength = 0
	for posSequence in posSequenceCounter:
		length = getSequenceLength(posSequence)
		if length > maxSequenceLength:
			maxSequenceLength = length
	return maxSequenceLength

def getSequenceLength(posSequence):
	return len(posSequence.split(', '))

def getProbsSeqGivenNp(npPosSequenceCounter):
	probSeqGivenNp = Counter()
	nOSequences = sum(npPosSequenceCounter.values())
	for sequence in npPosSequenceCounter:
		probSeqGivenNp[sequence] = float(npPosSequenceCounter[sequence]) / nOSequences
	return probSeqGivenNp

def getNGramTree(fileIds):
	nGramTree = {}
	nGramTree['count'] = 0
	for fileId in tqdm(fileIds):
		tree = treebank.parsed_sents(fileId)[0]
		tree = ParentedTree.fromstring(str(tree))
		leaves = tree.leaves()
		for n in range(1, len(leaves)+1):
			for i in range(n, len(leaves)+1):
				currentNode = nGramTree
				nGramPosCounter = 0
				for leaf in leaves[i-n:i]:
					nGramPosCounter += 1
					leafIndex = leaves.index(leaf)
					treeLocation = tree.leaf_treeposition(leafIndex)
					leaveParent = str(tree[treeLocation[:-1]]).split(" ")
					pos = leaveParent[0][1:]
					if not pos in currentNode:
						currentNode[pos] = {}
						currentNode[pos]['count'] = 0
					currentNode = currentNode[pos]
					if nGramPosCounter == n:
						currentNode['count'] += 1			
	return nGramTree

def getCountForSequence(nGramTree, sequence):
	poss = sequenceToPoss(sequence)
	currentNode = nGramTree
	for pos in poss:
		if pos in currentNode:
			currentNode = currentNode[pos]
	return currentNode['count']

def sequenceToPoss(posSequence):
	result = posSequence[1:-1]
	if result[-1] == ',':
		result = result[:-1]
	return result.split(', ')

def getProbsNpGivenSeq(npPosSequenceCounter, otherPosSequenceCounter, probsSeqGivenNp):
	probsNpGivenSeq = Counter()
	# general probability of a sequence being a NP:
	nONpSequences = sum(npPosSequenceCounter.values())
	nOOtherSequences = sum(otherPosSequenceCounter.values())
	probIsNp =  (nONpSequences) / (nONpSequences + nOOtherSequences)
	for seq in npPosSequenceCounter:
		# general probability of this sequence occuring:
		probIsSequence = (npPosSequenceCounter[seq] + otherPosSequenceCounter[seq]) / (nONpSequences + nOOtherSequences)
		# probability of this seq occuring given that it's a NP:
		probSeqGivenNp = probsSeqGivenNp[seq]
		nominator = probSeqGivenNp * probIsNp
		if nominator == 0:
			probsNpGivenSeq[seq] = 0
		else:
			probsNpGivenSeq[seq] = np.round(nominator / probIsSequence, 3)
	return probsNpGivenSeq

def getProbsNgramIsSeq(nGramTree, npPosSequenceCounter, otherPosSequenceCounter):
	probsNgramIsSeq = Counter()
	for seq in npPosSequenceCounter:
		numerator = (npPosSequenceCounter[seq] + otherPosSequenceCounter[seq])
		if numerator == 0:
			probsNgramIsSeq[seq] = 0
		else:
			probsNgramIsSeq[seq] =  numerator / getCountForSequence(nGramTree, seq) 
		if seq == '(NN, NNS)':
			print(seq)
			print(probsNgramIsSeq[seq])
	return probsNgramIsSeq

def getProbsNgramIsNp(npPosSequenceCounter, probsNgramIsSeq, probsNpGivenSeq):
	probsNgramIsNp = Counter()
	for seq in npPosSequenceCounter:
		probsNgramIsNp[seq] = probsNgramIsSeq[seq] * probsNpGivenSeq[seq]
		# probsNgramIsNp[seq] = probsNpGivenSeq[seq]
	return probsNgramIsNp

def evaluateChunker(testFileIds, probsNgramIsNp, threshold=0.5):
	TP = 0
	FP = 0
	TN = 0
	FN = 0

	for fileId in testFileIds:

		actualLabels = getActualLabelsForFile(fileId)
		chunkerLabels = getNpChunks(fileId, probsNgramIsNp, threshold)

		for i in range(0, len(actualLabels)):
			if chunkerLabels[i] == 1:
				if actualLabels[i] == 1:
					TP += 1
				else:
					FP += 1
			else:
				if actualLabels[i] == 0:
					TN += 1
				else:
					FN += 1

	return (TP, FP, TN, FN)


def getActualLabelsForFile(fileId):
	result = []
	tree = treebank.parsed_sents(fileId)[0]
	tree = ParentedTree.fromstring(str(tree))
	leaves = tree.leaves()
	# Fill result with actual labels:
	for leaf in leaves:
		leafIndex = leaves.index(leaf)
		treeLocation = tree.leaf_treeposition(leafIndex)
		nPFound = False
		for i in range(2,len(treeLocation)):
			leaveGrandParent = str(tree[treeLocation[:-i]]).split(" ")
			pos = str(leaveGrandParent[0][1:]).strip()
			if str(pos).startswith('NP'):
				nPFound = True
		# leaveGrandParent = str(tree[treeLocation[:-2]]).split(" ")
		# pos = str(leaveGrandParent[0][1:]).strip()
		# if str(pos).startswith('NP'):
		# 	nPFound = True
		if nPFound:
			result.append(1)
		else:
			result.append(0)
	# print('actual labels: ' + str(result))
	return result

def getNpChunks(fileId, probsNgramIsNp, threshold):
	result = []
	tree = treebank.parsed_sents(fileId)[0]
	tree = ParentedTree.fromstring(str(tree))
	leaves = tree.leaves()
	# Fill result with default negative labels:
	for leaf in leaves:
		result.append(0)
	poss = leavesToPosList(leaves, tree)
	for startIndex in range(0, len(poss)):
		for endIndex in range(startIndex+1, len(poss)+1):
			possibleChunk = poss[startIndex:endIndex]
			possibleSequence = posListToSequence(possibleChunk)
			if possibleSequence in probsNgramIsNp:
				if probsNgramIsNp[possibleSequence] > threshold:
					for i in range (startIndex, endIndex):
						result[i] = 1
	# print('chunks:\t' + str(result))
	# print(leaves)
	# print(poss)
	return result

def printErrorReport(TP, FP, TN, FN):
	print('TP: '+ str(TP))
	print('FP: '+ str(FP))
	print('TN: '+ str(TN))
	print('FN: '+ str(FN))
	print('accuracy: ' + str((TP + TN)/(TP + FP + TN + FN)))







