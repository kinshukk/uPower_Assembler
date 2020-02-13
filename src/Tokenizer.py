
class Tokenizer:
    def __init__(self):
        self.assembler_direc=[]
        self.instruct=[]
        self.label=[]

    def run(self, source):
        return self.line_detect(source)

    def line_detect(self,lines):
        for idx,li in enumerate(lines):
            tmp=li.split(" ")
            if tmp[0]==".data":
                self.assembler_direc.append((tmp,idx))
            elif tmp[0]==".text":
                self.assembler_direc.append((tmp,idx))
            elif tmp[0].endswith(":"):
                self.label.append((tmp,idx))
            else:
                self.instruct.append((tmp,idx))
