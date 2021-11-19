---
date: 2021-11-17
category: Firmware
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

```sh
sudo apt-get install virtualbox vagrant
```

#### Download `uEmu`

```sh
git clone https://github.com/MCUSec/uEmu.git
cd uEmu
```

Modify the RAM allocation in [`uEmu/Vagrantfile`](https://github.com/MCUSec/uEmu/blob/dbba62a03a19e3aa021742165c4bd80d8a9eefcb/Vagrantfile#L58) to 8192 MB, or it may fail to build `afl-fuzz`:

```{code-block} sh
---
linenos:
lineno-start: 58
---
vb.memory = "8192"
```

#### Lanuch a virtual machine

Start a vritual machine from the vagrant file in the repo:

```sh
vagrant up  # this will take a while, please be patient
vagrant ssh # connect to the virtual machine
```

Now, you will enter the virtual machine:

#### Install AFL ++

From the [readme](https://github.com/AFLplusplus/AFLplusplus#building-and-installing-afl) of AFL ++

```sh
sudo apt-get update
sudo apt-get install -y build-essential python3-dev automake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools 
# try to install llvm 11 and install the distro default if that fails
sudo apt-get install -y lld-11 llvm-11 llvm-11-dev clang-11 || sudo apt-get install -y lld llvm llvm-dev clang 
sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-dev
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
make distrib
sudo make install
```

````{warning}

You may config `llvm` as `llvm-11` by:

```sh
export LLVM_CONFIG=/usr/bin/llvm-config-11
```

If it says that `ninja: command not found`, install `ninja` by:

```sh
sudo apt-get install ninja-build
```
````

#### Access from VS code

### Test Firmwares (`.cfg` included)

- https://github.com/MCUSec/uEmu-unit_tests
- https://github.com/MCUSec/uEmu-real_world_firmware

### Usages





