import json
from pydantic import BaseModel, Field
from typing import Literal, List
from openai import OpenAI
from ai.utils import extract_json
from ai.models import (
    AnalysisInput,
    AnalysisOutput,
    Recommendation,
    QualityMetrics,     
    QualitySummary,
    AIInsight,
    TestMetrics,
    CoverageMetrics,
)

class QualityAnalyzer:

    def analyze(self, data: AnalysisInput) -> AnalysisOutput:

        test_status = "PASS" if data.tests.failed == 0 else "FAIL"

        coverage_status = (
            "PASS"
            if data.coverage.percent >= data.coverage.threshold
            else "FAIL"
        )

        overall_status = (
            "PASS"
            if test_status == "PASS" and coverage_status == "PASS"
            else "FAIL"
        )

        # Deterministic risk logic
        if overall_status == "PASS":
            risk_level = "LOW"
            recommendations = []
        else:
            risk_level = "HIGH"
            recommendations = [
                Recommendation(
                    message="Resolve failing tests before deployment.",
                    severity="HIGH",
                )
            ]

        return AnalysisOutput(
            summary=QualitySummary(
                test_status=test_status,
                coverage_status=coverage_status,
                overall_status=overall_status,
            ),
            metrics=QualityMetrics(
                total_tests=data.tests.total,
                passed=data.tests.passed,
                failed=data.tests.failed,
                coverage_percent=data.coverage.percent,
                coverage_threshold=data.coverage.threshold,
            ),
            risk_level=risk_level,
            recommendations=recommendations,
        )

    def generate_markdown_report(self, result: AnalysisOutput) -> str:

        lines = []

        lines.append("# Quality Gate Report")
        lines.append("")
        lines.append("## Summary")
        lines.append(f"- Test Status: **{result.summary.test_status}**")
        lines.append(f"- Coverage Status: **{result.summary.coverage_status}**")
        lines.append(f"- Overall Status: **{result.summary.overall_status}**")
        lines.append(f"- Risk Level: **{result.risk_level}**")
        lines.append("")
        lines.append("## Metrics")
        lines.append(f"- Total Tests: {result.metrics.total_tests}")
        lines.append(f"- Passed: {result.metrics.passed}")
        lines.append(f"- Failed: {result.metrics.failed}")
        lines.append(
            f"- Coverage: {result.metrics.coverage_percent}% "
            f"(Threshold: {result.metrics.coverage_threshold}%)"
        )
        lines.append("")

        if result.recommendations:
            lines.append("## Recommendations")
            for rec in result.recommendations:
                lines.append(f"- [{rec.severity}] {rec.message}")
            lines.append("")

        return "\n".join(lines)
    
    def generate_ai_insight(self, result: AnalysisOutput) -> AIInsight:

        client = OpenAI(base_url="http://localhost:11434/v1",api_key="ollama")

        prompt = f"""
You are a strict software quality analyst.

You must analyze the structured CI result below.
You are NOT allowed to change pass/fail decisions.
You must return JSON only with this structure:

{{
  "executive_summary": string,
  "risk_explanation": string,
  "improvement_suggestions": [string]
}}

Do not include markdown.
Do not include explanations outside JSON.

CI RESULT:
{result.model_dump_json(indent=2)}
"""

        response = client.chat.completions.create(
            model="gpt-oss:20b",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise and structured software quality analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        content = response.choices[0].message.content

        if content is None:
            raise RuntimeError("AI returned empty content.")

        try:
            json_content = extract_json(content)
            return AIInsight.model_validate_json(json_content)

        except Exception as e:
            raise RuntimeError(
                f"AI response validation failed.\n"
                f"Raw response:\n{content}\n"
                f"Error: {e}"
    )

# -------------------------
# Local Execution Example
# -------------------------

if __name__ == "__main__":

    example_input = AnalysisInput(
        tests=TestMetrics(total=4, passed=3, failed=1),
        coverage=CoverageMetrics(percent=96.3, threshold=80.0),
    )

    analyzer = QualityAnalyzer()
    result = analyzer.analyze(example_input)

    print("\nAI INSIGHT:\n")

    try:
        insight = analyzer.generate_ai_insight(result)
        print(insight.model_dump_json(indent=2))
    except Exception as e:
        print("AI validation failed:", e)

    print("JSON OUTPUT:")
    print(result.model_dump_json(indent=2))

    print("\nMARKDOWN REPORT:\n")
    print(analyzer.generate_markdown_report(result))