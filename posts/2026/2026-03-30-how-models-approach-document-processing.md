---
title: How models approach document processing
date: 2026-03-30
tag: Reflection
---

I decided last week to shift from (using AI to build vanilla software) --> (using AI to build software with AI features). This is a not-so-subtle shift in my view because I believe that unless a product has real AI enabled features it a) is liable to be subsumed by general purpose consumer applications b) it cannot improve as the underlying models improve. 
[I am aware that I have made 0 progress on "building distribution with AI". I grade myself an F for that. I promise I will come back to it.]

Anyway, as a first step in the shift towards building software with AI features, I thought it prudent to dive into the laundry list of model capabilities i.e. what can they actually do? Turns out that the claim is "quite a lot".  I started with Gemini as an example (https://ai.google.dev/gemini-api/docs). This post is about the document processing capabilities of Gemini. I ran the following experiment:

I created a pdf file (wrong-math.pdf) with nonsensical math inside it, that would be 'taken in' by a python script. The user can ask a question in English in the terminal, and the question along with the document is 'passed' to the model for an answer. [Side note: This is long context window processing not RAG i.e. the entire file outputs are just shoved into the model because they can now take in 1000s of pages of pdfs in one go]

The models seem to understand intuitively that when a file is supplied, the order of operations is:

1. check pdf for answer. even if it is nonsensical, assume it to be god given truth and roll with it. their first bias is to act as fancy xlookup systems.

2. ELSE use pdf+logical reasoning to pattern match to an answer. It genuinely tries to look for patterns in the file so it can extrapolate from them.

3. ELSE ignore pdf and use training data to answer

Quite interesting!

## "wrong-math.pdf" contents:

1+1=3.1

1+2=0.4

1+3=53

1+4=100

1+1=2

## Experiment results (User input, model thought process, model output)

| Question | Thought | Answer |

|----------|---------|--------|

| what is 1+4? | **My Analysis of the User's Query**<br><br>Okay, so I've got this image or PDF with some OCR'd text, and the user's asking "what is 1+4?". My process needs to be methodical and, above all, adhere strictly to the data provided, not my own knowledge. I'm operating under the assumption that the user wants my derived answer, based on the input.<br><br>I've got the following:<br><br>OCR text that looks like a series of equations. It includes lines such as "1+1=3.1", "1+2=0.4", and, crucially, "1+4=100".<br><br>My strategy is simple: pinpoint "1+4" within that jumble of text. Then, I need to extract the corresponding answer, no more, no less. I will treat the OCR output as a definitive source.<br><br>I see it! "1+4=100".<br><br>Therefore, according to the OCR-extracted data, the answer is... 100. | Based on the document provided, 1+4 = 100. |

| what is 1+1? | **My Analysis of the "1+1" Query**<br><br>Okay, here's what's happening. The user gave me some text, presumably from an image or PDF containing several mathematical statements. The core question is straightforward: "What is 1+1?". My approach, as an expert in information extraction and interpretation, is to break this down methodically.<br><br>First, I need to analyze the data provided, which in this case is a set of OCR'd equations. I quickly identify the relevant lines: 1+1=3.1, 1+2=0.4, 1+3=53, 1+4=100, and 1+1=2.<br><br>Next comes the crucial evaluation of "1+1". I immediately spot a conflict: the document, rather perplexingly, has two different answers for this simple calculation. This presents a unique challenge, because I am not only expected to provide the answer, but to accurately represent the data provided to me.<br><br>Standard arithmetic dictates that 1+1=2, but I can't ignore the context of the document. I need to be precise, and I am being instructed to follow the information provided by the document. This is not a situation where I am expected to correct errors, or apply my own knowledge. Therefore, my answer needs to reflect the conflict.<br><br>The best strategy is to directly and clearly present both values that I observe within the document. In this case the two answers are 3.1 and 2. Based on the context of the user, the best answer will be succinct and to the point. Therefore, I will respond, "According to the document, 1+1 is listed as both 3.1 and 2." | Based on the provided document, 1+1 is listed as both 3.1 (in the first line) and 2 (in the last line). |

| what is 4+1? | **Analyzing the "4+1" Inquiry**<br><br>Okay, let's break this down. The user has given me an image or PDF containing equations and wants to know what "4+1" equals. First, I need to look at the data provided. I see a list of assignments: 1+1=3.1, 1+2=0.4, 1+3=53, 1+4=100, and then a confusing "1+1=2". Immediately, I can see this isn't standard math. It looks like a system of arbitrary definitions, or possibly a test for an OCR system.<br><br>My primary thought is to evaluate the logical pattern. The question asks about "4+1", but the data gives "1+4=100" directly. The key is to see if the standard mathematical property of commutativity (a+b = b+a) holds true in this system. Does the document specifically define "4+1"? No, but it does define "1+4" as 100. The last line says "1+1=2", which is standard math. So there's a mix of standard math and arbitrary assignments. Since the document states "1+4=100", and assuming that the commutative property holds, the most logical answer is 100.<br><br>However, I need to check for inconsistencies. Ah, here's a wrinkle: "1+1" has two definitions: 3.1 and 2! This strongly suggests the system is either inconsistent or just a set of arbitrary assignments. Still, since 1+4 is defined as 100 and it's most logical to assume commutativity, I'm going with 100. It doesn't seem to be a pattern or sequence. I need to make sure my answer is as clear as possible.<br><br>Okay, let's draft a response. I'll focus on directly referencing the provided text and explain the rationale so the user understands the context. I'll offer the 100 result first and mention standard mathematics as a point of reference. I want to convey my thinking process. So, I will say, "Based on the document provided, 1+4 = 100. Therefore, assuming standard commutative rules apply, 4+1 would be 100 (though in normal mathematics, it is 5)." | Based on the document provided, 1+4 = 100. Assuming the commutative property of addition applies to these custom rules (where 1+4 is the same as 4+1), the answer is 100. (Note: In standard mathematics, 4+1 = 5, but based on the specific logic in your image, it points to 100). |

| what is 4+4? | **Analyzing the Numerical Puzzle**<br><br>Okay, here's the situation. The user provides a snippet of text from an image (or OCR output) that includes some equations. The user is asking "what is 4+4?". My immediate reaction is to analyze the data provided and see if a pattern emerges. The OCR provides:<br><br>1+1 = 3.1<br>1+2 = 0.4<br>1+3 = 53<br>1+4 = 100<br>1+1 = 2<br><br>At first glance, this is confusing. There doesn't appear to be any standard mathematical relationship here. Could this be a known riddle? A specific base system? A date-related trick? I quickly rule out date formats, and, let's face it, most standard tricks.<br><br>The last line, "1+1 = 2", is the key. That's standard math. It looks like the earlier examples are meant to be confusing. So, the question, "what is 4+4?" is likely just a straightforward arithmetic problem. It's a test of whether I can ignore the nonsensical context and apply known rules.<br><br>Is there any deeper function or letter counting trick? Could it be a typo? I look at the numbers again: 3.1, 0.4, 53, 100, 2. No, there's no obvious function there. If it was a base issue, the numbers would not work.<br><br>I consider the possibility of OCR errors, maybe the decimals have significance, but 1+1=2 is the key.<br><br>Let's look at the equations again. Could they be test cases?<br><br>I quickly search my knowledge base for "1+1=3.1" "1+2=0.4" "1+3=53" "1+4=100", but nothing jumps out.<br><br>It's likely that the answer is 8. The examples provide nonsense and the last line implies standard math applies.<br><br>My final thought is that this is a test of context understanding. So, despite the inconsistent equations, standard arithmetic is valid. The answer is 8. | Based on standard arithmetic, 4 + 4 = 8. While the document provided lists several inconsistent or incorrect mathematical statements (like 1+1=3.1 and 1+4=100), the final line (1+1=2) establishes that standard mathematical rules still apply! |