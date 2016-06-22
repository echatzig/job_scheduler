#
# sample params:
#
# TROPO              265 OM      53 38 39 40 90 91 92  182 183 184 185      ftp.opd.xres.de     /GWG     MPIO   ZaiWifIgFi     Activate_R0      Activate_R1      Activate_R2      Activate_R3        Activate_R4        Activate_R5        Activate_R6      Activate_R7  Activate_R8  Activate_R9  Activate_R10    DatamixExportV2.exe
#
#



import sys
import os, subprocess
import random
import datetime

import win32api
import win32event
import win32process
import ctypes


SYNCHRONIZE=0x00100000


# ----


def append( src, dst ):
    #print("append(dst: $dst)");
    if not os.path.isfile(src):
        print("copy:: file: " + src + " missing")

    out = open(dst,"a", encoding="utf-8")
    inp  = open(src, encoding="utf-8")
    
    # skip header line
    headers = inp.readline()
    
    #read the rest
    for ln in inp:
       out.write(ln)

# ----


def append_and_backup( src, dst ):
    append( src, dst )
    
    # os.makedirs( os.path.dirname(src) + "/bak/", exist_ok=True )

    #foreach $file (@files) {
    #    move( $file , dirname($file) . "/bak/" . basename($file));
    #}    

# ----
def copy( src, dst ):
    #print("append(dst: $dst)");
    if not os.path.isfile(src):
        print("copy:: file: " + src + " missing")

    out = open(dst,"w", encoding="utf-8")
    inp  = open(src, encoding="utf-8")
    
    #read the rest
    for ln in inp:
       out.write(ln)

# --

def copy_and_backup( src, dst ):
    copy( src, dst )

# ----
def getnewestfile(folder):
    newtime = sys.float_info.min
    newfile = None

    # check if the folder exists - to avoid getting an exception from os.path.isdir
    if not os.path.isdir(folder):
        return None

    for file in os.listdir(folder):
       if os.path.isdir(folder+file):
           continue
       atime = os.path.getatime(folder + file)
       if (atime>newtime):
           newtime=atime
           newfile=folder+file
           
    return newfile
# ----    

# ------------------
def run(data):
    #folder = data["folder"]
    #path= '//{server}/d$/MasterDataExport/DatamixV2/{folder}/{CountryCode}/' % (data["server"],folder,CountryCode)

    #cmd  = "c:\\windows\\system32\\cmd.exe"
    #args = "/c d:\\setup\\PsTools\\psexec.exe \\\\" + server + " -w D:\\Tasks D:\\Data\\DatamixV2\\" + \
    #       datamixapp + " " + data["id"] + " " + CountryCode + " " + AgentID + \
    #       exportDate + " NOTFILE > logs\\" + data["server"] + "-" + AgentName + "-" + CountryCode + "-" + \
    #       date + ".LOG"
    cmd = "c:\python34\python.exe"
    args = "spawner.py " + server + " " + datamixapp + " " + data["id"] + " " + CountryCode + " " + AgentID + " " + exportDate + " " + AgentName + " " + date

    print(args)   
    p = subprocess.Popen([cmd] + args.split(), shell=False) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) #, cwd = r'd:\Tasks'])
    return p

# ----------------

if len(sys.argv) != 31:
    exit("usage: DataMix.py ...29 params...")


AgentName   = sys.argv[ 1]   # TROPO
AgentID     = sys.argv[ 2]   # 265
CountryCode = sys.argv[ 3]   # A
ID1         = sys.argv[ 4]   # 53
ID2         = sys.argv[ 5]   # 38
ID3         = sys.argv[ 6]   # 39
ID4         = sys.argv[ 7]   # 40
ID5         = sys.argv[ 8]   # 90
ID6         = sys.argv[ 9]   # 91
ID7         = sys.argv[10]   # 92
ID8         = sys.argv[11]   # 182
ID9         = sys.argv[12]   # 183
ID10        = sys.argv[13]   # 184
ID11        = sys.argv[14]   # 185
ftpsrv      = sys.argv[15]   # data01.opd.xres.de
ftpdir      = sys.argv[16]   # /GWG
username    = sys.argv[17]   # MPIO
password    = sys.argv[18]   # ZaiWifIgFi
firm1       = sys.argv[19]   # Activate_R0
firm2       = sys.argv[20]   # Activate_R1
firm3       = sys.argv[21]   # Acrivate_R2
firm4       = sys.argv[22]   # Activate_R3
firm5       = sys.argv[23]   # Activate_R4
firm6       = sys.argv[24]   # Acrivate_R5
firm7       = sys.argv[25]   # Activate_R6
firm8       = sys.argv[26]   # Activate_R3
firm9       = sys.argv[27]   # Activate_R4
firm10      = sys.argv[28]   # Acrivate_R5
firm11      = sys.argv[29]   # Activate_R6
datamixapp  = sys.argv[30]   # DatamixExportV2.exe



