# Bina (بینا)

**Bina** is a deterministic, rule-based static analysis tool for Python.
It focuses on logical correctness, edge cases, and misleading patterns without using AI or heuristics.

## Features (v3)
- **Deterministic**: No AI, no guessing.
- **Fast**: AST-based analysis and multiprocessing.
- **Custom Rules API**: Write your own rules in Python.
- **Baseline Mode**: Focus on new issues by ignoring technical debt.
- **CI Integrated**: Ready for GitHub Actions.

## Installation
```bash
poetry install
```

## Usage
```bash
poetry run bina check <path_to_file_or_dir>
```

## GitHub Action Usage

To use Bina in your own repository, add this to your `.github/workflows/main.yml`:

```yaml
steps:
  - uses: actions/checkout@v3
  
  - name: Run Bina Static Analysis
    uses: AhmadGhadiri/bina-review@v1
    with:
      path: .
      fail_on_high: true
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright © 2025-2026 Bonyad-Labs
