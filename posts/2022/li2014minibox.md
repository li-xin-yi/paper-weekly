---
date: 2022-01-28
category: Operating System
tags: PaaS
blogpost: true
---

# MiniBox: A Two-Way Sandbox for x86 Native Code (ACT'14)

Link: https://www.usenix.org/conference/atc14/technical-sessions/presentation/li_yanlin

## Problem to solve


Provides a two-way sandbox for x86 native code:

- **OS protection**: prevent a benign OS from a misbehaving app (e.g., sandbox)
- **App protection**: prevent an application from a malicious OS (e.g., SGX, enclave)

Risks in previously existing work:

![](/images/minibox/pre.png)

**Iago attack**: a malicious OS can subvert a protected process by returning a carefully chosen sequence of return values to **sensitive system calls**. 
  - For example, a malicious OS returns a memory address that is in the application’s stack memory for an `mmap` system call
  - sensitive data (e.g., a return address) in the stack may subsequently be overwritten by the mapped data.