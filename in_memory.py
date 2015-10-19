#!/usr/local/env python
def mkdir(someFolder):
    files[someFolder]="D"
def create(file1):
    files[file1]="F"
def create2(someFolder, file1):
    files[someFolder+file1]="F"
def write (some_text, file1):
    files[file1]="F"+some_text
def cat(file1):
    if file1 in files:
       print files[file1]
def find(file1):
    for fi in files:
       if fi.find(file1)>=0:
          print fi
def find2(someFolder, file2):
    for fi in files:
       if fi == someFolder + file2:
          print fi
def ls(someFolder):
    for fi in files:
       if fi.find(someFolder+"/")>=0:
          print fi
def cp(file1, file_path):
    if file1 not in files or file_path not in files:
       print "Error: A file does not exit"
    else:
       files[file_path]=files[file1]
def cp2(someFolder, copyFolder):
    fix=0
    if someFolder not in files or copyFolder not in files:
       print "Error: A folder does not exit"
    else:
       for fi in files:
           f = fi.find(someFolder+"/")
           if f >=0 :
              copyfile = fi[len(someFolder+"/")-1:]
              fix      = files[fi]
    files[copyFolder+copyfile]=fix

def fil(file1):
    if files[file1]=="F":
       return True

def dir(dir1):
    if files[dir1]=="D":
       return True

#############################################################################
files={}
cmd=[]
testing=True
while (testing):
   line = raw_input("/")
   cmd=line.split(' ')
   if cmd[0] == "mkdir":
      if len(cmd) > 2:
          print "Error: Too many parameters - only 1 allowed"
      mkdir(cmd[1])
   elif cmd[0] == "create":
      if len(cmd) > 3:
          print "Error: Too many parameters - only 2 allowed"
      if len(cmd) == 2:
         if cmd[1] in files:
            print "Error: file:"+cmd[1]+" already exists"
         else:
            create(cmd[1])
      if len(cmd)==3:
         if cmd[1]+cmd[2] in files: 
            print "Error: file:"+cmd[2]+" already exists"  
         else:
            create2(cmd[1],cmd[2])
   elif cmd[0] == "write":
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      write(cmd[1],cmd[2])

   elif cmd[0] == "cat":
      if len(cmd) > 2:
         print "Error: Too many parameters - only 1 allowed"      
      cat(cmd[1])
      
   elif cmd[0] == "find":
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      if len(cmd) == 2:
         find(cmd[1])
      else:
         find2(cmd[1],cmd[2])

   elif cmd[0] == "ls":
      if len(cmd) > 2:
         print "Error: Too many parameters - only 1 allowed"      
      ls(cmd[1])

   elif cmd[0] == "cp":
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      if fil(cmd[1]) and fil(cmd[2]):
         cp(cmd[1],cmd[2])
      if dir(cmd[1]) and dir(cmd[2]) :
         cp2(cmd[1],cmd[2])

   elif cmd[0] == "Q" or  cmd[0] == "q":
      exit(0)

   elif cmd[0] =="":
      print files
   else:
      print "Error: Unknown command"
