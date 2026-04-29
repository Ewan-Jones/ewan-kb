"""`ewankb config` — Show or edit project configuration."""

import json
import os

from ._helpers import resolve_kb_dir


def run(args):
    kb_dir = resolve_kb_dir()
    config_file = kb_dir / "project_config.json"
    llm_file = kb_dir / "llm_config.json"

    if getattr(args, 'edit_llm', False):
        editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "vim")
        os.system(f'"{editor}" "{llm_file}"')
    elif args.edit:
        editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "vim")
        os.system(f'"{editor}" "{config_file}"')
    elif args.show:
        with open(config_file, encoding="utf-8") as f:
            print(f.read())
    else:
        with open(config_file, encoding="utf-8") as f:
            data = json.load(f)
        print(f"project_name: {data.get('project_name', '?')}")
        print(f"system_name:  {data.get('system_name', '?')}")
        domains_file = kb_dir / "domains" / "_meta" / "domains.json"
        if domains_file.exists():
            with open(domains_file, encoding="utf-8") as f:
                domains_data = json.load(f)
            domain_list = domains_data.get("domain_list", [])
            print(f"domains:      {len(domain_list)} (auto-discovered)")
            for d in domain_list[:10]:
                print(f"  - {d}")
            if len(domain_list) > 10:
                print(f"  ... and {len(domain_list) - 10} more")
        else:
            print("domains:      (not yet discovered — run ewankb extract)")
