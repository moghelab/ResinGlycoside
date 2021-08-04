import sys
import sys, itertools
print ("INP1:  4_predictMotifs/motifs.grp.mod.frequent")
print ("INP2: Output of step 2 (filelist.tab.nid1.id2) NOT the tab file")
print ("INP3: How many sugars do you want to consider? (1-7)")
print ("INP4: How many acyl chains do you want to consider? (0-5)")

file1=open(sys.argv[1],'r')
line1=file1.readline()
msug=int(sys.argv[3])
macyl=int(sys.argv[4])
dict1={}; dict2={}

################
def add2dict(dictx,v1,v2,v3):
    if v1 not in dictx:
        dictx[v1]={}
        dictx[v1][v2]=[v3]
    else:
        if v2 not in dictx[v1]:
            dictx[v1][v2]=[v3]
        else:
            if v3 not in dictx[v1][v2]:
                dictx[v1][v2].append(v3)
    return dictx
################
ndict={}; sugars=[]; acyls=[]
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        tp=tab1[0]; mass=float(tab1[1]); name=tab1[2]
        if tp=='sugar':
            sugars.append(mass)
        if tp=='smallacyls':
            acyls.append(mass)
        ndict[mass]=name        
    line1=file1.readline()
file1.close()

#Make a dictionary of all masses and all fragments
#considering 1-3 sugars and 1-3 acyl frags
sucset=[]; acylset=[[]]
for i in range(0,5):
    for j in itertools.combinations_with_replacement(sugars, i+2):
        if len(j)<=msug:
            sucset.append(list(j))
        
for i in range(0,len(acyls)):
    #print (itertools.combinations(acyls, i))
    for j in itertools.combinations_with_replacement(acyls, i+1):
        if len(j)<=macyl:
            acylset.append(list(j))

#print (sugars)
#for item in sucset:
#    print (item)
#sys.exit()
            
#Get combined masses of combinations
ydict={}
for suc in sucset:    
    for ac in acylset:
        comb=suc+ac        
        if comb!=[]:
            #Get sum of all fragments
            sumx1=sum(comb)-(len(comb)*18.010)
            sumx2=sumx1+46.00548 #Formate adduct
            
            nlist=[]
            for item in comb:
                name=ndict[item]
                nlist.append(name)

            #Make an entry of names and associate it with fragsum
            nline='+'.join(nlist)
            isumx1=int(sumx1)
            if isumx1 not in ydict:
                ydict[isumx1]={}
                ydict[isumx1][sumx1]=[nline]
            else:
                if sumx1 not in ydict[isumx1]:
                    ydict[isumx1][sumx1]=[nline]
                else:
                    if nline not in ydict[isumx1][sumx1]:
                        ydict[isumx1][sumx1].append(nline)

            nlist.append('Formate')
            nline='+'.join(nlist)
            sumx1=sumx2 #for ease of coding the block below - laziness
            isumx1=int(sumx1)
            if isumx1 not in ydict:
                ydict[isumx1]={}
                ydict[isumx1][sumx1]=[nline]
            else:
                if sumx1 not in ydict[isumx1]:
                    ydict[isumx1][sumx1]=[nline]
                else:
                    if nline not in ydict[isumx1][sumx1]:
                        ydict[isumx1][sumx1].append(nline)

out1=open(sys.argv[2]+".estm",'w')
for entry in ydict:
    fentrys=ydict[entry]
    for fentry in fentrys:
        lines=ydict[entry][fentry]
        for line in lines:
            out1.write('{}\t{}\t{}\n'.format(entry,fentry,line))
out1.close()
#sys.exit()

ykeys=list(ydict.keys())

