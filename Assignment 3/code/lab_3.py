from functions_lab_3 import *

# Get the fileIds from the NLTK treebank split up into train and test set:
# (trainFileIds, testFileIds) = getFileIds(0.01)
(trainFileIds, testFileIds) = getFileIds(0.9)

# Get all subtrees with second-level POS tags (grandfathers of leaves) as root:
secondLevelPosTrees = getSecondLevelPosTrees(trainFileIds)

# Get counters of the POS sequences for all second-level POS trees:
# The counters are split up into sequences of NP and others.
(npPosSequenceCounter, otherPosSequenceCounter) = getPosSequenceCounters(secondLevelPosTrees)

probsSeqGivenNp = getProbsSeqGivenNp(npPosSequenceCounter)

print(probsSeqGivenNp.most_common(10))

probsNpGivenSeq = getProbsNpGivenSeq(npPosSequenceCounter, otherPosSequenceCounter, probsSeqGivenNp)

nGramTree = getNGramTree(trainFileIds)

probsNgramIsSeq = getProbsNgramIsSeq(nGramTree, npPosSequenceCounter, otherPosSequenceCounter)

probsNgramIsNp = getProbsNgramIsNp(npPosSequenceCounter, probsNgramIsSeq, probsNpGivenSeq)


TPRs = []
FPRs = []
accs = []

for i in tqdm(range(0, 101)):
	f = float(i)/100
	(TP, FP, TN, FN) = evaluateChunker(testFileIds, probsNgramIsNp, f)
	# printErrorReport(TP, FP, TN, FN)
	TPR = TP / (TP + FN)
	FPR = FP / (FP + TN)
	acc = (TP + TN)/(TP + FP + TN + FN)
	TPRs.append(TPR)
	FPRs.append(FPR)
	accs.append(acc)

print(TPRs)

print()

print(FPRs)

print()

print(accs)





















