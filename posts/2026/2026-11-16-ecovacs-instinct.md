---
title: "$1 and 3 hours later...I can run my ecovacs robo vaccum via Instinct"
date: 2026-11-16
---

## What did you build?
The ability to control my robo vaccum (the Ecovacs N30 pro omni) directly from Instinct (the chat based assistant).

## How did I build it?
Took about 3 hours end to end. Of which half was coding and the other half was test runs. Needless to say the kitchen was spotless.

- Some googling led me to stumble upon the official ecovacs mcp (https://open.ecovacs.com). Bless them. But more interestingly, Deepseek actually found an approach that offers me more fine-grained control than the official mcp . What do I mean by fine grained? Picking particular rooms, adjusting vaccum suction power etc. which are not available in the official mcp.
- Instinct (bless them) has access to it's own computer, including a shell from which it can run commands. So when I send Instinct a message like 'mop the dining area', it translates that into the right command, opens a shell, establishes a connection to the robot and fires away the instruction.
- Details: I used Pi as the coding agent running deepseek-v4.1-flash on 'high' effort. Took about $0.1 (10 rupees) to get to a bare bones working version and $1 total as I iterated through and fixed bugs. Instinct (bless them) can also work in a github repo. So in a sense it was deepseek & Instinct (via whatever model they used) riffing off of each other to fix bugs and improve the code.

## What did you learn?
I love it! I don't have to make the effort of finding the app, manually selecting a room on the map it has drawn, and then scrolling down to adjust the cleaning settings. I can just say what I want and see it done. Instinct acts as a beautiful universal interpretor from English -> commands/code that a computer can run.

## Give it to me
Email chinmay27.deo@gmail.com for the codebase.
