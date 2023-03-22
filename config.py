from pathlib import Path


commands = {
    "list": {
        "command": "devs",
        "help": "List serial devices",
    },
    "run script='main.py'": {
        "command": ["exec", "exec( open(script).read() , globals() )"],
        "help": "Run a script on the remote device",
    },
    "format": {
        "command": [
            "exec",
            "--no-follow" "import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()",
        ],
        "help": "Format the device",
    },
    "unsafe": {
        "command": [
            "exec",
            "--no-follow" "{{import random}}",
            "import os, machine; os.umount('/'); os.VfsLfs2.mkfs(bdev); os.mount(bdev, '/'); machine.reset()",
        ],
        "help": "Format the device",
    },
}

# register com ports in poth upper and lower case
for port_num in range(1,30):
    prefix, port = ("com", "COM")
    commands["{}{}".format(prefix, port_num)] = {
        "command": "connect {}{}".format(port, port_num),
        "help": 'connect to serial port "{}{}:"'.format(port, port_num),
    }
    prefix, port = ("COM", "COM")
    commands["{}{}".format(prefix, port_num)] = {
        "command": "connect {}{}".format(port, port_num),
        "help": 'connect to serial port "{}{}:"'.format(port, port_num),
    }

here  = Path(__file__).parent.absolute()

files = (here / "snippets").glob("*.py")
for file in files:
    with open(file, encoding="utf-8") as f:
        help = f.readline()
    if help[0] in ("#", '"'):
        help = help[1:].strip().strip('"').strip()
        help = f"{help} - {file.absolute()}"
    else:
        help = file.absolute()
    commands[file.stem] = {
        "command": ["exec", file.read_text()],
        "help": help,
    }
