# Error Analysis

Real failure cases found while building and testing this project, why they
happened, and what was changed to fix or explain them. Unlike a synthetic
error-analysis exercise, every case below was actually observed while
running the app.

## 1. Retrieval rejected a short, valid question ("How to print?")

**Symptom:** a short question with common words scored too low against the
absolute relevance threshold and was rejected as "no matching topic."

**Cause:** short queries naturally produce lower absolute hybrid scores than
longer ones, even when the retrieved chunk is clearly correct — the
threshold was tuned against long queries and was too strict for short ones.

**Fix:** lowered `MIN_RELEVANCE_SCORE` in `06_retrieve_context.py` to `0.08`,
validated against a set of intentionally short test questions.

## 2. Two fundamental topics were missing entirely

**Symptom:** questions about `if/elif/else` and `for`/`while` loops returned
"topic not covered," even though these are core Python basics.

**Cause:** dropped by accident while expanding the knowledge base from 17 to
61 topics — an oversight, not a retrieval bug.

**Fix:** added `conditionals`, `for_while_loops`, and later
`nested_conditionals` (see #4) to `01_documents.py`.

## 3. Cross-lingual queries (Arabic) often fail to retrieve

**Symptom:** an Arabic-phrased question semantically equivalent to an
English topic in the knowledge base ("ازاي اخلي البرنامج ياخد قرار؟" ≈ "how
do I make the program take a decision?") returned no match, while the
English phrasing of the same question worked.

**Cause:** the embedding model (`all-MiniLM-L6-v2`) is primarily
English-trained; its cross-lingual similarity is much weaker than its
within-English similarity, so an Arabic query's embedding doesn't land close
enough to the English chunk embeddings to clear `MIN_RELEVANCE_SCORE`.

**Status: known limitation, not fixed.** A true fix needs a multilingual
embedding model, which is significantly heavier to download and run than
`all-MiniLM-L6-v2` and was judged not worth the added setup complexity this
close to submission. Mitigation instead: the UI shows a visible hint
("Works best with questions written in English") so the limitation is
disclosed rather than silently confusing the user.

## 4. A partially-covered question got a partial (correct) refusal

**Symptom:** "what's the difference between elif and nested if statements"
got an answer about `elif` but an honest "I don't have material on nested
if" instead of a full comparison.

**Cause:** this was not a bug — `nested if` genuinely wasn't in the
knowledge base yet, and refusing to fabricate the missing half of the
comparison is exactly the grounding behavior a RAG system should have.

**Fix (content gap, not a bug fix):** added a dedicated
`nested_conditionals` topic so this specific comparison is now fully
answerable.

## 5. Free-tier LLM returned an empty response and crashed the app

**Symptom:** `TypeError: 'NoneType' object is not subscriptable` in
`ask_llm()` — `response.choices` was empty on a free-tier model under load.

**Fix:** `ask_llm()` now checks `response.choices` before indexing, retries
once, and returns a clear "please try again" message instead of raising.

## 6. Current-vs-outdated conflicts (this variant's addition)

**Symptom (by design, for testing):** three deliberately outdated topics
(`python2_print_statement`, `distutils_deprecated`, `urllib2_deprecated`)
were added, each conflicting with a current topic covering the same task.

**Naive behavior:** sorting retrieved chunks by `(is_current, score)` ranks
current sources first, but does **not** stop an outdated chunk from also
being included in the context alongside its current counterpart, which
would hand the LLM contradictory instructions in the same prompt.

**Fix:** `build_context()` now explicitly drops an outdated source whenever
its current replacement (tracked via each doc's `replaces` field) was also
retrieved for the same question. If no current replacement was retrieved,
the outdated source is kept but labeled `(OUTDATED — do not recommend this,
prefer current practice)` in the context, and the `grounded_currency` prompt
variant is explicitly instructed to warn the student when only an outdated
source is available. See `evaluation/compare_prompts.py` for a direct
comparison against the two weaker prompt variants that don't have this
instruction.
