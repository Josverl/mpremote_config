"stubber: extract the MCU hardware and firmware information across different families and firmwares and devices"
import os
import sys
if 1:
    try:
        print(sys.platform ) # 'samd'
        print(sys.version) #'3.4.0; MicroPython v1.19.1-705-gac5934c96 on 2022-11-18
        build = sys.version.split(';')[1].strip().split(' ')[1].split('-')[1]
        print(build)
        print(sys.implementation) # (name='micropython', version=(1, 19, 1), _machine='Wio Terminal D51R with SAMD51P19A', _mpy=7430)
        print(os.uname()) # (sysname='esp32', nodename='esp32', release='1.19.1', version='v1.19.1 on 2022-06-18', machine='ESP32 module (spiram) with ESP32')
    except:
        pass
    try:
        import platform
        print(platform.platform() ) # MicroPython-1.19.1-xtensa-IDFv4.2.2-with-newlib3.0.0
        print(platform.libc_ver()) # ('newlib', '3.0.0')
        print(platform.python_compiler()) # GCC 8.4.0
    except:
        pass

print("--------------------------------------------------")

_n = sys.implementation.name  # type: ignore
_p = sys.platform if not sys.platform.startswith("pyb") else "stm32"
info = {
    "name": _n,  # - micropython
    "release": "0.0.0",  # mpy semver from sys.implementation or os.uname()release
    "version": "0.0.0",  # major.minor.0
    "build": "",  # parsed from version
    "sysname": "unknown",  # esp32
    # "nodename": "unknown",  # ! not on all builds
    "machine": "unknown",  # ! not on all builds
    "family": _n,  # fw families, micropython , pycopy , lobo , pycom
    "platform": _p,  # port: esp32 / win32 / linux
    "port": _p,  # port: esp32 / win32 / linux
    "ver": "",  # short version
}
try:
    info["version"] = ".".join([str(n) for n in sys.implementation.version])
    info["release"] = info["version"]
    info["name"] = sys.implementation.name
    if '_machine' in dir(sys.implementation):
        info["machine"] = sys.implementation._machine  # type: ignore
    if '_mpy' in dir(sys.implementation):
        info["mpy"] = sys.implementation._mpy  # type: ignore
    if 'mpy' in dir(sys.implementation):
        info["mpy"] = sys.implementation.mpy  # type: ignore
except AttributeError:
    pass

try:
    info["mpy"] = sys.implementation._mpy  # type: ignore
except AttributeError:
    pass

if sys.platform not in ("unix", "win32"):
    try:
        u = os.uname()
        info["sysname"] = u.sysname
        # info["nodename"] = u.nodename
        info["release"] = u.release
        if info["machine"] == "":
            info["machine"] = u.machine
        # parse micropython build info
        if " on " in u.version:
            s = u.version.split(" on ")[0]
            if info["sysname"] == "esp8266":
                # esp8266 has no usable info on the release
                if "-" in s:
                    v = s.split("-")[0]
                else:
                    v = s
                info["version"] = info["release"] = v.lstrip("v")
            try:
                info["build"] = s.split("-")[1]
            except IndexError:
                pass
    except (IndexError, AttributeError, TypeError):
        pass

try:  # families
    from pycopy import const as _t  # type: ignore

    info["family"] = "pycopy"
    del _t
except (ImportError, KeyError):
    pass
try:  # families
    from pycom import FAT as _t  # type: ignore

    info["family"] = "pycom"
    del _t
except (ImportError, KeyError):
    pass
if info["platform"] == "esp32_LoBo":
    info["family"] = "loboris"
    info["port"] = "esp32"
elif info["sysname"] == "ev3":
    # ev3 pybricks
    info["family"] = "ev3-pybricks"
    info["release"] = "1.0.0"
    try:
        # Version 2.0 introduces the EV3Brick() class.
        from pybricks.hubs import EV3Brick  # type: ignore

        info["release"] = "2.0.0"
    except ImportError:
        pass

# version info
if info["release"]:
    info["ver"] = "v" + info["release"].lstrip("v")
if info["family"] == "micropython":
    if (
        info["release"]
        and info["release"] >= "1.10.0"
        and info["release"].endswith(".0")
    ):
        # drop the .0 for newer releases
        info["ver"] = info["release"][:-2]
    else:
        info["ver"] = info["release"]
    # add the build nr, but avoid a git commit-id
    if info["build"] != "" and len(info["build"]) < 4:
        info["ver"] += "-" + info["build"]
if info["ver"][0] != "v":
    info["ver"] = "v" + info["ver"]
# spell-checker: disable
if "mpy" in info:  # mpy on some v1.11+ builds
    sys_mpy = int(info["mpy"])
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


print('=========================================')
print(repr(info))
print('=========================================')
