#!/usr/bin/python

#PBS -A @project@
#PBS -N mom-job
#PBS -l select=@select@
#PBS -l walltime=00:@walltime@:00

import sys,os,getopt
import socket,subprocess
from subprocess import *

HOST = '@server@'
PORT = '@port@'

#os.system("export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR")
#os.chdir(os.environ["PBS_O_WORKDIR"])
#os.chdir("/work/e290/e290/antonst")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(( HOST, int(PORT) ))

task = ""
while (str(task) != 'STOP'):
    s.sendall('SEND')
    task = s.recv(1024)
    print 'client received: ', repr(task)
    task_str = str(task)
    if (str(task) == 'STOP'):
        s.close()
    elif (str(task) == 'WAIT'):
        print "waiting..."
    else:
        (out, err) = subprocess.Popen([task_str], stdout=subprocess.PIPE, shell=True).communicate()


