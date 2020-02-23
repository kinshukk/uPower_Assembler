import re

def startswith(line, starting, withspace=True):
    if withspace:
        starting = starting + ' '

    l = len(starting)

    if len(line) >= len(starting):
        return line[:l] == starting
    else:
        return False

def preprocess(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        tokens = line.split()
        
        if startswith(line, 'la'):
            Rx, dry = tokens[1], tokens[2]

            if '(' in dry:
                i1 = dry.index('(')
                i2 = dry.index(')')
                D = dry[:i1]
                Ry = dry[i1+1:i2]
                lines[i] = f"addi {Rx}, {Ry}, {D}"
            else:
                #TODO: implement
                print("not implemented value loading offset for la...")
                pass

def get_symbol_table_instructions(lines):
    f = preprocess(lines)

    start_data=0
    start_labels=0
    for i in range(len(f)):
        if f[i]==".text":
            start_labels=i
        if f[i]==".data":
            start_data=i


    cur_location=0x4000000
    labels={}
    instruction={}
    var=re.compile(r'.+:')
    for i in range(start_labels+1,len(f)):
        if bool(var.match(f[i])):
            x=re.split(":",f[i])
            labels[x[0]]=hex(cur_location)
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
    initilized={}
    for i in range(start_data+1,start_labels):
        if bool(var.match(f[i])):
            arr=f[i].split()
            lable=re.split(":",arr[0])[0]
            data[lable]=hex(cur_location)
            datatype=arr[1][1:]
            string=""
            if datatype=="ascii":
                for i in f[i]:
                    if i=="\"" and flag==0:
                        flag=1
                        continue
                    if flag==1 and i!="\"":
                        string=string+f[i]
                    if flag==1 and i=="\"":
                        flag=0
                initilized[str(cur_location)]=string
            elif datatype=="word":
                x=f[i].split(',')
                for i in range(len(x)):
                    if i==0:
                        initilized[str(cur_location+i*4)]=x[i].split()[-1]
                    else:
                        initilized[str(cur_location+i*4)]=x[i]			
            else:
                y=f[i].split("#")
                y=y[0].split()
                if len(y)>=2:
                    initilized[str(cur_location)]=y[2]
            if datatype=="byte":
                cur_location=cur_location+1
            elif datatype=="word":
                x=len(f[i].split(','))
                cur_location=cur_location+4*x
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

        return (instruction, labels, data,initilized)
