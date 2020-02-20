import re

def get_symbol_table_instructions(lines):
        f = lines
        start_data=0
        start_text=0
        for i in range(len(f)):
                if f[i]==".text":
                        start_text=i
                if f[i]==".data":
                        start_data=i


        cur_location=0x4000000
        text={}
        instruction={}
        var=re.compile(r'.+:')
        for i in range(start_text+1,len(f)):
                if bool(var.match(f[i])):
                        x=re.split(":",f[i])
                        text[x[0]]=hex(cur_location)
                        cur_location=cur_location-4
                else:
                        tmp=f[i].split('#')[0]
                        tmp=" ".join(tmp.split())
                        if tmp.strip():
                                instruction[cur_location]=tmp
                        else:
                                cur_location=cur_location-4
                cur_location=cur_location+4


        cur_location=0x10000000
        data={}
        for i in range(start_data+1,start_text):
                if bool(var.match(f[i])):
                        arr=f[i].split()
                        lable=re.split(":",arr[0])[0]
                        data[lable]=hex(cur_location)
                        datatype=arr[1][1:]
                        if datatype=="byte":
                                cur_location=cur_location+1
                        elif datatype=="word":
                                cur_location=cur_location+4
                        elif datatype=="halfword":
                                cur_location=cur_location+2
                        elif datatype=="space":
                                cur_location=cur_location+int(arr[2])
                        elif datatype=="ascii":
                                flag=0
                                count=0
                                for i in f[i]:
                                        if i=="\"" and flag==0:
                                                flag=1
                                                continue
                                        if flag==1 and i!="\"":
                                                count=count+1
                                        if flag==1 and i=="\"":
                                                flag=0
                                cur_location=cur_location+count

        return (instruction, text, data)
