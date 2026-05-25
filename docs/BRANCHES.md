# Branch layout

## `main` (deploy from here)

Production-ready application and documentation only.

**Included**

- Django apps: `config/`, `core/`, `site_settings/`, `pages/`, `content/`, `catalog/`, `inquiries/`
- `manage.py`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini`
- `.env.example`, `README.md`, `docs/`
- Management commands in `core/management/` (`seed_demo_data`, `benchmark_apis`) for staging checks and local integrators

**Not in git on `main`** (ignored via `.gitignore`)

- `.planning/` — internal planning artifacts
- `AGENTS.md`, `bymer_project_info.md`, `bymer_be_base_prompt.md`
- `.codex/`, `.cursor/`, `.agent/`, `.agents/`, `.claude/`, `.gemini/`, `.opencode/` — local tooling only

Merge flow: finish work on `development`, run tests, merge into `main` without the paths above.

## `development` (active work)

Everything on `main`, plus tracked planning and project notes:

- `.planning/` — roadmap, phase plans, state
- `AGENTS.md`, `bymer_project_info.md`, `bymer_be_base_prompt.md`

AI/editor folders (`.codex/`, `.cursor/`, etc.) stay **untracked** on both branches so they never pollute either history; keep them only on your machine under `development` checkouts.

## `.gitignore` differs by branch

| Branch | Extra ignore rules |
|--------|-------------------|
| **`main`** | `.planning/`, `AGENTS.md`, spec markdown files, `.codex/`, `.cursor/`, etc. |
| **`development`** | Shared rules only (so `.planning/` stays tracked) |

After merging, fix `.gitignore` if Git merged the wrong variant: **short file on `development`**, **long file on `main`**.

## Keeping branches in sync

```powershell
# After features are ready on development:
git checkout main
git merge development
git rm -r --cached .planning AGENTS.md bymer_project_info.md bymer_be_base_prompt.md 2>$null
# Restore main .gitignore (dev-only section) if the merge overwrote it
git add .gitignore
git commit -m "Release: merge development into main"
git push origin main

git checkout development
git merge main
# Keep development .gitignore (no .planning/ line)
git commit -m "merge main"  # only if you fixed .gitignore
```
