from __future__ import print_function
import copy
itemset_num=-1
list_itemsets=list()
bfs_queue=list()
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
	rhs=itemset[-1][1]
	try:
		next_state=rhs[rhs.index(".")+1]
		if(states.__contains__(next_state)):
			parent_production=itemset[-1]
			new = productionsWithLHS(next_state,productions)
			for temp in new:
				temp[1]="." + temp[1]
				if temp not in itemset:
					lookahead[str(temp)]=lookahead[str(parent_production)]
					itemset.append(temp)
					closure(itemset,states,productions,lookahead)
	except IndexError:
		pass				

def swap(string,i):
	j=i+1
	c=list(string)
	c[i],c[j]=c[j],c[i]
	return ''.join(c)

#Only generating ItemSet0 so far.			
def generateItemSets(productions,states,info_list):
	prod=info_list[0]
	parent_number=info_list[1]
	transitionOn=info_list[2]
	itemset=list()
	lookahead=dict()
	flag=False
	for p in prod:
		if(not p[1].__contains__(".")):
			p[1]="." + p[1]
			flag=True
		elif(p[1][-1]!="."):
			index_of_dot=p[1].index(".")
			p[1]=swap(p[1],index_of_dot)
			flag=True
		itemset.append(p)
		lookahead[str(p)]="$"
	if(flag):	
		closure(itemset,states,productions,lookahead)
	if(itemset not in list_itemsets):
		global itemset_num
		itemset_num+=1
		if(itemset_num>0):
			f2.write("From itemset {} on {} goto itemset {}\n".format(parent_number,transitionOn,itemset_num))	
		f1.write("ItemSet {}\n".format(itemset_num))
		f1.write(str(itemset)+"\n")
		list_itemsets.append(itemset)
	else:
		f2.write("From itemset {} on {} goto itemset {}\n".format(parent_number,transitionOn,list_itemsets.index(itemset)))
		if(len(bfs_queue)!=0):
			generateItemSets(productions,states,bfs_queue.pop(0))
		return;
	afterDot=list()
	# Key -> terminal/non terminal after the dot. 
	# Value -> List of all productions which have Key after the dot. Value forms the base of the itemset on transition on Key.
	rhs_afterDot=dict()
	copy_itemset=copy.deepcopy(itemset) 
	for i in copy_itemset:
		if (i[1][-1]=="."):
			continue
		next=i[1].index(".")+1
		if not afterDot.__contains__(i[1][next]):
			afterDot.append(i[1][next])
			rhs_afterDot[i[1][next]]=list()
		rhs_afterDot[i[1][next]].append(i)	
	#print(afterDot)	
	#print(rhs_afterDot)
	parent_itemset_number = itemset_num	
	for var in afterDot:
		#Make a list of all variables after dot.Find their productions. Move the dot to the right by one. Find closure of that itemset.
		new_itemset_productions = rhs_afterDot[var]
		#generateItemSets(productions,states,new_itemset_productions) -----> DFS Method. Comment lines 116,117,138 and 139 to use this.
		bfs_queue.append([new_itemset_productions,parent_itemset_number,var])
	generateItemSets(productions,states,bfs_queue.pop(0))
	#print("LookAhead")
	#print(lookahead)

def main():
	productions=list()
	states=set()
	getProductions(productions,states)
	first=findFirst(productions)
	#Augmenting The Grammar
	extra_production = ['S1',productions[0][0]]
	productions.insert(0,extra_production)
	print(productions)
	for key,value in first.items():
		print("First(",key,") = ",str(value),sep='')
	generateItemSets(productions,states,[[productions[0]],None,None])	


if(__name__=="__main__"):
	f1=open("itemsets.txt","w")
	f2=open("transitions.txt","w")
	main()
	f1.close()
	f2.close()	