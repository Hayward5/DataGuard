# Step-by-Step Presentation Planning

This document records the slide content decisions made during step-by-step planning.
Each slide should be updated here after its content and presentation details are agreed.

---

## Slide 1 — Title

### Purpose

Establish the project identity and frame DataGuard as a complete data quality CLI tool.
This slide should feel like a formal final project opening slide with a terminal-first identity, not an engineering metrics dashboard.

### Final Content

**Main title**

```text
DataGuard
```

**Subtitle**

```text
A Schema-Driven CLI for Data Validation, Cleaning, and Conversion
```

**Positioning line**

```text
A reusable, testable data quality pipeline for CSV, JSON, and JSONL.
```

**Student number**

```text
510558020
```

### Visual Layout

- Use a hybrid layout with two balanced regions.
- One region should feel like a flat terminal homepage without a prompt, command line frame, or icon treatment.
- The terminal region should contain only the main title, subtitle, and positioning line.
- Keep the text centered inside the terminal region.
- The second region should be a horizontal three-node data flow card.
- The data flow card should use plain text nodes only, without icons:

```text
CSV / JSON / JSONL  ->  DataGuard  ->  Report / Clean Output / Converted File
```

- Place `510558020` in the bottom-right corner as small footer text.
- Use a deep charcoal background with a very subtle gradient.
- Use teal as the primary accent color.
- Set `DataGuard` in bold sans-serif text.

### Explicit Decisions

- Use `DataGuard` as the title.
- Do not use `DataGuard Rebuild`.
- Do not show a terminal prompt or shell command example.
- Do not use terminal-style borders or frame lines.
- Do not use icons in the data flow card.
- Do not show core metrics on this slide.
- Do not show test count, coverage, transformer count, or report format count here.
- Do not include any note about rerunning `pytest`.
- Save engineering metrics for a later testing or results slide.

### Speaker Notes

```text
DataGuard is a schema-driven command-line tool for structured data quality workflows.
It supports validation, cleaning, and format conversion for CSV, JSON, and JSONL files.
The goal of this project is to build a reusable and testable pipeline rather than a one-off script.
```

---

## Slide 2 — Workflow Overview

### Purpose

Explain what DataGuard does before introducing implementation details, testing results, or progress history.
This slide should establish the three CLI workflows as the core product surface of the project.

### Final Content

**Slide title**

```text
DataGuard Workflow Overview
```

**Main message**

```text
Three workflows in one data quality pipeline.
```

**Workflow 1**

```text
Validate
Input + Schema
    ↓
Validation Report
```

**Workflow 2**

```text
Clean
Input + Schema + Transforms
    ↓
Clean Output + Report
```

**Workflow 3**

```text
Convert
Input File
    ↓
Converted File
```

**Bottom note**

```text
All workflows share the same parser and output foundation, but each serves a different data quality task.
```

### Visual Layout

- Use a three-column layout.
- Each column represents one workflow: `Validate`, `Clean`, and `Convert`.
- Each workflow should have a simple vertical flow with input requirements at the top, arrow in the middle, and output result at the bottom.
- Use distinct but restrained visual accents for each workflow.
- Use `Validate = teal`, `Clean = deeper teal`, and `Convert = blue-teal`.
- Add a very small input/output hint line in each column for fast scanning.
- Keep the slide conceptual; do not show full CLI commands on this page.
- Reserve command examples for a later CLI reference or demo slide.

### Explicit Decisions

- Slide 2 will use the Workflow Overview concept.
- Do not use the original Week 11 to Final progress bridge as Slide 2.
- Introduce progress comparison later, after the audience understands the product surface.
- Focus this slide on what the tool does, not how it is implemented.

### Speaker Notes

```text
DataGuard is organized around three workflows.
Validate checks whether records match a YAML schema and produces a report.
Clean applies transformation rules first, then validates the transformed records and writes only clean output rows.
Convert performs format conversion between CSV, JSON, and JSONL without loading a schema or producing a validation report.
These workflows share the same parser and output foundation, but each workflow targets a different data quality task.
```

