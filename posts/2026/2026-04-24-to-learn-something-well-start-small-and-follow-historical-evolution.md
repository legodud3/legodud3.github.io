---
title: To learn something well, start small and follow historical evolution
date: 2026-04-24
tag: Reflection
---

I have been heads-down for the past ~3 weeks understanding agents. I played around with them, listened to podcasts, and explored GitHub repos.

H/T to smol-agents (Hugging Face) and pi (Mario Zechner). I am on board with their philosophy of building minimal coding agents and letting the models do the work, especially as they improve. I particularly liked the smol-agents approach of stripping down tools and instead letting agents construct custom approaches on the fly.

In that vein, I said, let's start from the beginning, start small, and follow the historical evolution of agents. With that, I created [micro-agent](https://github.com/legodud3/micro-agent), the simplest possible agent to understand the core concepts:

1. Loading 'helper stuff' like config, system prompt, environment variables

2. Understanding the concepts of chat history (i.e., "memory") and how that is built and fed to the model

3. Understanding the 'harness' role

4. Understanding tool calling—tool definition and execution loops

Let's see where my exploration takes me next!
