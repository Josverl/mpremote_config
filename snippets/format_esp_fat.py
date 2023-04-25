"format/erase an ESPxx with the FAT filesystem"
import os

if 'mount_point' not in globals():
    mount_point = '/flash'

os.umount(mount_point)
os.VfsFat.mkfs(bdev)
os.mount(bdev, mount_point, readonly=False)

print(mount_point, os.listdir(mount_point))

