---
title: Why My AI food logger lost out to Lose It!, and what I believe it means for the future of apps
date: 2026-02-07
tag: Reflection
---

### Food logging experiment

I got Gemini CLI to help me build a custom food-tracking system that works through PowerShell in plain English. I cooked up 1–2 custom "skills," a CSV file as my database, and Python scripts (using the magic of pandas) to log meals, generate daily dashboards, and record everything. It was… nifty. For a few days, I was logging food from my terminal, though this could just as easily be Gemini/ChatGPT/Claude in the web browser or their apps. I felt like a digital health pioneer. Then, I defaulted back to Lose It! Why? It wasn't because my custom scripts were "bad" or inaccurate. It was because the friction of interaction slowly chipped away at my resolve.

### My observations

1. Dedicated "Spot" vs. Command Line: Lose It! has an app icon on my phone—a constant, subtle reminder to log. My CLI script? It lived in a terminal, buried in my work environment.

2. Mindset Shift: Tapping the Lose It! icon instantly puts me in "food logging mode." My CLI, however, lives in the same window where I'm debugging code or manipulating some local files. The mental context switch felt surprisingly heavy.

3. Click, Swipe & Tap vs. Type: Logging in Lose It! is a symphony of quick taps, barcode scans, and intuitive selections. My CLI demanded specific trigger words ("log meal A, B, C items") and zero typos.

4. Instant Dashboard vs. Prompting: Lose It! greets me with a visual dashboard—a quick glance tells me where I stand. My CLI required me to explicitly prompt it, wait a few seconds, and then parse text.


### Second-order implications

I believe my experience isn't just about my personal preference or this workflow; it highlights fundamental principles of how we interact with products and services.

Cognitive Load & Context Switching: My brain is already juggling work, family, and hobbies. Manually switching a CLI from "developer" to "nutritionist" every time I wanted to log food was exhausting. Dedicated apps eliminate this mental friction.

The "Glance" Factor (Pre-attentive Processing): Humans process visuals 60,000 times faster than text. A red/green bar on a dashboard instantly communicates "over/under." Reading numbers in a CLI requires active processing, which takes precious mental energy.

Interaction Cost: The time and effort to perform a task. For frequent actions like food logging, the "cost" of typing a precise command will always be higher than the "cost" of tapping a large, familiar button. Low-cost wins for high-frequency habits.

Information "Scent": A well-designed UI has "information scent"—visual cues that guide you effortlessly. A CLI is a blank slate; you have to generate the "scent" yourself by remembering commands.

### The Future of Apps

Why Lose It! will likely endure? I believe that dedicated apps like Lose It! aren't going anywhere, even as generative AI becomes more powerful. The future will likely be a hybrid:

Quick Actions Go Headless: The "easiest" parts of an app—the quick log ("Hey Gemini, I just ate two eggs") or the quick view ("Siri, how many calories do I have left?")—will become available directly in generalized chat apps. These will likely be powered by APIs connecting to specialized services (think of Lose It! as a "headless" calorie brain).

Deep Work Stays Dedicated: For more involved use cases like reviewing historical trends, performing multi-step diet adjustments, or exploring complex recipe builders, people will still go into the dedicated app. Why? These workflows are inherently harder to translate into a chat interface. They require dedicated and familiar interfaces, complex inputs, and often, multi-stage interaction.

Performance Physics: While generative UIs might eventually be able to create interfaces on the fly, they will always be slower than precompiled, natively optimized code and interfaces. For critical, high-frequency tasks, that time difference matters.

So, while my Python scripts were a fun experiment, for the serious business of tracking my food, I'm sticking with the app that respects my precious cognitive budget. Lose It! remains on my home screen, a constant, low-friction partner in my daily health journey.
