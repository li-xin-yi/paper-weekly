---
date: 2021-9-25
category: firmware
tags: firmware analysis, symbolic execution
blogpost: true
---

# LIGHTBLUE: Automatic Profile-Aware Debloating of Bluetooth Stacks (USENIX Security'21)

## Source

- Paper & Presentation: https://www.usenix.org/conference/usenixsecurity21/presentation/wu-jianliang

<!-- more -->

## Problem to Solve

Bluetooth standards and their implementations are diverse and complex, which contains many functionalities that **never be required** in the common scenarios. Those useless parts actually extend the **attack surface**.

`LIGHTBLUE` is a framework that performs **automatic**, profile-aware debloating of Bluetooth stacks. It allows users to automatically minimize their Bluetooth attack surface by removing _unneeded_ Bluetooth features and introduce no performance overhead or effect on the behaviors.

## Methodology

The workflow of `LIGHTBLUE`:

![Workflow of `LIGHTBLUE`](/images/wu2021lightblue/workflow.png)

`LIGHTBLUE` takes an application and a Bluetooth stack implementation (host code + firmware) as inputs. `LIGHTBLUE` has three parts: 1. profile identification 2. host code analysis 3. firmware analysis

### Profile Identification

```{admonition} Purpose
In step 1, LIGHTBLUE first identifies the profile used by the application.
```

As that the host code provides **fixed interfaces** to the application so that the application can use the functionalities provided by the profile. For example:

- In Android, the call of [`getProfileProxy`](<https://developer.android.com/reference/android/bluetooth/BluetoothAdapter#getProfileProxy(android.content.Context,%20android.bluetooth.BluetoothProfile.ServiceListener,%20int)>) API can return the interfaces of a specific profile.
- On Linux, the application can access the profile provided by the Bluetooth stack
  by accessing the relevant [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/) services.

To identify those profiles, `LIGHTBLUE` scans for these interfaces in app's code.

### Host Code Analysis

```{admonition} Purpose
In step 2-4, `LIGHTBLUE` analyzes the source code of the host, performing a *profile-aware dependence* analysis and generates a *profile-aware dependency* graph. Removing the code **outside** this graph, a host code is successfully **debloated**.
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

`LIGHTBLUE` adds a dummy function invoking the different functions exposed by a specific profile to make sure the program has a **single** entry point so that existing traditional *data-flow* analysis approach can be applied to detect the exact function called in dispatching functions.
