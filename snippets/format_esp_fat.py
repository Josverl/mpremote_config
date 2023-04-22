"format/erase an ESPxx with the FAT filesystem"
import os

os.umount('/')
os.VfsFat.mkfs(bdev)
os.mount(bdev, '/')
