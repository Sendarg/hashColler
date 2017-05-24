#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding=utf-8
__author__ = "haha@Ingeek"

import sys, os, glob, string
from os.path import join
from parseLib import process_aix, process_line



def isPlainText(filename):
	s = open(filename).read(512)
	text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
	_null_trans = string.maketrans("", "")#TypeError: expected a string or other character buffer object
	if not s:
		# Empty files are considered text
		return True
	if "\0" in s:
		# Files with null bytes are likely binary
		return False
	# Get the non-text characters (maps a character to itself then use the 'remove' option to get rid of the text characters.)
	t = s.translate(_null_trans, text_characters)
	# If more than 30% non-text characters, then this is considered a binary file
	if float(len(t)) / float(len(s)) > 0.30:
		return False
	return True


def splitHashes():
	# split to single hashtype file
	out = open("outall.txt", "r")
	for l in out.readlines():
		hashtype = l.split(":")[3]
		typefile = open("format-%s.txt" % hashtype, "a")
		typefile.writelines(l)
		typefile.close()
	#count lines
	for format in glob.glob("format-*.txt"):
		with open(format) as f:
			count = sum(1 for l in f)
		print "==== %d\thash in %s"%(count,format)
	
	out.close()
	

if __name__ == '__main__':
	
	# do some clean
	for format_txt in glob.glob("format-*.txt"):
		os.remove(format_txt)
	
	rootDIRs = [os.path.abspath(dir) for dir in sys.argv]
	# import magic
	# mime = magic.Magic(mime=True)
	# print mime.from_file()
	
	out = open("outall.txt", "w+")
	for DIR in rootDIRs:
		if os.path.exists(DIR) and os.path.isdir(DIR):
			for root, dirs, files in os.walk(DIR):
				for f in [join(root, file) for file in files]:
					if isPlainText(f):
						dir=root.replace(DIR+"/","").replace("/",":")
						print "++++ Process:\t\t%s " % f
						if "aix" in dir.lower():
							# out.writelines(l+":dir\n" for l in process_aix(f))
							hashes=[l+":%s\n"%dir for l in process_aix(f)]
						else:
							hashes = [l + ":%s\n" % dir for l in process_line(f)]
						print "++++ Get %d hash from:\t%s " % (len(hashes), f)
						out.writelines(hashes)
	out.close()
	splitHashes()
