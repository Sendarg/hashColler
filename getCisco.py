#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# coding=utf-8
__author__ = "haha@Ingeek"

import sys, os, glob, string
from os.path import join
from parseLib import process_aix, process_line

# todo  decrypt network passwords
'''
use /Users/neoo/PycharmProjects/crypto/hashColler/ref/cisco_pwdecrypt.py code
直接跟文件： 破解出来
直接跟hash： 破解出来
如果破解不出来，给出hash串


just
Cisco Type 0 Password: These passwords are stored in plain text
Cisco Type 5 Password: These passwords are stored as salted MD5 hash. Requires brute-force attack to recover password
Cisco Type 7 Password: These passwords are encoded using Cisco's private encryption algorithm & can be decrypted instantly.

'''

