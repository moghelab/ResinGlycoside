from __future__ import division
import sys, operator

class step5:
    def __init__(self):
        pass
    
    def filmsms(self,syslist):
        file1=open(syslist[1],'r')
        thresh=int(syslist[2])
        line1=file1.readline()
        flist=[]; fdict={}
        while line1:
            if line1.startswith('#') or line1.startswith('Category'):
                pass
            else:        
                tab1=line1.strip().split(';')
                freq=int(tab1[1])
                if freq>thresh:
                    flist.append(int(tab1[0]))
            line1=file1.readline()
        file1.close()

        #print ("Peaks in fdict: ", len(fdict.keys()))
        #print (fdict)
        #sys.exit()

        file1=open(syslist[0],'r')
        out1=open(syslist[0]+".fil3.t{}.mgf".format(thresh),'w')
        line1=file1.readline()
        while line1:
            sp=line1.strip().split()
            try:
                v1=int(sp[0].split('.')[0])
                if v1 in flist:
                    out1.write(line1)
            except:
                out1.write(line1)
            line1=file1.readline()
        file1.close(); out1.close()

if __name__ == '__main__':
    step5 = step5()
    print ("INP1: mgf.fil output of step4")
    print ("INP2: MSMS frag. frequency CSV output by GNPS")
    print ("    Format: NominalMass;<#ofSamplesWithThatMSMSfragment>")
    print ("INP3: Threshold for filtering (10/20/30..)")
    fragfile=sys.argv[1]; mgffile=sys.argv[2]
    step5.filmsms([fragfile,mgffile,threshx])
    print ("Done!")


    
                    
                    
                        
