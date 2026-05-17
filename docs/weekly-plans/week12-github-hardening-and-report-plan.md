# Week 12 GitHub Hardening and Feature Follow-up Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a clean GitHub-based development workflow on `main`, then deliver one small but complete follow-up feature that is still missing from the current codebase and can realistically be finished within one week.

**Architecture:** Use `main` as the official integration branch. All new work starts from `main` on issue-based branches, goes through PR review, and is verified by GitHub Actions CI before merge. The feature work should remain small and bounded so it can be completed within the week without reopening the core `validate` / `clean` / `convert` architecture.

**Tech Stack:** GitHub branches and PRs, GitHub Actions, Python 3.12, Click, pytest, existing parser / schema / transformer / reporter modules, small `test -> feat` commits.

---

## Week 12 Preconditions

These are required before normal feature work begins. They are not counted as the main feature deliverable, but the week depends on them.

- Create and push `main`.
- Set GitHub default branch to `main`.
- Use issue-based branch names, for example `issue-12-add-text-report`.
- Route all new work through `Issue -> branch -> PR -> CI -> merge`.

---

## Task 1: Formalize GitHub Workflow

**Files:**
- Create: `.github/pull_request_template.md`
- Create: `.github/ISSUE_TEMPLATE/feature.md`
- Modify: `README.md` or a short workflow note if needed

- [ ] **Step 1: Write the workflow templates**

Keep the templates short and practical:

- Issue template should ask for goal, current behavior, expected behavior, and acceptance criteria.
- PR template should ask for summary, files changed, testing steps, and linked issue number.

- [ ] **Step 2: Verify the workflow matches the repo**

The templates must fit the current project shape:

- `main` is the default branch
- PRs merge back to `main`
- CI runs automatically on PRs

- [ ] **Step 3: Commit**

```bash
git add .github/pull_request_template.md .github/ISSUE_TEMPLATE/feature.md README.md
git commit -m "docs: add github workflow templates"
```

---

## Task 2: Add Text Report Rendering

**Files:**
- Modify: `src/dataguard/reporter/json_report.py` or add a new reporter module for text rendering
- Modify: `src/dataguard/cli.py`
- Test: `tests/unit/reporter/test_text_report.py`
- Integration: `tests/integration/test_validate_flow.py` and `tests/integration/test_clean_flow.py`

- [ ] **Step 1: Write the failing tests**

The text report should provide a human-readable summary of validation results. Keep it short and consistent with the current JSON report data.

Suggested coverage:

- valid report content renders summary lines
- error rows are included in a readable list
- `--format text` works for `validate` and `clean`

- [ ] **Step 2: Implement minimal text rendering**

Use the existing `Report` model and keep the reporter focused on formatting only.

- [ ] **Step 3: Wire CLI format selection**

`validate` and `clean` should accept `--format json|text` and dispatch to the correct renderer.

- [ ] **Step 4: Run unit and integration tests**

The important check is that JSON remains the default behavior and text output does not break existing reports.

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/reporter src/dataguard/cli.py tests/unit/reporter tests/integration/test_validate_flow.py tests/integration/test_clean_flow.py
git commit -m "feat: add text report output"
```

---

## Task 3: Add Field Mapping Transformer

**Files:**
- Create: `src/dataguard/transformer/field_map.py`
- Modify: `src/dataguard/transformer/engine.py`
- Test: `tests/unit/transformer/test_field_map.py`
- Integration: `tests/integration/test_clean_flow.py`

- [ ] **Step 1: Write the failing tests**

Focus on the two behaviors already described in the Phase 3 design:

- rename source columns to target names
- drop specified columns

- [ ] **Step 2: Implement the transformer**

Keep the implementation pure and record-based, matching the existing transformer style.

- [ ] **Step 3: Register the new operation**

Add `field_map` to the transformer engine registry so `clean` can use it from YAML.

- [ ] **Step 4: Add one integration case**

Verify that `clean` can apply `field_map` together with the existing transform flow.

- [ ] **Step 5: Commit**

```bash
git add src/dataguard/transformer/field_map.py src/dataguard/transformer/engine.py tests/unit/transformer/test_field_map.py tests/integration/test_clean_flow.py
git commit -m "feat: add field map transformer"
```

---

## Task 4: Week 12 Regression Check

**Files:**
- No new files expected

- [ ] **Step 1: Run the full test suite**

Use the same command already used in the project:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q
```

- [ ] **Step 2: Fix regressions if any appear**

Keep the scope bounded to the new Week 12 work only.

- [ ] **Step 3: Commit regression fixes**

Use a focused commit message if any fix is needed.

---

## Deliverables

- `main` is the default branch.
- PRs use issue-based branch names.
- GitHub Actions CI runs automatically on PRs.
- `validate` / `clean` support both `json` and `text` report formats.
- `field_map` is available as a transformer operation.
- Full pytest passes.

## Out of Scope

- Adding new CLI commands.
- Expanding `convert` beyond the current CSV / JSON / JSONL conversion support.
- Reworking the current schema format.
- Large-scale refactors unrelated to the selected Week 12 feature work.
