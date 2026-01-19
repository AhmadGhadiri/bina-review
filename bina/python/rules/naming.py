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
from typing import List
from ...core.models import Finding, Severity, RuleContext, BaseRule

class MisleadingNameRule(BaseRule):
    id = "N001"
    name = "Misleading Name"
    description = "Misleading function name."
    severity = Severity.LOW

    def visit_FunctionDef(self, node: ast.FunctionDef):
        name = node.name.lower()
        
        # 1. 'is_...' should return boolean (simplified heuristic)
        # (Heuristic partially implemented in v2, keeping same logic)
        
        # 2. 'get_...' should return something
        if name.startswith("get_"):
            has_return = False
            for child in ast.walk(node):
                if isinstance(child, ast.Return) and child.value is not None:
                    has_return = True
                    break
            
            # If function is empty (pass/ellipsis), ignore (abstract method)
            is_abstract = False
            if len(node.body) == 1 and isinstance(node.body[0], (ast.Pass, ast.Expr)):
                is_abstract = True
            
            if not has_return and not is_abstract:
                 self.report(
                    message=f"Function '{node.name}' starts with 'get_' but does not return a value.",
                    node=node,
                    suggestion="Ensure function returns a value or rename it."
                )
