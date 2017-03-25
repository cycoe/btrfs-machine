#!/usr/bin/bash

if [ ! -d "/mnt/system" ]; then
    sudo mkdir /mnt/system
    echo "/mnt/system directory not exist! creating..."
fi

mountStatus=`mount | grep '/mnt/system'`
if [ "$mountStatus" != "" ]; then
    echo "/mnt/system has mounted by other device!"
    read -p "Do you want to remove it? (y/n)" umountFlag
    if [ "$umountFlag" = "y" ]; then
        sudo umount /mnt/system && echo "unmount successfully!"
    else
        echo "cannot mount! exiting..."
        exit
    fi
fi
    
rootDevice=`mount | grep ' / ' | awk '{print $1}' | tr -d '\n'`
sudo mount $rootDevice /mnt/system

if [ ! -d "/mnt/system/backup" ]; then
    sudo mkdir /mnt/system/backup
fi

listSnapshot () {
    echo ""
    echo "Snapshots List:"
    echo "-------------------------------------------------------------"
    snapshotList=`sudo btrfs subvolume list / | grep "backup"`
    if [ "$snapshotList" = "" ]; then
        echo "No Snapshot now!"
    else
        sudo btrfs subvolume list / | grep "backup"
    fi
    echo ""
}

createSnapshot () {
    backupTime=`date -d now +%Y-%m-%d_%H-%M-%S`
    backupDir=/mnt/system/backup/$backupTime
    sudo mkdir $backupDir
    sudo btrfs subvolume snapshot /mnt/system/@ $backupDir
    listSnapshot
}

deleteSnapshot () {
    listSnapshot
    read -p "Input the ID of the snapshot you want to delete: " selectedID
    read -p "Are you sure to delete $selectedID?(y/n)" deleteFlag
    if [ "$deleteFlag" != "y" ]; then
        sudo umount /mnt/system
        exit
    fi
    selectedSnap=`sudo btrfs subvolume list / | grep "backup" | grep "$selectedID" | awk '{print $9}'`
    sudo btrfs subvolume delete /mnt/system/$selectedSnap
    snapDate=`echo "$selectedSnap" | awk '{split($0,a,"/");print a[2]}'`
    sudo rm -r /mnt/system/backup/$snapDate
    echo "delete successfully!"
    listSnapshot
}

restoreSnapshot () {
    listSnapshot
    read -p "Input the ID of the snapshot you want to restore: " selectedID
    read -p "Are you sure to restore to $selectedID?(y/n)" restoreFlag
    if [ "$restoreFlag" != "y" ]; then
        sudo umount /mnt/system
        exit
    fi
    selectedSnap=`sudo btrfs subvolume list / | grep "backup" | grep "$selectedID" | awk '{print $9}'`
    createSnapshot
    if [ -d "/mnt/system/@_ori" ]; then
        echo "/mnt/system/@_ori has exist! cleaning..."
        sudo btrfs subvolume delete /mnt/system/@_ori || exit
        echo "Clean successfully!"
    fi
    echo "Backup /mnt/system/@ to /mnt/system/@_ori..."
    sudo mv /mnt/system/@ /mnt/system/@_ori
    echo "Backup successfully!"
    echo "rename /mnt/system/$selectedSnap to /mnt/system/@..."
    sudo cp -r /mnt/system/$selectedSnap /mnt/system/@
    echo "Rename successfully!"
    echo "Every will shift back to $selectedSnap after you reboot!"
}
    
if [ "$1" = "-c" ]; then
    createSnapshot
elif [ "$1" = "-d" ]; then
    deleteSnapshot
elif [ "$1" = "-l" ]; then
    listSnapshot
elif [ "$1" = "-r" ]; then
    restoreSnapshot
fi

sudo umount /mnt/system
    