file1=open(sys.argv[2],'r')
out1=open(sys.argv[2]+".pred3",'w')
out2=open(sys.argv[2]+".pred3.tab",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
out2.write('#python {}\n'.format(' '.join(sys.argv)))
line1=file1.readline()
dict2={}; nopred=0; predcount=0
while line1:
    if line1.startswith('#'):
        if line1.startswith('#python'):
            pass
        else:
            out1.write('{}\tPredictedRemainingGroups\n'.format(line1.strip()))
    else:
        tab1=line1.strip().split('\t')

        #Initialize value variables
        fn=tab1[0]; scan=tab1[1]
        maxpeak=float(tab1[2]); maxpeaki=int(maxpeak)
        combs=eval(tab1[3]); losses=eval(tab1[4]); unm=eval(tab1[5])
        flag=0; formate=0

        #Calculate the mass difference that needs to be accounted for
        xdict={}; pentose=0
        for px in combs:            
            mass=float(px.split('|')[0]); name=px.split('|')[-1]
            xdict[mass]=name
            if 'Pentose' in name:
                pentose+=1
        xlist=(list((xdict.keys())))
        
        if xlist!=[]:
            maxfrag=max(xlist)
            #print (scan, maxfrag, xdict[maxfrag])
            if '-Water' not in xdict[maxfrag]: #If -water not present, ring is open
                maxfrag_closed=maxfrag-18.011
                maxfrag_open=maxfrag
            else:
                maxfrag_open=maxfrag
                maxfrag_closed=maxfrag+18.011
                
            fdiff1=maxpeak-maxfrag_closed
            fdiff2=maxpeak-maxfrag_open
            
            idiff1=int(fdiff1); idiff2=int(fdiff2)
            
            plist2x=[]; plist2y=[]
            #print (">>", maxpeak, maxfrag, idiff)

            #Identify the combinations resulting in that mass
            if idiff1 in ydict:
                yx=list(ydict[idiff1])
                for ymass in yx:
                    adiff=abs(ymass-fdiff1)
                    #print (ymass, fdiff, adiff)
                    if adiff<=0.015:
                        predlist=ydict[idiff1][ymass]                        
                        for pred in predlist:
                            if 'Pentose' in pred:
                                if pentose>0:
                                    plist2x.append(pred)                                    
                                    flag=1
                            else:
                                plist2x.append(pred)                                    
                                flag=1
            if idiff2 in ydict:
                yx=list(ydict[idiff2])
                for ymass in yx:
                    adiff=abs(ymass-fdiff2)
                    #print (ymass, fdiff, adiff)
                    if adiff<=0.015:
                        predlist=ydict[idiff2][ymass]                        
                        for pred in predlist:
                            if 'Pentose' in pred:
                                if pentose>0:
                                    plist2y.append(pred)                                    
                                    flag=1
                            else:
                                plist2y.append(pred)                                    
                                flag=1
                                

            #Write to output
            if flag==1:
                predcount+=1
                out1.write('{}\t{}\t{}\n'.format(line1.strip(), plist2x, plist2y))
                for item in combs:                    
                    sp=item.split('|')
                    n1=sp[0]; n2='|'.join([sp[0],sp[1],sp[2]]); n3=sp[3]
                    out2.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(fn,scan,maxpeak,n1,n2,n3))
                for item in losses:
                    sp=item.split('|')
                    m1=sp[0]; m2='|'.join([sp[1],sp[2]])
                    out2.write('{}\t{}\t{}\t{}\t{}\tNeutralLoss\n'.format(fn,scan,maxpeak,m1,m2))
                for item in unm:
                    sp=item.split('|')
                    d1=sp[0]; d2=sp[1]
                    out2.write('{}\t{}\t{}\t{}|{}\tNA\tUnmatchedFrags\n'.format(fn,scan,maxpeak,d1,d2))
                for item in plist2x: #Closed
                    out2.write('{}\t{}\t{}\t{}\tPredictedRemaining_Closed|{}\tRemainingPrediction\n'.format(fn,scan,maxpeak,item,maxfrag_closed))
                    #print('{}\t{}\t{}\t{}\tPredictedRemaining_Closed|{}'.format(fn,scan,maxpeak,item,maxfrag_closed))
                for item in plist2y: #Open
                    out2.write('{}\t{}\t{}\t{}\tPredictedRemaining_Open|{}\tRemainingPrediction\n'.format(fn,scan,maxpeak,item,maxfrag_open))
                    #print('{}\t{}\t{}\t{}\tPredictedRemaining_Open|{}'.format(fn,scan,maxpeak,item,maxfrag_open))
                out2.write('######\n')
                
        if flag==0:
            for item in combs:                
                sp=item.split('|')
                n1=sp[0]; n2='|'.join([sp[0],sp[1],sp[2]]); n3=sp[3]
                out2.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(fn,scan,maxpeak,n1,n2,n3))
            for item in losses:
                sp=item.split('|')
                m1=sp[0]; m2='|'.join([sp[1],sp[2]])
                out2.write('{}\t{}\t{}\t{}\t{}\tNeutralLoss\n'.format(fn,scan,maxpeak,m1,m2))
            for item in unm:
                sp=item.split('|')
                d1=sp[0]; d2=sp[1]
                out2.write('{}\t{}\t{}\t{}|{}\tNA\tUnmatchedFrags\n'.format(fn,scan,maxpeak,d1,d2))            
            out2.write('######\n')
            nopred+=1
            
    line1=file1.readline()
file1.close()
print ("Pred: ", predcount)
print ("Nopred: ", nopred)
print ("Done!")
        

