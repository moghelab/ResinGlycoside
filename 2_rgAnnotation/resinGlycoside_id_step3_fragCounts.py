from __future__ import division
import sys
import sys, itertools
print ("INP1: Output of step 2 (filelist.tab.nid1.id2) NOT the tab file")
file1=open(sys.argv[1],'r')
line1=file1.readline()
dict1={}; dict2={}; dict3={}
#########
def getPeakInfo(list1,dictm):
    justStarted=0
    for item in list1:
        annot=item.split('|')[-1]
        if annot not in dictm:
            dictm[annot]=1
            justStarted=1
        else:
            if justStarted==0:
                dictm[annot]+=1
    return dictm
#########
    
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')

        #Initialize value variables
        fn=tab1[0]; scan=tab1[1]; str1=f'{fn}-{scan}'
        maxpeak=float(tab1[2]); maxpeaki=int(maxpeak)
        combs=eval(tab1[3])
        losses=eval(tab1[4])
        dict1=getPeakInfo(combs,dict1)
        dict2=getPeakInfo(losses,dict2)
        dict3[str1]=1
    line1=file1.readline()
file1.close()

npeaks=len(list(dict3.keys()))
out1=open(sys.argv[1]+".fragCounts",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
out1.write('#FragORLoss\tNpeaks\PercPeaks\n')
for key in dict1:
    val=dict1[key]
    perc=(val/npeaks)*100
    out1.write('{}\t{}\t{:.1f}\n'.format(key,val,perc))
    
for key in dict2:
    val=dict2[key]
    perc=(val/npeaks)*100
    out1.write('{}\t{}\t{:.1f}\n'.format(key,val,perc))
out1.close()
print ("Done!")
