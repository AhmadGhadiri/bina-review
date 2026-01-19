import ast
from bina.core.models import BaseRule, Severity

class NoPrintRule(BaseRule):
    id = "C001"
    name = "No Print"
    description = "Checks for print() calls."
    severity = Severity.LOW

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.report("Avoid using print() in production code.", node)
        self.generic_visit(node)
