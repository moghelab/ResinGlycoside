from __future__ import division
import sys, operator, random
import pandas as pd

print ("INP1: mzsuffixes in csv eg: mz132,mz146,mz162")
print ("INP2: filelist.tab")
sufs=sys.argv[1].split(',')

file1=open(sys.argv[2],'r')
out2=open(sys.argv[2]+".skippedCounts",'w')
out2.write('#python {}\n'.format(' '.join(sys.argv)))
line1=file1.readline()
while line1:
    if line1.startswith('#'):
        pass
    else:
        sp=line1.strip().split('\t')

        #Rename the file to account for different fragpairs files
        fcount=sp[0].zfill(2)
        dict1={}; dict2={}; mdict={}; scandict={}
        for suf in sufs:
            fn=f'2_MGF/{fcount}-Cent.mgf.{suf}.fil.mgf'
            print ("Now reading: ", fn)
            file2=open(fn,'r')
            line2=file2.readline()
            start=0
            dict1[suf]={}; repscan=[]
            while line2:
                if 'SCANS=' in line2:
                    scan=line2.strip().split('=')[1]
                    if scan not in dict1:
                        dict1[scan]=[suf]
                    else:
                        dict1[scan].append(suf)
                        repscan.append(scan)
                line2=file2.readline()
            file2.close()

        donelist=[]; skipped={}
        for suf in sufs:
            fn=f'2_MGF/{fcount}-Cent.mgf.{suf}.fil.mgf'
            print ("Now Re-reading: ", fn)
            file2=open(fn,'r')
            out1=open(fn+".uniq",'w')
            line2=file2.readline()
            while line2:
                if line2.startswith('BEGIN IONS'):
                    list1=[]
                    list1.append(line2)
                elif line2.startswith('END IONS'):
                    list1.append(line2)
                    if scan not in repscan:
                        block=''.join(list1)
                        out1.write(block)
                        list1=[]
                    else:
                        if scan not in donelist:
                            donelist.append(scan)
                            block=''.join(list1)
                            out1.write(block)
                            list1=[]
                        else:
                            list1=[]
                            if suf not in skipped:
                                skipped[suf]=1
                            else:
                                skipped[suf]+=1
                elif line2.strip()=='':
                    out1.write(line2)
                else:
                    if '=' not in line2:
                        list1.append(line2)
                    else:
                        list1.append(line2)
                        if 'SCANS' in line2:
                            scan=line2.strip().split('=')[1]
                line2=file2.readline()
            file2.close(); out1.close()

        if suf in skipped:
            out2.write(f'2_MGF/{fcount}-Cent.mgf\t{suf}\t{skipped[suf]}\t{sp[1]}\t{sp[2]}]\n')
        else:
            out2.write(f'2_MGF/{fcount}-Cent.mgf\t{suf}\t0\t{sp[1]}\t{sp[2]}]\n')
    line1=file1.readline()
file1.close(); out2.close()
print ("All done!")
        



        
            
