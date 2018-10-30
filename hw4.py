import math
import matplotlib.pyplot as plt

'''
vocab = open("hw4_vocab.txt", "r").read().splitlines();
uni = open("hw4_unigram.txt", "r").read().splitlines();
bigram = open("hw4_bigram.txt", "r").read().splitlines();
'''
vocab = open("hw4_vocab.txt", "r").read().splitlines();
vocab = [v.upper() for v in vocab];
vocab.insert(0, 'NULL')

def partA():
	uni = open("hw4_unigram.txt", "r").read().splitlines();
	uni = [int(u) for u in uni];
	totalNum = sum(uni);

	#unigram distribution over all words
	for i in range(len(uni)):
		uni[i] = uni[i] / totalNum

	uniPairs = list(zip(vocab, uni));

	'''
	nPairs = [n for n in uniPairs if n[0][0] == 'N']
	print(nPairs)
	'''

	return uniPairs;

def partB():
	bigram = open("hw4_bigram.txt", "r").read().splitlines();

	bigramTable = [];
	for i in range(len(bigram)):
		bigramTabs = bigram[i].split('\t');
		bigramTable.append([int(bigramTabs[0]), int(bigramTabs[1]), int(bigramTabs[2])]);

	startIndex = 0;
	endIndex = 0;
	size = len(bigramTable) + 1
	wordCounts = [0] * size;
	for i in range(len(bigramTable)):
		index = bigramTable[i][0];
		wordCounts[index] += bigramTable[i][2];

	for i in range(len(bigramTable)):
		bigramTable[i][2] /= wordCounts[bigramTable[i][0]];

	return bigramTable;
	'''
		if(i != bigramTable[startIndex][0]):
			print("no bigrams at: %d" % (i))
			continue;
		else:
			for j in range(startIndex, len(bigramTable)):
				if(bigramTable[j][0] != bigramTable[startIndex][0]):
					endIndex = j
					break;

			print("Vocab Word: " + vocab[i])
			print("StartIndex: %d" % startIndex)
			print("EndIndex: %d" % endIndex)

			totalWordsGiven = sum([w[2] for w in bigramTable[startIndex:endIndex]])

			curr = startIndex;
			while curr < endIndex:
				bigramTable[curr][2] /= totalWordsGiven
				curr += 1;

			startIndex = endIndex;
			'''
	
	'''
	haveIndex = vocabIndex('HAVE')

	haveTable = [b for b in bigramTable if b[0] == haveIndex]
	haveTable = sorted(haveTable, key = lambda x: x[2], reverse = True)
	topTen = haveTable[:10];

	wordTable = [];
	for i in range(len(topTen)):
		wordTable.append([vocab[topTen[i][1]], topTen[i][2]);

	#print(wordTable)
	'''

	
def partC(sentence, v):
	
	uniTable = partA();
	bigramTable = partB();

	words = sentence.split(' ');
	unigramProb = 1.0

	for w in words:
		unigramProb *= uniTable[vocabIndex(w)][1]

	bigramProb = 1.0
	previous = '<s>'
	for w in words:
		index = vocabIndex(w)
		givenIndex = vocabIndex(previous)

		subset = [b for b in bigramTable if b[1] == index and b[0] == givenIndex]

		if(len(subset) == 0):
			bigramProb = 0;
			print("In Training Corpus " + w + " is never preceded by " + previous)
			print("Previous Word: " + previous + " index is %d" % givenIndex)
			print("Current Word: " + w + " index is %d" % index)
		else:	
			bigramProb *= subset[0][2];

		previous = w;

	LLUni = -10000000;
	print("Log Likelihood Unigram")
	if(unigramProb == 0):
		print("Undefined domain error")
	else:
		LLUni = math.log(unigramProb);
		print(LLUni)
	print("Log Likelihood Bigram")
	LLBi = -10000000;
	if(bigramProb == 0):
		print("Undefined domain error")
	else:
		LLBi = math.log(bigramProb);
		print(LLBi)

	return [unigramProb, bigramProb];

def partE(sentence):
	Probabilities = partC(sentence, 1.0);
	XData = []
	YData = []
	for i in range(0, 100):
		v = i * .01;
		XData.append(v)
		mixture = math.log(((1-v) * Probabilities[0]) + (v * Probabilities[1]))
		YData.append(mixture)

	plt.scatter(XData, YData);
	plt.title("Mixture Model")
	plt.xlabel("lamda")
	plt.ylabel("log likelihood")
	plt.show();

	return;

def vocabIndex(word):
	
	for i in range(len(vocab)):
		if(vocab[i] == word.upper()):
			return i
#partA()
#partB()
#partC("ten billion dollars didn't last very long", 1.0)
#partC("the recent officials said they incorporated prices", 1.0)
partE("the recent officials said they incorporated prices")
