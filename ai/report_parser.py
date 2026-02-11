import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Tuple
from ai.models import AnalysisInput, AIInsight, TestMetrics, CoverageMetrics


def build_input_from_reports(junit_path: str, coverage_path: str) -> AnalysisInput:
    # --- Parse JUnit XML ---
    junit_tree = ET.parse(junit_path)
    junit_root = junit_tree.getroot()

    # JUnit root is typically <testsuite>
    total_tests = int(junit_root.attrib.get("tests", 0))
    failures = int(junit_root.attrib.get("failures", 0))
    errors = int(junit_root.attrib.get("errors", 0))

    failed = failures + errors
    passed = total_tests - failed

    test_metrics = TestMetrics(
        total=total_tests,
        passed=passed,
        failed=failed,
    )

    # --- Parse Coverage XML ---
    coverage_tree = ET.parse(coverage_path)
    coverage_root = coverage_tree.getroot()

    # coverage.py stores line-rate as a decimal like 0.963
    line_rate = float(coverage_root.attrib.get("line-rate", 0))
    coverage_percent = round(line_rate * 100, 2)

    coverage_metrics = CoverageMetrics(
        percent=coverage_percent,
        threshold=80.0,  # keep consistent with your CI gate
    )

    return AnalysisInput(
        tests=test_metrics,
        coverage=coverage_metrics,
    )