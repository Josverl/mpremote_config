# command = "wipe_folder folder='/'"
# Clean all files from flash ,use with care ; there is no undo or trashcan 
import uos as os

if not folder: # Default to root # type: ignore
    folder = '/'


def wipe_folder( folder=".",sub=True):  # sourcery skip: use-fstring-for-formatting
    print( "wipe path {}".format(folder) )
    l = os.listdir(folder)
    l.sort()
    #print(l)
    # if l != ['']:
    for f in l:
        if f:
            child = "{}/{}".format(folder, f)
            print(" - ", child)
            st = os.stat(child)
            if st[0] & 0x4000:  # stat.S_IFDIR
                if sub:
                    wipe_folder(child,sub)
                    try:
                        os.rmdir(child)
                    except OSError:
                        print("Error deleting folder {}".format(child))
            else: # File
                try:  
                    os.remove(child)
                except OSError:
                    print("Error deleting file {}".format(child))

wipe_folder(folder=folder)
