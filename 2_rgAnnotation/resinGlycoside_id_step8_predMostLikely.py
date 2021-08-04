import sys
import sys, itertools
print ("INP2: Output of step 6 (*.pred3) NOT the tab file")

file1=open(sys.argv[1],'r')
out1=open(sys.argv[1]+".mostLikely",'w')
out2=open(sys.argv[2]+".mostLikely.tab",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
out2.write('#python {}\n'.format(' '.join(sys.argv)))
line1=file1.readline()
dict2={}; nopred=0; predcount=0
while line1:
    if line1.startswith('#'):
        if line1.startswith('#python'):
            pass
        else:
            out1.write('{}\MostLikely\n'.format(line1.strip()))
    else:
        tab1=line1.strip().split('\t')

        #Initialize value variables
        fn=tab1[0]; scan=tab1[1]
        maxpeak=float(tab1[2]); maxpeaki=int(maxpeak)
        combs=eval(tab1[3]); losses=eval(tab1[4]); unm=eval(tab1[5])
        predRem=eval(tab1[6])
        flag=0; formate=0
