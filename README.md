# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Alan Fowler Reviews | Text File | data/raw/alan_fowler.txt |
| 2 | Charles Bryan Reviews |Text File |data/raw/charles_bryan.txt |
| 3 | David Schuessler Reviews | Text File | data/raw/david_schuessler.txt |
| 4 | Jeffery Weiss Reviews | Text File | jeffery_weiss.txt |
| 5 | Tom Capaul Reviews | Text File | tom_capaul.txt |
| 6 | Wes Lloyd | Text File | wes_lloyd.txt |
| 7 | UW Tacoma CSS Student Discussion | Text File | data/raw/reddit_uwt_cs.txt |
| 8 | UW Tacoma Professor Discussion | Text File | data/raw/reddit_professor_thread.txt |
| 9 | UW Tacoma Faculty Information | Text File | data/raw/uwt_faculty_directory.txt |
| 10 | UW Tacoma CSS Program Information | Text File | data/raw/uwt_css_program.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
400 characters

**Overlap:**
100 characters

**Why these choices fit your documents:**
I split the documents into 400-character chunks with a 100-character overlap. This size fit my documents because most of the source material consisted of short professor reviews and student discussion posts, so 400 characters usually preserved one complete opinion or idea without combining too many unrelated reviews. The 100-character overlap helped preserve context when a sentence or important detail crossed a chunk boundary.

Before chunking, I cleaned the text by unescaping HTML entities, removing any HTML tags, and normalizing extra whitespace. The final pipeline loaded 10 documents and produced 62 chunks across all documents.

**Final chunk count:**
62

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 from the sentence-transformers library.

**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it runs locally, is free to use, and provides strong semantic search performance for short review-style text. If I were deploying this system for real users and cost was not a constraint, I would evaluate larger embedding models that provide better retrieval accuracy and domain understanding. I would also consider multilingual support, longer context windows, and API-hosted models that may provide higher quality embeddings at the cost of increased latency and infrastructure complexity.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
The system prompt instructed the model to answer using only the retrieved context, avoid outside knowledge, and respond with "I don't have enough information on that" when the retrieved documents did not contain sufficient information. The retrieved chunks were formatted and passed directly to the model as context before the user's question.

**How source attribution is surfaced in the response:**
Source attribution is handled programmatically. The filenames of the retrieved documents are collected during retrieval and displayed alongside the generated answer. This guarantees that source information is always available even if the model does not explicitly mention it.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor is helpful outside class? | Charles Bryan and David Schuessler are frequently described as helpful. |Returned reviews mentioning office hours, availability, and willingness to help students. | Relevant | Accurate |
| 2 | Which professor is a tough grader? | David Schuessler is often described as a strict grader. | Returned reviews discussing rigorous grading and high standards. | Relevant | Accurate |
| 3 | Which professor uses project-based learning? | Charles Bryan and Tom Capaul use projects extensively. | Returned reviews mentioning quarter-long projects and project-based coursework. | Relevant | Accurate |
| 4 | Which professor is enthusiastic about teaching? | Charles Bryan is frequently described as enthusiastic and passionate. | Returned reviews discussing enthusiasm and passion for teaching. | Relevant | Accurate |
| 5 | Which professors are described as having a heavy workload? | Reviews should identify professors associated with demanding workloads. | Retrieved partially related chunks discussing course difficulty rather than workload. | Partially Relevant | Partially Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professors are described as having a heavy workload?

**What the system returned:**
The system returned chunks discussing course difficulty, grading rigor, and challenging coursework rather than explicit descriptions of workload.

**Root cause (tied to a specific pipeline stage):**
The retrieval stage was the primary source of failure. The review corpus contained relatively few direct references to workload, homework volume, or time commitment. As a result, the embedding model retrieved semantically related content about difficulty and grading instead of workload-specific information. This led to weaker retrieval scores and less precise answers.

**What you would change to fix it:**
I would collect additional review data that explicitly discusses workload, homework, projects, and time commitment. I would also experiment with larger chunk sizes and alternative embedding models to improve retrieval quality.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The planning document provided a clear roadmap for implementing the system. Defining the chunking strategy, retrieval approach, and evaluation questions before coding made it easier to build the ingestion, retrieval, and generation components incrementally. The evaluation plan also provided a structured way to test the system after implementation.

**One way your implementation diverged from the spec, and why:**
The original plan assumed that all evaluation questions would retrieve highly relevant chunks. During testing, some questions produced weaker retrieval results than expected because the source documents did not contain enough information on those topics. Rather than redesigning the entire corpus, I documented the limitation and used it as a failure case to better understand the behavior of the retrieval pipeline.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- My planning document, chunking strategy, and document structure.
- *What it produced:*
- An ingestion and chunking pipeline that loaded text files, cleaned content, and generated overlapping chunks.
- *What I changed or overrode:*
- I verified the chunk output manually and ensured the implementation used my planned chunk size of 400 characters and 100-character overlap.

**Instance 2**

- *What I gave the AI:*
- The retrieval architecture, embedding model choice, and ChromaDB requirements.
- *What it produced:*
- Code that generated embeddings using all-MiniLM-L6-v2, stored vectors in ChromaDB, and retrieved the most relevant chunks for a query.
- *What I changed or overrode:*
- I tested retrieval manually, adjusted evaluation queries, and documented retrieval limitations after observing high distance scores on some questions.
