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

import yaml
import os
import sys
import glob
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .models import Severity

DEFAULT_PROFILES = {
    "default": ["correctness", "security", "maintainability"],
    "strict": ["correctness", "security", "performance", "architecture", "maintainability", "style", "uncategorized"],
    "security": ["correctness", "security"],
    "performance": ["performance"]
}

@dataclass
class RuleConfig:
    severity: Optional[Severity] = None
    enabled: bool = True

@dataclass
class Config:
    rules: Dict[str, RuleConfig] = field(default_factory=dict)
    exclude: List[str] = field(default_factory=list)
    custom_rules: List[str] = field(default_factory=list)
    profile: str = "default"
    profiles: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str = "bina.yaml") -> 'Config':
        if not os.path.exists(path):
            return cls()
        
        try:
            with open(path, 'r') as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            # Fallback to defaults on error? Or raise?
            # For now, print warning and return default
            print(f"Warning: Failed to load config from {path}: {e}", file=sys.stderr)
            return cls()

        rules = {}
        if 'rules' in data and isinstance(data['rules'], dict):
            for rule_id, rule_data in data['rules'].items():
                # Rule data can be string "HIGH"/"OFF" or dict
                r_config = RuleConfig()
                if isinstance(rule_data, str):
                    if rule_data.upper() == "OFF":
                        r_config.enabled = False
                    elif rule_data.upper() in Severity.__members__:
                        r_config.severity = Severity[rule_data.upper()]
                elif isinstance(rule_data, bool):
                    r_config.enabled = rule_data
                elif isinstance(rule_data, dict):
                    if 'severity' in rule_data and rule_data['severity'] in Severity.__members__:
                        r_config.severity = Severity[rule_data['severity']]
                    if 'enabled' in rule_data:
                        r_config.enabled = bool(rule_data['enabled'])
                
                rules[rule_id] = r_config

        exclude = data.get('exclude', [])
        if not isinstance(exclude, list):
            exclude = []

        custom_rules = []
        if 'custom_rules' in data and isinstance(data['custom_rules'], dict):
             custom_rules = data['custom_rules'].get('paths', [])
             if not isinstance(custom_rules, list):
                 custom_rules = []

        profile = data.get('profile', 'default')
        if not isinstance(profile, str):
            profile = 'default'

        profiles = {}
        if 'profiles' in data and isinstance(data['profiles'], dict):
            for p_name, p_content in data['profiles'].items():
                if isinstance(p_content, list):
                    profiles[p_name] = p_content

        return cls(rules=rules, exclude=exclude, custom_rules=custom_rules, profile=profile, profiles=profiles)

    def is_rule_enabled(self, rule: Any, override_profile: Optional[str] = None) -> bool:
        # 1. Individual rule override (highest precedence)
        if rule.id in self.rules:
            return self.rules[rule.id].enabled
        
        # 2. Profile-based enablement
        active_profile = override_profile or self.profile
        active_categories = self.profiles.get(active_profile)
        if active_categories is None:
            active_categories = DEFAULT_PROFILES.get(active_profile, DEFAULT_PROFILES["default"])
            
        return rule.category in active_categories

    def get_rule_severity(self, rule_id: str, default_severity: Severity) -> Severity:
        if rule_id in self.rules and self.rules[rule_id].severity:
            return self.rules[rule_id].severity
        return default_severity

    def is_path_excluded(self, path: str) -> bool:
        # Check against exclude patterns
        # We need to handle relative paths carefully
        # Simple glob matching
        import fnmatch
        for pattern in self.exclude:
            # Check if path matches pattern
            if fnmatch.fnmatch(path, pattern):
                return True
            # Also check if it matches a directory pattern ending in /**
            # Logic: if pattern is "tests/**", we want to match "tests/foo.py"
            # standard fnmatch might not handle ** recursive logic exactly like gitignore
            # but simple prefix check is often good enough for basics if pattern ends in /
            pass
        return False
