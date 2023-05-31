# command = "wipe_folder" , or exec "folder='/foobar'" wipe_folder
# Clean all files from flash ,use with care ; there is no undo or trashcan
# todo: integrate with the way mpremote handles parameters.
import uos as os

if "folder" not in globals():
    folder = "/"


def wipe_folder(folder=".", sub=True):  # sourcery skip: use-fstring-for-formatting
    print("wipe path {}".format(folder))
    l = os.listdir(folder)
    l.sort()
    # print(l)
    # if l != ['']:
    for f in l:
        if f:
            folder.rstrip("/")
            child = "{}/{}".format(folder, f)
            print(" - ", child)
            st = os.stat(child)
            if st[0] & 0x4000:  # stat.S_IFDIR
                if sub:
                    wipe_folder(child, sub)
                    try:
                        os.rmdir(child)
                    except OSError:
                        print("Error deleting folder {}".format(child))
            else:  # File
                try:
                    os.remove(child)
                except OSError:
                    print("Error deleting file {}".format(child))
    # delete rootfolder
    if folder.rstrip("/") not in {"", ".", "/flash", "/sd"}:
        try:
            os.chdir("/")
            os.rmdir(folder)
        except OSError:
            print("Error deleting folder {}".format(folder))


wipe_folder(folder=folder)  # type: ignore
