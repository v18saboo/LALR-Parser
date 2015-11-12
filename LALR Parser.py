from __future__ import print_function
import copy
itemset_num=-1
list_itemsets=list()
bfs_queue=list()
terminals=set()
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
				first[p[0]].add(str(rhs[0]))
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

def findLookahead(temp,parent,la_parent):
	#print("In findLookahead")
	rhs=parent[1]
	index_of_dot=rhs.index(".")
	if(len(rhs)-index_of_dot>2):
		s=rhs[index_of_dot+2]
		if(states.__contains__(s)):
			#print("First(beta alpha)=",first[s])
			res = first[s]
		else:
			res=s
			if(s in la_parent):
				res=la_parent	
	else:
		#print("Nothing new")
		res = la_parent	
	#print("Finished checking")
	return res	

def closure(itemset,states,productions,lookahead):
	print("In Closure")
	print("Current Itemset = ",itemset,"\nlookaheads = ",lookahead)
	rhs=itemset[-1][1]
	try:
		next_state=rhs[rhs.index(".")+1]
		if(states.__contains__(next_state)):
			parent_production=itemset[-1]
			new = productionsWithLHS(next_state,productions)
			print("New list = ",new)
			for temp in new:
				temp[1]="." + temp[1]
				print("Checking  ",temp)
				print("Function Call with args = ",temp,parent_production,lookahead[str(parent_production)])
				new_lookahead=findLookahead(temp,parent_production,lookahead[str(parent_production)])
				print("New lookahead=",new_lookahead)
				print(temp not in itemset)
				if temp not in itemset:
					lookahead[str(temp)]=new_lookahead
					itemset.append(temp)
					closure(itemset,states,productions,lookahead)
				elif (temp in itemset and new_lookahead not in lookahead[str(temp)]):
					print("Already there")
					lookahead[str(temp)]= lookahead[str(temp)]+"|"+new_lookahead
					print(lookahead[str(temp)])
					closure(itemset,states,productions,lookahead)
	
	except IndexError:
		pass				

def swap(string,i):
	j=i+1
	c=list(string)
	c[i],c[j]=c[j],c[i]
	return ''.join(c)

def generateItemSets(productions,states,info_list):
	print("New Itemset!")
	prod=info_list[0]
	parent_number=info_list[1]
	transitionOn=info_list[2]
	parent_lookahead=info_list[3]
	itemset=list()
	lookahead=dict()
	flag=False
	for p,l in zip(prod,parent_lookahead):
		if('e' in p[1]):
			generateItemSets(productions,states,bfs_queue.pop(0))
		if(not p[1].__contains__(".")):
			p[1]="." + p[1]
			flag=True
		elif(p[1][-1]!="."):
			index_of_dot=p[1].index(".")
			p[1]=swap(p[1],index_of_dot)
			flag=True
		itemset.append(p)
		lookahead[str(p)]=l
		if(flag):
			print("lookahead=",lookahead)	
			closure(itemset,states,productions,lookahead)
	if(itemset not in list_itemsets):
		global itemset_num
		itemset_num+=1

		if(itemset_num>0):
			#f2.write("From itemset {} on {} S{}\n".format(parent_number,transitionOn,itemset_num))
			f2.write("{} {} S{}\n".format(parent_number,transitionOn,itemset_num))

			for p in itemset:
				rhs=p[1]
				if(rhs[-1]=="."):
					#f2.write(str(p)+"\n")
					rhs_without_dot=rhs[0:len(rhs)-1:]
					#f2.write(str(rhs_without_dot)+"\n")
					k=[p[0],rhs_without_dot]
					#f2.write(str(k)+"\n")
					#f2.write(str(productions))
					k1=final_productions.index(k)
					#f2.write("From itemset {} on {} R{}\n".format(itemset_num,lookahead[str(p)],k1))
					f2.write("{} {} R{}\n".format(itemset_num,lookahead[str(p)],k1))
		f1.write("ItemSet {}\n".format(itemset_num))
		f1.write(str(itemset)+"\n"+"Lookeahead = \n"+str(lookahead)+"\n")
		list_itemsets.append(itemset)

	else:
		#f2.write("From itemset {} on {} S{}\n".format(parent_number,transitionOn,list_itemsets.index(itemset)))
		f2.write("{} {} S{}\n".format(parent_number,transitionOn,list_itemsets.index(itemset)))
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
		corresponding_lookaheads=[]
		for p in new_itemset_productions:
			corresponding_lookaheads.append(lookahead[str(p)])
		bfs_queue.append([new_itemset_productions,parent_itemset_number,var,corresponding_lookaheads])
	generateItemSets(productions,states,bfs_queue.pop(0))


if(__name__=="__main__"):
	f1=open("itemsets.txt","w")
	f2=open("transitions.txt","w")
	productions=list()
	states=set()
	getProductions(productions,states)
	first=findFirst(productions)
	#Augmenting The Grammar
	extra_production = ['S1',productions[0][0]]
	productions.insert(0,extra_production)
	print(productions)
	for p1 in productions:
		rhs=p1[1]
		for i in rhs:
			if(not i.isupper()):
				terminals.add(i)
				
	f3=open("first.txt","w")
	for key in first.keys():
			f3.write("First("+key+") = ")
			for e in first[key]:
				f3.write(e+" ")
			f3.write("\n")		
	f3.close()
	for s in states:
		f2.write(str(s)+ " ")
	f2.write("\n")	
	for t in terminals:
		f2.write(str(t)+ " ")
	f2.write("\n")	
	final_productions=copy.deepcopy(productions)	
	generateItemSets(productions,states,[[productions[0]],None,None,["$"]])	
	f1.close()
	f2.write(str(itemset_num))
	f2.close()	