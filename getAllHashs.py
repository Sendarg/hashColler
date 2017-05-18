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
			# dirname = p.split("/")[-2:-1][0]
			print "++++ process file:\t%s " % p
			if isAIX:
				for h in process_aix(p):
					yield h
			else:
				for h in process_line(p):
					yield h


# do some clean
for format_txt in glob.glob("format-*.txt"):
	os.remove(format_txt)


rootDIRs = [ os.path.abspath(dir) for dir in sys.argv]


out = open("outall.txt", "w+")
for DIR in rootDIRs:
	if os.path.exists(DIR) and os.path.isdir(DIR):
		DIRname=os.path.basename(DIR)
		# for double layer dir
		for dir in glob.glob(DIR + "/*"):
			dirname = os.path.basename(dir)
			if os.path.isdir(dir):
				print "++++ process dirctory:\t%s/%s " % (DIR,dirname)
				if "aix" in dirname.lower():
					isAIX = True
				else:
					isAIX = False
				for l in parseDir(dir, isAIX=isAIX):
					# l=l.replace(":","\t")
					out.writelines(l + ":%s:%s\n"%(DIRname,dirname))
			# for 1 dir layer
			if os.path.isfile(dir):
				file=dir
				print "++++ process file:\t%s " % file
				for h in process_line(file):
					out.writelines(h + ':%s\n'%DIRname)
out.close()


# split to single hashtype file
out = open("outall.txt", "r")
for l in out.readlines():
	hashtype=l.split(":")[3]
	typefile=open("format-%s.txt"%hashtype,"a")
	typefile.writelines(l)
	typefile.close()
out.close()