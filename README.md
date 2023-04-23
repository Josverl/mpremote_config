# mpremote_config

[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) configuration and script snippets that can be executed simply

Note that this configuration has a dependency on a [pre-release fork](https://github.com/Josverl/mpremote) of mpremote to make the mpremote configuration work on Windows at all, and to pass the location of the configuration file in the `__file__` variable. 

- config.py
  Adds a simple mechanism to create additional `mpremote` commands by just creating a `my_command.py` script in the `./snippets` folder.
  These then can be executed by running `mpremote my_command` referencing a file `my_command`
  or in combination with additional commands `mpremote mount . connect_wifi my_command` 

- adds COM4: .. COM30: to simplify connection to multiple boards (only when running on windows) 
- adds all scripts in the snippets folder as commands

- list all commands and scripts using `mpremote help`

## Setup
- install mpremote ( pre-release fork) 
  `pip install  git+https://github.com/Josverl/mpremote.git@main#subdirectory=tools/mpremote `
  
- locate the folder and file where mpremote looks for its configuration.
  this is briefly mentioned at : https://docs.micropython.org/en/latest/reference/mpremote.html#shortcuts 
  the relevant code is in mpremote/main.py ( improved version below) 
  ```python 
      # use $XDG_CONFIG_HOME, if on Windows use $APPDATA
    if os.name != "nt":
        path = os.getenv("XDG_CONFIG_HOME") or os.getenv("HOME")
        path = os.path.join(path, ".config") if path else None
    else:
        path = os.getenv("HOME") or os.getenv("APPDATA")
   ```
  On *nix the paths will be tried: 
    `<$XDG_CONFIG_HOME>/.config/config.py`
    `<$HOME>/.config`
  on Windows the windows paths will be tried:
    `<$env:HOME>\config.py`
    `<$env:APPDATA>\config.py`
  
   Unfortunatly there is no indication what paths are tested or used.  
   For troubleshooting you should add a line like: https://github.com/Josverl/mpremote/blob/291b219ebc753ec71b587dcbe9c591e382b86aef/tools/mpremote/mpremote/main.py#L345

- fork / clone or download this repro to the folder relevant to your OS and configuration

## Examples 
Get family / port information on a specific device
`mpremote get_port`
`mpremote COM5 get_port`  
![image](https://user-images.githubusercontent.com/981654/233866669-d999c174-b085-4c72-9908-5c1d58ebf92e.png)

Scan WiFi 
`mpremote wifi_scan` using the first avaiable device (which just happens to have a WiFi connector)  
![image](https://user-images.githubusercontent.com/981654/233866528-8e38990a-39d5-4b5b-a0ec-91691dd2ffa3.png)

Connect to Wifi ( SSID / pwrd are currently hardcoded in the script) 
`mpremote wifi_connect`  
![image](https://user-images.githubusercontent.com/981654/233866761-7655cbf1-c989-4970-96c6-c2458b5faa59.png)

## Creating scripts / cmdlets 
Create a new .py file in the snippets folder 

- if the first line of the file starts with a comment `#` or a double-quote `"` , then the first line is used as the help text to the cmdlet 
- The entire script is read from disk, and added to mpremotes commands.

- if you need to pass parameters to a script this is possible.
  while there apparently is a way that mpremote allows for parameter intsertion , i have not been able to grok this yet.
  the currently simple workaround is the run 2 commands , first to set a variable and then in your script detect if that variable exists , and otherwise us a deafault value.
  (see the wipe_folder script for an example)  
   ![image](https://user-images.githubusercontent.com/981654/233867460-e3fbad71-713c-4575-b7bc-1a3b72a51d26.png)

  


