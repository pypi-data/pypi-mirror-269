import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
import requests
import platform
import logging

from template_generator import binary

def ffmpegBinary(searchPath):        
    binaryFile = ""
    if sys.platform == "win32":
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "win", "ffmpeg.exe")
    elif sys.platform == "linux":
        machine = platform.machine().lower()
        if machine == "x86_64" or machine == "amd64":
            machine = "amd64"
        else:
            machine = "arm64"
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "linux", machine, "ffmpeg")
    elif sys.platform == "darwin":
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "darwin", "ffmpeg")
    
    if len(binaryFile) > 0 and sys.platform != "win32":
        cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            print(cmd.stdout.readline().rstrip().decode('utf-8'))
    return binaryFile

def realCommand(cmd):
    if sys.platform == "linux":
        return "./" + " ".join(cmd)
    if sys.platform == "darwin":
        return "./" + " ".join(cmd)
    else:
        return cmd
    
def videoInfo(file,searchPath):
    w = 0
    h = 0
    bitrate = 0
    fps = 0
    duration = 0

    ffmpeg = ffmpegBinary(searchPath)
    command = [ffmpeg,"-i",file]
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        str = ""
        if result.returncode == 0:
            str = result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            str = result.stderr.decode(encoding="utf8", errors="ignore")
        if str.find("yuv420p") > 0 and str.find("fps") > 0:
            s1 = str[str.find("yuv420p"):str.find("fps")+3].replace(' ', "")
            s1_split = s1.split(",")
            for s1_it in s1_split:
                s2 = s1_it
                if s2.find("[") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("(") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("x") > 0:
                    sizes = s2.split("x")
                    if len(sizes) > 1:
                        w = sizes[0]
                        h = sizes[1]
                if s2.find("kb/s") > 0:
                    bitrate = s2[0:s2.find("kb/s")]
                if s2.find("fps") > 0:
                    fps = s2[0:s2.find("fps")]
        if str.find("Duration:") > 0 and str.find(", start:") > 0:
            s2 = str[str.find("Duration:")+9:str.find(", start:")].replace(' ', "")
            s2_split = s2.split(":")
            if len(s2_split) > 2:
                hour = float(s2_split[0])
                min = float(s2_split[1])
                second  = float(s2_split[2])
                duration = hour*3600 + min*60 + second
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    return float(w),float(h),float(bitrate),float(fps),float(duration)

def process(args, searchPath):
    binary = ffmpegBinary(searchPath)
    command = [binary] + args
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            print(result.stdout.decode(encoding="utf8", errors="ignore"))
            return True
        # else:
        #     print("====================== ffmpeg error ======================")
        #     print(result.stderr.decode(encoding="utf8", errors="ignore"))
        #     print("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        print(e)
        print("======================      end      ======================")
    return False