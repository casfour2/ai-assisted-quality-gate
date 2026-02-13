# AI-Assisted Quality Gate

## Purpose

This repository is an exploratory implementation of automated testing,
deterministic quality enforcement, AI-assisted analysis, and CI/CD
pipelines working together to produce actionable quality signals.

It exists as a learning space to examine how deterministic guardrails
and probabilistic AI can coexist without compromising reliability.

------------------------------------------------------------------------

## Core Thesis

This project explores the boundary between **deterministic software
quality enforcement** and **probabilistic AI interpretation**.

-   Deterministic logic decides.
-   AI explains and contextualizes.
-   The two are intentionally separated.

------------------------------------------------------------------------

## What This Is

-   An exploratory, reference-style project\
-   A learning-focused repository for examining how automated testing,
    structured analysis, and AI augmentation can interact\
-   A structure-first implementation that emphasizes guardrails, intent,
    and quality signals over features\
-   A controlled environment for experimenting with AI inside CI/CD
    without surrendering determinism

------------------------------------------------------------------------

## What This Is Not

-   A production-ready system or reference architecture\
-   A complete or finalized implementation\
-   A drop-in solution for real-world environments\
-   A benchmark, compliance framework, or best-practice guide\
-   An endorsement of specific tools, models, or vendors

------------------------------------------------------------------------

## Decision Authority Model

The quality gate status (PASS / FAIL and risk level) is determined
**exclusively** by deterministic rules based on:

-   Test results
-   Coverage thresholds

AI-generated insights are advisory.\
AI **cannot override** or modify the quality gate decision.

This separation ensures reproducibility, auditability, and predictable
CI behavior.

------------------------------------------------------------------------

## Design Principles

1.  **Structure Over Features**\
    Prioritizes clear architecture and explicit guardrails over feature
    completeness.

2.  **Layered Separation of Concerns**

    -   **CI/CD Layer** -- Test execution and metric collection\
    -   **Analysis Layer** -- Deterministic quality evaluation\
    -   **AI Enhancement Layer** -- Optional contextual insights\
    -   **Application Layer** -- API exposure and report delivery

3.  **Type Safety and Explicit Contracts**\
    All inter-layer communication uses strict Pydantic models.\
    Quality is represented as structured data, not loosely formatted
    text.

4.  **Determinism First**\
    The core gate is reproducible and rule-driven. AI augments, but does
    not decide.

5.  **Extensibility by Design**\
    Report parsing, analysis logic, and AI providers are modular and
    replaceable.

6.  **Learning-Focused Clarity**\
    The codebase emphasizes readability and conceptual transparency over
    optimization.

------------------------------------------------------------------------

## Quality Data Contracts

All quality data flows through explicitly defined Pydantic models,
including:

-   `AnalysisInput`
-   `TestMetrics`
-   `CoverageMetrics`
-   `QualityMetrics`
-   `AnalysisOutput`
-   `AIInsight`

This approach ensures:

-   Deterministic validation of CI inputs\
-   Stable AI prompt construction\
-   Reproducible analysis results\
-   Clear boundaries between metrics and narrative insight

The system treats quality as structured data first, narrative second.

------------------------------------------------------------------------

## Repository Structure

-   `app/` -- FastAPI application and execution surface\
-   `tests/` -- Automated test suite\
-   `ai/` -- Report parsing, deterministic analyzer, AI integration\
-   `.github/workflows/` -- CI/CD workflows and automation policies\
-   `docker/` -- Container definitions and runtime isolation

------------------------------------------------------------------------

## CI Execution Flow

During CI execution:

1.  Tests run via `pytest`
2.  Coverage is collected
3.  JUnit XML and Coverage XML reports are generated
4.  `ai/run_analyzer.py` parses reports into structured models
5.  Deterministic analysis evaluates:
    -   Test pass/fail state
    -   Coverage thresholds
    -   Risk level
6.  Optional AI enhancement generates contextual insights
7.  JSON and Markdown outputs are produced as artifacts

The quality decision occurs before any AI augmentation.

------------------------------------------------------------------------

## Architecture Overview

The system follows a pipeline approach:

1.  **CI/CD Pipeline** -- GitHub Actions runs tests and measures
    coverage\
2.  **Report Collection** -- JUnit and Coverage XML are generated\
3.  **Analysis Layer** -- Structured parsing and deterministic quality
    evaluation\
4.  **AI Enhancement** -- Optional contextual recommendations\
5.  **Output Layer** -- FastAPI exposes analysis results

------------------------------------------------------------------------

## Example Outputs

### Example 1: Quality Gate Pass

**JSON Output**

``` json
{
  "summary": {
    "test_status": "PASS",
    "coverage_status": "PASS",
    "overall_status": "PASS"
  },
  "metrics": {
    "total_tests": 45,
    "passed": 45,
    "failed": 0,
    "coverage_percent": 85.3,
    "coverage_threshold": 80.0
  },
  "risk_level": "LOW",
  "recommendations": []
}
```

------------------------------------------------------------------------

### Example 2: Quality Gate Fail (Coverage Below Threshold)

**JSON Output**

``` json
{
  "summary": {
    "test_status": "PASS",
    "coverage_status": "FAIL",
    "overall_status": "FAIL"
  },
  "metrics": {
    "total_tests": 42,
    "passed": 42,
    "failed": 0,
    "coverage_percent": 72.1,
    "coverage_threshold": 80.0
  },
  "risk_level": "HIGH",
  "recommendations": [
    {
      "message": "Increase test coverage to meet the configured threshold.",
      "severity": "HIGH"
    }
  ]
}
```

------------------------------------------------------------------------

## How to Run Locally

1.  Install dependencies

    ``` bash
    pip install -r requirements.txt
    ```

2.  Run tests and generate reports

    ``` bash
    pytest --junitxml=report.xml --cov=app --cov-report=xml
    ```

3.  Execute analyzer

    ``` bash
    python ai/run_analyzer.py
    ```

4.  Run FastAPI app

    ``` bash
    uvicorn app.main:app --reload
    ```

------------------------------------------------------------------------

## Current Capabilities

-   Deterministic quality gate based on test and coverage metrics\
-   Structured validation using Pydantic models\
-   Optional AI-generated contextual analysis\
-   JSON and Markdown reporting\
-   CI integration via GitHub Actions\
-   Dockerized runtime environment

------------------------------------------------------------------------

## Future Exploration

-   Multiple configurable quality policies\
-   Historical trend analysis\
-   Policy-as-code experimentation\
-   Multi-model AI comparison\
-   Pluggable scoring strategies

------------------------------------------------------------------------

## Status

This project is an ongoing learning environment.\
It is experimental and intended for education, exploration, and
architectural experimentation rather than production use.

------------------------------------------------------------------------

## Disclaimer

This repository contains illustrative and fictional examples intended
for learning purposes only. Systems and workflows described here are not
production-ready and should not be used as-is in real-world
environments.
