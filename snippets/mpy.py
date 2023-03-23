import sys

sys_mpy = sys.implementation._mpy if "_mpy" in dir(sys.implementation) else sys.implementation.mpy if "mpy" in dir(sys.implementation) else 0
arch = [None, 'x86', 'x64',
    'armv6', 'armv6m', 'armv7m', 'armv7em', 'armv7emsp', 'armv7emdp',
    'xtensa', 'xtensawin'][sys_mpy >> 10]
v_mpy = "v{}.{}".format(sys_mpy & 0xff, sys_mpy >> 8 & 3)

print('mpy arch   :', arch)
print('mpy version:', v_mpy)