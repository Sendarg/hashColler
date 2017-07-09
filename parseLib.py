# coding=utf-8
__author__ = "haha Ingeek"

import os
import re
from re import match

HASHES = (
	("Blowfish(Eggdrop)", "^\+[a-zA-Z0-9\/\.]{12}$"),
	("Blowfish(OpenBSD)", "^\$2a\$[0-9]{0,2}?\$[a-zA-Z0-9\/\.]{53}$"),
	("Blowfish(my)", "^\$2y\$[0-9]{0,2}?\$[a-zA-Z0-9\/\.]{53}$"),
	("Blowfish crypt", "^\$2[axy]{0,1}\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	(("DES(Unix)", "DES crypt", "DES hash(Traditional)"), "^.{0,2}[a-zA-Z0-9\/\.]{11}$"),
	("MD5(Unix)", "^\$1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
	(("MD5(APR)", "Apache MD5"), "^\$apr1\$.{0,8}\$[a-zA-Z0-9\/\.]{22}$"),
	("MD5(MyBB)", "^[a-fA-F0-9]{32}:[a-z0-9]{8}$"),
	("MD5(ZipMonster)", "^[a-fA-F0-9]{32}$"),
	(("MD5 crypt", "FreeBSD MD5", "Cisco-IOS MD5"), "^\$1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("MD5 apache crypt", "^\$apr1\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("MD5(Joomla)", "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$"),
	("MD5(Wordpress)", "^\$P\$[a-zA-Z0-9\/\.]{31}$"),
	("MD5(phpBB3)", "^\$H\$[a-zA-Z0-9\/\.]{31}$"),
	("MD5(Cisco PIX)", "^[a-zA-Z0-9\/\.]{16}$"),
	(("MD5(osCommerce)", "xt:Commerce"), "^[a-fA-F0-9]{32}:[a-zA-Z0-9]{2}$"),
	("MD5(Palshop)", "^[a-fA-F0-9]{51}$"),
	("MD5(IP.Board)", "^[a-fA-F0-9]{32}:.{5}$"),
	("MD5(Chap)", "^[a-fA-F0-9]{32}:[0-9]{32}:[a-fA-F0-9]{2}$"),
	("Juniper Netscreen/SSG (ScreenOS)", "^[a-zA-Z0-9]{30}:[a-zA-Z0-9]{4,}$"),
	("Fortigate (FortiOS)", "^[a-fA-F0-9]{47}$"),
	("Minecraft(Authme)", "^\$sha\$[a-zA-Z0-9]{0,16}\$[a-fA-F0-9]{64}$"),
	("Lotus Domino", "^\(?[a-zA-Z0-9\+\/]{20}\)?$"),
	("Lineage II C4", "^0x[a-fA-F0-9]{32}$"),
	("CRC-96(ZIP)", "^[a-fA-F0-9]{24}$"),
	("NT crypt", "^\$3\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("Skein-1024", "^[a-fA-F0-9]{256}$"),
	(("RIPEMD-320", "RIPEMD-320(HMAC)"), "^[A-Fa-f0-9]{80}$"),
	("EPi hash", "^0x[A-F0-9]{60}$"),
	("EPiServer 6.x < v4", "^\$episerver\$\*0\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9\+]{27}$"),
	("EPiServer 6.x >= v4", "^\$episerver\$\*1\*[a-zA-Z0-9]{22}==\*[a-zA-Z0-9]{43}$"),
	("Cisco IOS SHA256", "^[a-zA-Z0-9]{43}$"),
	("SHA-1(Django)", "^sha1\$.{0,32}\$[a-fA-F0-9]{40}$"),
	("SHA-1 crypt", "^\$4\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("SHA-1(Hex)", "^[a-fA-F0-9]{40}$"),
	(("SHA-1(LDAP) Base64", "Netscape LDAP SHA", "NSLDAP"), "^\{SHA\}[a-zA-Z0-9+/]{27}=$"),
	("SHA-1(LDAP) Base64 + salt", "^\{SSHA\}[a-zA-Z0-9+/]{28,}[=]{0,3}$"),
	("SHA-512(Drupal)", "^\$S\$[a-zA-Z0-9\/\.]{52}$"),
	("SHA-512 crypt", "^\$6\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("SHA-256(Django)", "^sha256\$.{0,32}\$[a-fA-F0-9]{64}$"),
	("SHA-256 crypt", "^\$5\$[a-zA-Z0-9./]{8}\$[a-zA-Z0-9./]{1,}$"),
	("SHA-384(Django)", "^sha384\$.{0,32}\$[a-fA-F0-9]{96}$"),
	("SHA-256(Unix)", "^\$5\$.{0,22}\$[a-zA-Z0-9\/\.]{43,69}$"),
	("SHA-512(Unix)", "^\$6\$.{0,22}\$[a-zA-Z0-9\/\.]{86}$"),
	(("SHA-384", "SHA3-384", "Skein-512(384)", "Skein-1024(384)"), "^[a-fA-F0-9]{96}$"),
	(("SHA-512", "SHA-512(HMAC)", "SHA3-512", "Whirlpool", "SALSA-10", "SALSA-20", "Keccak-512", "Skein-512",
	  "Skein-1024(512)"), "^[a-fA-F0-9]{128}$"),
	("SSHA-1", "^({SSHA})?[a-zA-Z0-9\+\/]{32,38}?(==)?$"),
	(("SSHA-1(Base64)", "Netscape LDAP SSHA", "NSLDAPS"), "^\{SSHA\}[a-zA-Z0-9]{32,38}?(==)?$"),
	(("SSHA-512(Base64)", "LDAP {SSHA512}"), "^\{SSHA512\}[a-zA-Z0-9+]{96}$"),
	("Oracle 11g", "^S:[A-Z0-9]{60}$"),
	("SMF >= v1.1", "^[a-fA-F0-9]{40}:[0-9]{8}&"),
	("MySQL 5.x", "^\*[a-f0-9]{40}$"),
	(("MySQL 3.x", "DES(Oracle)", "LM", "VNC", "FNV-164"), "^[a-fA-F0-9]{16}$"),
	("OSX v10.7", "^[a-fA-F0-9]{136}$"),
	("OSX v10.8", "^\$ml\$[a-fA-F0-9$]{199}$"),
	("SAM(LM_Hash:NT_Hash)", "^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$"),
	("MSSQL(2000)", "^0x0100[a-f0-9]{0,8}?[a-f0-9]{80}$"),
	(("MSSQL(2005)", "MSSQL(2008)"), "^0x0100[a-f0-9]{0,8}?[a-f0-9]{40}$"),
	("MSSQL(2012)", "^0x02[a-f0-9]{0,10}?[a-f0-9]{128}$"),
	(("substr(md5($pass),0,16)", "substr(md5($pass),16,16)", "substr(md5($pass),8,16)", "CRC-64"),
	 "^[a-fA-F0-9./]{16}$"),
	(("MySQL 4.x", "SHA-1", "HAVAL-160", "SHA-1(MaNGOS)", "SHA-1(MaNGOS2)", "TIGER-160", "RIPEMD-160",
	  "RIPEMD-160(HMAC)",
	  "TIGER-160(HMAC)", "Skein-256(160)", "Skein-512(160)"), "^[a-f0-9]{40}$"),
	(("SHA-256", "SHA-256(HMAC)", "SHA-3(Keccak)", "GOST R 34.11-94", "RIPEMD-256", "HAVAL-256", "Snefru-256",
	  "Snefru-256(HMAC)", "RIPEMD-256(HMAC)", "Keccak-256", "Skein-256", "Skein-512(256)"), "^[a-fA-F0-9]{64}$"),
	(("SHA-1(Oracle)", "HAVAL-192", "OSX v10.4, v10.5, v10.6", "Tiger-192", "TIGER-192(HMAC)"), "^[a-fA-F0-9]{48}$"),
	(("SHA-224", "SHA-224(HMAC)", "HAVAL-224", "Keccak-224", "Skein-256(224)", "Skein-512(224)"), "^[a-fA-F0-9]{56}$"),
	(("Adler32", "FNV-32", "ELF-32", "Joaat", "CRC-32", "CRC-32B", "GHash-32-3", "GHash-32-5", "FCS-32", "Fletcher-32",
	  "XOR-32"), "^[a-f0-9]{8}$"),
	(("CRC-16-CCITT", "CRC-16", "FCS-16"), "^[a-fA-F0-9]{4}$"),
	(("MD5(HMAC(Wordpress))", "MD5(HMAC)", "MD5", "RIPEMD-128", "RIPEMD-128(HMAC)", "Tiger-128", "Tiger-128(HMAC)",
	  "RAdmin v2.x", "NTLM", "Domain Cached Credentials(DCC)", "Domain Cached Credentials 2(DCC2)", "MD4", "MD2",
	  "MD4(HMAC)", "MD2(HMAC)", "Snefru-128", "Snefru-128(HMAC)", "HAVAL-128", "HAVAL-128(HMAC)", "Skein-256(128)",
	  "Skein-512(128)", "MSCASH2"), "^[0-9A-Fa-f]{32}$"),
)


def identify_hashes(input_hash):
	"""
	Function to identify all the hashes and return the results as list.
	:rtype : list
	:param input_hash:
	"""
	res = []
	for items in HASHES:
		if match(items[1], input_hash):
			res += [items[0]] if isinstance(items[0], str) else items[0]
	return res


def process_line(filename):
	ip = os.path.basename(filename)
	if ip.endswith(".log"):
		ip = ip[:-4]
	elif ip.endswith("_shadow"):
		ip = ip[:-7]
	# parse
	# username = "?"
	fd = open(filename, "rb")
	for line in fd.readlines():
		if "::" in line:
			name, hash = line.split(":")[0:2]
		else:
			continue
		if hash and hash not in ["x", "*"] and hash[:1] not in ["*", "!"]:
			# print ip,line
			hashtype = identify_hashes(hash)[0]
			if "SHA-512" in hashtype:
				hashtype = "sha512crypt"
			if "MD5" in hashtype:
				hashtype = "md5crypt"
			if "Blowfish" in hashtype:
				hashtype = "bcrypt"
			if "DES" in hashtype:
				hashtype = "descrypt"
			if "SHA-256" in hashtype:
				hashtype = "sha512crypt"
			out = '%s:%s:%s:%s' % (name, hash, ip, hashtype)
			yield out


def process_aix(filename, is_standard=False):
	ip = os.path.basename(filename)
	if ".log" in ip:
		ip = ip[:-4]
	# parse
	username = "?"
	fd = open(filename, "rb")
	for line in fd.readlines():
		# get username
		if re.match('^\s*\S+\s*:\s*$', line):
			username = line.split(':')[0].strip()
		# get hash
		h = ""
		if "password =" in line and "smd5" in line:
			h = line.split("=")[1].strip()
			if len(h) != 37:
				continue
			if is_standard:
				h = "%s:$1$%s" % (username, h[6:])
			else:
				h = "%s:%s" % (username, h)
		elif "password =" in line and "ssha" in line:
			h = line.split("=")[1].strip()
			tc, salt, h = h.split('$')
			h = "%s:%s$%s$%s" % (username, tc, salt, h)
		
		elif "password =" in line:  # DES
			h = line.split("=")[1].strip()
			if h != "*" and h != "":
				h = "%s:%s" % (username, h)
		# return result
		if len(h) > 6:
			out = ("%s:%s:descrypt" % (h, ip))
			yield out
