'''from Tkinter import *
root=Tk()
root.geometry("250x250")
rows = []
var = StringVar()
label = Label( root, textvariable=var, relief=RAISED )

var.set("Hey!? How are you doing?")
label.place(bordermode=OUTSIDE,x=100,y=100)
label.pack()'''
'''for i in range(5):
    cols = []
    for j in range(4):
        e = Label(relief=RIDGE)
        e.grid(row=i, column=j, sticky=NSEW)
        e.insert(END, '%d.%d' % (i, j))
        cols.append(e)
    rows.append(cols)

def onPress():
    for row in rows:
        for col in row:
            print col.get(),
        print'''

'''B=Button(text='Fetch')
B.place(bordermode=OUTSIDE, height=100, width=100)
root.mainloop()'''
from tkinter import *
def foo():
	f=open("transitions.txt","r")
	terminals=[]
	nonterminals=[]
	nonterminals=f.readline().split(" ")
	terminals=f.readline().split(" ")
	#print terminals
	#print nonterminals
	lines=f.readlines()
	l=[]
	for item in lines:
		l.append(item.replace("\n",""))
	root = Tk()
	var=StringVar()
	var1=StringVar()
	var2=StringVar()
	label = Label( root, text="State", relief=RAISED ).grid(row=0,column=0)
	#var.set("State")
	label=Label(root,text="ACTION",relief=RAISED).grid(row=0,column=len(nonterminals)//2)
	#var1.set("Goto")
	label=Label(root,text="GOTO",relief=RAISED).grid(row=0,column=len(nonterminals)+len(terminals)//2)
	#var2.set("ACTION")
	'''for j in range(1,len(nonterminals)):
		b = Label(root,text=nonterminals[j])
		b.grid(row=1, column=j)
	print l'''
	#print l
	height = int(l[-1])
	nonterminals.pop()
	terminals.pop()
	terminals.append("$")
	width = 1+len(nonterminals)+len(terminals)
	for i in range(1,height+2): #Rows
		for j in range(0,width): #Columns
			if i==1:
				if j==0:
					b = Label(root, text="")
					b.grid(row=i, column=j)
				else:
					if(j<=len(terminals)):
						#print terminals[j-1]
						b = Label(root, text=terminals[j-1],bg="white",width=5)
						b.grid(row=i, column=j,sticky="nsew", padx=1, pady=1)
					else:
						b = Label(root, text=nonterminals[(j-1)-len(terminals)],bg="white",width=5)
						b.grid(row=i, column=j)
	for i in range(2,height+3):
		b = Label(root, text=i-2,bg="white",width=5)
		b.grid(row=i, column=0)
	#print "List of terminals"
	#print terminals
	l.pop()
	for item in l:
		temp=item.split()
		t=""
		l1=[]
		if temp[1] in nonterminals:
			indexOfNonterm=nonterminals.index(temp[1])
			t=temp[2]
			l1.append(indexOfNonterm + len(terminals))
		else:
			listOfTerminals=temp[1].split("|")
			for item1 in listOfTerminals:
				#print item1
				l1.append(terminals.index(item1))
		for i in range(len(l1)):
			b=Label(root, text=temp[2],bg="white",width=5,borderwidth=0)
			b.grid(row=int(temp[0])+2,column=l1[i]+1,sticky="nsew", padx=1, pady=1)
			
	b=Label(root, text="Accept",bg="white",width=5)
	b.grid(row=3,column=len(terminals))	
	root.mainloop()