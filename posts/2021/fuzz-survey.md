---
date: 2021-10-27
category: Software Engineering
tags: Fuzzing
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

```{seealso}
Understanding the status screen: https://afl-1.readthedocs.io/en/latest/user_guide.html
- **Total crashes**: the number of different inputs that cause a crash. **unique** means the occurance of this crash takes a different execution path through the program. (not *unique bugs*)
- **Total paths**: unique execution path driven by all inputs.
- **Hangs:** timeout caused by the inputs.
- **Total execs**: the total number of executions. (i.e. how many times the program is executed)
- **Map coverage**: it maintains a global map where the hashed value of an edge (i.e., the pair of the current basic block address and the next basic block address) is used as an
indexing key.
  - observed by the instrumentation embedded in the target binary
  - **map density** shows how many branch tuples it have alreadly hit (for current input), in proportion to how many the bitmap can hold (for the entire input corpus).
  - **count coverage**: indicates the *variability* in tuple hit counts seen in the binary.
    - *In essence, if every taken branch is always taken a fixed number of times for all the inputs we have tried, this will read "1.00". As we manage to trigger other hit counts for every branch, the needle will start to move toward "8.00" (every bit in the 8-bit map hit), but will probably never reach that extreme.*
```

![](/images/fuzz/afl-screenshot.png)

- Edge coverage: Inputs that cover **new branch(es)** will be added to the seed pool.

- Test Harness: wrap functions to narrow down the fuzzing range

![](/images/fuzz/harness.png)

## Some papers

- **[Reinforcement Learning-based Hierarchical Seed Scheduling for Greybox Fuzzing](https://scholar.archive.org/work/sxi4fekp2rdizcv3ad7itgg4vy/access/wayback/https://www.ndss-symposium.org/wp-content/uploads/ndss2021_6A-4_24486_paper.pdf)** *(NDSS'21)*
- [Android SmartTVs Vulnerability Discovery via Log-Guided Fuzzing](https://www.usenix.org/system/files/sec21fall-aafer.pdf) *(USENIX Security'21)*
- [Send Hardest Problems My Way: Probabilistic Path Prioritization for Hybrid Fuzzing](https://www.cs.ucr.edu/~heng/pubs/digfuzz_ndss19.pdf) *(NDSS'21)*
- [VDF: Targeted Evolutionary Fuzz Testing of Virtual Devices](https://www.cs.ucr.edu/~heng/pubs/VDF_raid17.pdf)
- [FuzzGen: Automatic Fuzzer Generation](https://www.usenix.org/conference/usenixsecurity20/presentation/ispoglou)

## Basic Notes
  


`````{panels}

---

**Black‐box fuzzing**:

- Treating the system as a **blackbox** during fuzzing;
- **not knowing** details of the implementation;
- Feed the program **random** inputs and see if it crashes;

---

**White‐box fuzzing**:

- Design fuzzing based on internals of the system;
- Combines **test generation** with fuzzing (*static analysis*/*symbolic execution*);
- Goal: Given a sequential program with a set of input parameters, generate a set of inputs that maximizes code coverage


`````

### Greybox Fuzzing

Grey‐box fuzzing is also called *coverage‐Based fuzzing*. It instruments the program, instead of simply treating the program as a black-box, to trace coverage (e.g. path, edge, code, etc.)

![](/images/fuzz/greybox-fuzz-workflow.png)

1. New inputs are generated through *mutation* and *crossover/splice* on seeds;
    - Only a few inputs from the seed pool will be scheduled to generate the next batch of inputs (due to the limited processing capability)
    - *For example, a single fuzzer instance can only schedule one seed at a time*
2. The generated inputs are selected according to a *fitness function*;
3. Selected inputs are then added back to the seed pool for further mutation;

The details of a genetic fuzzing process can be described as:

![](/images/fuzz/greybox-algo.png)

1. Given a program $P$ and a set of initial seeds $S^0$; *(Input)*
2. Each round starts with selecting the next seed for fuzzing according to the *scheduling criteria*; *(Line 5)*
3. Assign a certain amount of *power* to the scheduled seed, determining how many new test cases will be generated; *(Line 6)*
4. Test cases are generated through (random) mutation and crossover based on the scheduled seed; *(Line 9)*
5. Compared to blackbox and whitebox fuzzing, the most distinctive step of greybox
fuzzing is that, **when executing a newly generated input $I$, the fuzzer uses lightweight instrumentations to capture runtime features and expose them to the fitness function to measure the "quality" of a generated test case** ;

```{note}
  - Test cases with good quality will then be saved as a new seed into the seed pool; *(Line 13-14)*
  - This step allows a greybox to gradually evolve towards a target (e.g., more coverage).
```





## Miscellaneous

- *[Cornell CS3110](https://www.cs.cornell.edu/courses/cs3110/2018sp/htmlman/afl-fuzz.html)* AFL + Ocaml