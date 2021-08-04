import sys
import numpy as np
print ("INP1: Output of step2 (id2 not id2.tab)")

file1=open(sys.argv[1],'r')
out1=open(sys.argv[1]+".fragExplPerc",'w')
out2=open(sys.argv[1]+".fragExplPerc.frags",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
out2.write('#python {}\n'.format(' '.join(sys.argv)))
out1.write('#Filename\tScan\tMass\tTotalFrag\tExplFrag\tUnexplFrag\tPercExpl\tPercUnexpl\n')
line1=file1.readline()
vlist1=[]; vlist2=[]
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        frags=eval(tab1[3])
        neut=eval(tab1[4])
        unmatched=eval(tab1[5])
        mlist=[]

        #Count fragments in each group
        for item in frags:
            mass=item.split('|')[0]
            if mass not in mlist:
                mlist.append(mass)
        for item in neut:
            massx=item.split('|')[0].split('-')
            m1=massx[0]; m2=massx[1]
            if m1 not in mlist:
                mlist.append(m1)
            if m2 not in mlist:
                mlist.append(m2)
        
        unexp=[]
        for item in unmatched:
            mass=item.split('|')[0]
            if mass not in unexp:
                fmass=float(mass)
                if abs(fmass-125.02)<0.01:
                    #print (mass)
                    if mass not in mlist:
                        mlist.append(mass)
                else:                    
                    unexp.append(mass)
        

        #Calculate percentages
        explen=len(mlist)
        unexplen=len(unexp)
        total=unexplen+explen

        per1=(explen/total)*100
        per2=(unexplen/total)*100
        vlist1.append(per1)
        vlist2.append(per2)

        #Write to out
        out1.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'. \
                   format(tab1[0], tab1[1],tab1[2],  total, explen, unexplen, per1, per2))
        out2.write('{}\t{}\t{}\t{}\t{}\t{}\n'. \
                   format(tab1[0], tab1[1], tab1[2], total, mlist, unexp))
        
    line1=file1.readline()
file1.close(); out1.close()
print ("Average expl: ", sum(vlist1)/len(vlist1), np.median(vlist1))
print ("Average unexpl: ", sum(vlist2)/len(vlist2), np.median(vlist2))
print ("Done!")

       
