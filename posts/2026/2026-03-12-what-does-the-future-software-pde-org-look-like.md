---
title: What does the future software PDE org look like?
date: 2026-03-12
tag: Reflection
---

I was listening to a wonderful [interview with Bret Taylor](https://www.youtube.com/watch?v=n4E4xNYCkYM) by John Collison. It got my brain gears spinning on this particular question:

What does a software PDE org look like in the next 12–18 months?

I think making predictions beyond this year is moot. Specifically in PDE because the rate of change of AI models is fastest here. If we see a plateauing of the improvement, then this prediction could hold true for longer.

Anyway, here is my take on it. I structure it as position, role, goal, why agents cannot do it, and why a human is needed.

- Product manager: Their role will be to talk a lot—to customers, internal teams, and employees. Their goal will be to produce a document that specifies what should be built, why, and what great looks like (including, but not limited to, evals, which are one way of defining "great" for agentic apps). The reason that an agent cannot do this job is that the CEO/management team has limited time and will want a dedicated human whose neck is on the line wrt the design of a product that delivers customer value and business results. I believe the biggest differences here vs. today will be (a) a 10–100x increase in scope—many product managers today are feature managers and not product managers—and (b) writing great evals and constructing the datasets against which agentic software is evaluated.

- Builder: Their role will be to translate the product manager's document into technical decisions (system architecture, data schema, jiving with legal and regulatory compliance, etc.) AND manage an army of agents to produce robust, working code. The reason that an agent cannot do this job is that the CEO/management team has limited time and will want a human whose neck is on the line wrt building & maintaining their product.

- Infra & safety: Their role will be to build & maintain stuff that goes around the product code—QA/QC, testing, A/B experiments, cybersecurity, PII, etc. For smaller companies, this role may not exist, but as companies grow bigger and have multiple products, they will create an infra support position. The reason that an agent cannot do this job is that the CEO/management team has limited time and will want a dedicated human whose neck is on the line wrt the risks created (customer trust, audits, legal).
