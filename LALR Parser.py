from __future__ import print_function
import copy


def getProductions(productions,states):
	file=open("grammar.txt","r")
	inp=file.readlines()    
	for prod in inp:
		prod=prod.replace("\n","")
		prod=prod.replace("|","->")
		temp=prod.split("->")
		productions.append([temp[0],temp[1]])
		states.add(temp[0])
		for i in range(len(temp)-2):
			productions.append([temp[0],temp[i+2]])
	#print(productions)	
	#print(states)

''' 
Recursively finding first.
Ex: S->ABC
	A->a|epsilon
	B->b|epsilon
	C->c
Therefore, First(S)={a,b,c,epsilon}

'''
def handleEpsilon(first,p,rhs,i):
	try:
		first[p[0]]=first[p[0]].union(first[rhs[i]])
		if(first[rhs[i]].__contains__("e")):
			if(rhs[i+1].isupper()):
				handleEpsilon(first,rhs,i+1)
			else:
				first[p[0]].add(rhs[i+1])	
	except IndexError:
		pass

def findFirst(productions):
	first=dict()
	seen=set()
	while(True):
		old=copy.deepcopy(first);
		for p in productions:
			if(not first.__contains__(p[0])):
				first[p[0]]=set()
			seen.add(p[0])
			rhs=p[1]
			if(rhs[0].islower() or not rhs[0].isalpha()):
				first[p[0]].add(rhs[0])
			elif(seen.__contains__(rhs[0])):
				handleEpsilon(first,p,rhs,0)
			else:
				seen.remove(p[0])
		if(old==first):
			break;
	return first

def productionsWithLHS(element,productions):
	result=list()
	for p in productions:
		if(p[0]==element):
			result.append(p)
	return copy.deepcopy(result)

def closure(itemset,states,productions,lookahead):
	#print(itemset)
	if(states.__contains__(itemset[-1][1][1])):
		parent_production=itemset[-1]
		new = productionsWithLHS(itemset[-1][1][1],productions)
		for temp in new:
			temp[1]="." + temp[1]
			if temp not in itemset:
				lookahead[str(temp)]=lookahead[str(parent_production)]
				itemset.append(temp)
				closure(itemset,states,productions,lookahead)

#Only generating ItemSet0 so far.			
def generateItemSets(productions,states):
	prod=copy.deepcopy(productions)
	itemset=list()
	lookahead=dict()
	p=prod[0]
	p[1]="." + p[1]
	itemset.append(p)
	lookahead[str(p)]="$"
	closure(itemset,states,productions,lookahead)
	print("ItemSet0")
	print(itemset)
	print("LookAhead")
	print(lookahead)

def main():
	productions=list()
	states=set()
	getProductions(productions,states)
	first=findFirst(productions)
	#Augmenting The Grammar
	extra_production = ['S1',productions[0][0]]
	productions.insert(0,extra_production)
	'''print(productions)
	for key,value in first.items():
		print("First(",key,") = ",str(value),sep='')'''
	generateItemSets(productions,states)	


if(__name__=="__main__"):
	main()		