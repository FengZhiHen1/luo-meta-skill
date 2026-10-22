# Review comment research notes (raw)

## Source A: large-project review practice
- Reviewers who comment on intent ("what happens if X fails?") get more author changes than
  reviewers who comment on style. Style comments still help but must not crowd out intent.
- Blocking versus non-blocking labels change author behavior more than comment length.
- Reviews over 400 changed lines lose most defect detection; split the change or review in passes.
- A review that names a concrete failure scenario gets a fix; a review that says "this feels wrong"
  usually gets a reply, not a change.

## Source B: postmortem of two incidents
- Incident 1: the reviewer approved a change that removed a retry. Nobody asked what happens when
  the upstream times out. Condition: retry removal is invisible in the diff.
- Incident 2: the reviewer asked 34 style questions, the author rewrote the file, and the real
  problem (a lock held across an await) survived the rewrite.

## Source C: review guidance from platform docs
- Prefer commenting on the change, not the author.
- Ask about tests only when the behavior is not covered; blanket "add tests" comments are ignored.
- When the project has a waiver convention, a waived rule is not a defect.

## Trade-offs noted
- Thorough reviews catch more, but review latency delays the queue; teams with shared ownership
  accept longer latency, teams shipping daily do not.
- A short checklist of failure questions beats a long style guide for defect detection.
- Reviewing generated code is different: check the regeneration path, not the generated text.
