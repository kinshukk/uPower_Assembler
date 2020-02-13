assembler_direc=[]
instruct=[]
label=[]

def line_detect(lines):
    for idx,li in enumerate(lines):
        tmp=li.split(" ")
        if tmp[0]==".data":
            assembler_direc.append((tmp,idx))
        elif tmp[0]==".text":
            assembler_direc.append((tmp,idx))
        elif tmp[0].endswith(":"):
            label.append((tmp,idx))
        else:
            instruct.append((tmp,idx))

line_detect([".data","main:","add $a0,$a1,$a2"])

print(assembler_direc)
print(instruct)
print(label)
