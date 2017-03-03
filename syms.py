#SYMbolSctak 1.3.1
from __future__ import print_function #required for compatibility with python 2.x
from sys import argv
#parse=input("Program:"); #read prog from stdin, single line
try:
    unicode
    realinput=raw_input
    v=2
except:
    unicode=lambda x:x
    realinput=input
    v=3
if len(argv)==1:
    argv+=realinput("Args: ").split(" ")
cmdoptions="".join([i[1:] for i in argv if len(i)>0 and i[0]=="-"]) #i'd do this better, but i'm lazy
if "h" in cmdoptions or argv[1]=="":
    print("Usage: python syms.py (-h|file.syms -ridc)\n-h: Prints this help message.\n-d: Prints debug output.\n-c: Colors debug output. (Not recommended on TIO.)\n-i: Dumps stack at end of execution.\n-r: Reverses inputs to {+-*/@}.")
    if idle==0:
        exit(0)
    else:
        "Idle does not like exit()"/0
with open(argv[1]) as w:
    parse=w.read()
options={"reverse-math":False,"debug-messages":False,"color-debug":False,"full-debug":False,"implicit-output":False,"fixed-equals":True}
if "d" in cmdoptions:
    options["debug-messages"]=True
    if "c" in cmdoptions:
        options["color-debug"]=True
if "i" in cmdoptions:
    options["implicit-output"]=True
if "r" in cmdoptions:
    options["reverse-math"]=True
tokens=list(parse)
extensions=[]
stack=[]
parsemode=0 #0 for normal, 1 for string ##unused
parselevel=0 # # of nested {}s
temp=""
pvars=dict()
try:
    unicode("")
except NameError:
    def unicode(x):return x #more compatitbility stuff
def modprint(x):
    x=str(x)
    print(x)
def modinput(x):
    x=str(x)
    try:
        return raw_input(x)
    except NameError:
        return input(x)
def reverseif():
    if options["reverse-math"]:
        a=stack.pop()
        b=stack.pop()
        stack.append(a);stack.append(b)
while len(tokens)>0:
    try:
        if options["debug-messages"] and (options["full-debug"] or parselevel==0):
            if options["color-debug"]:
                print("\033[31m",end="");print("Program: "+"".join(tokens));print("\033[35m",end="");print("Stack: "+str(stack))
                if options["full-debug"]: 
                    print("\033[33mTemporary: "+temp);print("String nest: "+str(parselevel+parsemode))
                print("\033[34mIteration...\033[30;0m") #colorized debug code (if random junk appears, do not use)
            else:
                print("Cycle");print("Program: "+"".join(tokens));print("Stack: "+str(stack))
                if options["full-debug"]: 
                    print("Temporary: "+temp);print("String nest: "+str(parselevel+parsemode))
                print("Program") #debug code
        current=tokens.pop(0)
#       if current=='"' and False:
#           if parsemode==1:
#               parsemode=0
#               stack.append(temp)
#               temp=""
#           else:
#               parsemode=1
#           continue
        #string
        if current=="{": #open string
            parselevel+=1
            if parselevel>1:
                temp+="{"
            continue
        if current=="}": #close string
            parselevel-=1
            if parselevel==0:
                stack.append(temp)
                temp=""
            else: #we're still in a string
                temp+="}"
                continue
        if current=='\\': #add next
            temp+=tokens.pop(0)
            continue
        if parsemode==1 or parselevel>0: #in a string, nothing special
            temp+=current
            continue
        #we are not in a string/function
        #???? a number
        if unicode(current).isnumeric():
            temp+=str(current)
            continue
        #booleans
        if current=="\"":
            stack.append(True)
            continue
        if current=="\'":
            stack.append(False)
            continue
        #instructions
        #io
        if current==">":
            modprint(stack.pop()) #For this and modinput, see top.
        if current=="<":
            stack.append(modinput(stack.pop()))
        #math operations
        if current=="+":
            reverseif() #see top
            stack.append(stack.pop()+stack.pop())
        if current=="-":
            reverseif()
            stack.append(stack.pop()-stack.pop())
        if current=="*":
            reverseif()
            stack.append(stack.pop()*stack.pop())
        if current=="/":
            reverseif()
            stack.append(stack.pop()/stack.pop())
        if current==";":
            if temp=="":
                stack.append(int(stack.pop()))
            else:
                stack.append(int(temp))
                temp=""
        #boolean operations
        if current=="=":
            if options["fixed-equals"]:
                a,b=stack.pop(),stack.pop()
                stack.append(type(a)==type(b) and a==b)
            else:
                stack.append(stack.pop()==stack.pop())
        if current=="!":
            stack.append(not stack.pop())
        #string operations
        #add
        if current=="@":
            reverseif()
            stack.append(stack.pop()[stack.pop()])
        if current=="#":
            stack.append(len(stack.pop()))
        if current==":":
            if temp=="":
                stack.append(str(stack.pop()))
            else:
                stack.append(str(temp))
                temp=""
        #stack operations
        if current=="~":
            a=stack.pop()
            b=stack.pop()
            stack.append(a);stack.append(b)
        if current=="]":
            stack.pop()
        if current==")": #run string as code
            tokens=list(stack.pop())+tokens
        if current=="?":
            if stack.pop():
                tokens=list(stack.pop())+tokens
            else:stack.pop()
        if current=="(": #~opposite of toins (useful for looping, see repl)
            #equivalent to {\{}+{\}}~+
            stack.append("{"+str(stack.pop())+"}")
        if current=="[": #duplicate
            stack.append(stack[-1])
        if current=="_": #empty stack
            stack.append(len(stack)==0)
        #unsupported
        if current=="py": #run as python code (warning:probably exclusive to this interpreter)
            exec(stack.pop())
        if current=="interpreter": #interpreter data
            stack.append(options["reverse-add"])
            stack.append(options["fixed-print"])
            stack.append("Syms1.0.1.py Reference Interpreter") #make sure this line is different in your implementation
        #custom operations
        if current=="joinc": #equivalent to +
            stack.append(stack.pop()+" "+stack.pop())
    except SyntaxError:pass
if options["implicit-output"]:print(stack)
