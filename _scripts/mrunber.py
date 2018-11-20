import subprocess as commands
import time
import os
import sys
import numpy as np

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)
l=len(sys.argv)
outname=sys.argv[-1]
OUTNAME=outname+'.txt'
lOUTNAME='_OUTPUTS/'+outname+'-br.txt'
gpu_no=-1
try:
    bt=commands.check_output('ssh amit@bernie.uchicago.edu \'nvidia-smi -q --id=0 | grep Performance | cut -d: -f2 | cut -dP -f2\' ', shell=True)
    if (np.int32(bt)>=5):
       gpu_no=0
except:
    print('gpu 0 info failed')
if (gpu_no<0):
    try:
        bt=commands.check_output("ssh amit@bernie.uchicago.edu \'nvidia-smi -q --id=1 | grep Performance | cut -d: -f2 | cut -dP -f2\' ",shell=True)
        if (np.int32(bt) >= 5):
            gpu_no=1
    except:
        print('gpu 1 info failed')
print('gpu',gpu_no)
ss='/opt/anaconda/anaconda3/bin/python run_conv.py '+' '.join(sys.argv[1:l-1]) + ' ' + str(gpu_no) + ' >'+OUTNAME


if 'loc' in outname:
    os.system(ss)
else:
    f=open('runthingsBR.txt','w')
    f.write(ss+'\n')
    f.close()
    try:
        commands.check_output('rm ' + outname +'-br.txt', shell=True)
    except:
        print('Failed rm')
    try:
        commands.check_output('../Class/GIT.sh',shell=True)
    except:
        print('GIT failed')
    try:
        commands.check_output("ssh amit@bernie.uchicago.edu \'cd /ga/amit/Desktop/Dropbox/Python; git pull\' ",shell=True)
    except:
        print('pull failed')

    os.system("ssh amit@bernie.uchicago.edu \'cd /ga/amit/Desktop/Dropbox/Python/TF/; ./runthingsBR.txt \' & ")

    ny='no'
    while (ny != ''):
        time.sleep(10)
        try:
            #ss=commands.check_output('cp /Volumes/amit/Desktop/Dropbox/Python/TF/'+OUTNAME+' '+ lOUTNAME,shell=True)
            ss=commands.check_output('scp amit@aitken:Desktop/Dropbox/Python/TF/'+OUTNAME+' '+ lOUTNAME,shell=True)
            print(ss)
            ny=''
        except:
            ny='no'
            print('Initial copy fialed')
    done=False
    while (not done):
        time.sleep(10)
        try:
          ss=commands.check_output('grep DONE '+lOUTNAME,shell=True)
          print('Done grep',ss)
          if (ss!=''):
              done=True
        except:
            done=False
        try:
            #commands.check_output('scp /Volumes/amit/Desktop/Dropbox/Python/TF/'+OUTNAME+' ' + lOUTNAME,shell=True)
            ss=commands.check_output('scp amit@aitken:Desktop/Dropbox/Python/TF/'+OUTNAME+' '+ lOUTNAME,shell=True)
        except:
            print('copy failed')
    time.sleep(5)
    # pnn=commands.check_output('grep NNN ' + lOUTNAME)
    # pnnn=str.split(pnn,':')
    # netname=str.strip(pnnn[1],' ,\')')
    #
    # com='scp amit@bernie.uchicago.edu:/ga/amit/Desktop/Dropbox/Python/Class/'+netname+'.txt  _br/Amodels/.'
    #os.system(com)
    #manage_OUTPUT.print_OUTPUT(outname+'-br')

