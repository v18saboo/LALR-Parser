from tkinter import *
import table1
import table
import LALR
#import imageTk
count=0
def sel():
   global count
   count+=1
   selection = "You selected the option " + str(var.get())
   f=open("grammar.txt","w")
   if(count==1):
      s=T.get("1.0", END)
      f.write(s)
      print("Done")
      f.close()
      LALR.main()
   if(var.get()==3):
        table1.foo()
   elif(var.get()==1):
        #lines =T.get("1.0", END).splitlines()
        table.func()
   label.config(text = selection)
#LALR.main()
root = Tk()
root.geometry("500x500")
var = IntVar()
#photo=PhotoImage(file="images.png")
B = Button(root,state="disabled",height=10,width=10,text="LALR PARSER")#image="C:\Users\Kumar BN\Desktop\CDLAb\images.png")
B.place(x=200,y=200)
B.pack()
R1 = Radiobutton(root, text="Find First", variable=var, value=1,
                  command=sel)
R1.pack( anchor = W )

R2 = Radiobutton(root, text="Generate Item Sets (Not Working Yet)", variable=var, value=2,
                  command=sel)
R2.pack( anchor = W )

R3 = Radiobutton(root, text="Generate Table", variable=var, value=3,
                  command=sel)
R3.pack( anchor = W)

label = Label(root)
label.pack()
T = Text(root,borderwidth=2, height=20, width=60,highlightthickness=1)
T.config(highlightbackground="white")
T.pack(side=LEFT,padx=10,pady=10)
T.place()
root.mainloop()