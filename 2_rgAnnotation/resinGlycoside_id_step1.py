from __future__ import division
import sys, operator, random
import pandas as pd

print ("INP1: mzsuffixes in csv eg: mz132,mz146,mz162")
print ("INP2: filelist.tab")
print ("INP3: motif masses e.g. motifs.grp")
print ("INP4: How many top frags do you want to select? 5/10/15/20")
print ("INP5: Do you want to restrict to just 271.2279 (y/n)")

sufs=sys.argv[1].split(',')

file1=open(sys.argv[3],'r')
desfrags=int(sys.argv[4])
ch=sys.argv[5]
line1=file1.readline()
motifdict={}
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        grp=tab1[0]; mass=float(tab1[1]); annot=tab1[2]
        if grp.startswith('comb'):
            mass=mass
        else:
            mass=mass-1.007

            
        if mass not in motifdict:
            motifdict[mass]=annot
        else:
            print ("Mass repeat: ", mass)
    line1=file1.readline()
file1.close()
motiflist=list(motifdict.keys())

file1=open(sys.argv[2],'r')
if ch=='y':
    out1=open(sys.argv[2]+".only271.id1",'w')
    out1.write("#python {}\n".format(' '.join(sys.argv)))
    out1.write('#FileID\tScanID\tMaxPeaks\tIdentifiedPeaks\tUnexplainedPeaks\n')
    non271=open(sys.argv[2]+".non271.tab",'w')
    non271.write("#python {}\n".format(' '.join(sys.argv)))
    non271.write('#FileID\tScanID\n')
else:
    out1=open(sys.argv[2]+".id1",'w')
    out1.write("#python {}\n".format(' '.join(sys.argv)))
    out1.write('#FileID\tScanID\tMaxPeaks\tIdentifiedPeaks\tUnexplainedPeaks\n')
line1=file1.readline()

############
def getTop(d,nfrags,scanx,pdictx,dict1x,mdictx):
    sorted_d = sorted(d.items(), key=operator.itemgetter(1))
    sorted_d.reverse()

    if len(sorted_d)>=nfrags:
        ftuples=sorted_d[0:desfrags]
    else:
        ftuples=sorted_d

    for str1 in ftuples:
        #print ("file-{}".format(fcount), scan, pepmass, str1)
        mass=list(str1)[0]; intensity=int(list(str1)[1])
        pdictx[scan][mass]=intensity
        if intensity>3000:
            dict1x[suf][scan].append(mass)
            if mass not in mdictx:
                mdictx[mass]=1
    return pdictx,dict1x,mdictx
############

    
    
