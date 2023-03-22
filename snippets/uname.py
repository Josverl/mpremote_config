# Display the mcu uname and unique_id
import machine
import ubinascii
import uos

try:
    unique_id = ubinascii.hexlify(machine.unique_id())
except Exception:
    unique_id = None
print("uname:", uos.uname())
print("unique_id:", unique_id)