dt = datetime.datetime.now()
exportDate = dt.strftime("%Y-%m-%d")
date = dt.strftime("%Y%m%d")


# runcodes = ["sleep10.py", "sleep.py"]
# ps = {}
# for script in runcodes:
#     args = script
#     p = subprocess.Popen(["python", args])
#     ps[p.pid] = p
# print("Waiting for %d processes..." % len(ps))
# while ps:
#     pid, status = os.wait()
#     if pid in ps:
#         del ps[pid]
#         print("Waiting for %d processes..." % len(ps))
# 




hSem = win32event.CreateSemaphore (None, 1, 1,"Datamix_{AgentName}_{CountryCode}".format(**locals()))
rt=win32event.WaitForSingleObject (hSem, 0)
if rt == win32event.WAIT_TIMEOUT:
    print("application already running: {AgentName}-{CountryCode}".format(**locals()))
    sys.exit(1)


servers = [
    'FTI-AMS01-GWG36',
    'FTI-AMS01-GWG15',
    'FTI-AMS01-GWG16',
    'FTI-AMS01-GWG17',
    'FTI-AMS01-GWG22',
    'FTI-AMS01-GWG24',
    'FTI-AMS01-GWG25',
    'FTI-AMS01-GWG26',
    'FTI-AMS01-GWG27',
    'FTI-AMS01-GWG28',
    'FTI-AMS01-GWG29',
]

workload = [
    { 'id': ID1 ,  'folder': firm1  },
    { 'id': ID2 ,  'folder': firm2  },
    { 'id': ID3 ,  'folder': firm3  },
    { 'id': ID4 ,  'folder': firm4  },
    { 'id': ID5 ,  'folder': firm5  },
    { 'id': ID6 ,  'folder': firm6  },
    { 'id': ID7 ,  'folder': firm7  },
    { 'id': ID8 ,  'folder': firm8  },
    { 'id': ID9 ,  'folder': firm9  },
    { 'id': ID10,  'folder': firm10 },
    { 'id': ID11,  'folder': firm11 },
]


### suffle server list to simulate a round-robin load balancing algorithm
random.shuffle(servers)

#print servers

#    "c:\\windows\\system32\\cmd.exe",
#    "/c d:\\setup\\PsTools\\psexec.exe \\\\FTI-AMS01-GWG29 -w D:\\Tasks D:\\Data\\DatamixV2\\".$datamixapp." $ID11 $CountryCode $AgentID $exportDate NOTFILE > logs\\GWG29-".$AgentName."-".$CountryCode."-".$date.".LOG",
#    0, NORMAL_PRIORITY_CLASS, "D:\\Tasks") || die ErrorReport();

#    "c:\\windows\\system32\\cmd.exe",
#    "/c d:\\setup\\PsTools\\psexec.exe \\\\FTI-AMS01-GWG29 -w D:\\Tasks D:\\Data\\DatamixV2\\".$datamixapp." $ID11 $CountryCode $AgentID $exportDate NOTFILE > logs\\GWG29-".$AgentName."-".$CountryCode."-".$date.".LOG",



# subprocess.Popen( [r'd:\setup\PsTools\psexec.exe', 
#                     \\\\FTI-AMS01-GWG29 -w D:\\Tasks D:\\Data\\DatamixV2\\".$datamixapp." $ID11 $CountryCode $AgentID $exportDate NOTFILE > logs\\GWG29-".$AgentName."-".$CountryCode."-".$date.".LOG",
#cwd=r'd:\Tasks')

