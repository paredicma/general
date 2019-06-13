################## DISCO ( DISC SIZE CONTROLLER ) ###########
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com
## Version			: 0.1
## Date				: 11.02.2019
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
import os
import commands
import glob
from time import *
from string import *
##################DIRECTORY INFO################################
#1 - target directory info 			-> True/False delete Anyway( Even cannot move remote site), target dir and file extension
#2 - diskUsedPercBaseDelete policy 	-> True/False( Policy Active-inactive ) , Disc usage percentage limit
#3 - timeBaseDelete policy  		-> True/False( Policy Active-inactive ) , File age limit
#4 - remoteBackupLocation 			-> True/False( Copy file before delete ) , ssh server ip, remote backup dir.
#dirList.append([[True/False(Force Delete),'directory','extension'],[True/False,Percentage(80,90 vb.)],[True/False,hour],[True/False,'remoteServer','remoteDir']])
dirList= []
dirList.append([[True,'/tmp/test1/','.log'],[True,30],[True,48],[True,'10.10.10.215','/tmp/test/']])
dirList.append([[False,'/tmp/test2/','.tar.gz'],[True,25],[True,1],[True,'172.21.162.215','/tmp/test/']])
##################PARAMETERS################################
writeLogFile=True
logFile='/tmp/disco.log'
sshUser='admin'
##################PARAMETERS################################
def diskUPDeleter(isForce,targetDir,targetExt,targetPerc,willMove,remoteServer,remoteLocation):
	list_of_files = glob.glob(targetDir+'*'+targetExt)
	for myfile in list_of_files:
		if(diskSizePercGetter(targetDir)>targetPerc):
			if(willMove):
				if(sshFileMover(isForce,myfile,remoteServer,remoteLocation)):
					if(os.path.exists(myfile)):
						os.remove(myfile)
						logWrite(logFile,' !!!! INFO !!!::  diskUPDeleter :: File was deleted because of disk usage percentage -> '+str(diskSizePercGetter(targetDir))+' \n File name : '+str(myfile))
					else:
						logWrite(logFile,' !!!! WARNING !!!::  diskUPDeleter :: File not Found : '+str(myfile))	
			else:
				if(os.path.exists(myfile)):
					os.remove(myfile)
					logWrite(logFile,' !!!! INFO !!!::  diskUPDeleter :: File was deleted because of disk usage percentage -> '+str(diskSizePercGetter(targetDir))+' \n File name : '+str(myfile))
				else:
					logWrite(logFile,' !!!! WARNING !!!::  diskUPDeleter :: File not Found : '+str(myfile))						
#	list_of_files.sort(key=os.path.getctime)
def diskTimeDeleter(isForce,targetDir,targetExt,targetTime,willMove,remoteServer,remoteLocation):
	list_of_files = glob.glob(targetDir+'*'+targetExt)
	for myfile in list_of_files:
		if(fileDeletebyTime(myfile,targetTime)):
			if(willMove):
				if(sshFileMover(isForce,myfile,remoteServer,remoteLocation)):
					if(os.path.exists(myfile)):
						os.remove(myfile)
						logWrite(logFile,' !!!! INFO !!!::  diskTimeDeleter :: File was deleted because of file age -> '+str(targetTime)+' hour \n File name : '+str(myfile))
					else:
						logWrite(logFile,' !!!! WARNING !!!::  diskTimeDeleter :: File not Found : '+str(myfile))	
			else:
				if(os.path.exists(myfile)):
					os.remove(myfile)
					logWrite(logFile,' !!!! INFO !!!::  diskTimeDeleter :: File was deleted because of disk usage percentage -> '+str(diskSizePercGetter(targetDir))+' \n File name : '+str(myfile))
				else:
					logWrite(logFile,' !!!! WARNING !!!::  diskTimeDeleter :: File not Found : '+str(myfile))						
def sshFileMover(isForce,fileName,moveServer,moveLocation):
	moveResult=os.system('scp -o ConnectTimeout=5  '+fileName+' '+sshUser+'@'+moveServer+':'+moveLocation)
	if(moveResult==0):
		return True
	else:
		if(isForce):
			return True
		else:
			return False	
def fileDeletebyTime(fileName,targetTime):
	fileCreTime=os.path.getmtime(fileName)
	curTime = time()
	if((curTime - (60*60*targetTime))>fileCreTime):
		return True		
	else:
		return False
def diskSizePercGetter(dirName):
	cmdStatus,cmdResponse = commands.getstatusoutput("df -P "+dirName+" | awk 'END{print $5}'")
	discPerc=cmdResponse[:cmdResponse.find('%')]
	if (discPerc.isdigit() and cmdStatus==0):
		return int(discPerc)
	else:
		logWrite(logFile,' !!!! ERROR !!!::  diskSizePercGetter :: unexpected value : '+str(discPerc))
		return 0		
def lastCharChecker(dName):
	if(dName[len(dName)-1]=='/'):
		return dName
	else:
		return dName+'/'
def get_datetime():
	my_year=str(localtime()[0])
	my_mounth=str(localtime()[1])
	my_day=str(localtime()[2])
	my_hour=str(localtime()[3])
	my_min=str(localtime()[4])
	my_sec=str(localtime()[5])	
	if(len(str(my_mounth))==1):
		my_mounth="0"+my_mounth		
	if(len(my_day)==1):
		my_day="0"+my_day
	if(len(my_hour)==1):
		my_hour="0"+my_hour
	if(len(my_min)==1):
		my_min="0"+my_min
	if(len(my_sec)==1):
		my_sec="0"+my_sec
	return my_year+"."+my_mounth+"."+my_day+" "+my_hour+":"+my_min+":"+my_sec
def fileAppendWrite(file, writeText):
	try :
		fp=open(file,'ab')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print ('!!! An error is occurred while writing file !!!')
def logWrite(logFile,logText):
	if(writeLogFile):
		print (logText)
		logText='* ('+get_datetime()+') '+logText
		fileAppendWrite(logFile,logText)		
	else:
		print (logText)
def main():
	for myDir in dirList:
		if (myDir[1][0]):
			diskUPDeleter(myDir[0][0],lastCharChecker(myDir[0][1]),myDir[0][2],myDir[1][1],myDir[3][0],myDir[3][1],lastCharChecker(myDir[3][2]))
		if (myDir[2][0]):
			diskTimeDeleter(myDir[0][0],lastCharChecker(myDir[0][1]),myDir[0][2],myDir[2][1],myDir[3][0],myDir[3][1],lastCharChecker(myDir[3][2]))
main()