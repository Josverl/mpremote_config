# mpremote_config

[mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) configuration and script snippets that can be executed simply

- config.py
  Adds a simple meganism to create additional `mpremote` commands by just creating a `my_command.py` script in the snippets folder.
  This then can be executed by running `mpremote my_command` 
  or in combination with additional commands `mpremote mount . connect-wifi my_command` 


- adds COM4: .. COM30: to simplify connection to multiple boards
- adds all scripts in the snippets folder as commands

- list all commands and scripts using `mpremote help`
 
