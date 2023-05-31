"""\
mpremote configuration file that defines a custom configuration for mpremote.
- add a few handly commands that are coded in the first part of this file 
- reads additional scripts from the snippets folder and adds them as individual commands to mpremote.
"""

import os
from pathlib import Path

commands = {
    "list": {
        "command": ["connect", "list"],
        "help": "List serial devices",
    },
    "xrun script='main.py'": {
        "command": ["exec", "exec( open(script).read() , globals() )"],
        "help": "Run a script on the remote device",
    },
    "md": {"command": "mkdir", "help": "alias for mkdir"},
    "del": {"command": "rm", "help": "alias for rm"},
    "dir": {"command": "ls", "help": "alias for ls"},
    "copy": {"command": "cp", "help": "alias for cp"},
}

# register COM ports in both upper and lower case
if os.name == "nt":
    for port_num in range(1, 30):
        prefix, port = ("com", "COM")
        commands[f"{prefix}{port_num}"] = {
            "command": f"connect {port}{port_num}",
            "help": f"connect to serial port {port}{port_num}:",
        }
        prefix, port = ("COM", "COM")
        commands[f"{prefix}{port_num}"] = {
            "command": f"connect {port}{port_num}",
            "help": f"connect to serial port {port}{port_num}:",
        }

here = Path(os.getcwd())
files = (here / "snippets").glob("*.py")
for file in files:
    try:
        with open(file, encoding="utf-8") as f:
            help = f.readline()
            params = f.readline()
    except UnicodeDecodeError:
        continue
    if help[0] in ("#", '"'):
        help = help[1:].strip().strip('"').strip()
        help = f"{help}\n{file.absolute()}"
        # help = f"{help}\n - {file.relative_to(here)}"
    else:
        help = ""
    command = file.stem
    # BUG: Quote handling from commandline --> mpremote.main:do_command_expansion(args): prevents handling string parameters 
    # if command == "wipe_folder":
    #     command = "wipe_folder folder='/'"
    # if params[0] not in ("#", '"') and '=' in params:
    #     params = params.strip()
    #     command += f" {params}"

    commands[command] = {
        "command": ["exec", file.read_text()],
        "help": help,
    }
