# Bina Static Analysis (بینا)

**Deterministic, rule-based static analysis for Python — with profiles, baselines, and GitHub-native feedback.**

Bina focuses on **logical correctness, edge cases, and misleading patterns** without using AI, heuristics, or probabilistic models.  
The goal is **predictable, explainable results** that teams can adopt gradually.

---

## 🚀 Quick Start (GitHub Actions)

Add Bina to your repository in **under 1 minute**:

```yaml
name: Bina Static Analysis
on: [pull_request, push]

jobs:
  bina:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Bina Static Analysis
        uses: bonyad-labs/bina-review@main # Use @v1 or @main
        with:
          path: .
          fail_on_high: true
```

## Features
- **Deterministic**: No AI, no guessing.
- **Fast**: AST-based analysis and multiprocessing.
- **Custom Rules API**: Write your own rules in Python.
- **Rule Profiles & Categories**: Group rules by category and enable them using high-level profiles (e.g., `strict`, `security`).
- **Baseline Mode**: Focus on new issues by ignoring technical debt.
- **SARIF Support**: Export results in v2.1.0 format for GitHub Code Scanning.

## Who is this for?
Bina is ideal for:
- Teams introducing static analysis gradually
- Codebases with existing technical debt
- Organizations needing custom, deterministic rules

Bina is **NOT**:
- A replacement for security scanners
- An AI-based code reviewer

## 🛠 Local Usage

If you want to run Bina locally:

```bash
# Install (Once published)
pip install bina-review

# Run a check
bina check .
```

## SARIF Output

Bina can export analysis results in the SARIF v2.1.0 format. This is useful for integration with GitHub Code Scanning or other static analysis platforms.

### Configuration (`bina.yaml`)

```yaml
output:
  sarif: true
  sarif_path: results.sarif
```

### CLI Override
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

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Copyright © 2025-2026 Bonyad-Labs
