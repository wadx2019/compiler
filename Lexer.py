# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 01:17:27 2020

@author: HP
"""

Key_word=["if","else","while","do","break","true","false"]
Type=["int","char","bool","float"]
Logical=["true","false"]
Split=["\t"," ","\n"]

def Lexer(src):
    obj=[]
    for line in src:
        out=[]
        i=0
        while i<len(line):
            i,token=scan(i,line)
            if i!=len(line)+1:
                out.append(token)
        obj.append(out)
    return obj

def scan(i,line):
    while i<len(line):
        if line[i] in Split:
            i+=1
            continue
        else:
            break
    if i==len(line):
        return i+1,("",)
    if line[i]=='&':
        if readch(i+1,line,'&'):
            return i+2,("&&",)
        else:
            return i+1,("&",)
    elif line[i]=='|':
        if readch(i+1,line,"|"):
            return i+2,("||",)
        else:
            return i+1,('|',)
    elif line[i]=='=':
        if readch(i+1,line,"="):
            return i+2,("==",)
        else:
            return i+1,('=',)
    elif line[i]=='>':
        if readch(i+1,line,"="):
            return i+2,(">=",)
        else:
            return i+1,('>',)
    elif line[i]=='<':
        if readch(i+1,line,"="):
            return i+2,("<=",)
        else:
            return i+1,('<',)
    elif line[i]=='!':
        if readch(i+1,line,"="):
            return i+2,("!=",)
        else:
            return i+1,('!',)
    elif getch(i,line) and getch(i,line).isdigit():
        v=0
        while getch(i,line) and getch(i,line).isdigit():
            v=10*v+int(getch(i,line))
            i+=1
        if getch(i,line) and readch(i,line,'.'):
            d=0.1
            i+=1
            while getch(i,line) and getch(i,line).isdigit():
                v+=d*int(getch(i,line))
                i+=1
                d*=0.1
            return i,("real",v)
        else:
            return i,("num",v)
    elif getch(i,line) and (getch(i,line).isalpha() or getch(i,line)=='_') :
        tmp=""
        tmp+=getch(i,line)
        i+=1
        while getch(i,line) and (getch(i,line).isalnum() or getch(i,line)=='_'):
            tmp+=getch(i,line)
            i+=1
        if tmp in Key_word+Logical:
            return i,(tmp,)
        elif tmp in Type:
            return i,("basic",tmp)
        else:
            return i,("id",tmp)
    else:
        return i+1,(line[i],)        
        
def readch(i,line,ch):
    if i<len(line) and line[i]==ch:
        return True
    else:
        return False

def getch(i,line):
    if i<len(line):
        return line[i]
    else:
        return False
if __name__=="__main__":
    with open("test.txt","r") as f:
        src=f.readlines()
        obj=Lexer(src)
        for items in obj:
            for item in items:
                print(item,end="\t")
            print()