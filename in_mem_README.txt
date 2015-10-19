4 - In-Memory File System

Create a progrm that will mimic a file system in a non-persistent way. 
Your program should not write anything to the HDDs and when it is restarted, 
the "file system" should be empty. Assume file names can contain only [A-Za-z0-9_] and start with a letter. (No spaces)
Parameters should be preceded by "/" (slash) character
Your program should handle the following file system commands:

Create a new folder - Takes a parameter of absolute folder path
Create a new file - Take a parameter of absolute file path
Add content to a file - Take 2 parameters: Content to append to a file; Absolute path to a file
Copy files - Takes 2 parameters: Absolute path to a source file; Absolute path to a destination file (NOTE: If destination file exists, it will be overwritten)
Display file contents - Takes absolute path to a file as an input; Prints out file contents as an output
List folder contents - Takes absolute path to a folder as an input; Prints out folder contents as an output
Search for a file by name - Takes name of a file to find; Prints out list of absolute paths to files with matching names
Search for a file by name - Takes 2 parameters: Absolute path to a starting folder and file name; Outputs list of absolute paths to files with matching names
(Bonus) Copy folders - Takes 2 parameters: Absolute path to source folder, Absolute path to destination folder
Your program should be capable of running the following commands:

mkdir /someFolder
create /file1
create /someFolder/file1
write "Some text" /file1
cat /file1
cp /file1 /someFolder/file2
find /file2                  (Should return all found locations for file2)
find /someFolder /file2
ls /someFolder
(Bonus) cp /someFolder /copyFolder
Your program should also handle error cases. Here are some examples:

Creating a file in a non-existent folder
Appending text to a non-existent file
Listing contents of a non-existent folder
Displaying contents of a non-existent file
