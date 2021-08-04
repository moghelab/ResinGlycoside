from __future__ import division
import sys

class step1:
    def __init__(self):
        pass
    def full_script(self,syslist):

        #Read fragment file
        file1=open(syslist[0],'r')
        line1=file1.readline()
        fdict={}
        while line1:
            if line1.startswith('#'):
                pass
            else:        
                frags=line1.strip()#.split(',')
                #[float(x) for x in frags]
                fdict[frags]=1
            line1=file1.readline()
        file1.close()

        #Read all lines in INP2 first
        file1=open(syslist[1],'r').readlines()
        dictx={}
        for line in file1:
            sp=line.strip().split('\t')
            id1=sp[0]
            dictx[id1]=line.strip()
        file1=''
        

        #Re-read INP2 line by line now
        file1=open(syslist[1],'r')
        out1=open(syslist[1]+".parsed",'w')
        line1=file1.readline()
        startProcessing=0; m=0
        while line1:
            if line1.startswith('Alignment'):
                startProcessing=1
                out1.write(line1)
            elif startProcessing==1:
                tab1=line1.strip().split('\t')               

                #Specify values
                #Filter by peak area vs. blank
                id1=tab1[0]; postCuration=tab1[5]; flag=0; finStatus='fail'; hflag=0
                
                #Remove in-source fragments defined by 'found in higher' tag
                #if 'found in higher' in postCuration:
                #    hflag=1
                '''
                if 'found in higher' in postCuration:
                    xsp=postCuration.split('; '); hflag=0
                    for item in xsp:
                        if item.startswith('found in higher'):
                            idx=item.split('_')[1]                            
                            if idx in dictx:                                
                                hflag=1
                else:
                    hflag=0
                '''
                    
                if hflag==0:                    
                    #Remove peaks without MS/MS
                    if tab1[21]!='':            
                        #Get maximum blank area
                        pa_samples=[float(x) for x in [tab1[22],tab1[23]]]
                        pa_blanks=[float(x) for x in tab1[24:]]
                        max_blank=max(pa_blanks)

                        #Estimate if peak area of at least 1 sample is 10X max_blank                        
                        for area in pa_samples:                
                            if area>1000:
                                if max_blank==0:
                                    flag=1
                                else:
                                    norm=max_blank/area                    
                                    if norm<=0.10:
                                        flag=1                        
                
                if flag==1:
                    printstat=0
                    if syslist[1]=='34-Cent.txt' and id1=='7119':
                        printstat=1
                        
                    #Get reference peak intensity from the isotope file
                    refpeaks=tab1[20].split(' ')
                    plist=[]
                    for px in refpeaks:
                        plist.append(int(px.split(':')[1]))
                    maxpeak=max(plist)
                    
                    #Get MS/MS fragments and their intensities
                    #Get maximum intensity
                    msms=tab1[21].split(' ')                        
                    
                    #Initialize gdict and get fragments from fdict into gdict
                    gdict={}
                    for linex in fdict:                                        
                        frags=[float(x) for x in linex.split(',')]                        
                        for frag in frags:                        
                            #Initialize a dict to capture all intensities
                            if frag not in gdict:
                                gdict[frag]=[]

                    #Gather all MSMS fragment intensities for fragment combinations listed in file 1
                    idict={}
                    for item in msms:
                        if item!='':
                            sp=item.split(':')                
                            ion=float(sp[0]); intensity=float(sp[1])
                            if intensity>0:
                                if intensity not in idict:
                                    idict[intensity]=[ion]
                                else:
                                    idict[intensity].append(ion)
                                for frag in gdict:                            
                                    if abs(frag-ion)<=0.01:                                
                                        gdict[frag].append(intensity)
                                    
                    #Get maximum ion intensity for each frag
                    hdict={}
                    for linex in fdict:
                        frags=[float(x) for x in linex.split(',')]                        
                        for frag in frags:                    
                            if gdict[frag]!=[]:
                                maxion=max(gdict[frag]) #v2
                                #maxion=sum(gdict[frag])
                                if frag not in hdict:
                                    if maxion>0.0:
                                        hdict[frag]=maxion
                                else:
                                    #print ("repeat: ", frag)
                                    #print (hdict)
                                    #print (linex)
                                    #sys.exit()
                                    pass
                        
                    #Get maximum intensity of all fragments
                    max_int=max(idict.keys())      #v2      
                    
                    #Filter using MS/MS fragment combinations
                    for linex in fdict:
                        frags=[float(x) for x in linex.split(',')]                        
                        count=0
                        for frag in frags:
                            if frag in hdict:
                                maxion=hdict[frag]
                                ratio=max_int/maxion #v2
                                #if id1=='7119':
                                #    print ("~~~~", frag, maxion, max_int, ratio)
                                #ratio=maxpeak/maxion
                                if ratio<=20:
                                    count+=1
                                    #if id1=='7119':
                                    #    print ('####', frag, maxion, max_int, ratio, 'pass')
                                    
                        #Both MS/MS peaks in the combination need to have
                        #intensities above 10% of max ion intensity
                        if count>=len(frags):
                            out1.write(line1)
                            m+=1
                            finStatus='pass'
                '''
                if id1=='7119':# or id1=='6838' or id1=='6839':
                    print (id1, flag, postCuration)
                    print (id1, pa_samples)
                    print (id1, pa_blanks)
                    print (id1, max_blank)
                    print (id1, maxpeak)
                    print (id1, hdict)
                    try:
                        print (">>>", id1, maxpeak, maxion, ratio)
                        print (">>>", count, len(frags))
                    except:
                        pass
                    print (finStatus)
                    print ("######")
                #sys.exit()
                '''
                
            else:
                pass
            line1=file1.readline()
        file1.close(); out1.close()
        print ("# of targeted compounds in {}: {}".format(syslist[2],m))        

if __name__ == '__main__':
    step1 = step1()
    print ("INP1: Fragment combinations to filter using this script")
    print ("INP2: Peak area file")
    print ("INP3: Species name as Genus_species")
    fragfile=sys.argv[1]; areafile=sys.argv[2]; species=sys.argv[3]
    step1.full_script([fragfile,areafile, species])
    print ("Done!")
    


        
        