---

## Slide 3 — Issue-Driven Delivery

### Purpose

Show that after Week 12, the project shifted to a formal issue and PR workflow.
Use this slide to summarize the kinds of problems that were solved or added through that process.

### Final Content

**Slide title**

```text
Issue-Driven Delivery
```

**Main message**

```text
After Week 12, every change moved through a formal review workflow.
```

**Workflow line**

```text
Week 12 policy -> Issue -> PR -> CI -> Merge
```

**Card 1**

```text
Reporting
text report
Error Summary
```

**Card 2**

```text
Transformer Capability
field_map
remaining transformer gaps
```

**Card 3**

```text
Parser / Runtime Robustness
encoding detection
JSON / JSONL root validation
write failure handling
```

**Card 4**

```text
Coverage & Docs
fixtures / edge cases
error-path tests
docs alignment
```

### Visual Layout

- Use a mixed layout with a simple left-side workflow line and four right-side summary cards.
- Keep the workflow line minimal and clean.
- Use concise card titles only; do not include issue or PR numbers anywhere on the slide.
- Do not add any extra bottom summary sentence.

### Explicit Decisions

- Use English for both title and subtitle.
- Keep the card titles short and noun-based.
- Do not show issue numbers or PR numbers.
- Do not add a closing tagline at the bottom.

### Speaker Notes

```text
After Week 12, the project switched to an issue-driven development process.
That process was used to deliver reporting improvements, transformer capability expansion, parser and runtime hardening, and broader coverage plus documentation alignment.
The slide highlights the process change first, then groups the resulting work into four concise themes.
```

---

## Slide 4 — Three Workflows, One CLI

### Purpose

Show the representative CLI surface for the three core workflows.
This slide should feel like a compact reference page that proves the tool is complete and usable, while still matching the hybrid CLI showcase style.

### Final Content

**Slide title**

```text
Three Workflows, One CLI
```

**Card 1 title**

```text
Validate
```

**Card 1 format tag**

```text
JSON | text
```

**Card 1 focus line**

```text
schema validation, report out
```

**Card 1 command line**

```text
validate
```

**Card 1 detail line**

```text
CSV / JSON / JSONL input
```

**Card 2 title**

```text
Clean
```

**Card 2 format tag**

```text
JSON | text
```

**Card 2 focus line**

```text
apply transforms, clean output + report
```

**Card 2 command line**

```text
clean
```

**Card 2 detail line**

```text
structured input
```

**Card 3 title**

```text
Convert
```

**Card 3 format tag**

```text
CSV | JSON | JSONL
```

**Card 3 focus line**

```text
format conversion, converted file out
```

**Card 3 command line**

```text
convert
```

**Card 3 detail line**

```text
input file
```

### Visual Layout

- Use three equal-width cards in a single row.
- Keep the cards ordered as `Validate`, `Clean`, `Convert`.
- Use a small format tag at the top of each card.
- Use short, mixed-purpose descriptions rather than full CLI syntax blocks.
- Keep the command line short and plain, without monospaced code styling.
- Use subtle per-card accents, with `Validate = teal`, `Clean = blue-teal`, and `Convert = deeper teal`.
- Keep the overall layout clean enough to read quickly, not crowded like a terminal reference sheet.

### Explicit Decisions

- Use `Three Workflows, One CLI` as the slide title.
- Do not add a subtitle.
- Do not use full command examples.
- Do not show `--limit`.
- Do not add a footnote or disclaimer.
- Do not switch the order away from `Validate -> Clean -> Convert`.
- Keep the cards as a compact CLI reference, not a demo or architecture slide.

### Speaker Notes

```text
This slide shows the practical command surface for the three workflows.
Validate and clean both support JSON and text reports, while convert is a pure format conversion command across CSV, JSON, and JSONL.
The goal is to give the audience a quick, readable reference for how the tool is actually used.
```
