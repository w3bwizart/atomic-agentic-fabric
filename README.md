# Atomic Agentic Fabric (AAF)

Welcome to the Master Repository for the **Atomic Agentic Fabric (AAF)** framework.

This project shifts software engineering from "Construction" (writing lines of code) to "Orchestration" (orchestrating intent) using a Zero-Trust Fission Sandbox and a highly deterministic Atomic Architecture.

For the comprehensive master architecture blueprint, please refer to the [Atomic Agentic Fabric Architecture](./Atomic%20Agentic%20Fabric.md) document.

## 🚀 Sprawl CLI Quickstart Guide

The `sprawl` CLI Orchestrator is the execution engine that provisions and syncs your Sovereign DNA across your local web development environments.

### Step 1: Initialize the Global Hub

The initial setup clones your DNA remote repository globally and provisions the workspace.

```bash
python3 src/sprawl.py init <YOUR_GIT_URL>
```

*This command clones your DNA into `~/.agents/`, creates your `~/Documents/Sprawl/` working directory, and automatically links `sprawl` globally to `~/.local/bin/` so it can be run from anywhere.*

### Step 2: Create a New App Scaffold

Start a new project within your Sprawl Hub.

```bash
sprawl create <APP_NAME>
```

*Creates the project directory `~/Documents/Sprawl/<APP_NAME>/` and automatically drops a blank `package.md` inside.*

### Step 3: Define your Dependencies

Navigate into your newly created app directory.

```bash
cd ~/Documents/Sprawl/<APP_NAME>/
```

Edit the `package.md` to define which rules and skills your app needs. For example:

```markdown
# My App

## [rules]
- PRIME_DIRECTIVE.md

## [skills]
- my_skill_folder
```

### Step 4: Sync your Local DNA

To inject your requested skills and rules directly from your global repository into your app's local `.agents/` folder, simply run:

```bash
sprawl sync
```

*If you run this inside an app folder, it only syncs that specific app (Targeted Mode). If you run it from the Sprawl Hub root (`~/Documents/Sprawl/`), it will sync all app folders recursively.*

Once synced, `sprawl` automatically compiles your `AGENTS.md` active registry and builds out a local `mcp_config.json`.

---

## ⚙️ Enterprise Capabilities

The newly updated Sprawl Engine possesses the following state-of-the-art native runtime modifiers:

- `sprawl man`: Serves exactly this `README.md` block directly into your terminal.
- `sprawl sync --dry-run`: Safety net parser. Identifies path structures and resolves arrays, but guarantees 0 files will be overwritten or cloned by operating purely in standard-out mode.
- `sprawl sync --verbose`: Replaces silent executions with strict native logging, outputting exactly which rules, files, and symlink layers are actively shifting via Cyber-Brutalist color formatting.
- `sprawl --version`: Tracks your deterministic engine architecture dynamic builds.

---

## 🧪 Testing Suite

To ensure the CLI's string-parsing handlers and path configurations are executing correctly, this codebase uses Python's native `unittest` suite. 

To execute all tests locally, run from the root directory:
```bash
python3 -m unittest discover -s tests
```
