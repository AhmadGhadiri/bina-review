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

class MutableDefaultRule(BaseRule):
    id = "B001"
    name = "Mutable Default"
    description = "Mutable default argument detected."
    severity = Severity.MEDIUM

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for default in node.args.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.report(
                    message="Mutable default argument detected. Use None and initialize inside the function.",
                    node=default,
                    suggestion="Change default to None and set it to [] inside the function."
                )

class SilentExceptionRule(BaseRule):
    id = "B002"
    name = "Silent Exception"
    description = "Silent exception swallowing detected."
    severity = Severity.HIGH

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        # Check for bare except or except Exception
        is_bare = node.type is None
        is_exception = False
        if isinstance(node.type, ast.Name) and node.type.id == "Exception":
            is_exception = True
        
        if is_bare or is_exception:
            # Check body for strict pass or ...
            if len(node.body) == 1:
                stmt = node.body[0]
                if isinstance(stmt, (ast.Pass, ast.Ellipsis)) or (
                    isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis
                ):
                     self.report(
                        message="Silent exception swallowing. Log the error or handle it explicitly.",
                        node=node,
                        suggestion="Add a logging statement or specific exception handling logic."
                    )

class ResourceCleanupRule(BaseRule):
    id = "B003"
    name = "Resource Cleanup"
    description = "Resource usage without proper cleanup (open without with)."
    severity = Severity.MEDIUM

    def __init__(self):
        super().__init__()
        self._safe_open_nodes = set()

    def visit_With(self, node: ast.With):
        for item in node.items:
            for subnode in ast.walk(item.context_expr):
                if isinstance(subnode, ast.Call) and isinstance(subnode.func, ast.Name) and subnode.func.id == "open":
                    self._safe_open_nodes.add(subnode)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            if node not in self._safe_open_nodes:
                self.report(
                    message="Resource usage without context manager. Use 'with open(...)' to ensure cleanup.",
                    node=node,
                    suggestion="Wrap the open() call in a 'with' statement."
                )
        self.generic_visit(node)
