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

from typing import Callable, Dict, List, Type, Any, Optional
from dataclasses import dataclass
from .models import Finding, Severity

@dataclass
class RuleDefinition:
    id: str
    description: str
    severity: Severity
    language: str  # e.g., "python"
    check_fn: Callable[..., List[Finding]]

class RuleRegistry:
    _rules: Dict[str, RuleDefinition] = {}

    @classmethod
    def register(cls, id: str, description: str, severity: Severity, language: str = "python"):
        """Decorator to register a rule."""
        def decorator(func: Callable):
            cls._rules[id] = RuleDefinition(
                id=id,
                description=description,
                severity=severity,
                language=language,
                check_fn=func
            )
            return func
        return decorator

    @classmethod
    def get_rules_for_language(cls, language: str) -> List[RuleDefinition]:
        return [r for r in cls._rules.values() if r.language == language]

    @classmethod
    def get_all_rules(cls) -> List[RuleDefinition]:
        return list(cls._rules.values())
