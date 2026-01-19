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

import importlib.util
import os
import sys
import inspect
from typing import List, Type
from .models import BaseRule

class RuleLoader:
    @staticmethod
    def load_from_directory(directory: str) -> List[BaseRule]:
        """Load all BaseRule classes from the given directory."""
        rules = []
        if not os.path.isdir(directory):
            return rules

        # Add directory to sys.path to allow worker processes to unpickle classes
        if directory not in sys.path:
            sys.path.insert(0, directory)

        for filename in os.listdir(directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(directory, filename)
                module_name = filename[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        for name, obj in inspect.getmembers(module):
                            if inspect.isclass(obj) and issubclass(obj, BaseRule) and obj is not BaseRule:
                                rules.append(obj())
                except Exception as e:
                    print(f"Error loading custom rule module {file_path}: {e}", file=sys.stderr)
        
        return rules
