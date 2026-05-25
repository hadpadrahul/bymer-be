# Branches

## `main` — clean deployable project

Only what you need to run, test, document, and deploy the backend.

| Included | Excluded (never on `main`) |
|----------|----------------------------|
| Django apps, `manage.py`, migrations, tests | `.planning/` |
| `requirements.txt`, `requirements-dev.txt`, `pytest.ini` | `.codex/`, `.cursor/`, and other agent tool folders |
| `.env.example`, `README.md`, `docs/` | `AGENTS.md` |
| `core/management/` scripts (`seed_demo_data`, `benchmark_apis`) | `bymer_project_info.md`, `bymer_be_base_prompt.md` |

Deploy and release from `main`.

## `development` — everything else for active work

Same application and docs as `main`, **plus** files you only need while building:

| Also on `development` | Still local only (gitignored) |
|-------------------------|-------------------------------|
| `.planning/` | `.codex/`, `.cursor/`, `.agent/`, `.agents/`, `.claude/`, `.gemini/`, `.opencode/` |
| `bymer_project_info.md`, `bymer_be_base_prompt.md` | |
| `AGENTS.md` (optional workspace notes) | |

Push feature work to `development`. When ready for production, merge into `main` and strip dev-only paths (see below).

## `.gitignore` per branch

- **`development`** — shared rules + agent folders (above). `.planning/` is **not** ignored so it stays in git.
- **`main`** — shared rules + agent folders + `.planning/` + `AGENTS.md` + project spec markdown files.

If a merge overwrites the wrong `.gitignore`, restore: short file on `development`, long file on `main`.

## Merge `development` → `main`

```powershell
git checkout main
git merge development
git rm -r --cached .planning AGENTS.md bymer_project_info.md bymer_be_base_prompt.md 2>$null
# Ensure main .gitignore still lists the dev-only section
git add .gitignore
git commit -m "Release: merge development into main"
```

Then merge `main` back into `development` and keep the **development** `.gitignore` (no `.planning/` line).
