from reportlab.lib.units import cm
from Bio import SeqIO
from Bio.Graphics import BasicChromosome
import os,shutil

def get_chromlen(faifile):
    chromlen={}
    with open(faifile,'r') as r:
        for line in r:
            if not line.startswith('#'):
                lines=line.strip().split()
                chromlen.update({str(lines[0]):int(lines[2])})
        return chromlen

def get_gbfile(chromlen,vcffile):
    #get snpdict
    snpdict={}
    innerlist=[]
    with open(vcffile,'r') as r:
        for line in r:
            if not line.startswith('#'):
                    lines=line.strip().split()
                    tuple1=tuple((int(lines[1]),str(lines[2])))
                    if lines[0] in snpdict.keys():
                        innerlist.append(tuple1)
                        snpdict[lines[0]] = innerlist
                    else:
                        innerlist=[]
                        innerlist.append(tuple1)
                        snpdict.update({lines[0]:innerlist})
                        #snpdict{chromname : (SNP_location,SNP_id)}
    #write snpdict to gbfile
    if not os.path.exists('gbfile'):
        os.mkdir('gbfile')
    for key in snpdict:
        with open(os.path.join('gbfile', key+'.gb'),'w') as w:
            w.write('LOCUS       {}            {} bp    DNA     \
                    linear   PLN 26-JUL-2020\n'.format(key,chromlen[key]))
            w.write('FEATURES             Location/Qualifiers\n')
            for (snploc,snpid) in snpdict[key]:
                w.write('     tRNA            complement({}..{})\n'\
                        .format(snploc, snploc+20))
                w.write('                     /locus_tag=\"{}\"\n'\
                        .format(snpid))
            w.write('ORIGIN      \n//')

def drawSNPLoc(vcffile, faifile, PageSize=(40*cm, 20*cm), \
               outfile="location_of_SNP.pdf", Title=None, \
               LabelCol=None, telomere_length=None ):
    chromlen=get_chromlen(faifile)
    get_gbfile(chromlen,vcffile)
    #set telomere_length
    max_len=max([i for i in chromlen.values()])
    if not telomere_length:telomere_length=int(max_len/20)
    
    #get entries (  example:  entries = [("Chr I", "test.gb")]  )
    gbfilename=os.listdir('gbfile')
    entries = [(i.split('.')[0], os.path.join('gbfile',i)) \
               for i in gbfilename if i.endswith('.gb')]
    
    #draw start
    #step1: draw the background of your picture
    chr_diagram = BasicChromosome.Organism()
    chr_diagram.page_size = PageSize
    
    #step2: draw chromsomes in background
    for index, (name, filename) in enumerate(entries):
        record = SeqIO.read(filename,"genbank")
        length = len(record)
        features = [f for f in record.features if f.type=="tRNA"]

        if not LabelCol:
            #Draw colorful labels
            for f in features: f.qualifiers["color"] = [index+2]
        else:
            #Draw color you set
            for f in features: f.qualifiers["color"] = [LabelCol]
    
        cur_chromosome = BasicChromosome.Chromosome(name)
        #Set the scale to the MAXIMUM length plus the two telomeres in bp
        cur_chromosome.scale_num = max_len + 2 * telomere_length
    
        #Add an opening telomere
        start = BasicChromosome.TelomereSegment()
        start.scale = telomere_length
        cur_chromosome.add(start)
    
        #Add a body - again using bp as the scale length here.
        body = BasicChromosome.AnnotatedChromosomeSegment(length, features)
        body.scale = length
        cur_chromosome.add(body)
    
        #Add a closing telomere
        end = BasicChromosome.TelomereSegment(inverted=True)
        end.scale = telomere_length
        cur_chromosome.add(end)
    
        #This chromosome is done
        chr_diagram.add(cur_chromosome)
    chr_diagram.draw(outfile, Title)
    shutil.rmtree('gbfile')

#run for test
if __name__ == "__main__":
    import sys
    os.chdir(os.path.dirname(sys.argv[0]))
    faifile=r'test_chrom_location.txt'
    vcffile=r'test.vcf'
    drawSNPLoc(vcffile, faifile, PageSize=(80*cm, 20*cm), \
               outfile="location_of_SNP.pdf", Title="Cotton", \
               LabelCol='green', telomere_length=4000000)