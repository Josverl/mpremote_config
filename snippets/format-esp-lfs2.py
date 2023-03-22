# format/erase an ESPxx with the lfs2 filesystem
import os

os.umount('/')
os.VfsFat.mkfs(bdev)
os.mount(bdev, '/')
