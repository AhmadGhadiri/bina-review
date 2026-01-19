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

from . import best_practices
from . import logic
from . import naming
from ...core.registry import RuleRegistry

# Register built-in rules
RuleRegistry.register_rule(logic.InfiniteLoopRule())
RuleRegistry.register_rule(logic.SortedUniquePromiseRule())
RuleRegistry.register_rule(logic.UncheckedNoneRule())

RuleRegistry.register_rule(best_practices.MutableDefaultRule())
RuleRegistry.register_rule(best_practices.SilentExceptionRule())
RuleRegistry.register_rule(best_practices.ResourceCleanupRule())

RuleRegistry.register_rule(naming.MisleadingNameRule())
