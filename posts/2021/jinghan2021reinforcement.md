---
title: Reinforcement Learning-based Hierarchical Seed Scheduling for Greybox Fuzzing
date: 2021-11-04
category: Software Engineering
tags: Fuzzing, Reinforcement Learning
blogpost: true
---

# Reinforcement Learning-based Hierarchical Seed Scheduling for Greybox Fuzzing

link: https://www.cs.ucr.edu/~heng/pubs/afl-hier.pdf


````{code-block} C
---
linenos:
---
char maze[7][11] = {
    "+-+---+---+",
    "| |     |#| " ,
    "| | --+ | | " ,
    "| |   | | | " ,
    "| +-- | | | " ,
    "|     |   | " ,
    "+-----+---+" };
int x = 1 , y = 1;
for (int i = 0; i < MAX_STEPS; i++) {
    switch (steps[i]) {
        case 'u': y--; break;
        case 'd': y++; break;
        case 'l': x--; break;
        case 'r': x++; break;
        default :
        printf( "Bad step!" ); return 1;
    }
    if (maze[y][x] == '#') {
        printf( "You win!");
        return 0;
    }
    if (maze[y][x] != ' ') {
        printf( "You lose.");
        return 1;
    }
}
return 1;
````