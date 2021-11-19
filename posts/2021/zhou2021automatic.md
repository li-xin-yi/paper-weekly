---
date: 2021-11-17
category: Firmware
tags: Vulnerability Fix, Machine Learning, NLP
tags: Firmware Analysis, Symbolic Execution, Dynamic Analysis, Fuzzing
blogpost: true
---

# Automatic Firmware Emulation through Invalidity-guided Knowledge Inference

Link: https://www.usenix.org/conference/usenixsecurity21/presentation/zhou

## Code Utilization Attempts

### Set-up

- Code: https://github.com/MCUSec/uEmu
- Environment: Azure Counter-Small Ubuntu 20.04

#### Install Vagrant

```
sudo apt-install virtualbox vagrant
```

#### Download `uEmu`

```
git clone https://github.com/MCUSec/uEmu.git
cd uEmu
```

Modify the RAM allocation in `uEmu/Vagrantfile` to 8194 MB, or it may fail to build `afl-fuzz`:


Start a vritual machine from the vagrant file in the repo:

```
git clone https://github.com/MCUSec/uEmu.git
cd uEmu
vagrant up  # this will take a while, please be patient
vagrant ssh # connect to the virtual machine
```



