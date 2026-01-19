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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any, Dict

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

@dataclass
class Position:
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None

@dataclass
class Finding:
    rule_id: str
    message: str
    severity: Severity
    file: str
    line: int
    column: int
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None

@dataclass
class RuleContext:
    """Context passed to rules during execution."""
    filename: str
    tree: Any  # ast.AST
    config: Optional[Any] = None  # Config object
    # Future: control flow state, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)
