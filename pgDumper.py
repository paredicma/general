#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author                                        : Mustafa YAVUZ
## E-mail                                        : mustafa.yavuz@turkcell.com.tr
## Version                                       : 0.1
## Date                                          : 21.01.2020
## OS System                                     : Redhat/Centos 6-7, debian/Ubuntu
## pg Version                                    : 9.x,10.x,11.x,12.x  
################## LIBRARIES ################################
import os
import commands
from time import *
import socket
from string import *
##################PARAMETERS##########################
myLogFile = 'pgBackup.log'
#backupOSUser = 'postgres'
writeLogFile = True
dbSuperUser = 'postgres'
dbSuperPass      = ''
pgPort='5432'
backupDir='/pgdata/backup/'
backupAlias='myDBBackup-'
backupKeepDay='7'
##################PARAMETERS##########################
def gzipBackupFile(backupFile):
                cmdStatus, cmdResponse = commands.getstatusoutput('gzip '+backupFile)
                if(str(cmdStatus)=='0'):
                                logWrite(myLogFile, False, 'INFO : DB backup file was zipped: File Name ->' +backupFile+'.gz')
                                return True
                else:
                                logWrite(myLogFile, True,'ERROR : When DB backup file was zipping. Something went wrong. \nCheck proccess !!!\nFile Name ->' +backupFile)
                                return False                        
def makeBackup( pgPort, backupDir, backupAlias):
                backupFileName=backupAlias+get_datetime()+'.sql'
                cmdStatus, cmdResponse = commands.getstatusoutput('pg_dumpall -p '+pgPort+' -f '+backupDir+backupFileName)
                if(str(cmdStatus)=='0'):
                                logWrite(myLogFile, False, 'INFO : DB backup completed: File Name ->' +backupDir+backupFileName)
                                zipStatus=gzipBackupFile(backupDir+backupFileName)
                                return zipStatus
                else:
                                logWrite(myLogFile, True,'ERROR : When DB backup proccess. Something went wrong. \nCheck proccess !!!\nFile Name ->' +backupDir+backupFileName)
                                return False
def delOldBackupFiles(backupDir):
                cmdStatus, delFileNameArray = commands.getstatusoutput('find '+backupDir+backupAlias+'*.sql* -mtime +'+backupKeepDay)
                if ( cmdStatus == 0 ):
                                for delFileName in  delFileNameArray:
                                                delResponse=os.system('rm -f '+delFileName)
                                                if(str(delResponse)=='0'):
                                                                logWrite(myLogFile, False, 'INFO : OLD (older than '+backupKeepDay+' days ) DB backup file deleted : File Name ->' +delFileName)
                                                else:
                                                                logWrite(myLogFile, True, 'ERROR : When DB backup file was deleting. Something went wrong. \nCheck proccess !!!\nFile Name ->' +delFileName)


#######################################################
############## AUXILIARY FUNCTIONS ##########
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
                return my_year+my_mounth+my_day+'_'+my_hour+my_min+my_sec
def fileAppendWrite(file, writeText):
                try :
                                fp=open(file,'ab')
                                fp.write(writeText+'\n')
                                fp.close()
                except :
                                print (bcolors.FAIL+'!!! An error is occurred while writing file !!!'+bcolors.ENDC)
def fileRead(file):
                returnTEXT=""
                try :
                                fp=open(file,'r')
                                returnTEXT=fp.readlines()
                                fp.close()
                                return returnTEXT
                except :
                                print (bcolors.FAIL+'!!! An error is occurred while reading file !!!'+bcolors.ENDC)
                                return ""
def fileReadFull(file):
                returnTEXT=""
                try :
                                fp=open(file,'r')
                                returnTEXT=fp.read()
                                fp.close()
                                return returnTEXT
                except :
                                print (bcolors.FAIL+'!!! An error is occurred while reading file !!!'+bcolors.ENDC)
                                return ""
def fileClearWrite(file, writeText):
                try :
                                fp=open(file,'w')
                                fp.write(writeText+'\n')
                                fp.close()
                except :
                                print (bcolors.FAIL+'!!! An error is occurred while writing file !!!'+bcolors.ENDC)
def logWrite(logFile, sendMail ,logText):
                if(writeLogFile):
                                print (logText)
                                logText='* ('+get_datetime()+') '+logText
                                fileAppendWrite(logFile,logText)
                                if ( sendMail ):
                                                print 'mail sended'
#                                             sendMailer(logText)                                       
                else:
                                print (logText)
################ Main Function ############
def main():
                delOldBackupFiles(backupDir)
                makeBackup( pgPort, backupDir, backupAlias)    