#!/usr/bin/env python3
"""
Sprawl CLI Orchestrator
-----------------------
A single-pane Zero-Trust Agentic Fabric execution utility. 
This Orchestrator fetches architectural rules, skills, and workflows from 
a globally authenticated Git remote, and structurally natively syncs them into 
sandboxed local agentic workspaces—establishing deterministic Multi-Agent operation architectures 
without the heavy resource bloat of containers.
"""

import os
import sys
import shutil
import subprocess
import json
import re

VERSION = "v1.1.0"

# ANSI Formatting Config
CYAN = '\033[96m'
AMBER = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# Global system configurations defining deterministic execution paths
AGENTS_DIR_GLOBAL = os.path.expanduser("~/.agents/")
SPRAWL_DIR = os.path.expanduser("~/Documents/Sprawl/")
CONFIG_PATH = os.path.expanduser("~/.sprawl_rc")

# Flags
DRY_RUN = False
VERBOSE = False

def print_status(msg):
    """Prints a standard status flow log with the [*] formatting."""
    print(f"{CYAN}[*] {msg}{RESET}")

def print_warning(msg):
    """Prints a non-fatal warning execution log with the [!] formatting."""
    print(f"{AMBER}[!] WARNING: {msg}{RESET}")

def print_error(msg):
    """Prints a fatal error log with the [X] formatting."""
    print(f"{RED}[X] ERROR: {msg}{RESET}")


def load_config():
    """Extracts JSON global system settings array resolving custom git overrides."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(git_url):
    """Binds global execution configs safely."""
    config = {
        "remote_dna_url": git_url,
        "global_hub": AGENTS_DIR_GLOBAL
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
        

def cmd_init(git_url):
    """
    Core Initialization Pipeline: Initializes the Sprawl network locally.
    
    Execution Logic:
    1. Configurations: Dumps an internal sys tracker into ~/.sprawl_rc.
    2. DNA Cloning: Git clones the provided master DNA repository to ~/.agents/ (The Global Brain).
    3. Scaffolding: Provisions the ~/Documents/Sprawl/ core application development environment.
    4. Exposure: Elevates this CLI into a global runtime by symlinking it strictly inside ~/.local/bin/.
    
    Args:
        git_url (str): The valid target Git remote URL outlining your Agent rulesets/skills.
    """
    print_status(f"Initializing Sprawl Hub from {git_url}...")
    
    save_config(git_url)
    if VERBOSE:
        print_status(f"Configuration written natively to {CONFIG_PATH}")
    
    # 1. Clone Global DNA natively ensuring isolated central caching.
    if os.path.exists(AGENTS_DIR_GLOBAL):
        print_warning(f"{AGENTS_DIR_GLOBAL} already exists. Skipping clone or you can manually update.")
    else:
        print_status(f"Cloning Global DNA to {AGENTS_DIR_GLOBAL}...")
        if not DRY_RUN:
            try:
                subprocess.run(["git", "clone", git_url, AGENTS_DIR_GLOBAL], check=True)
            except subprocess.CalledProcessError as e:
                print_error(f"Failed to clone repository: {e}")
                sys.exit(1)

    # 2. Architect the central workspace namespace to host target applications.
    if not os.path.exists(SPRAWL_DIR):
        print_status(f"Creating Workspace Hub at {SPRAWL_DIR}...")
        if not DRY_RUN:
            os.makedirs(SPRAWL_DIR)
    else:
        if VERBOSE:
            print_status(f"Workspace Hub {SPRAWL_DIR} already exists.")

    # 3. Global Symlink Injection without root/sudo privilege escalation logic.
    local_bin = os.path.expanduser("~/.local/bin")
    if not os.path.exists(local_bin) and not DRY_RUN:
        os.makedirs(local_bin)
        
    sprawl_bin_path = os.path.join(local_bin, "sprawl")
    current_script_path = os.path.abspath(__file__)
    
    # Strictly define permission models enabling runtime execution capabilities.
    if not DRY_RUN:
        os.chmod(current_script_path, 0o755)

    if os.path.lexists(sprawl_bin_path):
        if os.path.islink(sprawl_bin_path):
            if VERBOSE and DRY_RUN:
                print_status(f"DRY RUN: Would replace symlink at {sprawl_bin_path}")
            elif not DRY_RUN:
                os.remove(sprawl_bin_path)
                os.symlink(current_script_path, sprawl_bin_path)
                print_status(f"Updated symlink at {sprawl_bin_path}")
        else:
            print_warning(f"{sprawl_bin_path} exists and is not a symlink. Please configure PATH manually.")
    else:
        if VERBOSE and DRY_RUN:
            print_status(f"DRY RUN: Would create symlink for global access at {sprawl_bin_path}")
        elif not DRY_RUN:
            print_status(f"Creating symlink for global access at {sprawl_bin_path}...")
            os.symlink(current_script_path, sprawl_bin_path)
        
    print_status("Initialization complete. Ensure ~/.local/bin is in your PATH.")


def cmd_create(app_name):
    """
    Instantiates a brand new Agentic Sandbox App under the Central Sprawl directory.

    Operations:
    1. Sandbox Validation: Checks if the nested directory path exists to avoid fatal overwriting.
    2. Execution: Casts the directory skeleton.
    3. Template Bootstrapping: Injects a foundational `package.md` skeleton representing dependency targets.
    
    Args:
        app_name (str): Expected name parameter of the Sprawl workspace project.
    """
    app_dir = os.path.join(SPRAWL_DIR, app_name)
    if os.path.exists(app_dir):
        print_error(f"App directory {app_dir} already exists.")
        sys.exit(1)
        
    print_status(f"Creating new app '{app_name}' at {app_dir}...")
    if not DRY_RUN:
        os.makedirs(app_dir)
    
    # Generating foundational markdown schema layout mimicking package.json behavior natively.
    package_md_path = os.path.join(app_dir, "package.md")
    default_content = f"""# {app_name}

