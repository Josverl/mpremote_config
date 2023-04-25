# format/erase an ESPxx with the lfs2 filesystem
import os

if 'mount_point' not in globals():
    mount_point = '/flash'
    
os.umount(mount_point)
os.VfsLfs2.mkfs(bdev, readsize=32, progsize=32, lookahead=32)
os.mount(bdev, mount_point, readonly=False)

print(mount_point, os.listdir(mount_point))
