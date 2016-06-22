import re,sys,os
import subprocess
import time



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

# run command and capture output
def getoutput(cmd, args=None):
    if args==None:
       args=[]
    ps = subprocess.Popen( [cmd, args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    output = ps.communicate()[0]
    return (str(output), ps.returncode)

# exteract
def extractText(text, regStr):
    p = re.compile(regStr)
    reg = p.search(text)
    if reg == None:
       return ('', False)
    txt = reg.group(1)
    return (txt, True)

if len(sys.argv) != 10:
    exit("usage: spawner.py ...8 params...")

server       = sys.argv[ 1]
datamixapp   = sys.argv[ 2]
id           = sys.argv[ 3]
CountryCode  = sys.argv[ 4]
AgentID      = sys.argv[ 5]
exportDate   = sys.argv[ 6]
AgentName    = sys.argv[ 7]
date         = sys.argv[ 8]
path         = sys.argv[ 9]

args = "\\\\" + server + " -n 10 -w D:\\Tasks D:\\Data\\DatamixV2\\" + \
       datamixapp + " " + id + " " + CountryCode + " " + AgentID + " " + \
       exportDate + " NOTFILE"


for retries in range(5):
    print("    spawner.py is running(" + str(retries) + ") :" + args)
    (strout, exitcode) = getoutput('D:\setup\PsTools\psexec.exe', [args])
    if int(exitcode) == 0:
        time.sleep(5)

        file = getnewestfile(path) 
        if file == None:
            print("   spawner.py:: " + args + " No files in folder : " + path )
        else:
            break

    else:
        print("   spawner.py: " + args + " returned BAD errorcode: " + exitcode)

        
        
        
        
#   (pid, success) = extractText(strout, r'with process ID (.*)\.')
#   if not success:
#      print("spawner.py : FAILURE")
#      print(strout)
#      time.sleep(2)
#      print("spawner.py : running again: " + args )
#   else:
#      break




# 
# args = "\\\\" + server + " " + pid
# 
# while True:
#     (strout, exitcode) = getoutput('D:\setup\PsTools\pslist.exe', [args])
#     if int(exitcode)==0: 
#        #still running - sleep
#        time.sleep(2)
#     else:
#        break
#        
# print("spawner.py has completed running :" + args)
