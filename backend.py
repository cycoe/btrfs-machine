import os
import subprocess

class Logger(object):
    def __init__(self, logPath):
        self.logPath = logPath
        pass

class MountError(Exception):
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo
    def __str__(self):
        return self.errorInfo

class Backend(object):
    def __init__(self):
        logger = Logger("klone.log")
        pass
    def loadVal(self):
        self.mountPoint = "/mnt/system"
        self.backupDir = self.mountPoint + "/backup"
        self.snapLabels = [0, 2, 5, 7]
        self.snapitems = [1, 3, 6, 8]
        self.homeMode = False

        if not os.path.exists(self.mountPoint):
            os.mkdir(self.mountPoint)
        mountStr = subprocess.getoutput("mount")
        mountList = [i.split() for i in mountStr.split("\n")]
        for mount in mountList:
            if mount[2] == '/':
                self.rootDevice = mount[0]
            if mount[2] == '/home' and mount[0] == self.rootDevice:
                self.homeMode = True
        try:
            (flag, errorInfo) = subprocess.getstatusoutput("mount " + self.rootDevice + ' ' + self.mountPoint)
            if flag != 0:
                raise MountError(errorInfo)
        except AttributeError:
            print("Cannot find a root device or a mount point!")
            print("exiting...")
            return 1
        except MountError as e:
            return 2

        if not os.path.exists(self.backupDir):
            os.mkdir(self.backupDir)
        return self.homeMode

    def listRootSnap(self):
        pass

    def listSnapshot(self):
        snapStr = subprocess.getoutput("btrfs subvolume list " + self.mountPoint)
        snapMat = [snapList.split() for snapList in snapStr.split("\n") if snapList.split()[8][:6] == "backup"]
        self.snapLabels = [snapMat[0][i] for i in range(len(snapMat[0])) if i in self.snapLabels]
        self.rootSnapMat = [[snapMat[i][j] for j in range(len(snapMat[0])) if j in self.snapitems] for i in range(len(snapMat)) if snapMat[i][-1][-1] == '@']
        if self.homeMode:
            self.homeSnapMat = [[snapMat[i][j] for j in range(len(snapMat[0])) if j in self.snapitems] for i in range(len(snapMat)) if snapMat[i][-1][-5:] == '@home']
            return self.snapLabels, self.rootSnapMat, self.homeSnapMat
        return self.snapLabels, self.snapMat

    def createRootSnapshot(self):
        import time
        snapDir = self.backupDir + "/" + time.strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(snapDir)
        subprocess.getoutput("btrfs subvolume snapshot " + self.mountPoint + '/@' + " " + snapDir)
        return self.listSnapshot()

    def createHomeSnapshot(self):
        import time
        snapDir = self.backupDir + "/" + time.strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(snapDir)
        subprocess.getoutput("btrfs subvolume snapshot " + self.mountPoint + '/@home' + " " + snapDir)
        return self.listSnapshot()

    def deleteSnapshot(self, i):
        import re
        self.listSnapshot()
        snapshot = snapMat[i][-1]
        subprocess.getoutput("btrfs subvolume delete " + self.mountPoint + "/" + snapshot)
        #os.rmdir(self.mountPoint + "/" + re.findall('(.*)?/@.*', snapshot)[0])
        return self.listSnapshot()
        pass
    def restoreSnapshot(self):
        pass
    def release(self):
        try:
            flag, errorInfo = subprocess.getstatusoutput("sudo umount " + self.mountPoint)
            if flag != 0:
                raise MountError(errorInfo)
        except MountError as e:
            print(e)
            print("exiting...")
            exit(0)

def main():
    backend = Backend()
    backend.loadVal()
    print(backend.createSnapshot())
    backend.release()
