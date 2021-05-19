
from ftplib import FTP, error_perm
import os

class Download(object):
    def __init__(self):
        pass
    def ftpDownloader(self,stationId,startYear,endYear,url="ftp.pyclass.com",user="student@pyclass.com",passwd="student123"):
        ftps=FTP(url)
        ftps.login(user,passwd)
        if not os.path.exists("C:\\in"):
            os.makedirs("C:\\in")
        os.chdir("C:\\in")
        for year in range(startYear,endYear+1):
            fullpath='/Data/%s/%s-%s.gz' % (year,stationId,year)
            filename=os.path.basename(fullpath)
            try:
                with open(filename,"wb") as file:
                    ftps.retrbinary('RETR %s' % fullpath, file.write)
                print("%sc succesfully downloaded" % filename)
            except error_perm:
                print("%s is not available" % filename)
                os.remove(filename)
        ftps.close()

