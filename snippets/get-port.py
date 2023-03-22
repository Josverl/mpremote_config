"stubber: get-port"
import gc
import os
import sys

try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict  # type: ignore


def _info():  # type:() -> dict[str, str]
    info = OrderedDict(
        {
            "family": sys.implementation.name,
            "version": "",
            "port": "stm32" if sys.platform.startswith("pyb") else sys.platform,  # port: esp32 / win32 / linux / stm32
            "board": "GENERIC",
            "cpu": "",
            "build": "",
            "board_d": "",
            "mpy": "",
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
        b = info["board"].strip()
        print(f"board: '{b}'")
        with open("board_info.csv", "r") as f:
            if not find_board(info, b, f):
                if "with" in b:
                    f.seek(0)
                    b = b.split("with")[0].strip()
                    find_board(info, b, f)

        # info["board"] = info["board"].replace(" ", "_")
    except (AttributeError, IndexError, OSError):
        pass
    gc.collect()

    try:
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
            # from pycopy import const as _t  # type: ignore

            info["family"] = "pycopy"
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
    return info


def find_board(info, board_descr, f):
    for line in f:
        descr_, board_ = line.split(",")[0].strip(), line.split(",")[1].strip()
        if descr_ == board_descr:
            # print(line)
            info["board_d"] = descr_
            info["board"] = board_
            return True
    return False


info = _info()
# output the info dict as a string with the OrderedDict() removed
repr_info = str(info).replace("OrderedDict(", "").rstrip(")")
print(repr_info)
