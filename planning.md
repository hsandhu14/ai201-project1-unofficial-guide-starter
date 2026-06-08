# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My Unofficial Guide focuses on student reviews and experiences with Computer Science and Systems professors at the University of Washington Tacoma. This knowledge is valuable because students want to know about teaching style, workload, grading difficulty, and class experience before registering. Official university pages list faculty and course information, but student opinions are scattered across Rate My Professors, Reddit, and informal student discussions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professors |Charles Bryan student reviews |RMP professor page |
| 2 |Rate My Professors |Thomas Capaul student reviews |RMP professor page |
| 3 |Rate My Professors |Wes Lloyd student reviews |RMP professor page |
| 4 |Rate My Professors |Jeffery Weiss student reviews |RMP professor page |
| 5 |Rate My Professors |David Schuessler student reviews |RMP professor page |
| 6 |Rate My Professors |Alan Fowler student reviews |RMP professor page |
| 7 |UW Tacoma SET Faculty Directory |Official CSS faculty information |UW Tacoma SET faculty page |
| 8 |UW Tacoma Directory |Official professor department/contact information |UW Tacoma directory |
| 9 |Reddit |Student discussion about UW Tacoma CS experience |Reddit thread |
| 10 |Reddit |Student discussion about UWT classes and professors |Reddit thread |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Reasoning:**
Most of my documents are short student reviews or discussion posts rather than long guides. A 400-character chunk should usually keep one full review or one main opinion together. A 50-character overlap helps preserve context when important details are near the boundary between two chunks. If chunks are too small, reviews may lose meaning. If chunks are too large, retrieval may include too much unrelated information.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 using sentence-transformers

**Top-k:** 5


**Production tradeoff reflection:**
For this class project, all-MiniLM-L6-v2 is a good choice because it is free, local, fast, and does not require paid API credits. If this were deployed for real students, I would compare larger embedding models for better retrieval accuracy, longer context support, multilingual support, and stronger performance on informal student-review text. The tradeoff is that larger models may be slower, more expensive, or harder to run locally.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Which UW Tacoma CSS professors are described as helpful or supportive? |The answer should identify professors whose reviews mention office hours, help, support, or clear explanations. |
| 2 |Which professors are described as having a heavy workload? |The answer should summarize reviews that mention lots of homework, projects, difficult exams, or time-consuming assignments. |
| 3 |What do students say about TCSS 305 instructors? |The answer should mention teaching style, workload, projects, difficulty, and student experience for instructors connected to TCSS 305. |
| 4 |Which professor seems best for students who prefer clear lectures? |The answer should identify professors praised for organization, clarity, understandable explanations, or good lectures. |
| 5 |Which professors have mixed or negative reviews, and why? |The answer should summarize repeated complaints such as unclear lectures, harsh grading, heavy workload, or lack of support. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Student reviews are subjective and may contradict each other. One student may describe a professor as helpful while another may describe the same professor as difficult, making it challenging to generate balanced responses.

2. Some professors have significantly more reviews than others. This could cause the retrieval system to favor professors with larger amounts of available text, even when another professor may be a better answer to the user's question.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---
Document Ingestion
(Rate My Professors pages, Reddit threads, UW Tacoma faculty pages, saved .txt files)
        ↓
Chunking
(Custom Python chunk_text() function)
400-character chunks with 50-character overlap
        ↓
Embedding + Vector Store
(sentence-transformers: all-MiniLM-L6-v2)
(ChromaDB local vector database)
        ↓
Retrieval
(Top 5 most relevant chunks per query)
        ↓
Generation
(Groq API: llama-3.3-70b-versatile)
Final answer generated from retrieved professor-review context

(I tried to implement my pic from Mermaid but had trouble, so i had to use plain text.)

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use ChatGPT to help write the document loading and chunking code. I will give it the Documents and Chunking Strategy sections from this planning file and ask it to create a Python function that loads raw text files and splits them into 400-character chunks with 50-character overlap. I will verify the output by checking that chunks are not empty, overlap correctly, and preserve most review text.

**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT to help create the embedding and vector database code. I will give it the Retrieval Approach section and ask it to use sentence-transformers with all-MiniLM-L6-v2 and ChromaDB. I will verify the output by running my five evaluation questions and checking whether the retrieved chunks are related to the professor or course being asked about.

**Milestone 5 — Generation and interface:**
I will use ChatGPT to help connect retrieval results to Groq’s llama-3.3-70b-versatile model. I will give it the Architecture, Retrieval Approach, and Evaluation Plan sections and ask it to create a simple command-line question-answer interface. I will verify the output by asking the five test questions and checking whether the answers are grounded in the retrieved review chunks.
