"""Convert to and from Roman numerals"""

__author__ = "Yinjia Wang @(TBC)"
__version__ = "1.1"
__date__ = "8 August 2015"
__copyright__ = """Copyright (c) 2015 Tianjin Biochip Corp.

This program is free software; you can redistribute it and/or modify
it under the terms of the Python 2.1.1 license, available at
http://www.python.org/2.1.1/license.html

The UPDATE version can be found here:
https://github.com/WenchaoLin/pbCheck
"""

import sys,os
if len(sys.argv)!=2:
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "$$$$$   This soft is check a set of pb's raw data   $$$$$"
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    print "#########################################################"
    print "###  python pb_md5_one.py in_path                     ###"
    print "###example: python pb_md5_one.py /mnt/pb/H4_1         ###"
    print "#########################################################"
    exit(1)

fastas=os.popen("find "+sys.argv[1]+" -name \"*.fast*\"")
h5s=os.popen("find "+sys.argv[1]+" -name \"*.h5\"")
xmls=os.popen("find "+sys.argv[1]+" -name \"*.xml\"")
all_xml=''

xml_num=0
h5_num=0
fasta_num=0


for xml in xmls:
    all_xml=all_xml+open(xml.strip(),'r').read()
    xml_num+=1

md5_list=[]

for h5 in h5s:
    for h5_md5 in os.popen("md5sum "+h5.strip()):
        md5_list.append(h5_md5.strip().split())
        h5_num+=1

for fasta in fastas:
    for fasta_md5 in os.popen("md5sum "+fasta.strip()):
        md5_list.append(fasta_md5.strip().split())
        fasta_num+=1


for md5_line in md5_list :
    if md5_line[0] in all_xml:
        print "OK\t"+md5_line[1]
    else:
        print "FAIL\t"+md5_line[1]
        fail_all_w=open("Fail.out",'a')
        fail_all_w.write(md5_line[1]+" md5 error \n")
        fail_all_w.close()

if fasta_num!=6:
    fail_all_w=open("Fail.out",'a')
    fail_all_w.write(sys.argv[1]+" : fasta or fastq missing!!\n")
    fail_all_w.close()
if h5_num!=5:
    fail_all_w=open("Fail.out",'a')
    fail_all_w.write(sys.argv[1]+" : h5 md5 checksum failed, transfer incomplete!!\n")
    fail_all_w.close()
if xml_num!=5:
    fail_all_w=open("Fail.out",'a')
    fail_all_w.write(sys.argv[1]+" : xml md5 checksum failed, transfer incomplete!!\n")
    fail_all_w.close()
