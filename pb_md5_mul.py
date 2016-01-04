import sys,os,time
if len(sys.argv)<3:
    print "####################################################################"
    print "This soft is check all of pb raw data in choose path"
    print "\t"
    print "python pb_md5_mul.py in_path cpu_num"
    print "\t"
    print "\t"
    print "example : python pb_md5_mul.py /mnt/pb 5"
    print "--------------------------------------------------------------------"
    print "in_path \t pb raw data path"
    print "cpu_num \t number of threads running"
    print "####################################################################"
    exit(1)
if os.path.isfile("Fail.out"):
	os.system("rm Fail.out")
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