while line1:
    if line1.startswith('#'):
        pass
    else:
        sp=line1.strip().split('\t')

        #Rename the file to account for different fragpairs files
        fcount=sp[0].zfill(2)
        dict1={}; dict2={}; mdict={}; scandict={}; pdict={}
        for suf in sufs:
            fn=f'2_MGF/{fcount}-Cent.mgf.{suf}.fil.mgf'
            #os.system('cp {} {}.{}\n'.format(fnx,fnx,suf))
            print ("Now reading: ", fn)
            file2=open(fn,'r')
            line2=file2.readline()
            start=0; count=0
            dict1[suf]={}
            while line2:
                if line2.startswith('BEGIN IONS'):
                    start=1; count+=1; peak271=0
                elif line2.startswith('END IONS'):
                    start=0
                    #print ("######")
                    if count==10:
                        #sys.exit()
                        pass
                    
                    #See if only 271.2279 is desired
                    if ch=='y':
                        if peak271==1:
                            #Get top 10 ions in the dict sorted by their intensities
                            sorted_d = sorted(msdict.items(), key=operator.itemgetter(1))
                            sorted_d.reverse()

                            if len(sorted_d)>=desfrags:
                                ftuples=sorted_d[0:desfrags]
                            else:
                                ftuples=sorted_d

                            for str1 in ftuples:
                                #print ("file-{}".format(fcount), scan, pepmass, str1)
                                mass=list(str1)[0]; intensity=int(list(str1)[1])
                                pdict[scan][mass]=intensity
                                if intensity>3000:
                                    dict1[suf][scan].append(mass)
                                    if mass not in mdict:
                                        mdict[mass]=1
                        else:
                            non271.write('{}\t{}\n'.format(fn,scan))
                    else:
                        #REPEAT OF THE TOP LOOP -- NEED TO PROPERLY DEFINE A FUNCTION
                        #Get top 10 ions in the dict sorted by their intensities
                            sorted_d = sorted(msdict.items(), key=operator.itemgetter(1))
                            sorted_d.reverse()

                            if len(sorted_d)>=desfrags:
                                ftuples=sorted_d[0:desfrags]
                            else:
                                ftuples=sorted_d

                            for str1 in ftuples:
                                #print ("file-{}".format(fcount), scan, pepmass, str1)
                                mass=list(str1)[0]; intensity=int(list(str1)[1])
                                pdict[scan][mass]=intensity
                                if intensity>3000:
                                    dict1[suf][scan].append(mass)
                                    if mass not in mdict:
                                        mdict[mass]=1
                        
                    msdict={}
                    #sys.exit()
                    
                elif line2.strip()=='':
                    pass
                else:
                    if start==1:
                        if '=' in line2:
                            #Get MS1 peak information
                            if 'PEPMASS' in line2:
                                ms1=float(line2.strip().split('=')[1])
                                pepmass=ms1
                                dict1[suf][scan].append(ms1)
                                if ms1 not in mdict:
                                    mdict[ms1]=1
                                    
                            #Get Scan information
                            elif 'SCANS' in line2:
                                scan=int(line2.strip().split('=')[1])
                                dict1[suf][scan]=[]
                                scandict[scan]=1
                                if scan not in pdict:
                                    pdict[scan]={}
                                else:
                                    print ("Scan repeat: ", scan, suf)
                                    
                                #Initialize msdict for collecting msms to get top 10
                                msdict={} 
                            else:
                                pass
                        else:
                            #Get MSMS peak information
                            sp=line2.strip().split()
                            v1=float(sp[0]); v2=int(sp[1])
                            if int(v1)==271:
                                peak271=1
                            if v1 not in msdict:
                                msdict[v1]=v2
                            else:
                                if v2 > msdict[v1]:
                                    msdict[v1]=v2
                line2=file2.readline()
            file2.close()
            print ("Finished: ", fn)

        #Get all peaks list
        mlist=sorted(list(mdict.keys()))
        scanlist=sorted(list(scandict.keys()))
        sline='\t'.join([str(f) for f in scanlist])

        #Combine all masses from all 3 scans into one file
        dict2={}; m=0
        for suf in dict1:
            for scan in dict1[suf]:
                if scan not in dict2:
                    dict2[scan]=dict1[suf][scan] #peaks
                else:
                    print ("Scan repeat: ", fn, scan)
                    
        #For each scan classify the peaks based on motifs
        #print (pdict)
        #sys.exit()
        for scan in dict2:
            peaks=dict2[scan]; useful=[]; unexplained=[]
            maxpeak=max(peaks)

            #Get peak info
            for peak in peaks:
                flag=0
                #Get peak intensity
                try:
                    intense=pdict[scan][peak]
                except:
                    #First MS1 peak doesn't have any intensity value associated with it
                    intense=0.0

                #Identify peaks
                for motif in motiflist:
                    diffpeak=abs(peak-motif)
                    if diffpeak<0.04:
                        #First differentiate between pentanoic and acetoacetic masses
                        if round(motif,2)-101.06==0 or round(motif,2)-101.02==0:
                            if diffpeak<0.02:
                                str1='{}|{}|{}|{}'.format(peak, motif, intense, motifdict[motif])
                                useful.append(str1)
                                flag=1
                                
                        #then between caffeic acid and Hexose
                        elif round(motif,2)-179.05==0 or round(motif,2)-179.03==0:
                            if diffpeak<0.01:
                                str1='{}|{}|{}|{}'.format(peak, motif, intense, motifdict[motif])
                                useful.append(str1)
                                flag=1

                        #then between coumaric and deoxyhexose
                        elif round(motif,2)-163.06==0 or round(motif,2)-163.04==0:
                            if diffpeak<0.01:
                                str1='{}|{}|{}|{}'.format(peak, motif, intense, motifdict[motif])
                                useful.append(str1)
                                flag=1
                                
                        else:
                            str1='{}|{}|{}|{}'.format(peak, motif, intense, motifdict[motif])
                            useful.append(str1)
                            flag=1
                    else:
                        pass

                if flag==0:
                    str2='{}|{}'.format(peak, intense)
                    unexplained.append(str2)

            #Write to output
            out1.write('file-{}\t{}\t{}\t{}\t{}\n'.format(fcount,scan,maxpeak,useful,unexplained))
        print ("Done with this file")
        #sys.exit()
    line1=file1.readline()
file1.close()
print ("All done!")
        



        
            