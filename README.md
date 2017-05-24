# hashColler
收集各类型OS的hash,以方便john输入


## 使用方法
1. python getAllHashs 目录1 目录2 
2. 生成的结果会存储到当前目录的outall.txt，根据hash分类会分割到不同的文件，format-hashtype.txt，如下：

	```
	➜  hashColler git:(master) ✗ python getAllHashes.py /tmp/xproject/pass                                         
	++++ Process:		/tmp/xproject/pass/AIX/192.168.1.2.log 
	++++ Get 2 hash from:	/tmp/xproject/pass/AIX/192.168.1.2.log 
	++++ Process:		/tmp/xproject/pass/centos/192.168.1.1/shadow 
	++++ Get 1 hash from:	/tmp/xproject/pass/centos/192.168.1.1/shadow 
	==== 2	hash in format-des.txt
	==== 1	hash in format-sha512crypt.txt
	
	➜  hashColler git:(master) ✗ ls  *.txt  
	format-des.txt format-sha512crypt.txt outall.txt
	
	```
## 感谢
小伙加油学！！！
