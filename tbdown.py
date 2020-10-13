# -*- coding: utf-8 -*-
import os
import time
import datetime
import requests
import threading 
import traceback 
import sys
import getopt 
from os import listdir
from os.path import isfile, join
from urllib import parse
from pytube import YouTube
from flask_sqlalchemy import SQLAlchemy


def down(connection,tube):
    #result = connection.execute("select * from tube")
    #for row in result:
    #    print("id:", row['id'])
    hpre = 'https://www.youtube.com/'   
    ds = tube.LinkHRef
    yn = ""
    dpath = os.path.join(os.path.abspath(os.getcwd()),'videos')
    try:
        if not os.path.exists(dpath):
            os.makedirs(dpath)
        url = parse.urlparse(ds)
        if url.netloc == "youtu.be":
            wv = url.scheme + "://" + url.netloc + url.path
            yt = YouTube(wv)
            if not yt:
                tube.DownMsg = "Not YT"
            yn = yt.streams.first().default_filename 
            yn= str(yn).replace('?','').replace('--','').replace('*','').replace("'",'')
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()[1].download(output_path=dpath, filename=yn)            
            os.rename(os.path.join(dpath,yn.replace('.mp4','mp4.mp4')),os.path.join(dpath,yn))
            print("downcomplete:" + yn)
            tube.DownStatus = 1        


        elif len(ds) > 10 and str(ds).index(hpre) == 0: 
            qps = dict(parse.parse_qsl(parse.urlsplit(ds).query))
            wv = hpre + "watch?v=" + qps.get("v")
            yt = YouTube(wv)
            if not yt:
                tube.DownMsg = "Not YT"
            yn = yt.streams.first().default_filename 
            yn= str(yn).replace('?','').replace('--','').replace('*','').replace("'",'')
            yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()[1].download(output_path=dpath, filename=yn)
            os.rename(os.path.join(dpath,yn.replace('.mp4','mp4.mp4')),os.path.join(dpath,yn))
            print("downcomplete:" + yn)
            tube.DownStatus = 1      
           
        usl = "update tube set Title='" + yn + "',DownStatus=1,DownMsg='" + str(tube.DownMsg) + "' where id= %d" % tube.id
        connection.execute(usl)
        
    except:
        print("down error  ") 
        tube.DownMsg = "Address Not Valid"
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        #time.sleep(33)


def delete(connection,tube):
    if not tube.Title:
        print(" no exists title  ") 
        return
    dpath = os.path.join(os.path.abspath(os.getcwd()),'videos')
    try:
        bflag =False;
        filename =os.path.join(dpath, tube.Title)
        if isfile(filename):
            bflag=True
            os.remove(filename)
        if bflag:
            print('file removed!' +filename)
        else:
            print('File Not Exists!' + filename)
    except:
        print("delete error  ") 
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
