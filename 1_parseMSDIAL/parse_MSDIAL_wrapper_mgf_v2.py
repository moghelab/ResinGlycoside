import sys, os
import parse_MSDIAL_step0_reorder
import parse_MSDIAL_step1_gnps
import parse_MSDIAL_step2_filter
import parse_MSDIAL_step3_stats
import parse_MSDIAL_step4_MGFfilter
import parse_MSDIAL_step5_MSMSfilter

step0=parse_MSDIAL_step0_reorder.step0()
step1=parse_MSDIAL_step1_gnps.step1()
step2=parse_MSDIAL_step2_filter.step2()
step3=parse_MSDIAL_step3_stats.step3()
step4=parse_MSDIAL_step4_MGFfilter.step4()
step5=parse_MSDIAL_step5_MSMSfilter.step5()

print ("INP1: Fragment combinations file")
print ("INP2: File containing a list of files to process")
print ("Format should be FileName -- SpeciesName e.g. Ipomoea_tricolor")
print ("INP3: Suffix for filename (typically mz132 or mz146 or mz162)")
print ("INP4: Do you want to filter MGF file using MSMS fragments (y/n)")
print ("      If yes, provide INP4 and INP5")
print ("INP5: MSMS frag. frequency CSV output by GNPS")
print ("    Format: NominalMass;<#ofSamplesWithThatMSMSfragment>")
print ("INP6: Integer threshold for freq. filtering of MSMS frags (10/20/30...)")
print ("#########")
print ("NOTE: INP5 is typically a result of second iteration after you have " \
       "first made a preliminary network using fil.mgf (output of step4)")

fragfile=sys.argv[1]
file1=open(sys.argv[2],'r')
pf=sys.argv[1]
suf=sys.argv[3]
out1=open(sys.argv[2]+f".{suf}.combined.stats",'w')
out1.write('#python {}\n'.format(' '.join(sys.argv)))
yesno=sys.argv[4]
#out1.write('#FileName\tSpecies\tTotal\tShoot\tRoot\tOnlyRoot\tOnlyShoot\tBoth\t{}\n'. \
#           format('\t'.join(flist2)))
line1=file1.readline()
added=0
while line1:
    if line1.startswith('#'):
        pass
    else:
        sp=line1.strip().split('\t')
        #fcount=int(sp[0])
        #fn=f'_RawFiles/RG{fcount}_7_GnpsTable.txt'

        #Rename the file to account for different fragpairs files
        fcount=sp[0].zfill(2)
        fnx=f'1_GNPS/{fcount}-Cent.txt'
        os.system('cp {} {}.{}\n'.format(fnx,fnx,suf))
        fn=f'{fnx}.{suf}'

        #Reorganize table 
        species=sp[1]
        print (f'Processing {species} through file {fn}...')  
        step0.full_script([fn])                
            
        #Run pipeline
        step1.full_script([fragfile, fn+".reorder", species])
        step2.mergeLines(fn+".reorder.parsed")

        #Remove duplicated lines
        lines=open(fn+".reorder.parsed.fil",'r')
        outx=open(fn+".reorder.parsed.fil.uniq",'w')
        doneline=[]
        for line in lines:
            if line not in doneline:
                outx.write(line)
                doneline.append(line)
        outx.close()
        
        step3.stats([fragfile, fn+".reorder.parsed.fil.uniq", species,suf])
        step4.filmgf([fn+".reorder.parsed.fil.uniq", f'2_MGF/{fcount}-Cent.mgf', suf])
        #sys.exit()

        #Get stats based on filtering of GNPS table file
        file2=open(fn+".reorder.parsed.fil.uniq.{}.stats".format(suf),'r')
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

        if yesno=='y':
            #Filter fil.mgf using MSMS
            tx=sys.argv[6]
            step5.filmsms([f'2_MGF/{fcount}-Cent.mgf.{suf}.fil.mgf', sys.argv[5], tx])
        
        
            
    line1=file1.readline()
file1.close(); out1.close()

print ("All done!")
    
    
