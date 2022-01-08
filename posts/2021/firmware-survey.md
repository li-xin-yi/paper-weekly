---
date: 2021-12-25
category: Firmware
tags: Firmware
blogpost: true
---

# A Survey on Firmware Security

## List Summary

Paper List:
- https://github.com/onehouwong/Firmware-Analysis-Papershttps://github.com/onehouwong/Firmware-Analysis-Papers 

Course: 
- https://mews.sv.cmu.edu/teaching/14829/f18/files/firmware-analysis-tutorial.pdf

Toolkit:
- https://github.com/attify/firmware-analysis-toolkit

## Binary Analysis

From [this slides](https://mews.sv.cmu.edu/teaching/14829/f18/files/firmware-analysis-tutorial.pdf), we can view firmware releases as some kind of *executable binaries*, so many binary analysis (*especially some black-box*) techniques can also be applied on firmware. Those tools can give a quick insight on the firmware to analysis. To demonstrate these CLI on Linux, we can take samples in [my re-organized firmware collection](https://github.com/li-xin-yi/uEmu-real_world_firmware) as examples and then test with those tools.



````{list-table}
:header-rows: 1
:widths: 5 20 20

* -  
  - Usage
  - Example
* - `file`
  - Test file type (format) 
    Note: If the file format of the provided firmware image is unknown, then `file` will simply report that it contains binary data
  - ```sh
    $ file P2IM.Steering_Control.elf 
    # P2IM.Steering_Control.elf: 
    # ELF 32-bit LSB executable, 
    # ARM, EABI5 version 1 (SYSV), statically linked, 
    # with debug_info, not stripped
    ```
* - `strings`
  - Extract printable strings in file
  - ```sh
    $ strings P2IM.Steering_Control.elf | head
    # L#x3
    # O"F)F
    # ...
    # 9M(`4H
    ```
* - `hexdump`
  - Display binary files in hexadecimal
  - ```sh
    $ hexdump -C P2IM.Steering_Control.elf | head
    # ...
    ```
````

#### `binwalk`

> Binwalk is a fast, easy to use tool for analyzing, reverse engineering, and extracting firmware images

```
$ git clone https://github.com/ReFirmLabs/binwalk
$ cd binwalk
$ sudo python3 setup.py install
```

````{list-table}
:header-rows: 1
:widths: 5 20 20

* -  
  - Usage
  - Example
* - `--entropy`
  - inspection of regions with high entropy (compressed or encrypted data)
  - ```sh
    $ binwalk --term --entropy P2IM.Steering_Control.elf
    ```
````

#### `binvis`

`binvis` generates a **visualization** of the firmware image with space-filling curves in order to identify regions with non-random data.

[cortesi/scurve](https://github.com/cortesi/scurve) is not updated from many years ago, many dependencies are deprecated. 

- Todo: I may modify it later to fix those issues when I have time.
  
But we can upload the firmware file to http://binvis.io/ to view the results.
