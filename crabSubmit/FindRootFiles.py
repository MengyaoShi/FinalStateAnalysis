import subprocess
import sys
import fileinput
import os
import re
def getFileList(inDir, inputName):
    tempfile = open('tmpFile.txt','w')
    cmd_all='find ' + inDir + ' -maxdepth 2 -mindepth 2 -name *rawSkimTau' 
    print cmd_all
    process_all=subprocess.Popen(cmd_all.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tempfile.write(process_all.communicate()[0])
    tempfile.close()
    outDirList=[]
    with open('tmpFile.txt','r') as readfile:
        outDirList=[line.rstrip() for line in readfile]
    readfile.close()
    #os.remove('tmpFile.txt')
    JobList=[]
    for Dir in outDirList:
        print Dir
        result=Dir.split('/')[9]
        print result
        fileName='./AllRootFiles/SUB/'+result+'.txt'
        getFileInOneFolderList(Dir, fileName)
        
def getFileInOneFolderList(inDir, inputName):
    tempfile = open(inputName,'w')
    cmd = 'find ' + inDir + ' -mindepth 3 -maxdepth 3'+' -name *zmutauskim*.root'
    print cmd
    process = subprocess.Popen(cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tempfile.write(process.communicate()[0])
    tempfile.close()
    for line in fileinput.input([inputName], inplace=True):
        sys.stdout.write('{l}'.format(l=line[8:]))


inputName_='testscript.txt'
inDir_='/eos/cms/store/group/phys_higgs/HiggsExo/mshi'
#inDir_= '/eos/cms/store/user/mshi'
getFileList(inDir_,inputName_)

