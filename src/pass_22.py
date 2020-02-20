from tqdm import tqdm

def convert_lines(lines, label, data):
    instruct_x={"and":[31,None,0,28,None,None],"exstw":[31,None,0,986,None,None],"nand":[31,None,0,476,None,None],"or":[31,None,0,444,None,None],"xor":[31,None,0,316,None,None],"sld":[31,None,0,794,None,None],"srd":[31,None,0,539,None,None],"srad":[31,None,0,794,None,None],"cmp":[31,None,0,0,None,None]}
    
    instruct_xo={"add":[31,0,0,266,None,None],"subf":[31,0,0,40,None,None]}
    
    instruct_d={"addi":[14,None,None,None,None,0],"addis":[15,None,None,None,None,0],"andi":[28,None,None,None,None,0],"ori":[24,None,None,None,None,0],"xori":[26,None,None,None,None,0],"lwz":[32,None,None,None,None,1],"stw":[36,None,None,None,None,1],"stwu":[37,None,None,None,None,1],"lhz":[40,None,None,None,None,1],"lha":[42,None,None,None,None,1],"sth":[44,None,None,None,None,1],"lbz":[34,None,None,None,None,1],"stb":[38,None,None,None,None,1]}
    
    instruct_m={"rlwinm":[21,None,0,None,None,None]}
    
    # sradi
    
    instruct_xs={"sradi":[31,None,0,413,None,None]}
    
    
    instruct_i={"b":[18,None,None,None,0,0],"ba":[18,None,None,None,1,0],"bl":[18,None,None,None,0,1]}
    
    # take care
    instruct_b={"bc":[19,None,None,None,0,0],"bca":[19,None,None,None,1,0]}
    
    instruct_ds={"ld":[58,None,None,0,None,None],"std":[62,None,None,0,None,None]}
    
    
    reg_to_num={"R"+str(i):i for i in range(32)}
    reg_to_num["LR"]=32
    reg_to_num["CR"]=33
    reg_to_num["SRR0"]=34
    
    
    fin_ans={}
    
    
    for z in tqdm(lines):    
        #unpack key, value
        print(z)
        u=z
        v=lines[z]
        print(f"u: {u}, v: {v}") 
        #function name (add, sub, etc.)
        func=v[:v.index(' ')]
        args=v[v.index(' '):]
        print(func,"asdf ")
        print(args)

        tmp=""
        req=args.split(",")
        req=[i.replace(" ","") for i in req]
    
        if func in instruct_x.keys():
            tmp=tmp+"{:06b}".format(instruct_x[func][0])
            tmp=tmp+"{:05b}".format(reg_to_num[req[1]])
            tmp=tmp+"{:05b}".format(reg_to_num[req[0]])
            tmp=tmp+"{:05b}".format(reg_to_num[req[2]])
            tmp=tmp+"{:010b}".format(instruct_x[func][3])+"0"
            tmp=tmp.replace("0b","")
            fin_ans[u]=tmp
    
        elif func in instruct_xo.keys():
            tmp += "{:06b}".format(instruct_xo[func][0])
            tmp += "{:05b}".format(reg_to_num[req[0]])
            tmp += "{:05b}".format(reg_to_num[req[1]])
            tmp += "{:05b}".format(reg_to_num[req[2]])
            tmp += "{:01b}".format(instruct_xo[func][1])
            tmp += "{:09b}".format(instruct_xo[func][3]) + "0"
            tmp = tmp.replace("0b","")
            fin_ans[u]=tmp
    
        elif func in instruct_d.keys():
            if instruct_d[func][-1] == 1:
                #func RT, D(RA)
                RT = req[0].strip()
    
                i1 = req[1].index('(')
                i2 = req[1].index(')')
                
                SI = int(req[1][:i1].strip())
                RA = req[1][i1+1:i2].strip()
                
                tmp += "{:06b}".format(instruct_d[func][0])
                tmp += "{:05b}".format(reg_to_num[RT])
                tmp += "{:05b}".format(reg_to_num[RA])
                tmp += "{:016b}".format(SI)
                tmp = tmp.replace("0b","")
                fin_ans[u]=tmp
    
            elif instruct_d[func][-1] == 0:
                tmp += "{:06b}".format(instruct_d[func][0])
                tmp += "{:05b}".format(reg_to_num[req[0]])
                tmp += "{:05b}".format(reg_to_num[req[1]])
                tmp += "{:016b}".format(reg_to_num[req[2]])
                tmp = tmp.replace("0b","")
                fin_ans[u]=tmp
            
            else:
                print("\n\nO crap something isn't right. D type assembly\n\n")
    
        elif func in instruct_i.keys():
            tmp += "{:06b}".format(instruct_xo[func][0])
            tmp += "{:024b}".format(reg_to_num[req[0]])
            tmp += "{:01b}".format(instruct_xo[func][-2])
            tmp += "{:09b}".format(instruct_xo[func][-1])
            tmp = tmp.replace("0b","")
            fin_ans[u]=tmp
    
        elif func in instruct_ds.keys():
            RT = req[0].strip()
    
            i1 = req[1].index('(')
            i2 = req[1].index(')')
                
            DS = int(req[1][:i1].strip())
            RA = req[1][i1+1:i2].strip()
                
            tmp += "{:06b}".format(instruct_d[func][0])
            tmp += "{:05b}".format(reg_to_num[RT])
            tmp += "{:05b}".format(reg_to_num[RA])
            tmp += "{:014b}".format(DS)
            tmp += "{:02b}".format(instruct_d[func][3])
            tmp = tmp.replace("0b","")
            fin_ans[u]=tmp
    
        elif func in instruct_b.keys():
            print("B start!!")
            tmp += "{:06b}".format(instruct_b[func][0])
            tmp += "{:05b}".format(reg_to_num[req[0]])
            tmp += "{:05b}".format(reg_to_num[req[1]])
            
            if req[2] not in label:
                print("Label not found in symbol table!!")
                return

            label_address = int(label[req[2]], 0)
            
            if instruct_b[func][-2] == 0:
                label_address -= int(u)
            
            tmp += "{:014b}".format(label_address)
            tmp += "{:01b}".format(instruct_b[func][-2])
            tmp += "{:01b}".format(instruct_b[func][-1])

            print("B TYPE!!!")

            fin_ans[u] = tmp

        else:
            print(f"command '{func}' not recognized...exiting")
            return

    return fin_ans
