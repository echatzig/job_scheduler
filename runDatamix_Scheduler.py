import sys
import os, subprocess
import random
import datetime

import win32api
import win32event
import win32process
import ctypes




batchsize=10






batches = [


"Datamix.py XYZ        201 A        55 30 31 32 96 97 98  186 187 188 189     ftp.host.com      /GWG     user   pass      XYZ_R0      XYZ_R1      XYZ_R2      XYZ_R3    XYZ_R4      XYZ_R5     XYZ_R6  XYZ_R7  XYZ_R8  XYZ_R9  XYZ_R10    DatamixExportV2.exe",
"Datamix.py XYZ        201 IQ       55 30 31 32 96 97 98  186 187 188 189     ftp.host.com      /GWG     user   pass      XYZ_R0      XYZ_R1      XYZ_R2      XYZ_R3    XYZ_R4      XYZ_R5     XYZ_R6  XYZ_R7  XYZ_R8  XYZ_R9  XYZ_R10    DatamixExportV2.exe",



]


#cmd = "c:/perl/bin/perl.exe"
cmd = "c:/python34/python.exe"

ps = {}
index = 0
completed = {}
ibatches = iter(batches)
SYNCHRONIZE=0x00100000

dt = datetime.datetime.now()
log_filename = "logs/DM_Sche_" + dt.strftime("%Y-%m-%d") + ".log"
log = open(log_filename,"a", encoding="utf-8")

def trace(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M  ")
    
    log.write(timestamp)
    log.write(msg + "\n")
    log.flush()

    print(timestamp + msg + "\n")



trace("Starting Datamix_Scheduler")


for item in range(batchsize):
    batch = next( ibatches, None )
    if (batch==None):
        break
    #print(batch.split())

    p = subprocess.Popen([cmd] + batch.split(), shell=False) 
    h = ctypes.windll.kernel32.OpenProcess( SYNCHRONIZE, False, p.pid )
    ps[h] = { "pid": p.pid, "batch": batch }

    trace("statring pid: %6d batch: %s" % ( p.pid, batch ) )

while ps:
    print("Waiting for %d processes..." % len(ps))

    arrtype = ctypes.c_long * len(ps)
    _handles = arrtype( *ps.keys() )

    index = win32event.WaitForMultipleObjects( _handles, False, win32event.INFINITE )
    if (index==-1):
       err = ctypes.windll.kernel32.GetLastError()
       raise Err("WaitForMultipleObjects: %s" % win32api.FormatMessage(err))       
    h = _handles[index]
    exit = ctypes.windll.kernel32.GetExitCodeProcess( h )
    ctypes.windll.kernel32.CloseHandle(h)
    print("Process %d done with exit code %d" % (ps[h]["pid"],exit) )

    trace("completed pid: %6d batch: %s" % (ps[h]["pid"], ps[h]["batch"]) )

    del ps[h]

    batch = next( ibatches, None )
    if (batch!=None):
        #print(batch.split())

        p = subprocess.Popen([cmd] + batch.split(), shell=False) 
        h = ctypes.windll.kernel32.OpenProcess( SYNCHRONIZE, False, p.pid )
        ps[h] = { "pid": p.pid, "batch": batch }

        trace("statring pid: %6d batch: %s" % (p.pid,batch) )
