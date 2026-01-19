# Future Improvements

This document tracks potential enhancements for Bina Review.

## Strict Category Validation
In version v0.3.1, rules that do not declare a category are automatically assigned the `"uncategorized"` category. 

**Proposed Change**: 
Change this behavior to fail the analysis (or failing to load the rule) if a rule does not explicitly define a `category`. This ensures that all findings are properly grouped and conform to the profile system.

## Performance
- Move more AST calculations to the parse phase to speed up visitors.
- Investigate caching mechanisms for repeated analysis of unchanged files.
