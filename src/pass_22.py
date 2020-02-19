instruct_x={"and":[31,None,0,28,None,None],"exstw":[31,None,0,986,None,None],"nand":[31,None,0,476,None,None],"or":[31,None,0,444,None,None],"xor":[31,None,0,316,None,None],"sld":[31,None,0,794,None,None],"srd":[31,None,0,539,None,None],"srad":[31,None,0,794,None,None],"cmp":[31,None,0,0,None,None]}


reg_to_num={"R"+str(i):i for i in range(32)}
reg_to_num["LR"]=32
reg_to_num["CR"]=33
reg_to_num["SRR0"]=34


ans={"1":"and R1,R3,LR"}
fin_ans={}


for z in ans:    
    u=z
    v=ans[z]
    
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
            RT = req[0].trim()

            i1 = req[1].index('(')
            i2 = req[1].index(')')
            
            SI = int(req[1][:i1].trim())
            RA = req[1][i1+1:i2].trim()
            
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

print(fin_ans)
