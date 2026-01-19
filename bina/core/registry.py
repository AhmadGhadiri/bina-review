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

from typing import Dict, List, Optional
from .models import BaseRule

class RuleRegistry:
    _rules: Dict[str, BaseRule] = {}

    @classmethod
    def register_rule(cls, rule: BaseRule):
        """Register a rule instance."""
        cls._rules[rule.id] = rule

    @classmethod
    def get_rule(cls, rule_id: str) -> Optional[BaseRule]:
        return cls._rules.get(rule_id)

    @classmethod
    def get_all_rules(cls) -> List[BaseRule]:
        return list(cls._rules.values())

    @classmethod
    def clear(cls):
        cls._rules = {}
