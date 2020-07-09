# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 03:14:40 2020

@author: HP
"""
import os
import pickle

G=[["program","block"],
   ["block","{","decls","stmts","}"],
   ["decls","decls","decl"],["decls",""],
   ["decl","type","id",";"],
   ["type","type","[","num","]"],["type","basic"],
   ["stmts","stmts","stmt"],["stmts",""],
   ["stmt","loc","=","bool",";"],["stmt","if","(","bool",")","stmt"],["stmt","if","(","bool",")","stmt","else","stmt"],
   ["stmt","while","(","bool",")","stmt"],["stmt","do","stmt","while","(","bool",")",";"],["stmt","break",";"],
   ["stmt","block"],
   ["loc","loc","[","bool","]"],["loc","id"],
   ["bool","bool","||","join"],["bool","join"],
   ["join","join","&&","equality"],["join","equality"],
   ["equality","equality","==","rel"],["equality","!=","rel"],["equality","rel"],
   ["rel","expr","<","expr"],["rel","expr","<=","expr"],["rel","expr",">=","expr"],["rel","expr",">","expr"],["rel","expr"],
   ["expr","expr","+","term"],["expr","expr","-","term"],["expr","term"],
   ["term","term","*","unary"],["term","term","/","unary"],["term","unary"],
   ["unary","!","unary"],["unary","-","unary"],["unary","factor"],
   ["factor","(","bool",")"],["factor","loc"],["factor","num"],["factor","real"],["factor","true"],["factor","false"]]
unfinal=["program","block","decls","decl","type","stmts","stmt","loc","bool","join","equality","rel","expr","term",
         "unary","factor"]
final=["{","}","id","[","]","basic","if","(",")","else","while","do","break",";","&&","||","=","==","!=","<",">","<=",">=",
       "+","-","*","/","!","num","real","true","false"]
"""G=[["S'","S"],
   ["S","A","a"],["S","b","A","c"],["S","d","c"],["S","b","d","a"],
   ["A","d"]]
