---
date: 2021-11-17
category: Firmware
tags: Firmware Analysis, Symbolic Execution, Dynamic Analysis, Fuzzing
blogpost: true
---

# Automatic Firmware Emulation through Invalidity-guided Knowledge Inference

Link: https://www.usenix.org/confere/usenixsecurity21/presentation/zhou

## Code Utilization Attempts

### Set-up

- Code: https://github.com/MCUSec/uEmu
- Environment: Azure Counter-Small Ubuntu 20.04

#### Install Vagrant

```sh
sudo apt-get install virtualbox vagrant
```

````{error}
If `virtualbox --version` gives an error as `The character device /dev/vboxdrv does not exist. Please install the virtualbox-dkms package and the appropriate headers, most likely linux-headers-generic.`, try to disable secure boot in [BIOS configuration](https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/disabling-secure-boot?view=windows-11) and rebot.
````

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

![](/images/uEmu/vagrant.png)

`pwd` is `/home/vagrant`, the `uEmu/` folder on the host is mounted into `/vagrant/` folder on the vagrant VM. 

`````{dropdown}  **Install AFL ++** \*

```{note}
Usually, when you build the vagrant VM with 8 GB RAM, it will build `afl-fuzz` automatically (so the process may last for 3+ hrs). In this case, **just ignore this subsection**. However if you have difficulties with allocating RAM more than 4 GB, the `afl-fuzz` may also fail to build due to the limited RAM.
```

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
`````

`````{dropdown} **Access vagrant VM from VS code** \*
Although the host and VM share a mounted folder (`uEmu` / `/vagrant/`), which can be used to transfer files between them. To view the file strcuture clearly and edit files easily, we can also configure our VS code editor for remotely accessing the VM directly.

Print out the ssh configuration of the vagrant VM from the host terminal:

```sh
$ vagrant ssh-config
# Host default
#   HostName 127.0.0.1
#   User vagrant
#   Port 2222
#   UserKnownHostsFile /dev/null
#   StrictHostKeyChecking no
#   PasswordAuthentication no
#   IdentityFile /path/to/private_key
#   IdentitiesOnly yes
#   LogLevel FATAL
```

Copy the output to your `~/.ssh/config` file, change hostname `default` to whatever you like to distinguish it from other hosts (e.g. I use `vagrant`).

Install [Remote SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) for VS code, click here (on the bottom bar of VS) code window:

![](/images/uEmu/connect.png)

Then select "connect to host":

![](/images/uEmu/vs-ssh.png)

And choose "vagrant" host, open the `/vagrant` folder (or any other folder), then you can view and edit files like what you do on your local machine:

![](/images/uEmu/vs-remote.png)

````{note}
If your host is a remote host (like me, I also use Azure VM to test it), you have to first forward your local host port to corresponding remote host port, for example:

```sh
ssh -N -f -L localhost:2222:localhost:2222 your-remote-host
```

Don't forget to download the private key file to your local path and specify it in your local `~/.ssh/config` file.
````
`````

### Test Firmwares (`.cfg` included)

- https://github.com/MCUSec/uEmu-unit_tests
- https://github.com/MCUSec/uEmu-real_world_firmware

My re-organized real world firmware repo:

- https://github.com/li-xin-yi/uEmu-real_world_firmware

Use `git clone` to clone them into the local space.

### Usages

Since `launch-uEmu-template.sh`, `launch-AFL-template.sh`, `uEmu-config-template.lua` and `library.lua` must be placed in the same *work path* with the binary to test, First copy those files along with `uEmu-helper.py` into folder, for example:

```
cd /vagrant
cp launch-uEmu-template.sh launch-AFL-template.sh uEmu-config-template.lua library.lua uEmu-helper.py ~/uEmu-real_world_firmware
```

Enter the firmware folder:

```
cd ~/uEmu-real_world_firmware
```

#### Example: `P2IM.Drone.elf`

Extract KB:

```sh
python3 uEmu-helper.py P2IM.Drone.elf P2IM_Drone.cfg
```

Ignore the warnings. `launch-uEmu.sh` and `uEmu-config.lua` are generated from this command. Run `launch-uEmu.sh` to generate knowledge base (KB) file:

```sh
./launch-uEmu.sh
```

It mainly runs `S2E` for symbolic execution. Wait for a few minutes:

![](/images/uEmu/kb_extract.png)


A KB file `P2IM.Drone.elf-round1-state10-tbnum1371_KB.dat` (some numbers may differ) will be produced in `s2e-last`, copy it into `./` and then start dynamic analysis and fuzzing:

````{error}
Don't specify kb file like `s2e-last/P2IM.Drone.elf-round1-state10-tbnum1371_KB.dat` when generating `launch-AFL.sh` because the `s2e-last` will be overridden by outputs of the last execution of `s2e`, as `s2e` will serve as dynamic analyzer when fuzzing, the KB file might not be found when executing fuzzing and dynamic analysis. Copy the file out or use `s2e-out-xxx/xxx` as its path.
````

```sh
python3 uEmu-helper.py P2IM.Drone.elf P2IM_Drone.cfg -kb P2IM.Drone.elf-round1-state10-tbnum1371_KB.dat 
```

A `./launch-AFL.sh` appears after running the command. 


#### Example: XML_Parser

After reading `git log` of `uEmu-real_world_firmware`, I found that `WYCNINWYC` in the docs example is actually changed as `XML_Parser`. So I use it as an example here to run.

Extract KB:

```
python3 uEmu-helper.py XML_Parser.elf XML_Parser.cfg
```

Get `launch-uEmu.sh` and run it:

```
./launch-uEmu.sh
```

