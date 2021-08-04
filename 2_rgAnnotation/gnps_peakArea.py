from __future__ import division
import sys
print ("INP1: filelist")
file1=open(sys.argv[1], 'r')
line1=file1.readline()
ilist=[]

#Create output file
out1=open(sys.argv[1]+".mzAll.peakAreas.tab",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
out1.write('#File\tSugarType\tScan\tLeafArea\tLeafPercTotal\tRootArea\tRootPercTotal\t' \
           'LeafTotal\tRootTotal\n')
mcount=0
while line1:
    if line1.startswith('#'):
        pass
    else:
        tab1=line1.strip().split('\t')
        id1=tab1[0]; name=tab1[1]
        f1 = "1_GNPS/"+id1+"-Cent.txt"
        f2 = f1+".mz132.reorder.parsed.fil.uniq"
        f3 = f1+".mz146.reorder.parsed.fil.uniq"
        f4 = f1+".mz162.reorder.parsed.fil.uniq"
        flist=[f2,f3,f4]

        #Get internal standard peak aea
        #telmisartan actual monoisotopic mass = 513.2291
        fn=f1+".mz132.reorder"
        filex=open(fn,'r')
        linex=filex.readline()
        ilist=[]
        while linex:
            tab2=linex.strip().split('\t')
            if linex.startswith('Alignment'):        
                for i in range(0,len(tab2)):
                    if tab2[i].startswith('201') and 'Blank' not in tab2[i]:
                        ilist.append(i)
                        print (tab2[i])
            else:
                scan=tab2[0]; rt=float(tab2[1]); mz=float(tab2[2])
                if abs(rt-1.7)<=0.4 and abs(mz-513.2291)<=0.001:
                #if  abs(mz-513.2291)<=0.002:
                    if len(ilist)==2:
                        areas=[float(tab2[ilist[0]]), float(tab2[ilist[1]])]
                    elif len(ilist)==1:
                        areas=[float(tab2[ilist[0]])]
                    #else:
                    #    areas=[float(tab2[ilist[0]]), float(tab2[ilist[1]]), float(tab2[ilist[2]])]
                        
                        
                    print (fn, rt, mz, areas)
            linex=filex.readline()
        filex.close()

        #Read each filtered file for real
        leaflist=[]; rootlist=[]
        for fn in flist:
            file2 = open(fn, 'r')
            tag='mz'+(fn.split('.mz')[1].split('.reorder')[0])
            line2 = file2.readline()
            ilist=[]; 
            while line2:
                if line2.startswith('Alignment'):
                    tab2=line2.strip().split('\t')
                    for i in range(0,len(tab2)):
                        if tab2[i].startswith('201') and 'Blank' not in tab2[i]:
                            ilist.append(i)
                else:
                    #print (ilist)
                    tab2=line2.strip().split('\t')
                    leaf=int(tab2[ilist[0]])
                    try:
                        root=int(tab2[ilist[1]])
                    except:
                        root=0
                    leaflist.append(leaf)
                    rootlist.append(root)
                line2=file2.readline()
            file2.close()#; print ("####")

        #Calculate peak areas across all files from that species
        leaftot=sum(leaflist)
        roottot=sum(rootlist)
        #print (leaftot, roottot, fn)

        #Read file again
        ncount=0
        for fn in flist:
            file2 = open(fn, 'r')
            line2 = file2.readline()
            tag='mz'+(fn.split('.mz')[1].split('.reorder')[0])
            ilist=[]
            while line2:
                if line2.startswith('Alignment'):
                    tab2=line2.strip().split('\t')
                    for i in range(0,len(tab2)):
                        if tab2[i].startswith('201') and 'Blank' not in tab2[i]:
                            ilist.append(i)
                else:
                    tab2=line2.strip().split('\t')
                    scan=tab2[0]; rt=tab2[1]; mz=tab2[2]
                    str1='{}_{}_{}'.format(scan, rt, mz)
                    leaf=int(tab2[ilist[0]])
                    try:
                        root=int(tab2[ilist[1]])
                    except:
                        root=0

                    if leaftot>0:
                        leafper=(leaf/leaftot)*100
                    else:
                        leafper=0

                    if roottot>0:
                        rootper=(root/roottot)*100
                    else:
                        rootper=0
                    out1.write('{}\t{}\t{}\t{}\t{:.2f}\t{}\t{:.2f}\t{}\t{}\n' \
                        .format(fn,tag,str1,leaf,leafper,root,rootper,leaftot,roottot))
                    ncount+=1
                line2=file2.readline()
            file2.close()

        mcount+=ncount
        print ("Finished: ", f1, " Peaks: ", mcount)
        
    line1=file1.readline()
file1.close(); out1.close()
print ("Total peaks processed: ", mcount)
print ("Done!")
                        
        
        
