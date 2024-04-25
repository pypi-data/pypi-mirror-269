# ZrO2
util functions for projects

## Features
This module contains a series of files, each providing extended utility functions specific to the module that it named. The goal is to primarily utilize standard libraries to ensure maximum compatibility. 

This project does not introduce additional dependencies. However, some files may require extra dependencies and co-dependencies. Please refer to the table below for detailed information.

## Install
### by pypi

```bash
pip install zro2
```

### by github

```bash
pip install git+https://github.com/ZackaryW/ZrO2.git
```

## Index

|    File     |    Non Std Dependencies    | Co-dependencies | Test State |
| ----------- | -------------------------- | --------------- | ---------- |
| hashlib     | [None]                     | [None]          | tested     |
| json        | [None]                     | [None]          | untested   |
| logging     | [None]                     | [None]          | tested     |
| pygetwindow | pygetwindow                | sceeninfo       | untested   |
| requests    | [None]                     | [None]          | untested   |
| screeninfo  | screeninfo, pygetwindow    | [None]          | untested   |
| typing      | [None]                     | [None]          | untested   |
| subprocess  | [None]                     | [None]          | untested   |
| keyring     | keyring                    | [None]          | untested   |
| io          | pyyaml, toml               | [None]          | untested   |
| time        | [None]                     | [None]          | untested   |
| easyocr     | easyocr, numpy             | [None]          | untested   |
| pyscreeze   | pyscreeze, screeninfo, PIL | [None]          | tested     |
| pandas      | pandas                     | [None]          | tested   |

## Update cycles
1. by default, this project will update util functions every 30 days (month)
2. a beta release will be made available each week

