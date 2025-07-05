# Running on Windows

## Quick Start (with uv)

1. Install uv:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. In the project folder, run:
   ```
   uv sync
   uv run wizards-workshop
   ```

## Alternative (with Python)

1. Make sure Python 3.10+ is installed

2. In the project folder:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install ursina pillow
   python src/wizards_workshop/main.py
   ```

## Troubleshooting

- If uv command not found: restart your terminal after installation
- If graphics issues: update your graphics drivers
- The game window should appear after a few seconds of loading