import sys
import pandas as pd

print ("INP1: filelist.tab")
print ("INP2: nid1.id2 output of step2")

file1=open(sys.argv[1],'r')
line1=file1.readline()
dict1={}
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        id1='file-{}'.format(tab1[0]); name=tab1[1]
        dict1[id1]=name
    line1=file1.readline()
file1.close()

file1=open(sys.argv[2],'r')
line1=file1.readline()
dict2={}; pcount=0; pdict={}
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        fn=tab1[0]; peaks=eval(tab1[3]); losses=eval(tab1[4])
        flag=0
        
        #Peaks
        for peak in peaks:
            if '$' in peak:
                fname=peak.split('|')[3]
                if fn not in dict2:
                    dict2[fn]={}
                    dict2[fn][fname]=1
                else:
                    if fname not in dict2[fn]:
                        dict2[fn][fname]=1
                    else:
                        dict2[fn][fname]+=1
                flag=1
                
        #Check losses for acetyl
        aflag=0   
        for loss in losses:            
            if '$acetic' in loss:
                #print (">>>>", loss)
                if aflag==0:
                    fname='C2|Acetyl-loss'
                    if fn not in dict2:
                        dict2[fn]={}
                        dict2[fn][fname]=1
                    else:
                        if fname not in dict2[fn]:
                            dict2[fn][fname]=1
                        else:
                            dict2[fn][fname]+=1
                flag=1; aflag=1
                
        if flag==1:
            if fn not in pdict:
                pdict[fn]=1
            else:
                pdict[fn]+=1
            flag=0
    line1=file1.readline()
file1.close()

#print (pdict['file-08'])

out1=open(sys.argv[2]+".acyldist.tab",'w')
out2=open(sys.argv[2]+".acyldist.tab2",'w')
#out1.write('#python {}\n'.format(' '.join(sys.argv)))
out1.write('FileName\tSpecies\tChain\tnPeaks\tPeaks\tPerc\n')
out2.write('FileName\tSpecies\tChain\tnPeaks\tPeaks\tPerc\n')

alist=['Acetyl-loss','acrylic','propionic','crotonic','acetoacetic','butyric','pentanoic','HMBA', \
'tiglic','hexanoic','gallic','octanoic','cinnamic','coumaric','caffeic','ferulic','decanoic','hydroxydecanoic', \
'dodecanoic','hexadecanoic','octadecanoic']

for fn in dict2:    
    species=dict1[fn]
    pcount=pdict[fn]
    for peak in dict2[fn]:
        count=dict2[fn][peak]
        perc=(count/pcount)*100
        out1.write('{}\t{}\t{}\t{}\t{}\t{:.1f}\n'. \
                   format(fn, species, peak, count, pcount, perc))
        try:
            pbreak=peak.split('$')[1]
        except:
            pbreak=peak.split('|')[1]
        out2.write('{}\t{}\t{}\t{}\t{}\t{:.1f}\n'. \
                   format(fn, species, pbreak, count, pcount, perc))
out1.close(); out2.close()

df=pd.read_csv(sys.argv[2]+".acyldist.tab2", sep="\t", header=0)
print (df.head())
pv=df.pivot_table(index='Species', columns='Chain', values='Perc', fill_value=0)
pv.to_csv(sys.argv[2]+".acyldist.tab2.mat", sep="\t")

print ("Done!")
                
        
