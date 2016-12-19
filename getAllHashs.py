#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding=utf-8
__author__ = "haha Ingeek"

import sys, os, glob
# p=os.path.join(os.getcwd(),os.pardir,os.pardir)
# sys.path.append(p)
from parseLib import process_aix, process_line


def parseDir(dir, isAIX=False):
	if os.path.exists(dir) and os.path.isdir(dir):
		for p in glob.glob(dir + "/*"):
			dirname = p.split("/")[-2:-1][0]
			print "++++ process file:\t%s " % p
			if isAIX:
				for h in process_aix(p):
					yield "%s:%s" % (h, dirname)
			else:
				for h in process_line(p):
					yield "%s:%s" % (h, dirname)


rootDIR = sys.argv[1]
rootDIR = os.path.abspath(rootDIR)
if os.path.exists(rootDIR):
	out = open("outall.txt", "w+")
	# for double dir layer
	for dir in glob.glob(rootDIR + "/*"):
		if os.path.isdir(dir):
			print "++++ process dirctory:\t%s " % dir
			if "aix" in dir.lower():
				isAIX = True
			else:
				isAIX = False
			for l in parseDir(dir, isAIX=isAIX):
				# l=l.replace(":","\t")
				out.writelines(l + '\n')
	# for 1 dir layer
	if os.path.isfile(glob.glob(rootDIR + "/*")[0]):
		print "++++ process dirctory:\t%s " % rootDIR
		if "aix" in os.path.basename(rootDIR).lower():
			isAIX = True
		else:
			isAIX = False
		for l in parseDir(rootDIR, isAIX=isAIX):
			# l=l.replace(":","\t")
			out.writelines(l + '\n')
	out.close()
