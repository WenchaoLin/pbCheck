#!/usr/bin/python
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

import sys,os,time

def main():
    '''
    Main funcition entry, it calls pb_md5_one.py to calculate and compare the md5 in each pacbio raw data.
    '''

    import sys,os,time
    if len(sys.argv)<3:
        print '''This scripts depend on  pb_md5_one.py, which make consistency check
of raw Pacbio RSII data. the unconsistence Cells will print into [failed.txt].

----------------------------------------------------------------------
   sample usage: python pb_md5_mul.py <input_rawdata_path> <jobs>  
        
         input_rawdata_path     Pacbio Rawdata path
         jobs                   Threads for jobs
----------------------------------------------------------------------

        '''
        exit(1)
        
    if os.path.isfile("failed.txt"):
        os.system("rm failed.txt")
        
    time_n=str(time.time())
    all_pb_path=os.popen("find "+sys.argv[1]+" -name \"Analysis_Results\" | sed \'s/\/Analysis_Results//g\'")
    out_path="./"
    soft_path=os.path.dirname(os.path.abspath(__file__))
    pb_num=0
    pb_list=[]
    for pb_path in all_pb_path:
        pb_num+=1
        pb_list.append(pb_path.strip())
    
    if pb_num <= int(sys.argv[2]):
        one_run=open("/tmp/"+time_n+".sh",'w')
        for pb in pb_list :
            one_run.write("python "+str(soft_path)+"/pb_md5_one.py "+pb+"  &\n")
        one_run.close()
    
    mul_num=int(sys.argv[2])
    n=0
    
    if pb_num > mul_num:
        run_mul=open("/tmp/"+time_n+".sh",'w')
        run_num_line=(pb_num//mul_num)
        for i in range(mul_num+1):
            for j in range(run_num_line):
                if j==(run_num_line-1):
                    if (n<pb_num):
                        run_mul.write("python "+str(soft_path)+"/pb_md5_one.py "+pb_list[n]+"  &\n")
                        n+=1
                else:
                    if (n<pb_num):
                        run_mul.write("python "+str(soft_path)+"/pb_md5_one.py "+pb_list[n]+"  &&\n")
                        n+=1
        run_mul.close()
    os.system("sh /tmp/"+time_n+".sh 2> /dev/null &")
    print "jobs submitted, all files with erros will recored in failed.txt"
    while 1:
        print "["+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"]\tplease wait..."
        time.sleep(30)
        if os.path.exists('failed.txt'):
            print "["+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"]\tAll done!!"
            break

if __name__ == '__main__':
    main()
