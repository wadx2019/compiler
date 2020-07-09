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
"""G=[["S'","S"],
   ["S","if","e","then","S"],["S","if","e","then","S","else","S"],["S","while","e","do","S"],["S","begin","L","end"],["S","s"],
   ["L","L",";","S"],["L","S"]]
unfinal=["S'","S","L"]
final=["if","then","else","e","s",";","while","begin","end","do"]"""
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

def solvenum(product):
    return G.index(list(product))

def Parser(src):
    global PTable
    src+=[[("$",)]]
    sstack=[0]
    cstack=[("$",)]
    cnt=0
    for i,line in enumerate(src):
        j=0
        while j<len(line):
            top=sstack[-1]
            token=line[j][0]
            if token in PTable[top]:
                if type(PTable[top][token])==type(""):
                    print("acc")
                    return 
                elif type(PTable[top][token])==type(0):
                    cstack.append(line[j])
                    sstack.append(PTable[top][token])
                    j+=1
                    cnt+=1
                    print("状态栈:",sstack,"符号栈:",cstack,"输入带位置:",cnt,"动作:移入")
                else:
                    tokentmp=PTable[top][token][0]#tokentmp为归约到的非终结符号
                    isepl=PTable[top][token][1]
                    num=solvenum(PTable[top][token])
                    if not isepl:
                        token=tokentmp
                        cstack.append(token)
                        top=sstack[-1]
                        sstack.append(PTable[top][token])
                        print("状态栈:",sstack,"符号栈:",cstack,"输入带位置:",cnt,"动作:归约r"+str(num))
                    elif tokentmp in PTable[sstack[-len(PTable[top][token])]]:
                        
                        for k in range(len(PTable[top][token])-1):
                            sstack.pop()
                            cstack.pop()
                        token=tokentmp
                        cstack.append(token)
                        top=sstack[-1]
                        sstack.append(PTable[top][token])
                        print("状态栈:",sstack,"符号栈:",cstack,"输入带位置:",cnt,"动作:归约r"+str(num))
                    else:
                        print("reduce error in line",i)
                        j+=1
                        cnt+=1
            else:
                print("syntax error in line",i)
                j+=1
                cnt+=1
                
        
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
        
        
        
    
                
        