#!/usr/bin/env python
# SuperTester v1.4 by Albert Huang
# =================================
# SuperTester v1.4 - a mini testing suite for programs using standard I/O!
# Copyright (C) 2014 Albert Huang.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =========================================================================
# Before using this really fun (and colorful) debugging tool, you MUST put
# this line at the very beginning of main():
# 
# setvbuf(stdout, NULL, _IONBF, 0);
# 
# This forces your C program to buffer output!
# Finally, make sure to remove any extraneous debug statements before running
# this program! The valid output will not match any extra debug statements!
# 
# This little script assumes that your program is ./myprog.
# If it isn't, you can do either of the following:
#   1) Compile it to ./myprog:
#      gcc coolcode.c cool2.c cool3.c -o myprog
#   ~ OR ~
#   2) Modify this script to use a different file name. Really easy - just
#      open this script in your favorite editor (vi, emacs, nano),
#      scroll to the bottom, and follow the instructions there.
# 
# You will also need to provide input files and valid output files to compare
# to. Note that valid output does NOT contain program input. Currently, the
# input and output files are named test1.in and test1.out, respectively.
# You can also modify these file names at the bottom of this script.
# 
# Once you are sure you have done all of the above (AND recompiled your
# program), hit ENTER to begin. Good luck and have fun!
# 
import os
import sys
import signal
import time
import datetime
import subprocess
import select
import difflib
import traceback

def headermsg():
	sys.stdout.write("\033c")
	sys.stdout.flush()
	fh = open(__file__)
	equFound = False
	noPrint = False
	for line in fh.readlines():
		line = line.strip()
		if line[0] == '#':
			if line == '#!/usr/bin/env python':
				pass
			elif '=========' in line:
				if not equFound:
					print line[2:]
					print "Under GPL v3 license. See LICENSE and this script's header for details.\n"
					equFound = True
					noPrint = True
				else:
					noPrint = False
			else:
				if not noPrint:
					print line[2:]
		else:
			break
	sys.stdout.write("Hit ENTER > ")
	sys.stdout.flush()
	raw_input()

def tprint(text):
	now = datetime.datetime.now()
	timeStr = now.strftime("%Y-%m-%d %H:%M:%S")
	print "[%s] %s" % (timeStr, text)

def eprint(text):
	tprint("\033[31mError:  \033[0m %s" % text)

def iprint(text):
	tprint("\033[34mInfo:   \033[0m %s" % text)

def wprint(text):
	tprint("\033[33mWarning:\033[0m %s" % text)

def sprint(text):
	tprint("\033[32mSuccess:\033[0m %s" % text)

def countLines(f):
	return sum(1 for line in open(f))

def diffStr(str1, str2):
	if str1 != str2:
		output = ""
		for line in difflib.unified_diff(str1.splitlines(), str2.splitlines(), lineterm = ''):
			output += line + "\n"
		return output
	else:
		return None

# input: infile outfile
def tester(prgm, input, validOutput):
	# Start the process!
	iprint("Launching process %s with input %s..." % (prgm, input))
	p = subprocess.Popen([prgm], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	
	# Dirty hooks
	poll_obj = select.poll()
	poll_obj.register(p.stdout, select.POLLIN)
	
	try:
		# Some variables...
		lineCounter = 0
		totalLines = countLines(input)
		stdoutLines = ""
		unifiedLines = ""
	
		for line in open(input).readlines():
			line = line.strip()
			if p.returncode != None:
				if p.returncode == 0:
					sprint("Program exited successfully. Yay! (Make sure that it was supposed to exit, though!")
					break
				else:
					wprint("Program did NOT exit successfully. (Error code: %i)" % (p.returncode))
					break
			try:
				p.stdin.write(line + "\n")
			except:
				wprint("Program seems to be already closed, but no status code was returned. Eeek! Exiting anyway.")
				break
			
			p.stdin.flush()
			lineCounter += 1
			time.sleep(0.1)
			p.stdout.flush()
		
			unifiedLines += line + "\n"
		
			# Read in lines!
			tmpBuf = ""
			if select.select([p.stdout], [], [], 0)[0]:
				iprint("Reading output...")
				while poll_obj.poll(0):
					tmpBuf = p.stdout.read(1)
					if tmpBuf:
						stdoutLines += tmpBuf
						unifiedLines += tmpBuf
					else:
						break
			
				checkstdoutLines = '\n'.join(stdoutLines.splitlines()[:-1])
			
				curLinesInLog = len(checkstdoutLines.splitlines())
				iprint("Sent line '%s' (line %i/%i). (Current lines in log: %i)" % (line, lineCounter, totalLines, curLinesInLog))
				# Do a diff
				validLogPart = open(validOutput).read(len(checkstdoutLines))
				diffc = diffStr(validLogPart, checkstdoutLines)
				if diffc != None:
					eprint("Diff found on input line %i! (Actual input line: '%s')" % (lineCounter, line))
					#tprint("Program output follows:")
					#print checkstdoutLines
					#tprint("Valid output follows:")
					#print validLogPart
					tprint("Diff follows: (valid vs invalid)")
					print diffc
				
					fh = open("progout.txt", "w")
					fh.write(stdoutLines)
					fh.close()
					iprint("Program output has been written to progout.txt.")
				
					# Write a bigger diff
					fh = open("progdiff.txt", "w")
					for line in difflib.ndiff(validLogPart.splitlines(), checkstdoutLines.splitlines()):
						fh.write(line + "\n")
					fh.close()
					iprint("Advanced diff output has been written to progdiff.txt.")
				
					# Write unified output
					fh = open("progunified.txt", "w")
					for line in unifiedLines.splitlines():
						fh.write(line+"\n")
					fh.close()
					iprint("Unified output has been written to progunified.txt.")
					iprint("These files will help you figure out what went wrong.")
					iprint("Happy debugging, and good luck!")
				
					# Cleanup
					os.kill(p.pid, signal.SIGKILL)
					sys.exit(1)
			else:
				curLinesInLog = len(stdoutLines.splitlines())	
				iprint("Sent line '%s' (line %i/%i). (Current lines in log: %i)" % (line, lineCounter, totalLines, curLinesInLog))
	except SystemExit:
		sys.exit(1)
	except Exception, err:
		eprint("Oops, something went wrong!")
		print traceback.format_exc()
		os.kill(p.pid, signal.SIGKILL)
		sys.exit(1)

# Display header message!
headermsg()

####################################
# Tester commands
####################################
# --------------------
# Program Name Change
# --------------------
# To change the program name, simply replace "./myprog" with your
# program name. Make sure to include the './' part, since this prevents
# some weird stuff from happening!
# 
# For example, if your program is called a.out, the new lines would look
# like:
#   tester("./a.out", "test1.in", "test1.out")
#   tester("./a.out", "test2.in", "test2.out")
# ...and so on.
# 
# --------------------
# Additional Tests
# --------------------
# You can also add additional lines as necessary!
# Just add more "tester" lines! The syntax is as follows:
#   tester(program,
#            input_file_with_lines_to_feed_to_the_program,
#            valid_output_file_with_valid_output_to_compare_to)
# 
tester("./myprog", "test1.in", "test1.out")
# Uncomment these lines to use test2.in/test2.out, test3.in/test3.out, etc.
# tester("./myprog", "test2.in", "test2.out")
# tester("./myprog", "test3.in", "test3.out")
# tester("./myprog", "test4.in", "test4.out")
# tester("./myprog", "test5.in", "test5.out")
