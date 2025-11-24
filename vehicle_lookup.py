#!/usr/bin/env python3
# Firewall Breaker - Vehicle Info 
# Created by: thakur2309
# YouTube: Firewall Breaker

"""
DISCLAIMER:
This tool is for EDUCATIONAL and ETHICAL USE ONLY.
Unauthorized tracking, surveillance or background searches
without permission may be ILLEGAL. Use responsibly.
"""

import sys
import os
import json
import time
import hashlib
import requests
from urllib.parse import urlencode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.align import Align
from datetime import datetime

API_BASE = "https://vehicleinfobyterabaap.vercel.app/lookup"
VERSION = "2.0 PRO"
console = Console()

# ==================== UTILITIES ====================
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def ensure_dirs():
    os.makedirs("results", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("cache", exist_ok=True)

def log(msg):
    with open("logs/firewall.log", "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def cache_path(rc):
    return f"cache/{hashlib.md5(rc.encode()).hexdigest()}.json"

def save_cache(rc, data):
    with open(cache_path(rc), "w") as f:
        json.dump(data, f, indent=4)

def load_cache(rc):
    path = cache_path(rc)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


# ==================== UI / BANNER ====================
def loading_animation():
    console.print("\n[bold green]Initializing Firewall Breaker...[/bold green]\n")
    for step in ["Booting modules", "Checking network", "Loading UI", "Starting engine"]:
        console.print(f"[bold cyan]>> {step}...[/bold cyan]")
        time.sleep(0.3)
    time.sleep(0.4)

def banner():
    console.rule()
    console.print(Align.center(f"[bold red]FIREWALL BREAKER[/bold red]  •  [yellow]{VERSION}[/yellow]"))
    console.print(Align.center("[green]Created by: thakur2309 • YouTube: Firewall Breaker[/green]"))
    console.rule()
    console.print(
        Panel(
            "[bold white on red] DISCLAIMER [/bold white on red]\nThis tool is for lawful, educational use only.",
            style="red",
            expand=False,
        )
    )
    console.rule()

# ==================== CORE LOGIC ====================
def get_rc_input():
    console.print("\n[bold cyan]Enter Vehicle RC number:[/bold cyan] ", end="")
    return input().strip()

def fetch_vehicle_data(rc):
    cached = load_cache(rc)
    if cached:
        return cached, True

    params = {"rc": rc}
    url = f"{API_BASE}?{urlencode(params)}"

    start = time.time()
    try:
        resp = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "FirewallBreaker/PRO (by thakur2309)"},
        )
    except Exception as e:
        return {"error": str(e)}, False

    duration = round((time.time() - start) * 1000, 2)

    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code} – {resp.text}"}, False

    try:
        data = resp.json()
    except:
        return {"error": "Invalid JSON returned by API."}, False

    data["_api_time"] = duration
    save_cache(rc, data)
    return data, False

def export_json(rc, data):
    path = f"results/{rc}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def print_results(rc, data, from_cache):
    tool_info = f"[bold magenta]Firewall Breaker PRO[/bold magenta]  •  [bold magenta]by thakur2309[/bold magenta]"
    console.print(Panel(tool_info, style="magenta", expand=False))

    if "error" in data:
        console.print(Panel(f"[bold red]Error:[/bold red] {data['error']}", style="red"))
        return

    api_time = data.get("_api_time", None)

    status = Panel(
        f"[bold green]API: OK[/bold green]\nCached: {'YES' if from_cache else 'NO'}\nResponse Time: {api_time} ms",
        style="green",
        expand=False,
    )
    console.print(status)

    
    if "_api_time" in data:
        del data["_api_time"]

    table = Table(
        title=f"Vehicle Information — {rc}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for k, v in data.items():
        table.add_row(k.replace("_", " ").title(), str(v))

    console.print(table)

    console.print(
        "[bold yellow]Result saved to 'results/' folder. Logs saved in 'logs/' folder.[/bold yellow]\n"
    )

    console.print(
        Panel(
            Align.center(
                "Made with ♥ by Firewall Breaker\nYouTube: Firewall Breaker",
                vertical="middle",
            ),
            style="blue",
        )
    )


# ==================== ENTRY ====================
def main():
    ensure_dirs()
    clear_screen()
    loading_animation()
    banner()

    
    if len(sys.argv) > 1 and sys.argv[1].startswith("--rc="):
        rc = sys.argv[1].replace("--rc=", "")
    else:
        rc = get_rc_input()

    if not rc:
        console.print("[bold red]No RC entered – exiting.[/bold red]")
        sys.exit(1)

    log(f"Query started for RC: {rc}")

    data, from_cache = fetch_vehicle_data(rc)
    print_results(rc, data, from_cache)

    if "error" not in data:
        export_json(rc, data)
        log(f"Result exported for RC: {rc}")

    console.print("\n[bold green]Done.[/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user – exiting.[/bold red]")
        sys.exit(0)
