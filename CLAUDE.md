# Mockup Generator — Claude Instructions

## Project
- Path: `/Users/simon101ways/AI/Code/mockup-generator`
- Purpose: CLI tool to composite master artwork onto frame template mockups for BigCommerce product variants (~10 variants per product)

## Stack
- Python, Pillow, PyYAML, matplotlib

## Key Files
- `mockup_generator.py` — main CLI entry point
- `locate.py` — interactive helper to click artwork area corners and output placement coordinates
- `config.yaml` — defines variants (name, template path, placement x/y/w/h, fit_mode)
- `requirements.txt`
- `templates/` — frame mockup PNGs go here
- `output/` — generated variant images land here

## How It Works
- Templates with a **transparent artwork area**: artwork is placed behind the frame (alpha composite)
- Templates with a **solid placeholder**: artwork is pasted directly at the placement coordinates
- Output naming: `{artwork_stem}_{variant_name}.jpg`

## Config Options
- `fit_mode: stretch` — fill placement area exactly (default)
- `fit_mode: fit` — maintain aspect ratio, letterbox with white
- `fit_mode: fill` — maintain aspect ratio, crop to fill

## GitHub
- Account: `simon-attard`
- Repo: https://github.com/simon-attard/mockup-generator
- Auth: `gh` CLI (v2.87.2) authenticated via keyring, use full path `/usr/local/Cellar/gh/2.87.2/bin/gh` until terminal is restarted
- Push via HTTPS with token: `git remote set-url origin https://simon-attard:$(gh auth token)@github.com/simon-attard/mockup-generator.git`

## Preferences
- Always ask before pushing to GitHub or taking other actions that affect shared systems
- Keep this CLAUDE.md updated as the project evolves