Get the KB file, copy it into `pwd` and generate AFL file:

```
cp s2e-last/XML_Parser.elf-round1-state51-tbnum1061_KB.dat ./
python3 uEmu-helper.py XML_Parser.elf XML_Parser.cfg -kb XML_Parser.elf-round1-state51-tbnum1061_KB.dat -s small_document.xml
```

Get `launch-AFL.sh` script, to run the fuzzing and dynamic analysis simultaneously, you need to start two terminals as:

````{panels}
**Terminal 1**

- Fuzzing (AFL)
- Input test-cases 

```
./launch-AFL.sh
```

---

**Terminal 2**

- Dynamic analysis (S2E)
- Consume test-cases

```
./launch-uEmu.sh
```

````

![](/images/uEmu/split.png)

When terminating AFL, the other process will end automatically.

### Reproduce the vulnerabilities

It is mentioned in the paper that uEmu helps in finding two previously unknown bugs in `Steering_Control` and $\mu$`TaskerUSB`.

#### $\mu$`TaskerUSB`

> The bug is caused by *out-of-bound write*. The USB driver only uses a receive buffer of 512 bytes to read an input of up to 1,024 bytes, resulting in DoS or data corruption.

```
python3 uEmu-helper.py uEmu-real_world_firmware/uEmu/uEmu_utasker_USB/uEmu.uTasker_USB.out uEmu-real_world_firmware/uEmu/uEmu_utasker_USB/uEmu_utasker_USB.cfg
./launch-uEmu.sh
cp s2e-last/3/uEmu.uTasker_USB.out-round1-state4086-tbnum1019_KB.dat ./
python3 uEmu-helper.py uEmu-real_world_firmware/uEmu/uEmu_utasker_USB/uEmu.uTasker_USB.out uEmu-real_world_firmware/uEmu/uEmu_utasker_USB/uEmu_utasker_USB.cfg -kb uEmu.uTasker_USB.out-round1-state4086-tbnum1019_KB.dat 
```

```{caution}
I modified `S2E_MAX_PROCESSES` as 4 in `launch-uEmu.sh` to make S2E run in 4 workers, but it still took 7695s to finish, which is much longer than the time (227s) marked in the paper. (I have already re-launched the vagrant VM with 16 cores and 48 GB RAM).

Related issue: https://github.com/MCUSec/uEmu/issues/8
```

Then start two screens to run `./launch-uEmu.sh` and `./launch-AFL.sh` respectively. After about 7 hours, it found some crashes as:

![](/images/uEmu/usb.png)

And a bunch of identical warnings in `s2e-last/warnings.txt` like:

```
AFLFuzzer: Kill Fuzz State due to out of bound read, access address = 0x21 pc = 0x800f7d8
```

```{note}
TODO: I don't have the source code of this firmware (*may be [this one](https://github.com/uTasker/uTasker-Kinetis/blob/master/uTasker/USB_drv.c)*) and can't locate the bug.

- I uploaded the binary to an online disassembler: https://onlinedisassembler.com/odaweb/WynTPuPS , and try to find out what instruction at `0x800f7d8` (it looks like jump to an external function at address `0x808dc24` as `BLCS` may refer to a conditional jump)
- Run the firmware with QEMU to see the crash

![](/images/uEmu/800f7d8.png)
```

####  `Steering_Control` 

Source: https://github.com/RiS3-Lab/p2im-real_firmware/tree/master/Steering_Control

> It is caused by a double-free of a string buffer, allowing for arbitrary write. More specifically, the firmware uses dynamic memory to store the received data from the serial port. If the memory allocation fails, the same buffer will be freed twice. 

`````{hint}
I guess it may refer to [L131-132](https://github.com/RiS3-Lab/p2im-real_firmware/blob/d4c7456574ce2c2ed038e6f14fea8e3142b3c1f7/Steering_Control/car_controller.ino#L131). As `command` and `value` are declared as `String`s:

```{code-block} cpp
---
linenos:
lineno-start: 58
---
String command; //Keep track of our command as it comes in
String value;
```

But assigned with `String`s read from `Serial`

```{code-block} cpp
---
linenos:
lineno-start: 131
---
      command = Serial.readStringUntil(','); //Read all of the command
      value = Serial.readStringUntil('\n'); //Read all of the value to set
```

I have almost no knowledge about Arduino, but at least for C/C++ (see [`std::string::operator=`](https://www.cplusplus.com/reference/string/string/operator=/)), `String` is allocated dynamically as it has undetermined length, `=` only copies the reference shallowly. When the *moved* string is deleted, it will issue an error when deleting `command` and `value` again, which happens automatically when the two variables are deconstructed. 

`````


```
python3 uEmu-helper.py uEmu-real_world_firmware/P2IM/P2IM_Steering_Control/P2IM.Steering_Control.elf uEmu-real_world_firmware/P2IM/P2IM_Steering_Control/P2IM_Steering_Control.cfg
./launch-uEmu.sh
```

## Code Analysis

[`uEmu-helper.py`](https://github.com/MCUSec/uEmu/blob/main/uEmu-helper.py): Read the firmware name, configuration (and knowledge base file, seed file) from CLI, fill out placeholders in 

- [`launch-uEmu-template.sh`](https://github.com/MCUSec/uEmu/blob/main/launch-uEmu-template.sh) to generate specified `launch-uEmu.sh`,
-  `launch-AFL-template.sh` to generate `launch-AFL.sh`, 
-  `uEmu-config-template.lua` to generate `uEmu-config.lua`, which is used in `launch-uEmu-template.sh` as S2E configuration file (actually useless except in debug mode)