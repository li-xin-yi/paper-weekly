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