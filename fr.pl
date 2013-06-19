#!/usr/bin/perl
#########################################################
#  Author: Robin Randall
#    File: fr.pl          Find/Replace utility (across multiple files)
#    Date: 06/19/2013
#  Copyright (C) 2013, Robin Randall, All Rights Reserved
#  Internet Credits: Inspiration from similar program by Lionello Lunesu
#########################################################
use strict;
use warnings; 
print "FR\n";
my $args = scalar(@ARGV);
my $arg="";
my $ops="";
my $find="";
my $refind="";
my $replace="";
my $glob="";
my @chars;
if ($args > 0) {
   print "Arguments:\n";
   for (my $i=0 ;$i<$args; $i++) {
      $arg = $ARGV[$i];
      #print "arg[$i]=$arg\n";
      if ( $arg =~ m/^\-+\w+$/) {
         # Options
         if ( $arg =~ m/^\-+b(ackup)?$/i) {
            print "-b=backup mode\n";
            $ops = $ops . "-b";
         }
         if ( $arg =~ m/^\-+f(ilename)?$/i) {
            print "-f=filename mode [*** TO DO ***]\n";
            $ops = $ops . "-f";
         }
         if ( $arg =~ m/^\-+h(elp)?$/i) {
            print "-h=help mode [*** TO DO ***]\n";
            $ops = $ops . "-h";
         }
         if ( $arg =~ m/^\-+n(umber)?$/i) {
            print "-n=number mode [*** TO DO ***]\n";
            $ops = $ops . "-n";
         }
         if ( $arg =~ m/^\-+p(review)?$/i) {
            print "-p=preview mode\n";
            $ops = $ops . "-p";
         }
         if ( $arg =~ m/^\-+q(uiet)?$/i) {
            print "-q=quiet mode\n";
            $ops = $ops . "-q";
         }
         if ( $arg =~ m/^\-+s(ubdir)?$/i) {
            print "-s=subdir mode  [*** TO DO ***]\n";
            $ops = $ops . "-s";
         }
         if ( $arg =~ m/^\-+r(egex)?$/i) {
            print "-r=regex mode\n";
            $ops = $ops . "-r";
         }
         if ( $arg =~ m/^\-+w(ord)?$/i) {
            print "-w=whole word mode\n";
            $ops = $ops . "-w";
         }
      } elsif  ($find eq ""){
               $find = $arg;
               $refind = $find;
               
               if ($ops !~ /\-q/) {
                  print "find = $find\n";
               }
               @chars = split(//, $find);
               if ($ops =~ /\-r/) {
                  $refind = $find;
                  if ($ops !~ /\-q/) {
                     print "refind = $refind\n";
                  }
               } 
               else {
                  $find="";
                  for (my $i=0; $i <= $#chars; $i++) {
                     $find = $find . "[" . $chars[$i] . "]";
                  }
                  if ($ops =~ /\-w/) {
                     $find = "\\b".$find."\\b";
                  }
               }

      } elsif ($arg  =~ /\*\./ ) {
             $glob = "$arg";
             if ($ops !~ /\-q/) {
                print "include = $glob\n";   
             }
      }  
        elsif ($replace eq "") {
             $replace = $arg;
             if ($ops !~ /\-q/) {
                print "replace = $replace\n";
             }
      }
        else { 
           $arg = "Unknown arg";
      }
   }
}
else {
  print "\n  Usage:    FR.pl  [Options] [Find_String] [Replace_String] [include_String]\n";
  print   "  Examples: FR.pl  -w        \"your\"      \"my\"               \n"; 
  print   "            FR.pl  -p         your         my                \*\.\* \n";    
  print   "Options:\n";
  print   "  -w   = Word mode.  Searches only for words. i.e.  \"\\bString\\b\" \n";
  print   "  -p   = Preview mode. Lets you see what lines will be changed but does not change them.\n";
  print   "  -h   = Help mode. Shows this Usage statement and may include other helpful info.\n";
  print   "  -f   = File mode. Replaces filenames instead of the file content.\n";
  print   "  -n   = number mode. Includes the line number in the preview printout.\n";
  print   "  -q   = quiet mode. Suppresses all printout to the console (not recommended.)\n";
  print   "  -s   = Subdirectory mode. All files in the subdirectories will be included as well.\n";
  print   "  -b   = Backup mode. Make a backup (*.BAK) of any files that were changed.\n";
  print   "  -r   = Regex mode. Enter a Regular Expression as the find string.\n\n";
  exit(0);      
}
my $count = 0;
my $total = 0;
if ($glob eq "") {
    $glob = "*.BBE";
}
my @files = glob $glob;
my $file;
my $line;
my $cnt = 0;
my $subs = 0;
foreach $file (@files) {
   $count  = 0;
   $subs   = 0;
   $cnt    = 0;
   open   FILE, "$file" or die;                  # Open input file from @files glob
   print "*";
   if ($replace gt "") {                         # Only open a temp file if user is replacing strings
     open OFILE, ">$file.repl" or die;
   }
   while($line= <FILE> ){                        # Loop through $file looking for find string
     chomp $line;
     if ($cnt=$line=~ /$find/g) {                # Only replace find string if you find it first
        if ($replace gt "") {                    # If user included a replacement string, Try to change it
             $subs=$line=~ s/$find/$replace/g ;
           if ($subs > 0) {                      # Only update stats and print to console if changed
              if ($ops !~ /\-q/) {               # Quiet mode will override Preview mode!             
                 print "\n$line\n";                # For safety, changes are printed except in quiet mode
              }                 
              $count = $count + $subs;
           }
        }
        else {
          if ($ops =~ /\-p/) {
              if ($ops !~ /\-q/) {               # Quiet overrides Preview
                 print "\n$line\n";
              }
          }
        $count = $count + $cnt;
        }
     }
     if (($replace gt "") and ($ops !~ /\-p/ ))  {
       print OFILE "$line\n";                    # Print to temp file whether found or not (replace only)
     }
   }
   close FILE;
   if ($replace gt "") {
      close OFILE;
      if ($count > 0 ) {                   # We changed the file
         if ($ops =~ /\-b/) {
            system "copy $file  $file.BAK";
         }
         if ($ops !~ /\-p/ )  {   
            system "del $file";
            system "ren $file.repl  $file";  # Replace original with the temp .repl file
         }
      } 
      else {
         system "del $file.repl";         # No changes, so we can delete the templ .repl file
      }
   }
   if ($count > 0) {                       # Found or Replaced strings
      if ($ops !~ /\-q/) {                 # Quiet mode will override Preview mode!
         print "$file: ";
         print "\t\tFound $count occurance";  # Take care of single/multiple cases
         if ($count == 1) {
             print "\n";
         } 
         else {
             print "s\n";
         }
      }
   }

   $total = $total + $count;               # Add file count to total count
}
if ($ops !~ /\-q/) {                       # Quiet mode will override Preview mode!
  print "\nTotal $total occurance";          # Take care of single/multiple cases
  if ($total == 1) {
    print "\n";
  } 
  else {
    print "s\n";
  }
  if (($replace gt "") and ($ops =~ /\-p/)) {
    print "(This is only a PREVIEW! No changes have been made! Remove '-p' option and rerun to change.)\n";
  }
}