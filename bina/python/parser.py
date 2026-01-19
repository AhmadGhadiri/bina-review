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

import ast
import sys
from typing import List
from ..core.models import Finding
from ..core.registry import RuleRegistry

class PythonAnalyzer:
    @staticmethod
    def analyze(file_path: str, config=None) -> List[Finding]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            tree = ast.parse(code, filename=file_path)
            
            # Get Python rules
            rules = RuleRegistry.get_rules_for_language("python")
            findings = []

            # Create Context
            from ..core.models import RuleContext
            context = RuleContext(filename=file_path, tree=tree, config=config)

            for rule in rules:
                # Check config if provided
                if config:
                    if not config.is_rule_enabled(rule.id):
                        continue

                # Pass context to rule
                try:
                    # We need to detect if rule accepts context or old args?
                    # For V2, we enforce new signature or wrap it.
                    # Since we control the codebase, we update all rules.
                    results = rule.check_fn(context)
                    if results:
                        # Apply severity overrides
                        if config:
                            severity = config.get_rule_severity(rule.id, default_severity=rule.severity)
                            for r in results:
                                r.severity = severity
                        findings.extend(results)
                except Exception as e:
                    # Generic error handling to prevent one rule from crashing everything
                    # In a real tool we might log this or report as an error finding
                    print(f"Error running rule {rule.id} on {file_path}: {e}", file=sys.stderr)
            
            return findings

        except SyntaxError as e:
            # We could report syntax errors as findings too
            return []
        except Exception as e:
            print(f"Error parsing {file_path}: {e}", file=sys.stderr)
            return []
