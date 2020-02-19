
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
    if func in instruct_x.keys():
        
        tmp_ans=""
        req=args.split(",")
        req=[i.replace(" ","") for i in req]
        
        tmp_ans=tmp_ans+bin(instruct_x[func][0])
        tmp_ans=tmp_ans+bin(reg_to_num[req[1]])
        tmp_ans=tmp_ans+bin(reg_to_num[req[0]])
        tmp_ans=tmp_ans+bin(reg_to_num[req[2]])
        tmp_ans=tmp_ans+bin(instruct_x[func][3])+"0"
        tmp_ans=tmp_ans.replace("0b","");
        fin_ans[u]=tmp_ans;

print(fin_ans)
