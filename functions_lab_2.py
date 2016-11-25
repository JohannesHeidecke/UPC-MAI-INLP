def unigramProbabilities(listOfWords):
	
	probabilities = {}

	n = len(listOfWords)
	for word in listOfWords:
		pass

	


def countNgramsPWW(l,inic,end=0):
    """
    From a list l of pos tagged words, an inic position and an end position
    a tuple(U,B,T) of dics corresponding to smoothed unigrams, bigrams and trigrams are built following Pos Word Word
    """
    if end == 0:
        end = len(l)
    U={}
    B={}
    T={}
    U[(l[inic][1])]=1
    if (l[inic+1][1]) not in U:
        U[(l[inic+1][1])]=1
    else:
        U[(l[inic+1][1])]+=1
    B[(l[inic][1],l[inic+1][0])]=1
    for i in range(inic+2,end):
        if (l[i][1]) not in U:
            U[(l[i][1])]=1
        else:
            U[(l[i][1])]+=1
        if (l[i-1][1],l[i][0]) not in B:
            B[(l[i-1][1],l[i][0])] = 1
        else:
            B[(l[i-1][1],l[i][0])] +=1
        if (l[i-2][1],l[i-1][0],l[i][0]) not in T:
            T[(l[i-2][1],l[i-1][0],l[i][0])] = 1
        else:
            T[(l[i-2][1],l[i-1][0],l[i][0])] +=1
    return (U,B,T)

def countNgramsPPW(l,inic,end=0):
    """
    From a list l of pos tagged words, an inic position and an end position
    a tuple(U,B,T) of dics corresponding to smoothed unigrams, bigrams and trigrams are built following Pos Pos Word
    """
    if end == 0:
        end = len(l)
    U={}
    B={}
    T={}
    U[(l[inic][1])]=1
    if (l[inic+1][1]) not in U:
        U[(l[inic+1][1])]=1
    else:
        U[(l[inic+1][1])]+=1
    B[(l[inic][1],l[inic+1][1])]=1
    for i in range(inic+2,end):
        if (l[i][1]) not in U:
            U[(l[i][1])]=1
        else:
            U[(l[i][1])]+=1
        if (l[i-1][1],l[i][1]) not in B:
            B[(l[i-1][1],l[i][1])] = 1
        else:
            B[(l[i-1][1],l[i][1])] +=1
        if (l[i-2][1],l[i-1][1],l[i][0]) not in T:
            T[(l[i-2][1],l[i-1][1],l[i][0])] = 1
        else:
            T[(l[i-2][1],l[i-1][1],l[i][0])] +=1
    return (U,B,T)


