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
        self.backDir = self.mountPoint + "/backup"
        if not os.path.exists(self.mountPoint):
            os.mkdir(self.mountPoint)
        mountStr = subprocess.getoutput("mount")
        mountList = [i.split() for i in mountStr.split("\n")]
        for mount in mountList:
            if mount[2] == '/':
                self.rootDevice = mount[0]
        try:
            (flag, errorInfo) = subprocess.getstatusoutput("mount " + self.rootDevice + ' ' + self.mountPoint)
            if flag != 0:
                raise MountError(errorInfo)
        except AttributeError:
            print("Cannot find a root device or a mount point!")
            print("exiting...")
            exit(0)
        except MountError as e:
            print(e)

        if not os.path.exists(self.backDir):
            os.mkdir(self.backDir)

    def listSnapshot(self):
        snapStr = subprocess.getoutput("btrfs subvolume list " + self.mountPoint)
        snapMat = [snapList.split() for snapList in snapStr.split("\n") if snapList.split()[8][:6] == "backup"]
        return snapMat
    def createSnapshot(self):
        import time
        snapDir = self.backDir + "/" + time.strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(snapDir)
        subprocess.getoutput("btrfs subvolume snapshot " + self.mountPoint + '/@' + " " + snapDir)
        return self.listSnapshot()
    def deleteSnapshot(self, i):
        snapMat = self.listSnapshot()
        try:
            snapshot = snapMat[i][-1]
        except IndexError:
            return False
            print("Index out of range!")
        subprocess.getoutput("btrfs subvolume delete " + self.mountPoint + "/" + snapshot)
        os.rmdir(self.mountPoint + "/" + snapshot[:-2])
        return self.listSnapshot()
        pass
    def restoreSnapshot(self):
        pass
    def release(self):
        try:
            flag, errorInfo = subprocess.getstatusoutput("umount " + self.mountPoint)
            if flag != 0:
                raise MountError(errorInfo)
        except MountError as e:
            print(e)
            print("exiting...")
            exit(0)

backend = Backend()
backend.loadVal()
print(backend.createSnapshot())
backend.release()
