"stubber: get-port and board info "
import gc
import os
import sys

try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict  # type: ignore


def file_exists(filename: str):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False


def _info():  # type:() -> dict[str, str]
    info = OrderedDict(
        {
            "family": sys.implementation.name,
            "version": "",
            "port": "stm32" if sys.platform.startswith("pyb") else sys.platform,  # port: esp32 / win32 / linux / stm32
            "board": "GENERIC",
            "build": "",
            "cpu": "",
            "mpy": "",
            "arch": "",
        }
    )
    try:
        info["version"] = ".".join([str(n) for n in sys.implementation.version])
    except AttributeError:
        pass
    try:
        machine = sys.implementation._machine if "_machine" in dir(sys.implementation) else os.uname().machine
        info["board"] = machine.strip()
        info["cpu"] = machine.split("with")[1].strip()
        info["mpy"] = (
            sys.implementation._mpy
            if "_mpy" in dir(sys.implementation)
            else sys.implementation.mpy
            if "mpy" in dir(sys.implementation)
            else ""
        )
    except (AttributeError, IndexError):
        pass
    gc.collect()
    try:
        # look up the board name in the board_info.csv file
        for filename in ["board_info.csv", "lib/board_info.csv"]:
            if file_exists(filename):
                b = info["board"].strip()
                if find_board(info, b, filename):
                    break
                if "with" in b:
                    b = b.split("with")[0].strip()
                    if find_board(info, b, filename):
                        break
    except (AttributeError, IndexError, OSError):
        pass
    info["board"] = info["board"].replace(" ", "_")
    gc.collect()

    try:  # extract buildfrom uname().version if available
        info["build"] = os.uname()[3].split(" on ")[0].split("-")[1]
    except (AttributeError, IndexError):
        try:  # extract build from sys.version if available
            info["build"] = sys.version.split(";")[1].strip().split(" ")[1].split("-")[1]
        except (AttributeError, IndexError):
            pass

    if info["version"] == "" and sys.platform not in ("unix", "win32"):
        try:
            u = os.uname()
            info["version"] = u.release
        except (IndexError, AttributeError, TypeError):
            pass

    for mod_name, mod_thing in [("pycopy", "const"), ("pycom", "FAT")]:
        try:  # families
            _t = __import__(mod_name, None, None, (mod_thing))
            info["family"] = mod_name
            del _t
        except (ImportError, KeyError):
            pass

    if info["family"] == "micropython":
        if (
            info["version"]
            and info["version"].endswith(".0")
            and info["version"] >= "1.10.0"  # versions from 1.10.0 to 1.20.0 do not have a micro .0
            and info["version"] <= "1.20.0"
        ):
            # drop the .0 for newer releases
            info["version"] = info["version"][:-2]

    # spell-checker: disable
    if "mpy" in info:  # mpy on some v1.11+ builds
        sys_mpy = int(info["mpy"])
        # .mpy architecture
        arch = [
            None,
            "x86",
            "x64",
            "armv6",
            "armv6m",
            "armv7m",
            "armv7em",
            "armv7emsp",
            "armv7emdp",
            "xtensa",
            "xtensawin",
        ][sys_mpy >> 10]
        if arch:
            info["arch"] = arch
        # .mpy version.minor
        info["mpy"] = "v{}.{}".format(sys_mpy & 0xFF, sys_mpy >> 8 & 3)
        # extract_os_info(info)
    return info


def find_board(info: dict, board_descr: str, filename: str):
    "Find the board in the board_info.csv file"
    with open(filename, "r") as file:
        # ugly code to make testable in python and micropython
        while 1:
            line = file.readline()
            if not line:
                break
            descr_, board_ = line.split(",")[0].strip(), line.split(",")[1].strip()
            if descr_ == board_descr:
                info["board"] = board_
                return True
    return False


info = _info()
# output the info dict as a string with the OrderedDict() removed
repr_info = str(info).replace("OrderedDict(", "").rstrip(")")
print(repr_info)

print("{family}-{version}-{port}-{board}".format(**info))
