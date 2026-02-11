# AI-Assisted Quality Gate

## Purpose
This repository is an exploratory implementation of automated testing, AI-assisted analysis, and CI/CD pipelines working together to produce actionable quality signals. It exists as a learning space to broaden understanding of how these techniques interact in practice.

## What This Is
- An exploratory, reference-style project
- A learning-focused repository for examining how automated testing, AI-assisted analysis, and CI/CD workflows can interact
- A structure-first implementation that emphasizes guardrails, intent, and quality signals over features
- A space for experimentation and iteration rather than a production-ready system

## What This Is Not
- A production-ready system or reference architecture
- A complete or finalized implementation
- A drop-in solution for real-world environments
- A benchmark, compliance framework, or best-practice guide
- An endorsement of specific tools, models, or vendors

## Design Principles

This project follows several key design principles:

1. **Structure Over Features** – Prioritizes clear, understandable architecture and guardrails over feature completeness. The goal is to establish a solid foundation for exploration and iteration.

2. **Layered Separation of Concerns** – Distinct layers handle different responsibilities:
   - **CI/CD Layer** – Test execution and metric collection
   - **Analysis Layer** – Deterministic quality assessment
   - **AI Enhancement** – Optional contextual insights
   - **Application Layer** – External interfaces and endpoints

3. **Type Safety and Validation** – Uses Pydantic for strict data validation across all data transformations. Input and output models are explicitly defined, making the contract between layers clear.

4. **Determinism with Optional AI** – The core quality assessment is deterministic and reproducible (based on test metrics and coverage). AI enhancement is optional and treated as an augmentation, not a replacement.

5. **Extensibility by Design** – Each component (report parser, analyzer, API) is designed to be replaceable or extended without modification to other layers. This enables experimentation with different analysis strategies or AI models.

6. **Learning-Focused** – All design decisions prioritize clarity and demonstrating interaction patterns over optimization or production concerns. The codebase is intentionally simple to make concepts accessible.

## Repository Structure
- `app/` – Application code and execution surface
- `tests/` – Automated tests and validation logic
- `ai/` – AI-related logic, prompts, and model boundaries
- `.github/workflows/` – CI/CD workflows and automation policies
- `docker/` – Container definitions and runtime isolation

## Architecture

The system follows a pipeline approach that integrates testing, coverage analysis, AI-driven insights, and quality decisions:

1. **CI/CD Pipeline** – GitHub Actions runs tests and measures code coverage
2. **Report Collection** – Test results (JUnit XML) and coverage metrics (Coverage XML) are generated
3. **Analysis Layer** – Reports are parsed into structured data, analyzed for quality metrics, and risk levels are determined
4. **AI Enhancement** – Optional AI analysis provides contextual insights and recommendations beyond deterministic rules
5. **Output** – FastAPI application exposes endpoints and serves analysis results

graph TB
    %% CI/CD Layer
    subgraph CI["CI/CD Pipeline"]
        GH["GitHub Actions"]
        Tests["Run Tests<br/>(Pytest)"]
        Coverage["Measure Coverage"]
    end

    %% Test Reports
    subgraph Reports["Test Reports"]
        JUnit["JUnit XML<br/>(Test Results)"]
        Cov["Coverage XML<br/>(Coverage Data)"]
    end

    %% Analysis Layer
    subgraph Analysis["Analysis Layer"]
        Parser["Report Parser<br/>(ai/report_parser.py)"]
        Input["AnalysisInput<br/>(Models)"]
        Analyzer["Quality Analyzer<br/>(ai/analyzer.py)"]
        Output["AnalysisOutput<br/>(Risk Level,<br/>Recommendations)"]
    end

    %% AI Enhancement
    subgraph AI["AI Enhancement"]
        AIModel["AI Model<br/>(OpenAI/Ollama)"]
        Insight["AI Insight<br/>(Contextual Feedback)"]
    end

    %% Application & Docker
    subgraph Docker["Docker Runtime"]
        App["app container<br>FastAPI (Python 3.12)"]
        AIContainer["ai container<br>Python 3.12-slim"]
        App -->|Depends On| AIContainer
        App -->|Exposes API| Browser["Browser / API Client"]
        AIContainer -->|Optional Scripts / Models| App
    end

    %% Connections
    GH --> Tests
    GH --> Coverage
    Tests --> JUnit
    Coverage --> Cov

    JUnit --> Parser
    Cov --> Parser
    Parser --> Input
    Input --> Analyzer
    Analyzer --> Output
    Output --> AIModel
    AIModel --> Insight

    Output --> App
    Insight --> App

    %% Styling
    style CI fill:#e1f5ff
    style Reports fill:#f3e5f5
    style Analysis fill:#e8f5e9
    style AI fill:#fff3e0
    style Docker fill:#fce4ec

## Example Outputs

The system produces structured analysis outputs in both JSON and Markdown formats.

### Example 1: Quality Gate Pass (All Checks Pass)

**JSON Output:**
```json
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

**Markdown Report:**
```
# Quality Gate Report

## Summary
- Test Status: **PASS**
- Coverage Status: **PASS**
- Overall Status: **PASS**
- Risk Level: **LOW**

## Metrics
- Total Tests: 45
- Passed: 45
- Failed: 0
- Coverage: 85.3% (Threshold: 80.0%)
```

### Example 2: Quality Gate Fail (Coverage Below Threshold)

**JSON Output:**
```json
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
      "message": "Resolve failing tests before deployment.",
      "severity": "HIGH"
    }
  ]
}
```

**Markdown Report:**
```
# Quality Gate Report

## Summary
- Test Status: **PASS**
- Coverage Status: **FAIL**
- Overall Status: **FAIL**
- Risk Level: **HIGH**

## Metrics
- Total Tests: 42
- Passed: 42
- Failed: 0
- Coverage: 72.1% (Threshold: 80.0%)

## Recommendations
- [HIGH] Resolve failing tests before deployment.
```

## Status
This project is in an early, exploratory stage. It is currently focused on establishing structure and intent. Functionality is incomplete and expected to evolve over time.

## Disclaimer
This repository contains illustrative and fictional examples intended for learning and exploration purposes only. Any systems, workflows, configurations, or AI behaviors described here are not production-ready and should not be used as-is in real-world environments. The content is provided without guarantees and is subject to change.

## Tooling (Initial Selection)
- **Python** – Chosen as the primary implementation language for its readability, ecosystem, and strong support for testing and AI-related workflows.
- **Pytest** – Selected as the testing framework due to its expressiveness, extensibility, and widespread use in Python-based test automation.
- **GitHub Actions** – Used for CI/CD automation to keep workflows close to the repository and enable reproducible, version-controlled quality gates.