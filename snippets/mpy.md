# Versioning and compatibility of .mpy files

https://docs.micropython.org/en/latest/reference/mpyfiles.html#versioning-and-compatibility-of-mpy-files

A given .mpy file may or may not be compatible with a given MicroPython system. Compatibility is based on the following:

 * **Version** of the .mpy file: the version of the file must match the version supported by the system loading it.
 * **Sub-version** of the .mpy file: if the .mpy file contains native machine code then the sub-version of the file must match the version support by the system loading it. Otherwise, if there is no native machine code in the .mpy file, then the sub-version is ignored when loading.
 * **Small integer bits**: the .mpy file will require a minimum number of bits in a small integer and the system loading it must support at least this many bits.
 * **Native architecture**: if the .mpy file contains native machine code then it will specify the architecture of that machine code and the system loading it must support execution of that architecture’s code.

