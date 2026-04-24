---
title: To learn something well, start small and follow historical evolution
date: 2026-04-24
tag: Reflection
---

I have been heads down the past ~3 weeks understanding agents. I played around with them, I listened to podcasts, explored github repos.
H/T to smol-agents (huggingface) and pi (mario zechner). I am on board with their phiosophy of building minimal coding agents and letting the models do the work, especially as they improve. I particularly liked the smol-agents approach of stripping down tools and instead letting agents construct custom approaches on the fly.

In that vein, I said let's start from the beginning, start small, and follow the historical evolution of agents. With that, i created micro-agent (https://github.com/legodud3/micro-agent), the simplest possible agent to understand the core concepts:

1. Loading 'helper stuff' like config, system prompt, environment variables

2. Understanding the concepts of chat history (i.e. "memory") and how that is built and fed to the model

3. Understanding the 'harness' role

4. Understanding tool calling -- tool definition, execution loops

Let's see where my exploration takes me next!