ps = {}
index = 0
completed = {}
for (server,data) in zip(servers,workload):
    
    # "//{server}/d$/MasterDataExport/DatamixV2/{data["folder"]}/{CountryCode}",
    folder = data["folder"]
    path= '//{server}/d$/MasterDataExport/DatamixV2/{folder}/{CountryCode}/'.format(**locals())

    #cmd  = "c:\\windows\\system32\\cmd.exe"
    #args = "/c d:\\setup\\PsTools\\psexec.exe \\\\" + server + " -w D:\\Tasks D:\\Data\\DatamixV2\\" + \
    #       datamixapp + " " + data["id"] + " " + CountryCode + " " + AgentID + " " + \
    #       exportDate + " NOTFILE > logs\\" + server + "-" + AgentName + "-" + CountryCode + "-" + \
    #       date + ".LOG"
    #
    cmd = "c:\python34\python.exe"
    args = "spawner.py " + server + " " + datamixapp + " " + data["id"] + " " + CountryCode + " " + AgentID + " " + exportDate + " " + AgentName + " " + date + " " + path

    print(args)   
    p = subprocess.Popen([cmd] + args.split(), shell=False ) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) # , cwd = r'd:\Tasks'])
    h = ctypes.windll.kernel32.OpenProcess( SYNCHRONIZE, False, p.pid )

    ps[h] = { "pid": p.pid, "server": server, "folder": path, "id": data["id"], "index": index }
    index = index + 1
    
    print(ps[h])

while ps:
    print("  datamix.py:: Waiting for %d processes..." % len(ps))

    arrtype = ctypes.c_long * len(ps)
    _handles = arrtype( *ps.keys() )
    #print(_handles)
    index = win32event.WaitForMultipleObjects( _handles, False, win32event.INFINITE )
    if (index==-1):
       err = ctypes.windll.kernel32.GetLastError()
       raise Err("WaitForMultipleObjects: %s" % win32api.FormatMessage(err))       
    h = _handles[index]
    exit = ctypes.windll.kernel32.GetExitCodeProcess( h )
    ctypes.windll.kernel32.CloseHandle(h)
    print("Process %d done with exit code %d" % (ps[h]["pid"],exit) )

    rundata = ps[h]
    del ps[h]

    folder = rundata["folder"]
    file = getnewestfile(folder) 
    completed[ rundata["index"] ] = file

    #if file == None:
    #    print("   datamix.py:: No files in folder - retrying: " + rundata["server"] )
    #    p = run(rundata)
    #    h = ctypes.windll.kernel32.OpenProcess( SYNCHRONIZE, False, p.pid )
    #    ps[h] = { "pid": p.pid, "server": rundata["server"], "folder": rundata["folder"], "id": rundata["id"], "index": rundata["index"] }
    #else:
    #    print("   datamix.py:: success: " + rundata["server"])

    print("  datamix.py:: success: " + rundata["server"])

#-- now just merge the parts into one
outdir = "Datamix/{AgentName}/{CountryCode}".format(**locals())
os.makedirs(outdir, exist_ok=True);

outfile = outdir + "/Datamix_Export_2_0_{date}.csv".format(**locals())

index = 0
for key in sorted(completed.keys()):
    print(completed[key])
    if (index==0):
       copy_and_backup( completed[key], outfile )
    else:
       append_and_backup( completed[key], outfile )
    index = index + 1

#-- ftp the result


upload_ftp = '''\
{username}
{password}

prompt
bin

mkdir  {ftpdir}
cd  {ftpdir}
mkdir  {CountryCode}
cd  {CountryCode}


put Datamix/{AgentName}/{CountryCode}/Datamix_Export_2_0_{date}.csv

quit
'''.format(**locals())

filename = "upload_" + AgentName + "_" + CountryCode + ".ftp";

ftp = open( filename, "w", encoding="utf-8" )
ftp.write(upload_ftp)
ftp.close()

print("FTP command: ftp -s:$filename $ftpsrv\n");
os.system("ftp -s:{filename} {ftpsrv}".format(**locals()));
