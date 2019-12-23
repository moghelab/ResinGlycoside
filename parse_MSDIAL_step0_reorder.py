from __future__ import division
import sys

class step0:
    def __init__(self):
        pass

    def writeTabs(self, tab):
        nlist=[]
        if len(tab)==27:
            nlist=tab
        elif len(tab)==25:
            nlist=tab[0:22]
            nlist.append(tab[23])
            nlist.append(tab[24])
            nlist.append(tab[22])
        else:
            print ("Weird line in reorder: ")
            for i in range(0,len(tab)):
                print (i, tab[i])
            
            sys.exit()
        mynline='\t'.join(nlist)
        return (mynline)
        
    def full_script(self,syslist):
        #Read fragment file
        file1=open(syslist[0],'r')
        out1=open(syslist[0]+".reorder",'w')
        line1=file1.readline()
        startProcessing=0
        while line1:
            if line1.startswith('Alignment'):
                startProcessing=1
                tab1=line1.strip().split('\t')
                nline=self.writeTabs(tab1)
                out1.write(f'{nline}\n')
            elif startProcessing==1:
                tab1=line1.strip().split('\t')
                tab1=line1.strip().split('\t')
                nline=self.writeTabs(tab1)
                out1.write(f'{nline}\n')
            line1=file1.readline()
        file1.close(); out1.close()

if __name__ == '__main__':
    step0 = step0()    
    print ("INP1: Peak area file")    
    areafile=sys.argv[2]
    step0.full_script([areafile])
    print ("Done!")
    

