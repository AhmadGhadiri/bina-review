# Copyright 2025-2026 Bonyad-Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
from typing import List, Dict, Any
from ..core.models import Finding, Severity, BaseRule
from ..core.registry import RuleRegistry

class SarifReporter:
    """Reporter for SARIF v2.1.0 format."""

    def __init__(self, sarif_path: str):
        self.sarif_path = sarif_path

    def generate_report(self, findings: List[Finding]) -> Dict[str, Any]:
        """Generate a SARIF report from findings."""
        rules = RuleRegistry.get_all_rules()
        
        sarif_log = {
            "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Bina",
                            "semanticVersion": "0.3.2",
                            "informationUri": "https://github.com/bonyad-labs/bina-review",
                            "rules": self._get_sarif_rules(rules)
                        }
                    },
                    "results": self._get_sarif_results(findings)
                }
            ]
        }
        return sarif_log

    def save_report(self, findings: List[Finding]):
        """Save analysis results to a SARIF file."""
        report = self.generate_report(findings)
        with open(self.sarif_path, 'w') as f:
            json.dump(report, f, indent=2)

    def _get_sarif_rules(self, rules: List[BaseRule]) -> List[Dict[str, Any]]:
        sarif_rules = []
        for rule in rules:
            sarif_rules.append({
                "id": rule.id,
                "name": rule.name,
                "shortDescription": {
                    "text": rule.name
                },
                "fullDescription": {
                    "text": rule.description
                },
                "properties": {
                    "category": rule.category,
                    "precision": "very-high"
                }
            })
        return sarif_rules

    def _get_sarif_results(self, findings: List[Finding]) -> List[Dict[str, Any]]:
        results = []
        for f in findings:
            results.append({
                "ruleId": f.rule_id,
                "message": {
                    "text": f.message
                },
                "level": self._map_severity(f.severity),
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": os.path.relpath(f.file) if os.path.isabs(f.file) else f.file
                            },
                            "region": {
                                "startLine": f.line,
                                "startColumn": f.column + 1  # SARIF is 1-indexed
                            }
                        }
                    }
                ]
            })
        return results

    def _map_severity(self, severity: Severity) -> str:
        if severity == Severity.HIGH:
            return "error"
        if severity == Severity.MEDIUM:
            return "warning"
        return "note"
