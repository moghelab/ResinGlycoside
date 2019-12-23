import sys
import parse_MSDIAL_step0_reorder
import parse_MSDIAL_step1_gnps
import parse_MSDIAL_step2_filter
import parse_MSDIAL_step3_stats
step0=parse_MSDIAL_step0_reorder.step0()
step1=parse_MSDIAL_step1_gnps.step1()
step2=parse_MSDIAL_step2_filter.step2()
step3=parse_MSDIAL_step3_stats.step3()

print ("INP1: Fragment combinations file")
print ("INP2: File containing a list of files to process")
print ("Format should be FileName -- SpeciesName e.g. Ipomoea_tricolor")

fragfile=sys.argv[1]
file1=open(sys.argv[2],'r')
out1=open(sys.argv[2]+".combined.stats",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
#out1.write('#FileName\tSpecies\tTotal\tShoot\tRoot\tOnlyRoot\tOnlyShoot\tBoth\t{}\n'. \
#           format('\t'.join(flist2)))
line1=file1.readline()
added=0
while line1:
    if line1.startswith('#'):
        pass
    else:
        sp=line1.strip().split('\t')
        fcount=int(sp[0])
        fn=f'_RawFiles/RG{fcount}_7_GnpsTable.txt'    
        species=sp[1]
        print (f'Processing {species} through file {fn}...')
        #Reorganize table        
        step0.full_script([fn])                
            
        #Run pipeline
        step1.full_script([fragfile, fn+".reorder", species])
        step2.mergeLines(fn+".reorder.parsed")
        step3.stats([fragfile, fn+".reorder.parsed.fil", species])
        #sys.exit()

        file2=open(fn+".reorder.parsed.fil.stats",'r')
        line2=file2.readline()        
        while line2:
            if line2.startswith('#python'):
                pass
            elif line2.startswith('#'):
                if added==0:
                    out1.write(line2); added=1
            else:
                out1.write(line2)
            line2=file2.readline()
        file2.close()

        #print ("######")
        
            
    line1=file1.readline()
file1.close(); out1.close()

print ("All done!")
    
    
