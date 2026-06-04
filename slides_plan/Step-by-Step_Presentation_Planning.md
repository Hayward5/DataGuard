# Step-by-Step Presentation Planning

This document records the slide content decisions made during step-by-step planning.
Each slide should be updated here after its content and presentation details are agreed.

---

## Slide 1 — Title

### Purpose

Establish the project identity and frame DataGuard as a complete data quality CLI tool.
This slide should feel like a formal final project opening slide, not an engineering metrics dashboard.

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

- Place the main title in the center or slightly above center.
- Put the subtitle directly below the title.
- Put the positioning line below the subtitle with smaller text.
- Include a simple data flow visual in the middle or lower-middle area:

```text
CSV / JSON / JSONL  ->  DataGuard  ->  Report / Clean Output / Converted File
```

- Place `510558020` in the bottom-right corner as small footer text.

### Explicit Decisions

- Use `DataGuard` as the title.
- Do not use `DataGuard Rebuild`.
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
- Each workflow should have a simple vertical flow:
  input requirements at the top, arrow in the middle, output result at the bottom.
- Use distinct but restrained visual accents for each workflow.
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
