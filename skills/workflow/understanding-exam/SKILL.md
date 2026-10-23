---
name: understanding-exam
description: Give the engineer an understanding exam on the issue and the solution an agent produced, built from the real diff, graded with feedback, to confirm they understand and can own the change. Use after implementation or when a PR is opened, when the user says "quiz me", "exam", "check my understanding", or in the validation phase of dev-workflow.
---

# Understanding Exam

Agents write code faster than people can absorb it. This exam checks that the engineer understands the problem, the solution, and its risks well enough to defend it in review and fix it at 2 a.m. It teaches as it tests. It is not a punishment.

## 1. Build the knowledge map (silently)
Read the issue or requirement, the full diff (`git diff <base>...HEAD`), the tests, and the decisions made in this conversation. Note:
- **Problem:** the need or bug, root cause, who is affected
- **Approach:** what was chosen, alternatives rejected and why
- **Code paths:** the 3 to 5 places that matter most, as `file:line`
- **Edge cases and failure modes:** what happens on bad input, timeouts, concurrency
- **Tests:** what is covered and what is not
- **Risk:** blast radius, data safety, security, performance, rollback

Ask the engineer once, optionally, about their level with this codebase. Calibrate difficulty to it.

## 2. Compose the exam
Default 8 to 10 questions; 5 for small changes; up to 15 for risky ones. Cover:

| Type | Count | Example |
| --- | --- | --- |
| Problem | 1 to 2 | "Why did this bug only appear for users with more than one device?" |
| Rationale | 2 | "Why a queue here instead of calling the API inline?" |
| Code trace | 2 | "A request arrives with an expired token. Walk through what happens, step by step." |
| What if | 2 | "What breaks if the null check in `parse()` is removed?" |
| Risk and edges | 1 to 2 | "What happens to in-flight jobs when this migration runs?" |
| Tests | 1 | "Which failure would our tests miss?" |
| Spot the flaw | 1 | A plausible but wrong claim about the change. Find the error. |

Mix short answer, multiple choice (with plausible distractors) and ordering. Mark 2 to 3 questions **critical** (data loss, security, blast radius).

For each question, privately prepare: reference answer, key points, common misconceptions, and the code pointer. See [references/question-bank.md](references/question-bank.md) for templates.

Rules for good questions:
- Test reasoning, not syntax or trivia.
- The answer must not be readable straight off the diff with no thought.
- Do not leak the answer in the question.
- Only ask about things actually in this change.
- If you cannot write a clear reference answer from the code, the code or the PR is unclear. Say so and fix that instead of asking.

## 3. Administer
- One question at a time, unless the engineer prefers batches.
- Do not show the rubric or hints. A hint is available on request.
- "I don't know" is a valid answer. Teach, then move on.
- Let the engineer answer in their own words. Do not accept "same as the PR description".

## 4. Grade
Score each answer 0 (wrong), 1 (partial), 2 (correct). After each answer give:
- what was right
- what was missing or mistaken, citing `file:line`
- the correct explanation in a few lines

After a 0 or 1, optionally ask a short variant to check the gap closed.

## 5. Result
Pass when the score is at least 75% and no critical question scored 0.

| Outcome | Meaning | Next |
| --- | --- | --- |
| Pass | Understands the change | Mark PR ready |
| Pass with notes | Passed, small gaps | List topics to revisit |
| Not yet | Below the bar or a critical miss | Walk through the gaps, then retake only those topics with new questions. Never reuse the same questions |

End with a summary: score, strengths, topics to revisit, and one sentence on what the engineer should be able to explain in review. Offer a one-line note for the PR such as `Author completed an understanding check: 9/10.` Do not include questions or answers in the PR, and do not commit exam files unless asked.

## Anti-patterns
- Grading kindly to avoid friction. Be accurate and kind in tone.
- Quizzing on code the agent did not write or touch.
- Long lectures. Keep feedback short.
- Treating a waiver as failure. If the engineer declines the exam, record that in one line and continue.
