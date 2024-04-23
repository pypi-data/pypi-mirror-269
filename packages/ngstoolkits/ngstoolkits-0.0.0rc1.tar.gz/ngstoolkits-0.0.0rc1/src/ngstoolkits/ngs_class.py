# vcf
class single_mutation():
    def __init__(self,CHROM,POS,REF,ALT):
        self.CHROM = CHROM
        self.POS =  POS
        self.REF = REF
        self.ALT = ALT
        print("load mutation")

    @property
    def type(self):
        if len(self.REF)>len(self.ALT):
            return "DEL"
        elif len(self.REF)<len(self.ALT):
            return "INS"
        else:
            return "SNV"
    def vcfformat(self):
        self.REF = "." if self.REF == "" else self.REF
        self.ALT = "." if self.ALT == "" else self.ALT
        return(self.CHROM + "\t" +str(self.POS) +"\t.\t" + self.REF + "\t" + self.ALT +"\t.\t.\tDP="+str(self.DP)+";DP4="+self.DP4 + ";MergeMut=" + ",".join(self.MergeMut) +"\tGT:AD:DP\t"+ self.GT+":" + str(self.AD)  + ":" + str(self.DP)+"\n")

def unwrite():
    pass
