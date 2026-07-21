# Operations Guide

## Local execution

macOS/Linux:

```bash
./scripts/run_local.sh
```

Windows PowerShell:

```powershell
.\scripts\run_local.ps1
```

Open `http://localhost:8000`.

## Manual snapshot build

```bash
python3 validate_data.py
python3 -m unittest discover -s tests -v
python3 build_snapshot.py
```

## GitHub Pages setup

1. Create a new repository.
2. Upload the extracted package contents to the repository root.
3. Set the default branch to `main`.
4. Open **Settings → Pages**.
5. Under **Build and deployment**, select **GitHub Actions**.
6. Run **Build and deploy dashboard** manually or push a commit.

## Configuration before use

Update `config/dashboard.json`:

- `jira_base_url`
- `repository_url`
- `timezone`

## Ad-hoc publication

Open **Actions → Build and deploy dashboard → Run workflow**.

## Scheduled publication

The workflow runs at 12:00 and 18:00 Hong Kong time using UTC cron expressions.
Update the workflow cron values when another timezone is required.