## [rules]
- rule.md

## [skills]
- my_skill_folder

## [atoms]
- atom.md

## [workflows]
- workflow.md
"""
    if VERBOSE and DRY_RUN:
        print_status(f"DRY RUN: Would create default package.md in {app_dir}")
    elif not DRY_RUN:
        with open(package_md_path, "w") as f:
            f.write(default_content)
        print_status(f"Created default package.md in {app_dir}.")


def parse_package_md(file_path):
    """
    Core Schema Evaluation: Dynamically parses a given `package.md` identifying listed dependencies.
    It isolates markdown list elements (- filename) strictly contained within identified categorized headers.
    
    Args:
        file_path (str): The relative/absolute string path mapping to the evaluated payload schema.
        
    Returns: 
        dict: Target mapping structured exactly as: 
              {"rules": [], "skills": [], "atoms": [], "workflows": []}
    """
    required_files = {"rules": [], "skills": [], "atoms": [], "workflows": []}
    
    if not os.path.exists(file_path):
        return required_files

    with open(file_path, "r") as f:
        content = f.read()

    categories = ["rules", "skills", "atoms", "workflows"]
    
    for category in categories:
        # Complex RegEx ensuring scope extraction cleanly cuts horizontally across adjacent category headers or file tails.
        pattern = re.compile(rf"## \[{category}\](.*?)(?:## \[\w+\]|\Z)", re.DOTALL)
        match = pattern.search(content)
        if match:
            section_content = match.group(1)
            # Find all strictly formatted markdown array list strings inside the matched execution zone.
            items = re.findall(r"^\s*-\s+(.+)$", section_content, re.MULTILINE)
            # Ensure none definitions are purged as to not trigger arbitrary lookup errors natively.
            required_files[category] = [item.strip() for item in items if item.strip().lower() != "none"]
            
    return required_files


def sync_app_directory(app_dir):
    """
    File Orchestration Protocol: 
    Injects and mirrors DNA logic from the remote global vault deep into the local working space context.
    
    Logic:
    1. Validates structural schema.
    2. Purges historical runtime bloat inside `.agents/` mitigating cross-agent corruption.
    3. Mirrors assets natively checking for directory/file type execution structures (shutil target branches).
    4. Auto-generates mapping registries: AGENTS.md (for standard consumption) and mcp_config.json (for MCP protocol binding).
    
    Args:
        app_dir (str): Absolute working context bounding the targeted app container mapping.
    """
    package_md_path = os.path.join(app_dir, "package.md")
    
    if not os.path.exists(package_md_path):
        print_warning(f"No package.md found in {app_dir}. Skipping.")
        return
        
    print_status(f"Syncing {app_dir}...")
    
    reqs = parse_package_md(package_md_path)
    local_agents_dir = os.path.join(app_dir, ".agents")
    
    # Strict sandbox cleaning: Destroys and rebuilds targeted local `.agents/` container logic to promise absolute determinism.
    if os.path.exists(local_agents_dir):
        if not DRY_RUN:
            shutil.rmtree(local_agents_dir)
        elif VERBOSE:
            print_status(f"DRY RUN: Would destroy outdated container {local_agents_dir}")
            
    if not DRY_RUN:
        os.makedirs(local_agents_dir)
    
    copied_files = []
    
    # Executes File-Mapping Logic based on explicitly identified rules matched within the package constraint logic.
    for category, files in reqs.items():
        if files:
            category_dir = os.path.join(local_agents_dir, category)
            if not DRY_RUN:
                os.makedirs(category_dir, exist_ok=True)
            
            for file_name in files:
                src_path = os.path.join(AGENTS_DIR_GLOBAL, category, file_name)
                dest_path = os.path.join(category_dir, file_name)
                
                if os.path.exists(src_path):
                    if not DRY_RUN:
                        if os.path.isdir(src_path):
                            # Recursive injection logic handling deeply embedded structural directory chains via copytree mapping.
                            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src_path, dest_path)
                    
                    if VERBOSE or DRY_RUN:
                        action = "Would sync" if DRY_RUN else "Synced"
                        print_status(f"[{action}] {file_name} -> {category_dir}/")
                        
                    copied_files.append((category, file_name))
                else:
                    print_warning(f"Required file/dir {file_name} not found in {AGENTS_DIR_GLOBAL}{category}/")

    # Document Compilation: Structurally outlines the deployed assets building `AGENTS.md`.
    agents_md_path = os.path.join(local_agents_dir, "AGENTS.md")
    if VERBOSE and DRY_RUN:
        print_status(f"DRY RUN: Would generate AGENTS.md registry mapping.")
    elif not DRY_RUN:
        with open(agents_md_path, "w") as f:
            f.write(f"# AGENT REGISTRY\n\n")
            f.write(f"This file is auto-generated by sprawl sync.\n\n")
            categories = ["rules", "skills", "atoms", "workflows"]
            for cat in categories:
                cat_files = [fn for c, fn in copied_files if c == cat]
                if cat_files:
                    f.write(f"## {cat.capitalize()}\n")
                    for fn in cat_files:
                        f.write(f"- {fn}\n")
                    f.write("\n")

    # Server Compilation: Constructs the Model Context Protocol binding maps dynamically exposing the skills context pipeline.
    mcp_config_path = os.path.join(local_agents_dir, "mcp_config.json")
    mcp_config = {"mcpServers": {}}
    
    for c, fn in copied_files:
        if c == "skills":
            mcp_config["mcpServers"][f"local_{fn.replace('.', '_')}"] = {
                "command": "python3",
                "args": [f".agents/{c}/{fn}"]
            }
            
    if VERBOSE and DRY_RUN:
        print_status(f"DRY RUN: Would generate mcp_config.json routing pipeline.")
    elif not DRY_RUN:
        with open(mcp_config_path, "w") as f:
            json.dump(mcp_config, f, indent=4)
        
    if not DRY_RUN:
        print_status(f"Sync complete for {app_dir}")
    else:
        print_status(f"Dry Run Execution complete for {app_dir}")


def cmd_sync():
    """
    Context Orchestrator:
    Monitors relative path execution mapping bounding scopes natively logic ensuring global or atomic isolation execution patterns.
    """
    cwd = os.getcwd()
    
    if os.path.commonpath([cwd, SPRAWL_DIR]) == SPRAWL_DIR and cwd != SPRAWL_DIR:
        # TARGETED MODE: Isolated Sync execution logic invoked directly within a specific target context directory mapping.
        if VERBOSE:
            print_status("Running sync in TARGETED MODE.")
        sync_app_directory(cwd)
    else:
        # RECURSIVE MODE: Massive iteration mapping iterating and broadcasting syncing rules dynamically top-chunk array targets mapping out locally.
        if VERBOSE:
            print_status(f"Running sync in RECURSIVE MODE inside {SPRAWL_DIR}...")
        if not os.path.exists(SPRAWL_DIR):
            print_error(f"Sprawl Hub directory not found at {SPRAWL_DIR}")
            sys.exit(1)
            
        for item in os.listdir(SPRAWL_DIR):
            item_path = os.path.join(SPRAWL_DIR, item)
            if os.path.isdir(item_path):
                sync_app_directory(item_path)


def cmd_man():
    """Reads and prints the global README.md acting as a native CLI man page."""
    # Resolve the absolute real path of this script to navigate securely regardless of symlinks
    script_path = os.path.realpath(__file__)
    repo_root = os.path.dirname(os.path.dirname(script_path))
    readme_path = os.path.join(repo_root, "README.md")
    
    if os.path.exists(readme_path):
        with open(readme_path, "r") as f:
            print(f"{CYAN}{f.read()}{RESET}")
    else:
        print_error(f"Manual not found! Expected at: {readme_path}")
        sys.exit(1)


def print_help():
    """Outputs the stylish Sprawl ASCII logo and the terminal instructions manual."""
    # Cyber-Brutalist ASCII representation (Raw string to avoid escape sequence warnings)
    print(f"{CYAN}")
    print(r"""+----------------------------------------------------------+
