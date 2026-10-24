---
title: "Cutting my coding agent from 119k to 8k tokens"
date: 2026-10-24
---

A straightforward multi-file data query (orders.csv + models.json) was burning through a surprising amount of context on my setup, so I ran the same task five times, changing the setup between runs, and tracked the cumulative tokens sent to the API on each run. The numbers swung wildly: 119k → 56k → 80k → 50k → 8k.

This is one task on one machine, not a benchmark. But watching the counter on each run taught me more about where tokens actually go than any amount of prompt folklore.

```chart
{
  "type": "bar",
  "data": {
    "labels": ["A: verbose rules", "B: no rules", "C: custom rules", "D: env facts only", "E: Pi runtime"],
    "datasets": [
      {
        "label": "Cumulative tokens sent to the API (thousands)",
        "data": [119, 56, 80, 50, 8]
      }
    ]
  },
  "options": {
    "responsive": true,
    "maintainAspectRatio": false,
    "plugins": {
      "title": {
        "display": true,
        "text": "Same task, five runs"
      },
      "legend": {
        "display": false
      }
    },
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": {
          "display": true,
          "text": "Cumulative tokens (thousands)"
        }
      }
    }
  }
}
```

## Run A: 119k tokens, the verbose rule trap

My starting point: a long, highly detailed global rules file on top of Cline's default IDE extension harness. The agent burned 5 turns. It swallowed huge chunks of raw CSV and JSON via read_file on turn 1, hit CRLF line-ending errors with awk, then got stuck in "second-opinion" loops re-verifying its own math. Meanwhile, Cline's base system prompt (~12.5k tokens on my setup, full of browser tools and MCP schemas) was re-injected on every turn. Cumulative context: 119k.

## Run B: 56k, no rules at all

I wiped the global rules completely for a clean baseline. Usage dropped by more than half to 56k over 3 turns. Without instructions micromanaging every step, the model moved faster and skipped the redundant verification passes. First clue: my elaborate rules were making the agent *less* efficient, not more.

## Run C: 80k, custom rules round one

I wrote new structured global instructions (cli-tools.md) telling the agent to inspect schemas first and avoid bad commands. Usage bounced back up to 80k over 5 turns, and the agent again ran the same failing verification passes on \r\n line endings - the exact behavior the new rules were written to prevent. Whatever the mechanism, the rules didn't produce the behavior I asked for.

## Run D: 50k, environment facts only

I stripped all workflow micromanagement and cut the rules down to pure environment facts: which Homebrew binaries are installed (duckdb, jq, ast-grep), which interactive CLIs hang (bat, fzf), plus some safety protections. Usage settled at 50k over 4 turns. This looked like the ceiling of the Cline/VS Code harness: ~12.5k tokens of built-in tool schemas and IDE overhead rode along on every turn no matter how clean my prompt was.

## Run E: 8k, switching runtime to Pi

I moved from Cline to Pi, a lean terminal-first agent, moved my rules from AGENTS.md into Pi's APPEND_SYSTEM.md (which appends them to the system prompt), and let Pi read files surgically with line ranges (:1-50) instead of whole files. The task finished in 2 clean, Python-driven turns. Pi's UI showed ~2k completion tokens, but the true apples-to-apples cumulative context sent to the API was ~8k: an 84% drop from Run D and 93% below where I started.

## What I learned

- **My longest rules were my most expensive ones.** The rules that actually helped were short environment facts about what tools exist, not instructions on how to code.
- **Negative constraints didn't earn their tokens.** In Run C I banned the bad commands by name, and the agent still took the wrong path. I'm not claiming I know why; only that those rules cost tokens without changing the outcome.
- **Harness overhead was the biggest line item.** On my setup, ~12.5k tokens of system prompt and tool schemas went out on every turn before the model saw a single line of my task. My leanest Cline run still carried that overhead; the big drop came when the harness changed.
- **The biggest drop came with the runtime switch.** Run E changed several things at once - the harness, where my rules live, and how the agent reads files - so I can't pin the whole 50k to 8k on the harness alone. But that combined change is where the math moved.

## What I gave up

The 8k setup isn't free. I lost the GUI diff previews before file writes. And a terminal agent runs shell commands immediately, so I wrote a small TypeScript extension (safety.ts, ~25 lines) that intercepts .env reads and asks before destructive commands like rm -rf. A reasonable trade for my usage, but it is a trade.

My biggest takeaway: the model didn't need more rules, it needed fewer obstacles. Matching my instructions to my actual stack and moving to a lightweight terminal runtime cut token consumption by over 80% on this task without losing capability. Your mileage will vary, but measure it. The counter doesn't lie.
