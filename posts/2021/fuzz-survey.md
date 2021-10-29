---
date: 2021-10-27
category: Software engineering
tags: fuzz
blogpost: true
---

# A Survey on Fuzzing

> Conceptually, a fuzzing test starts with generating massive normal and abnormal inputs to target applications, and try to detect exceptions by feeding the generated inputs to the target applications and monitoring the execution states. [^1]

[^1]: https://cybersecurity.springeropen.com/articles/10.1186/s42400-018-0002

## Tutorial

- [Fuzzing with AFL workshop: AFL training](https://github.com/mykter/afl-training)
  - [video](https://www.youtube.com/watch?v=6YLz9IGAGLw)
  - [slides](https://docs.google.com/presentation/d/e/2PACX-1vQWx9bCm_WzSec1Okd8PM2vOf2TQRoM4snxsHSHSLWMfgSWzcJHxWkkdhRPw-a7Flq_5X2QpGI8vwUH/pub?start=false&loop=false&delayms=60000)
- [CMPSC 447 Software Security](http://www.cse.psu.edu/~gxt29/teaching/cs447s19/index.html)
   - [Testing and fuzzing](http://www.cse.psu.edu/~gxt29/teaching/cs447s19/slides/06testingFuzzing.pdf)
   - [White‐Box Fuzzing (Combining Testing and Symbolic Execution)](http://www.cse.psu.edu/~gxt29/teaching/cs447s19/slides/07staticAnalysis.pdf)


## Tool: AFL

![](/images/fuzz/afl-screenshot.png)

- Edge coverage: Inputs that cover **new branch(es)** will be added to the seed pool.

- test harness: wrap functions to narrow down the fuzzing range

![](/images/fuzz/harness.png)

## Some papers

- **[Reinforcement Learning-based Hierarchical Seed Scheduling for Greybox Fuzzing](https://scholar.archive.org/work/sxi4fekp2rdizcv3ad7itgg4vy/access/wayback/https://www.ndss-symposium.org/wp-content/uploads/ndss2021_6A-4_24486_paper.pdf)** *(NDSS'21)*
- [Android SmartTVs Vulnerability Discovery via Log-Guided Fuzzing](https://www.usenix.org/system/files/sec21fall-aafer.pdf) *(USENIX Security'21)*
- [Send Hardest Problems My Way: Probabilistic Path Prioritization for Hybrid Fuzzing](https://www.cs.ucr.edu/~heng/pubs/digfuzz_ndss19.pdf) *(NDSS'21)*
- [VDF: Targeted Evolutionary Fuzz Testing of Virtual Devices](https://www.cs.ucr.edu/~heng/pubs/VDF_raid17.pdf)


## Miscellaneous

- *[Cornell CS3110](https://www.cs.cornell.edu/courses/cs3110/2018sp/htmlman/afl-fuzz.html)* AFL + Ocaml