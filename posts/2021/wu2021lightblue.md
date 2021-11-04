---
date: 2021-9-25
category: Firmware
tags: Firmware Analysis, Symbolic Execution
blogpost: true
---

# LIGHTBLUE: Automatic Profile-Aware Debloating of Bluetooth Stacks (USENIX Security'21)

## Source

- Paper & Presentation: https://www.usenix.org/conference/usenixsecurity21/presentation/wu-jianliang

<!-- more -->

## Problem to Solve

Bluetooth standards and their implementations are diverse and complex, which contains many functionalities that **never be required** in the common scenarios. Those **useless** parts actually extend the **attack surface**.

`LIGHTBLUE` is a framework that performs **automatic**, profile-aware debloating of Bluetooth stacks. It allows users to automatically minimize their Bluetooth attack surface by removing _unneeded_ Bluetooth features and introduce no performance overhead or effect on the behaviors.

## Methodology

The workflow of `LIGHTBLUE`:

![Workflow of `LIGHTBLUE`](/images/wu2021lightblue/workflow.png)

`LIGHTBLUE` takes an application and a Bluetooth stack implementation (host code + firmware) as inputs. `LIGHTBLUE` has three parts: 1. profile identification 2. host code analysis 3. firmware analysis

### Profile Identification

```{admonition} Purpose
In step 1, LIGHTBLUE first identifies what profile is used by the application.
```

As that the host code provides **fixed interfaces** to the application so that the application can use the functionalities provided by the profile. For example:

- In Android, the call of [`getProfileProxy`](<https://developer.android.com/reference/android/bluetooth/BluetoothAdapter#getProfileProxy(android.content.Context,%20android.bluetooth.BluetoothProfile.ServiceListener,%20int)>) API can return the interfaces of a specific profile.
- On Linux, the application can access the profile provided by the Bluetooth stack
  by accessing the relevant [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/) services.

To identify those profiles, `LIGHTBLUE` scans for these interfaces in app's code.

### Host Code Analysis

```{admonition} Purpose
In step 2-3, `LIGHTBLUE` analyzes the source code of the host, performing a *profile-aware dependence* analysis and generates a *profile-aware dependency* graph. Removing the code **outside** this graph, a host code is successfully **debloated**.
```

Since a profile is exposed as a series of APIs/functions to the application, `LIGHTBLUE` builds the **call graph** (including all potential reachable functions in the host code) by a _conservative approach_.

````{note}
A *conservative* approach means that it will add **all** function in all instructions to the call graph in case missing any runtime called functions. **It absolutely leads to an over-approximation.** For example, the host code includes some *dispatching* functions like:

```c
// `service_id` represents the profile currently executed
// base on this value, only 1 of 3 function call will be actually executed
// however, the conservative way will take all three functions into the call graph
// Therefore, the number of reachable function is over-estimated for a certain profile 
bt_status_t btif_in_execute_service_request(
    tBTA_SERVICE_ID service_id, BOOLEAN b_enable){
  switch (service_id){
    case BTA_HFP_SERVICE_ID :
        btif_hf_execute_service (b_enable); break;
    case BTA_A2DP_SOURCE_SERVICE_ID :
        btif_av_execute_service (b_enable); break;
    case BTA_A2DP_SINK_SERVICE_ID :
        btif_av_sink_execute_service (b_enable); break;
    ...}
}
```
````

`LIGHTBLUE` adds a dummy function invoking the different functions exposed by a specific profile to make sure the program has a **single** entry point so that existing traditional *data-flow* analysis approach can be applied to detect the exact functions called in dispatching functions: LIGHTBLUE takes the constant values within the profile interface functions as the *source*, and *propagates* them across the host code, using an approach similar to what is proposed in [TRIMMER](http://www.csl.sri.com/users/gehani/papers/ASE-2018.Trimmer.pdf). Finally, `LIGHTBLUE` scnas each functiin for conditional jumps and check if the conditional value is known. For a known conditional value, it removes the basic blocks that are only reachable from the **unsatifiable** branches, which helps build a smaller and more accurate profile-aware call graph. All code outside the profile dependency graph is removed.

### HCI Command Extraction

```{admonition} Purpose
In step 4, a list of HCI (*Host Controller Interface*) commands used by the target profile is extracted, which guide to remove the unneeded functionalities in the firmware.
```

As **HCI send/receive interfaces** are well-defined, `LIGHTBLUE` can extract all HCI commands used from the dependency graph. It performs a *data-flow analysis* from all the functions in the profile dependency graph to the HCI interfaces. Then, it gets the used HCI commands by recovering the first two bytes used to generate the HCI packet.

```{tip}
The data format of HCI command:

![](/images/wu2021lightblue/hci-format.png)

The opcode differentiates HCI commands and has the Opcode Command Field (OCF) and the Opcode Group Field (OGF). The parameter field depends on the opcode.
```

> These two bytes contain the OGF and OCF fields of the packet, and they determine the invoked HCI command. For instance, if the first two bytes are `0x0405`, LIGHTBLUE recovers `OGF` and `OCF` by extracting the upper 6 bits and lower 10 bits. Based on the value of OGF and OCF (`0x1` and `0x5`), the HCI command is a `Create Connection` command.

### Firmware Analysis and Patching

```{admonition} Purpose
With a given firmware's binary, in step 5, `LIGHTBLUE` analyzes it to find the code to handle HCI commands; in step 6, `LIGHTBLUE` can identify the interfaces for setting up different types of links based on the identified code that handles the HCI commands. In step 7. `LIGHTBLUE` patches the firmware by debloating the unneed functionalities, which includes the code handling unneeded HCI commands (according to what are extracted in step 4) and the unneeded link interfaces of profile. Finally, the output is the compiled host code and the patched firmware.
```

```{attention}
How to identify HCI command dispatcher?
```

The HCI command dispatcher often needs to perform bitwise operations to extract the `OGF` and `OCF` values from opcode during parsing. For example:

```{code-block} C
---
linenos:
emphasize-lines: 2-4
---
bt_status_t bthci_cmd_dispatcher(PTR* hci_cmd_pkt){
  opcode = *(hci_cmd_pkt + 9);
  OGF = opcode >> 10;
  OCF = opcode & 0x3ff;
  handler = error_cmd_handler;
  switch(OGF) {
    case 0x01: switch(OCF) {
    case 0x01: handler = handle_inquiry; break;
    ...}
    ...
    default: // handling error HCI command
      handler = error_cmd_handler; break;}
  handler(hci_cmd_pkt);
}
```




