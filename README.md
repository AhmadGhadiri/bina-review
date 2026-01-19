# Bina (بینا)

**Bina** is a deterministic, rule-based static analysis tool for Python.
It focuses on logical correctness, edge cases, and misleading patterns without using AI or heuristics.

## Features (v3)
- **Deterministic**: No AI, no guessing.
- **Fast**: AST-based analysis and multiprocessing.
- **Custom Rules API**: Write your own rules in Python.
- **Rule Profiles & Categories**: Group rules by category and enable them using high-level profiles (e.g., `strict`, `security`).
- **Baseline Mode**: Focus on new issues by ignoring technical debt.
- **SARIF Support**: Export results in v2.1.0 format for GitHub Code Scanning.
- **CI Integrated**: Ready for GitHub Actions.

## SARIF Output

Bina can export analysis results in the SARIF v2.1.0 format. This is useful for integration with GitHub Code Scanning or other static analysis platforms.

### Configuration (`bina.yaml`)

```yaml
output:
  sarif: true
  sarif_path: results.sarif
```

### Usage

```bash
bina check . --sarif MyReport.sarif
```

## Rule Profiles

Bina allows you to enable sets of rules using **profiles**. You can choose from built-in profiles or define your own.

### Built-in Profiles

| Profile | Categories Included |
|---|---|
| `default` | `correctness`, `security`, `maintainability` |
| `strict` | All categories (`correctness`, `security`, `performance`, `architecture`, `maintainability`, `style`, `uncategorized`) |
| `security` | `correctness`, `security` |
| `performance` | `performance` |

### Configuration (`bina.yaml`)

Specify the profile in your configuration:

```yaml
profile: security

# You can also define custom profiles
profiles:
  my-team:
    - correctness
    - maintainability

# Individual rule settings have HIGHER precedence than profiles
rules:
  L001: OFF # Disable this rule even if included in the profile
```

### Usage

Override the profile via CLI:
```bash
bina check . --profile strict
```

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
