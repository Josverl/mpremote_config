

<details>
<summary>Table of Contents</summary>

- [Using GitHub CLI](#using-github-cli)
  - [using just git](#using-just-git)

</details>


## Using GitHub CLI

 - Install GitHub CLI from  https://cli.github.com/
 - use the [repo fork command](https://cli.github.com/manual/gh_repo_fork#) to clone the repo to your local machine

```bash
# fork repo to your account and clone it to local
gh repo fork josverl/mpremote_config  <your_path> --clone
```
    
If you already have a fork of the repo, you can clone it to your local machine with the gh repo clone subcommand.
```bash	
gh repo clone <your_username>/mpremote_config <your_path>

```
### using just git 
```bash	
# - Create a fork using the Github Web UI 
# - Clone the fork to your local machine
git clone https://github.com/<your_username>/mpremote_config.git <your_path>
# - [optionally] add an upstream remote to the original repo
```
