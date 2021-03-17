# -*- coding: utf-8 -*-
import sys
import os
from bypy import ByPy

def run():
    bp = ByPy()
    bp.syncup(localdir=u'', remotedir=u'youtube/', deleteremote=False)

def dellocalfile():
    cpath =os.getcwd()
    localfs =[]
    for fn in os.listdir(cpath):
        if fn.find('.mp4')>0:
            localfs.append(fn)
    remotefs = getbdlist()
    if len(localfs)>0 and len(remotefs)>0:
        for f in localfs:
            if f in remotefs:
                fpath = os.path.join(cpath,f)
                os.remove(fpath)

def getbdlist():
    bp = ByPy() 
    f_handler= sys.stdout
    f=open('blist', 'w',encoding='utf-8') 
    sys.stdout=f 
    bp.list(u'youtube/','$t $f')  
    sys.stdout =f_handler 
    f.close()
    fs=[]
    with open('blist', 'r',encoding='utf-8') as rf:
         blist= rf.readlines()
         fs =[l[l.find('F ')+2:-1]for l in blist if l[:1]=='F']

    return fs
if __name__=="__main__":
    run()
