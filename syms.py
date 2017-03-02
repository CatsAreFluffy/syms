#SYMbolSctak 1.2
from __future__ import print_function #required for compatibility with python 2.x
#parse=input("Program:");
parse='''
1;2:" 2;~[[:={2:~(~}~?[["=={2:~[{{"}~}~?![{{'}~}~?]~}~?[2:=!{[:{;}~+~}~?]~{~[[:={2:~(~}~?[["=={2:~[{{"}~}~?![{{'}~}~?]~}~?[2:=!{[:{;}~+~}~?]+}~:{;}~+~+)2;~-[0;=!{{~[[:={2:~(~}~?[["=={2:~[{{"}~}~?![{{'}~}~?]~}~?[2:=!{[:{;}~+~}~?]+}~:{;}~+~+)1;~-[0;=!}{[(+~[(~++~?}[(+~[(~++~?]~{)}~[[:={2:~(~}~?[["=={2:~[{{"}~}~?![{{'}~}~?]~}~?[2:=!{[:{;}~+~}~?]~+)
'''.strip("\n") #this is your syms program
tokens=list(parse)
extensions=[]
try:
    eval('print "m"')
    v=2
except SyntaxError:v=3
try:
    import extension1
    extensions.append("extension1")
except ImportError:pass
stack=[]
parsemode=0 #0 for normal, 1 for string ##unused
parselevel=0 # # of nested {}s
temp=""
pvars=dict()
options={"reverse-math":False,"debug-messages":False,"full-debug":False,"implicit-output":True,"fixed-print":False}
try:
    unicode("")
except NameError:
    def unicode(x):return x #more compatitbility stuff
def modprint(x):
    x=str(x)
    if options["fixed-print"]:
        if len(x)>0 and x[0]==" ":
            x=x[1:]
    print(x)
def modinput(x):
    x=str(x)
    if options["fixed-print"]:
        if len(x)>0 and x[0]==" ":
            x=x[1:]
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
            print("Cycle");print("".join(tokens));print(stack)
            if options["full-debug"]: 
                print(temp);print(parselevel+parsemode)
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
