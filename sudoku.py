from tkinter import *
from tkinter.filedialog import askopenfilename 
from tkinter import messagebox

#### GUI related section ############
def SolveOptionPressed():
   filemenu.entryconfig("Load",state=DISABLED)
   menu.entryconfig("Solve",state=DISABLED)
   Solve(sudoku,0,0)
   msgatbottom.configure(text="Solved. Ready to load next Sudoku")

def LoadFile():
   global endflag, origsudoku

   filname=askopenfilename() 
   sudoku=LoadCSVtoArray(filname)           
   endflag=False
   UpdateBoard(sudoku)
   menu.entryconfig("Solve",state=NORMAL)
   msgatbottom.configure(text="Sudoku loaded. Ready to solve")
   
def LoadCSVtoArray(filname):
   import csv
   with open(filname) as f:
       reader = csv.reader(f)
       i=0
       for row in reader:
          sudoku[i]=row
          i=i+1
   for i in range(0,9):
       for j in range(0,9):
          a=sudoku[i][j]
          if(len(a)==0):
             sudoku[i][j]=orig_sudoku[i][j]=0
          else:
             sudoku[i][j]=orig_sudoku[i][j]=int(sudoku[i][j])
   return sudoku          
   
def UpdateBoard(board):
   for i in range(0,9):
      for j in range(0,9):
           a=board[i][j]
           if a==0:
              cell[i+1][j+1].configure(text="")  
           else:      
              if (orig_sudoku[i][j]==0):
                 txtcolor="blue"
              else:
                 txtcolor="black"  
              cell[i+1][j+1].configure(text=a, fg=txtcolor)  
              
def GridColor(i,j):
    z=(3*int((i-1)/3))+1 + int((j-1)/3)
    if z%2==0:
       z="pink"
    else:
       z="ghostwhite"
    return z
    
########## Sudoku Solving section starts here ##########

def Solve(sudoku, cellX, cellY):    
    global endflag     
    #If the y value is 9 then the sudoku has been solved.
    if endflag==True:
      return
    if(cellY > 8):
      endflag=True
      UpdateBoard(sudoku)
      ShowBoard(sudoku);    
      filemenu.entryconfig("Load",state=NORMAL)
      return
        
    else:    
      #Here we calculate the next digit for the solve routine to try.
      nextX = cellX;
      nextY = cellY;
      if(cellX == 8):
        #When at the end of a row add 1 to the row and reset the "column" to 0.
        nextX = 0
        nextY += 1    
      else:
        nextX += 1
      
      #If the digit was already given to us, we can move onto the next one.
      if(sudoku[cellY][cellX] != 0):
        Solve(sudoku, nextX, nextY)
      else:
        #Otherwise, starting at 1 through 9 we check if the number is "legal"
        #and if so place that number, and move on to the next cell.
        for checkNum in range(1, 10):         
           if(CheckSquare(sudoku, cellX, cellY, checkNum) \
             and CheckRow(sudoku, cellY, checkNum) \
             and CheckCol(sudoku, cellX, checkNum)):          
             sudoku[cellY][cellX] = checkNum
             Solve(sudoku, nextX, nextY)    
        
        #If we get to here it means in it's current state the sudoku is impossible
        #which means that one of the numbers we "placed" earlier is incorrect.
        sudoku[cellY][cellX] = 0

def ShowBoard(s):
   for x in range(0,9):
      print()
      for y in range(0,9):
         print(s[x][y],end="")
   print() 
      
def CheckRow(sudoku,rowY,toCheck):
    # loops round each digit in a row.
    for x in range(0,9):
       #Checks if the given number is the same as 
       #the current digit and returns false if so.
       if (toCheck == sudoku[rowY][x]):
          return False        
    return True # the number is not in the row.

def CheckCol(sudoku, colX, toCheck):
    # Loops round each digit in a column.
    for y in range(0,9):    
      if (toCheck == sudoku[y][colX]):
      
        return False
    return True # the number is not in the column.


def CheckSquare(sudoku, reqX, reqY, toCheck):
   #This method is given a cell location and a number to check, it then checks
   #whether that number is already in the 3x3 square and returns false if so.

    if(reqX < 3):
      colX = 0
    elif (reqX < 6):
      colX = 3
    else:
      colX = 6
   
    #We do the same but for the rows. For example if the y value is 5 then
    #the related square would be on the second row.
    if(reqY < 3):
      rowY = 0
    elif (reqY < 6):
      rowY = 3
    else:
      rowY = 6
  
    # We have now defined the square we need to check and have the top left
    # co-ordinate stored in the variables rowY and colX.
    # We now loop round and check each digit in the square, and if a digit matches
    # we return false.

    for y in range(rowY, rowY + 3): 
      for x in range(colX, colX + 3):
        if(sudoku[y][x] == toCheck):
            return False
          
    return True # number not in the square.  
           

##############  Main procedure starts here  

sudoku = [[0 for x in range(9)] for x in range(9)]      # Define 2D array 9x9   
orig_sudoku = [[0 for x in range(9)] for x in range(9)] # Define 2D array 9x9  
cell   = [[1 for x in range(10)] for x in range(10)]    # Define 2D array 9x9  
endflag=False
root = Tk()
root.title("Sudoku")

menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)

actionmenu= Menu(menu)
menu.add_command(label="Solve", state=DISABLED, command=SolveOptionPressed)


filemenu.add_command(label="Load",  command=LoadFile)

frame=Frame(root)
frame.grid(ipady=1,ipadx=1)

for i in range(1,10):
   for j in range(1,10):
     cell[i][j] = Label(frame, width=4, font="bold", height=2, relief="sunken")
     cell[i][j].grid(row=i,column=j,  padx=3, pady=2)
     cell[i][j].configure(bg=GridColor(i,j))
msgatbottom=Label(frame,height=1)
msgatbottom.grid(row=10,column=1,columnspan=9,sticky="we")
msgatbottom.configure(text="Load a Sudoku puzzle")
mainloop()

