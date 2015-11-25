import tkinter as tk

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,2)
        t.pack(side="top", fill="x")
        #t.set(0,0,"Hello, world")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        f=open("first.txt","r")
        listOfLines=f.readlines()
        l=[]
        for item in listOfLines:
            l.append(item)
        #print l
        tup=[]
        for item in l:
            temp=item.split("=")
            temp[1]=temp[1].replace("\n","")
            tup.append(temp)
        #print tup
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(len(tup)):
            current_row = []
            for column in range(columns):
                if(column==1):
                    label = tk.Label(self, text="%s" % (tup[row][1],), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
                else:
                    label = tk.Label(self, text="%s" % (tup[row][0]), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
            self._widgets.append(current_row)
        '''for row in range(len(tup)):
            current_row=[]
            for column in range(columns):
                if(column==0):
                    label = tk.Label(self, text="%s" % (tup[row][0]), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
                else:
                    label = tk.Label(self, text="%s" % (tup[row][1]), 
                                 borderwidth=0, width=10)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)
            self._widgets.append(current_row)'''
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

def func():
    #print "Func"
    app = ExampleApp()
    app.mainloop()