unfinal=["S'","S","A"]
final=["a","b","c","d"]"""
symbols=unfinal+final

def first(X=None):
    if X:
        f=set()
        global FIRST
        for item in X:
            f=f-{""}
            if item in unfinal:
                f=f.union(FIRST[item])
            else:
                f=f.union({item})
            if "" not in f:
                break
        return f
    else:  
        global G
        f={}
        for item in unfinal:
            f[item]=set()
        update=True
        while update:
            update=False
            for items in G:
                tmp=set()
                for item in items[1:]:
                    tmp=tmp-{""}
                    if item in unfinal:
                        tmp=tmp.union(f[item])
                    else:
                        tmp=tmp.union({item})
                    if "" not in tmp:
                        break
                if f[items[0]]!=f[items[0]].union(tmp):
                    f[items[0]]=f[items[0]].union(tmp)
                    update=True
        return f
                       
FIRST=first()
def closure(items):
    global G
    update=True
    while update:
        update=False
        tmp=set()
        for item in items:            
            pos=item[2]
            if pos==len(item[0]):
                continue
            sym=item[0][pos]
            fba=first(list(item[0][pos+1:]+(item[1],)))
            if sym in unfinal:
                i=0
                while i<len(G) and G[i][0]!=sym:
                    i+=1
                while i<len(G) and G[i][0]==sym:
                    for follow in fba:
                        tmp=tmp.union({(tuple(G[i]),follow,1)})
                    i+=1
        if items.union(tmp)!=items:
            update=True
            items=items.union(tmp)
    return items
                    
    
def goto(items,X):
    jtems=set()
    for item in items:
        pos=item[2]
        if pos==len(item[0]):
            continue
        sym=item[0][pos]
        if sym==X:
            jtems=jtems.union({(item[0],item[1],pos+1)})
    return closure(jtems)
    
def itemsofG():
    global G
    C=[closure({(tuple(G[0]),"$",1)})]
    update=True
    while update:
        update=False
        Ctmp=[]#每回合添加的项集列表
        for item in C:
            for sym in symbols:
                tmp=goto(item,sym)#集合
                if tmp and tmp not in C and tmp not in Ctmp:
                    Ctmp.append(tmp)
                    update=True
        C=C+Ctmp
    return C


def build():
    global ItemsOfG
    ptable={}
    for i,items in enumerate(ItemsOfG):#item为项集，集合，元素是项，元组
        ptable[i]={}
        for item in items:
            pos=item[2]
            if pos==len(item[0]) or item[0][1]=="":
                if item==(tuple(G[0]),"$",2):
                    ptable[i]["$"]="acc"
                else:
                    ptable[i][item[1]]=item[0]
            else:
               
                sym=item[0][pos]
                #print(items,sym,items in ItemsOfG)
                nxt=ItemsOfG.index(goto(items,sym))
                ptable[i][sym]=nxt
    return ptable

if os.path.exists("ptable.pickle") and os.path.exists("items.pickle"):
    with open("items.pickle","rb") as ipkl:
        ItemsOfG=pickle.load(ipkl)
        with open("ptable.pickle","rb") as ppkl:
            PTable=pickle.load(ppkl)
else:
    ItemsOfG=itemsofG()
    PTable=build()
"""-----------------------------------------Action-----------------------------------------------------------------"""
"""--------------------const------------------"""
_value=0
_nextlist=0
_type=0
_id=2
_name=0
_etype=1
_enxtls=2
_offset=3
_first=1
"""-------------------const end---------------"""
"""-------------------control var-------------"""
symtable=[None,{}]
tmpcnt=[None,0]
codeseq=[]
error=False
"""----------------control var end------------"""
def solvenum(product):
    return G.index(list(product))

def solvetoken(token):
    if len(token)==2:
        return (token[1],)
    elif token[0]=="true":
        return (1,)
    elif token[0]=="false":
        return (0,)
    else:
        return ()

def vtot(val):
    if type(val)==int:
        return "int"
    else:
        return "float"
  
def gentmp():
    global tmpcnt
    tmp="t"+str(tmpcnt[1])
    tmpcnt[1]+=1
    return tmp

def symappend(sym,etype):
    global symtable
    if sym not in symtable[1]:
        symtable[1][sym]=etype
    else:
        return "error"
    
def offset(etype):
    tmp=etype
    off=1
    
    while type(tmp)!=tuple:
        off*=tmp[0]
    return off

def getid(idname):
    symtmp=symtable
    while symtmp:
        if idname in symtmp[1]:
            return symtmp[1][idname]
        symtmp=symtmp[0]
    else:
        return "error"
    
def maxtype(t1,t2):
    if t1 not in ["int","float","char"] or t2 not in ["int","float","char"]:
        return "error"
    elif t1=="float" or t2=="float":
        return "float"
    elif t1=="int" or t2=="int":
        return "int"
    else:
        return "char"        
    
def modify_jmps(pos,shift):
    for i in range(len(codeseq)):
        if codeseq[i][0].startswith("j") and codeseq[i][3]!=None and codeseq[i][3]>=pos:
            tmpls=list(codeseq[i])
            tmpls[3]+=shift
            codeseq[i]=tuple(tmpls)
    
def Action(num,sstack,cstack,astack):
    global symtable,domain,tmpcnt,codeseq
    if num in [41,42,43,44]:
        value=astack[-1][_value]
        tmp=gentmp()
        etype=vtot(value)
        symappend(tmp,etype)
        codeseq.append(("=",value,None,tmp))
        codeseq.append(("jz",tmp,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,etype,[[len(codeseq)-2],[len(codeseq)-1]],len(codeseq)-3)
    
    elif num==40:
        loc1=astack[-1]
        codeseq.append(("jz",loc1[_value],None,None))
        codeseq.append(("jmp",None,None,None))
        return (loc1[_value],loc1[_etype],[[len(codeseq)-2],[len(codeseq)-1]],loc1[_offset])
    
    elif num==39:
        return astack[-2]
    
    elif num in [36,37]:
        u1=astack[-1]
        tmp=gentmp()
        symappend(tmp,"int" if num==36 else u1[_etype])
        codeseq.append(("minus" if num==37 else "not",u1[_value],None,tmp))
        codeseq.append(("jz",tmp,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,"int" if num==36 else u1[_etype],[[len(codeseq)-2],[len(codeseq)-1]],u1[_offset])
    
    elif num in [33,34]:
        t1=astack[-3]
        u1=astack[-1]
        tmp=gentmp()
        tmptype=maxtype(t1[_etype],u1[_etype])
        symappend(tmp,tmptype)
        codeseq.append(("*" if num==33 else "/",t1[_value],u1[_value],tmp))
        codeseq.append(("jz",tmp,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,tmptype,[[len(codeseq)-2],[len(codeseq)-1]],t1[_offset])
    
    elif num in [30,31]:
        e1=astack[-3]
        t1=astack[-1]
        tmp=gentmp()
        tmptype=maxtype(e1[_etype],t1[_etype])
        symappend(tmp,tmptype)
        codeseq.append(("+" if num==30 else "-",e1[_value],t1[_value],tmp))
        codeseq.append(("jz",tmp,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,tmptype,[[len(codeseq)-2],[len(codeseq)-1]],e1[_offset])
    
    elif num in [25,26,27,28]:
        opt=["jb","jna","ja","jnb"]
        e1=astack[-3]
        e2=astack[-1]
        tmp=gentmp()
        symappend(tmp,"int")
        codeseq.append((opt[num-25],e1[_value],e2[_value],len(codeseq)+2))
        codeseq.append(("=",0,None,tmp))
        codeseq.append(("jmp",None,None,len(codeseq)+2))
        codeseq.append(("=",1,None,tmp))
        codeseq.append(("jmp",None,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,"int",[[len(codeseq)-3],[len(codeseq)-1]],e1[_offset])
    
    elif num in [22,23]:
        opt=["je","jne"]
        equ1=astack[-3]
        r1=astack[-1]
        tmp=gentmp()
        symappend(tmp,"int")
        codeseq.append((opt[num-22],equ1[_value],r1[_value],len(codeseq)+2))
        codeseq.append(("=",0,None,tmp))
        codeseq.append(("jmp",None,None,len(codeseq)+2))
        codeseq.append(("=",1,None,tmp))
        codeseq.append(("jmp",None,None,None))
        codeseq.append(("jmp",None,None,None))
        return (tmp,"int",[[len(codeseq)-3],[len(codeseq)-1]],e1[_offset])
        
    elif num in [19,21,24,29,32,35,38]:
        return astack[-1]
    
    elif num==20:
        j1=astack[-3]
        e1=astack[-1]
        tmp=gentmp()
        symappend(tmp,"int")
        codeseq.append(("=",1,None,tmp))
        codeseq.append(("jmp",None,None,len(codeseq)+2))
        codeseq.append(("=",0,None,tmp))
        codeseq.append(("jmp",None,None,None))
        codeseq.append(("jmp",None,None,None))
        for i in j1[_enxtls][0]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-3
            codeseq[i]=tuple(ls)
        for i in j1[_enxtls][1]:
            ls=list(codeseq[i])
            ls[3]=e1[_offset]
            codeseq[i]=tuple(ls)
        for i in e1[_enxtls][0]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-3
            codeseq[i]=tuple(ls)
        for i in e1[_enxtls][1]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-5
            codeseq[i]=tuple(ls)
        return (tmp,"int",[[len(codeseq)-2],[len(codeseq)-1]],j1[_offset])
            
    elif num==18:
        b1=astack[-3]
        j1=astack[-1]
        tmp=gentmp()
        symappend(tmp,"int")
        codeseq.append(("=",1,None,tmp))
        codeseq.append(("jmp",None,None,len(codeseq)+2))
        codeseq.append(("=",0,None,tmp))
        codeseq.append(("jmp",None,None,None))
        codeseq.append(("jmp",None,None,None))
        for i in b1[_enxtls][0]:
            ls=list(codeseq[i])
            ls[3]=j1[_offset]
            codeseq[i]=tuple(ls)
        for i in b1[_enxtls][1]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-5
            codeseq[i]=tuple(ls)
        for i in j1[_enxtls][0]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-3
            codeseq[i]=tuple(ls)
        for i in j1[_enxtls][1]:
            ls=list(codeseq[i])
            ls[3]=len(codeseq)-5
            codeseq[i]=tuple(ls)
        return (tmp,"int",[[len(codeseq)-2],[len(codeseq)-1]],b1[_offset])
    
    elif num==17:
        idname=astack[-1][_name]
        etype=getid(idname)
        return (idname,etype,idname,len(codeseq))
    
    elif num==16:
        loc1=astack[-4]
        bool1=astack[-2]
        srcname=astack[-4][_value]
        idname=astack[-4][_id]
        etype=astack[-4][_etype]
        val=astack[-2][_value]
        tmp=gentmp()
        symappend(tmp,"int")
        tmpname=gentmp()
        symappend(tmpname,etype[1])
        codeseq.append(("*",val,offset(etype),tmp))
        codeseq.append(("[]",srcname,tmp,tmpname))
        if type(etype)==str:
            print("error")
            return ()
        return (tmpname,etype[1],idname,loc1[_offset])
    
    elif num==15:
        b1=astack[-1]
        return b1
    
    elif num==14:
        codeseq.append(("jmp",None,None,None))
        return ([[len(codeseq)-1],[len(codeseq)-1]],len(codeseq)-1)
    
    elif num==13:
        bool1=astack[-3]
        stmt1=astack[-6]
        ltrue=stmt1[_first]
        lfalse=len(codeseq)
        truelist=stmt1[_nextlist][1]+bool1[_enxtls][1]
        falselist=stmt1[_nextlist][0]+bool1[_enxtls][0]
        for i in truelist:
            tmpls=list(codeseq[i])
            tmpls[3]=ltrue
            codeseq[i]=tuple(tmpls)
        for i in falselist:
            tmpls=list(codeseq[i])
            tmpls[3]=lfalse
            codeseq[i]=tuple(tmpls)
        return ([[],[]],stmt1[_first])
            
    elif num==12:
        bool1=astack[-3]
        stmt1=astack[-1]
        codeseq.append(("jmp",None,None,bool1[_offset]))
        ltrue=stmt1[_first]
        lfalse=len(codeseq)
        truelist=stmt1[_nextlist][1]+bool1[_enxtls][1]
        falselist=stmt1[_nextlist][0]+bool1[_enxtls][0]
        for i in truelist:
            tmpls=list(codeseq[i])
            tmpls[3]=ltrue
            codeseq[i]=tuple(tmpls)
        for i in falselist:
            tmpls=list(codeseq[i])
            tmpls[3]=lfalse
            codeseq[i]=tuple(tmpls)
        return ([[],[]],bool1[_offset])
    
    elif num==11:
        stmt1=astack[-3]
        stmt2=astack[-1]
        bool1=astack[-5]
        ltrue=stmt1[_first]
        lfalse=stmt2[_first]+1
        lend=len(codeseq)+1
        codeseq.insert(stmt2[_first],("jmp",None,None,lend))
        modify_jmps(stmt2[_first],1)
        truelist=bool1[_enxtls][1]
        falselist=bool1[_enxtls][0]
        for i in truelist:
            tmpls=list(codeseq[i])
            tmpls[3]=ltrue
            codeseq[i]=tuple(tmpls)
        for i in falselist:
            tmpls=list(codeseq[i])
            tmpls[3]=lfalse
            codeseq[i]=tuple(tmpls)
        for i in stmt1[_nextlist][0]+stmt2[_nextlist][0]:
            tmpls=list(codeseq[i])
            tmpls[3]=lend
            codeseq[i]=tuple(tmpls)
        return ([[],[]],bool1[_offset])
        
    elif num==10:
        stmt1=astack[-1]
        bool1=astack[-3]
        ltrue=stmt1[_first]
        lfalse=len(codeseq)
        truelist=bool1[_enxtls][1]
        falselist=bool1[_enxtls][0]+stmt1[_nextlist][0]
        for i in truelist:
            tmpls=list(codeseq[i])
            tmpls[3]=ltrue
            codeseq[i]=tuple(tmpls)
        for i in falselist:
            tmpls=list(codeseq[i])
            tmpls[3]=lfalse
            codeseq[i]=tuple(tmpls)
        return ([[],[]],bool1[_offset])
    
    elif num==9:
        bool1=astack[-2]
        loc1=astack[-4]
        codeseq.append(("=",bool1[_value],None,loc1[_value]))
        return ([[],[]],bool1[_offset])
        
    elif num==8:
        return ([[],[]],-1)
    
    elif num==7:
        stmts1=astack[-2]
        stmt1=astack[-1]
        return ([stmts1[_nextlist][0]+stmt1[_nextlist][0],stmts1[_nextlist][1]+stmt1[_nextlist][1]],
                stmt1[_first] if stmts1[_first]==-1 else stmts1[_first])
    
    elif num==6:
        basic1=astack[-1]
        return basic1
    
    elif num==5:
        num1=astack[-2]
        t1=astack[-4]
        return ((num1[_value],t1[_type]),)
    
    elif num==4:
        id1=astack[-2]
        t1=astack[-3]
        symappend(id1[_name],t1[_type])
        return ()
    
    elif num in [2,3]:
        symtable=[symtable,{}]
        tmpcnt=[tmpcnt,0]
        return ()
        
    elif num==1:
        stmts1=astack[-2]
        symtable=symtable[0]
        symtable[1]={}
        tmpcnt=tmpcnt[0]
        tmpcnt[1]=0
        return stmts1
    
    else:
        return ()
       

"""-----------------------------------------Action end-------------------------------------------------------------"""
def Parser(src):
    global PTable
    src+=[[("$",)]]
    sstack=[0]
    cstack=[("$",)]
    astack=[()]
    for i,line in enumerate(src):
        j=0
        while j<len(line):
            top=sstack[-1]
            token=line[j][0]
            if token in PTable[top]:#合法
                if type(PTable[top][token])==type(""):#接受
                    print("acc")
                    return 
                elif type(PTable[top][token])==type(0):#移入
                    cstack.append(line[j])
                    astack.append(solvetoken(line[j]))
                    sstack.append(PTable[top][token])
                    j+=1
                else:#归约和错误
                    tokentmp=PTable[top][token][0]#tokentmp为归约到的非终结符号
                    isepl=PTable[top][token][1]
                    num=solvenum(PTable[top][token])
                    if not isepl:#归约为空
                        attr=Action(num,sstack,cstack,astack)
                        token=tokentmp
                        cstack.append(token)
                        astack.append(attr)
                        top=sstack[-1]
                        sstack.append(PTable[top][token])
                    elif tokentmp in PTable[sstack[-len(PTable[top][token])]]:#归约
                        attr=Action(num,sstack,cstack,astack)
                        for k in range(len(PTable[top][token])-1):
                            sstack.pop()
                            cstack.pop()
                            astack.pop()
                        token=tokentmp
                        cstack.append(token)
                        astack.append(attr)
                        top=sstack[-1]
                        sstack.append(PTable[top][token])
                    else:#错误
                        print("reduce error in line",i+1)
                        j+=1
                print("状态栈：",sstack,"符号栈：",cstack)
            else:
                print("syntax error in line",i+1)
                j+=1
                
if __name__=="__main__":
    with open("test.lex","r") as f:
        content=f.read()
        lines=content.split("\n")
        lines=[item.split("\t") for item in lines]
        linestmp=[]
        for i,line in enumerate(lines):
            linestmp.append([])
            for item in line:
                if item:
                    linestmp[i].append(eval(item))
        lines=linestmp
        Parser(lines)
        codeseq.append(("nop",None,None,None))
##-------------------code del------------------------##
##-----------------none code del---------------------##
        codewithlabel=[]
        for i,item in enumerate(codeseq):
            if item[0].startswith("j") and item[3]!=None:
                itmp=item[3]
                while codeseq[itmp][0].startswith("j") and codeseq[itmp][3]==None:
                    itmp+=1
                else:
                    item=(item[0],item[1],item[2],itmp)
            codewithlabel.append([i,item])
        deltable=set()
        for item in codewithlabel:
            code=item[1]
            if code[0].startswith("j") and code[3]==None:
                deltable.add(item[0])
        codetmp=[]
        for i,item in enumerate(codewithlabel):
            if i not in deltable:
                codetmp.append(item)
        maptable={}
        for i,item in enumerate(codetmp):
            maptable[item[0]]=i
        codeseq=[]
        for i,item in enumerate(codetmp):
            code=list(item[1])
            if code[0].startswith("j"):
                code[3]=maptable[code[3]]
            codeseq.append(tuple(code))
##--------------near goto code del-------------------##
        codewithlabel=[]
        for i,item in enumerate(codeseq):
            if item[0].startswith("j") and item[3]!=i+1:
                itmp=item[3]
                while codeseq[itmp][0].startswith("j") and codeseq[itmp][3]==itmp+1:
                    itmp+=1
                else:
                    item=(item[0],item[1],item[2],itmp)
            codewithlabel.append([i,item])
        deltable=set()
        for item in codewithlabel:
            code=item[1]
            if code[0].startswith("j") and code[3]==item[0]+1:
                deltable.add(item[0])
        codetmp=[]
        for i,item in enumerate(codewithlabel):
            if i not in deltable:
                codetmp.append(item)
        maptable={}
        for i,item in enumerate(codetmp):
            maptable[item[0]]=i
        codeseq=[]
        for i,item in enumerate(codetmp):
            code=list(item[1])
            if code[0].startswith("j"):
                code[3]=maptable[code[3]]
            codeseq.append([i,tuple(code)])
##------------------code del end---------------------##
    if not error:
        with open("test.ir","w") as f:
            codeseqstr=[]
            for item in codeseq:
                codeseqstr.append(str(item[0])+'\t'+str(item[1])+"\n")
            f.writelines(codeseqstr)
        
                
            
        
        
        
    
                
        