|   _____                           __   ________    ____  |
|  / ___/____  _________ __      __/ /  / ____/ /   /  _/  |
|  \__ \/ __ \/ ___/ __ `/ | /| / / /  / /   / /    / /    |
| ___/ / /_/ / /  / /_/ /| |/ |/ / /  / /___/ /____/ /     |
|/____/ .___/_/   \__,_/ |__/|__/_/   \____/_____/___/     |
|    /_/                                                   |
|                                                          |
|              === Atomic Agentic Fabric ===               |
|                     by YOUNES_BAGHOR                     |
+----------------------------------------------------------+""")
    print(f"{RESET}")
    print("Usage: sprawl <command> [args]\n")
    print("Commands:")
    print("  init <GIT_URL>      Clones your Sovereign DNA globally (~/.agents) and links the CLI.")
    print("  create <APP_NAME>   Scaffolds a new standard application inside ~/Documents/Sprawl/")
    print("  sync                Injects rules, skills, and workflows from your DNA into local scope.")
    print("  man                 Prints the comprehensive AAF manual and setup guide directly.")
    print("\nOptions:")
    print("  -v, --version       Checks the active Sprawl engine version structure.")
    print("  --verbose           Engages strict logging mode dumping tracking execution outputs.")
    print("  --dry-run           Safety mode; simulates structural file logic without destroying paths.")
    print("  -h, --help          Display this interactive setup screen.\n")


if __name__ == "__main__":
    """Global execution pipeline routing."""
    
    # Pre-parse Global Native Extrapolators mapped inside standard Python lists
    clean_args = []
    for arg in sys.argv:
        if arg == "--verbose":
            VERBOSE = True
        elif arg == "--dry-run":
            DRY_RUN = True
        else:
            clean_args.append(arg)

    if len(clean_args) < 2 or clean_args[1] in ["-h", "--help", "-help"]:
        print_help()
        sys.exit(0)
        
    if clean_args[1] in ["-v", "--version", "version"]:
        print_status(f"Sprawl Orchestrator {VERSION} (Atomic Agentic Fabric)")
        sys.exit(0)

    command = clean_args[1]

    if command == "init":
        if len(clean_args) < 3:
            print_error("Usage: sprawl init <GIT_URL>")
            sys.exit(1)
        cmd_init(clean_args[2])
    elif command == "create":
        if len(clean_args) < 3:
            print_error("Usage: sprawl create <APP_NAME>")
            sys.exit(1)
        cmd_create(clean_args[2]) 
    elif command == "sync":
        cmd_sync()
    elif command == "man":
        cmd_man()
    else:
        print_error(f"Unknown command: {command}")
        print_help()
        sys.exit(1)
