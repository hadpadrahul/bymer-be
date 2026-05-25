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

## Keeping branches in sync

```powershell
# After features are ready on development:
git checkout main
git merge development
# Resolve if needed; ensure .gitignore on main still lists dev-only paths
git push origin main

git checkout development
git merge main
```

On `main`, if merge brings in `.planning/` or agent config files, remove them from the commit:

```powershell
git rm -r --cached .planning AGENTS.md bymer_project_info.md bymer_be_base_prompt.md
git commit -m "Keep main free of development-only artifacts"
```
