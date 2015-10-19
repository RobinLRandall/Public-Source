#!/usr/local/env python
#############################################################
# Subject: In-Memory File System
# Author:  Robin Randall 
# File:    obj_memory.py
# Date:    10/17/2015
# Copyright 2015 Robin Randall, All rights reserved
#############################################################A
class Folder:                         # Folder or Directory Object
  def __init__(self, name, kind="D"): # Constructor
      self.n =name
      self.k =kind
  def mkdir(self,someFolder):         # Folder methods
      filesys[someFolder]=self.k
  def ls(self,someFolder):
    for fi in filesys:
       if fi.find(someFolder+"/")>=0:
          print fi

class File:                            # File Object
  def __init__(self, name, kind="F", content=""):     # Constructor
      self.n =name
      self.k =kind
      self.c =content
  def create(self,file1):              # File methods
    filesys[file1]=self.k              # create
  def create2(self,someFolder, file1): # 2nd version of create
    filesys[someFolder+file1]=self.k
  def write (self,some_text, file1):   # write method 
    filesys[file1]=self.k+some_text    
  def cat(self,file1):                 # cat method
    if file1 in filesys:
       print filesys[file1]
  def find(self,file1):                # find method
    for fi in filesys:
       fr = fi[::-1]       #reverse
       f  = fr.find("/")
       if fi[-f-1:] == file1:
          print fi
  def find2(self,someFolder, file2):   # 2nd version of find method
    for fi in filesys:
       if fi == someFolder + file2:
          print fi
  def cp(self,file1, file_path):       # cp method
    if file1 not in filesys or file_path not in filesys:
       print "Error: A file does not exit"
    else:
       filesys[file_path]=filesys[file1]
  def cp2(self,someFolder, copyFolder):# 2nd version of cp method
    fix=0
    if someFolder not in filesys or copyFolder not in filesys:
       print "Error:  '"+someFolder+"' or '"+copyFolder+"' does not exit"
    else:
       for fi in filesys:
           f = fi.find(someFolder+"/")
           if f >=0 :
              copyfile = fi[len(someFolder+"/")-1:]
              fix      = filesys[fi]
    filesys[copyFolder+copyfile]=fix

def fil(file1):
    if file1 in filesys and filesys[file1][0]=="F":   # fil method to determine a File
       return True

def dir(dir1):                                        # dir method to determine a Folder or Directory
    if dir1 in filesys and filesys[dir1]=="D":
       return True

#############################################################################
global filesys  
filesys={}     # Dictionary used to model the filesystem  
cmd=[]         # Contains parsed command line
testing=True   # Program loops until user enters "q" or "Q" for quit
#############################################################################
def filesys_App():
  while (testing):                                           # Main command loop
   line = raw_input("$")
   if line == "Q" or  line == "q":                         # Quit program
      exit(0)
   cmd=line.split(' ')                                     # Parse command line
   if len(cmd) > 1:
      if cmd[1][0] != "/":
         print "Parameters must start with '/'"
   else:
      print "Error: Commands must have at least one parameter"

   if cmd[0] == "mkdir":                                    # "mkdir" Verification of parameters
      if len(cmd) > 2:
          print "Error: Too many parameters - only 1 allowed"
      folder=Folder(cmd[1],"D")                             # Create Folder object
      folder.mkdir(cmd[1])
   elif cmd[0] == "create":                                 # "create" Verification of parameters
      if len(cmd) > 3:
          print "Error: Too many parameters - only 2 allowed"
      if len(cmd) == 2:
         if cmd[1] in filesys:
            print "Error: file:"+cmd[1]+" already exists"
         else:
            filex=File(cmd[1])                              # Create File object
            filex.create(cmd[1])
      if len(cmd)==3:
         if cmd[1] not in filesys:
            print "Error: Folder:"+cmd[1]+" does not exist" # Check existance
         if cmd[1]+cmd[2] in filesys: 
            print "Error: file:"+cmd[2]+" already exists"  
         else:
            filex=File(cmd[1])                              # Create File object
            filex.create2(cmd[1],cmd[2])
   elif cmd[0] == "write":                                  # "write" Verification of parameters
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      if cmd[2] not in filesys:
         print "Error: file:"+cmd[2]+" does not exist"      # Check if file exists
      else:
         filex.write(cmd[1],cmd[2])
   elif cmd[0] == "cat":                                    # "cat" Verification of parameters
      if len(cmd) > 2:
         print "Error: Too many parameters - only 1 allowed"
      if cmd[1] not in filesys:
         print "Error: file:"+cmd[1]+" does not exist"      #  Check if file exists
      else:
         filex.cat(cmd[1])
      
   elif cmd[0] == "find":                                   # "find" Verification of parameters
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      if len(cmd) == 2:
         filex.find(cmd[1])
      else:
         filex.find2(cmd[1],cmd[2])

   elif cmd[0] == "ls":                                     # "ls" Verification of parameters
      if len(cmd) < 2:
         print "Error: Must have 1 parameter"
         continue
      if len(cmd) > 2:
         print "Error: Too many parameters - only 1 allowed"
      if cmd[1] not in filesys:
         print "Error: folder:"+cmd[1]+" does not exist"    # Check if folder exists
      else:
         folder.ls(cmd[1])

   elif cmd[0] == "cp":                                      # "cp" Verification of parameters
      if len(cmd) > 3:
         print "Error: Too many parameters - only 2 allowed"
      if fil(cmd[1]) and fil(cmd[2]):
         filex.cp(cmd[1],cmd[2])
      if dir(cmd[1]) and dir(cmd[2]) :
         filex.cp2(cmd[1],cmd[2])
      else:
         print "Error: a directory does not exist"

   elif cmd[0] =="":   # "\n" allows testing of "filesys" dictionary to see if commands populate correctly
      print filesys
   else:
      print "Error: Unknown command"

if __name__ == "__main__" :
     filesys_App()









