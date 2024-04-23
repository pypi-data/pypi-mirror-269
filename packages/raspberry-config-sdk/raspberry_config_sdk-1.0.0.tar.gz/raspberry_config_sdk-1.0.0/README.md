# Raspberry Config SDK ![Release](https://img.shields.io/github/v/release/DEADSEC-SECURITY/raspberry-config-sdk?label=Release&style=flat-square) ![Python_Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square) ![License](https://img.shields.io/github/license/DEADSEC-SECURITY/raspberry-config-sdk?label=License&style=flat-square) 

[![CodeQL](https://github.com/DEADSEC-SECURITY/raspberry-config-sdk/actions/workflows/codeql.yml/badge.svg)](https://github.com/DEADSEC-SECURITY/raspberry-config-sdk/actions/workflows/codeql.yml) 

![PyPI - Downloads](https://img.shields.io/pypi/dd/raspberry-config-sdk?label=Daily%20Downloads&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dw/raspberry-config-sdk?label=Weekly%20Downloads&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dm/raspberry-config-sdk?label=Monthly%20Downloads&style=flat-square)

## 📝 CONTRIBUTIONS

Before doing any contribution read <a href="https://github.com/DEADSEC-SECURITY/raspberry-config-sdk/blob/main/CONTRIBUTING.md">CONTRIBUTING</a>.

## 📧 CONTACT

Email: amng835@gmail.com

General Discord: https://discord.gg/dFD5HHa

Developer Discord: https://discord.gg/rxNNHYN9EQ

## 📥 INSTALLING
<a href="https://pypi.org/project/raspberry-config-sdk">Latest PyPI stable release</a>
```bash
pip install raspberry-config-sdk
```

## ⚙ HOW TO USE
```python
from raspberry_config_sdk.BootConfig import BootConfig, Option

config = BootConfig()
config.get_config("camera_auto_detect") # Option(path="camera_auto_detect", value="1", comments=[])
config.add_or_update_config(Option(path="camera_auto_detect", value="0", comments=[])) # Creates or Updates the value
config.save() # Saves to the file, restart is required for changed to take effect
```