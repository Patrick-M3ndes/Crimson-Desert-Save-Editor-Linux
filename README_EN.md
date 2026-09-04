# ⚔️ Crimson Desert - Item & Currency Save Editor (Linux & Windows)

[🇧🇷 Versão em Português](README.md) | [🇺🇸 English Version](README_EN.md)

A lightweight, fast, and high-precision Python save editor for **Crimson Desert** compatible with **Linux & Windows**.

> 🟢 **Status**: Tested and **working perfectly** on game version **2.01.00**!

---

## ⚡ Quick Launch Guide (1-Click / Easy Mode)

To easily run the application without typing commands manually:

### 🐧 On Linux:
- Open terminal in project folder and run:
  ```bash
  ./run.sh
  ```
  *(Or double-click `run.sh` in your file manager and choose "Run in Terminal").*

### 🪟 On Windows:
- **Double-click** the **`run.bat`** file inside the project folder. It will set up everything automatically and open the Save Editor screen!

---

## 💻 Complete Manual Guide for All Terminals (Linux & Windows)

If you prefer running commands manually in your favorite terminal:

### 🐧 Linux (Shell & Terminal Variations)

#### 1. Bash / Zsh (Ubuntu, Debian, Fedora, Arch Linux, Pop!_OS, etc.)
```bash
# Navigate to project folder
cd Crimson-Desert-Save-Editor-Linux-Windows

# Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements & launch
pip install -r requirements.txt
python3 main.py
```

#### 2. Fish Shell
```fish
# Create & activate virtual environment in Fish
python3 -m venv .venv
source .venv/bin/activate.fish

# Install requirements & launch
pip install -r requirements.txt
python3 main.py
```

---

### 🪟 Windows (Terminal Variations)

#### 1. PowerShell
```powershell
# Navigate to project folder
cd Crimson-Desert-Save-Editor-Linux-Windows

# Create & activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install requirements & launch
pip install -r requirements.txt
python main.py
```
> 💡 *Tip*: If PowerShell blocks script execution, run this first: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

#### 2. Command Prompt (`cmd.exe`)
```cmd
# Navigate to project folder
cd Crimson-Desert-Save-Editor-Linux-Windows

# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

# Install requirements & launch
pip install -r requirements.txt
python main.py
```

#### 3. Git Bash on Windows
```bash
# Create & activate virtual environment in Git Bash
python -m venv .venv
source .venv/Scripts/activate

# Install requirements & launch
pip install -r requirements.txt
python main.py
```

---

## 🎮 Step-by-Step Interactive Menu Guide

Once launched (`python main.py` or via `run.sh` / `run.bat`), the interactive terminal menu will appear:

```txt
==================================================
  CRIMSON DESERT - SAVE EDITOR (v2.01.00)
==================================================
 1. Select Save Slot
 2. 💰 Edit Money & Camp Resources
 3. View Full Inventory
 4. Search Item in Current Inventory
 5. Search Global Item Database
 6. Save Changes
 7. Restore Backup
 0. Exit
==================================================
```

### Simple Usage Instructions:

1. **Press `1` and hit Enter**: The application scans your computer automatically for Crimson Desert save files (on both Windows & Linux) and displays available slots with modification timestamps. Select your slot number.
2. **Press `2` and hit Enter**: Modify your player coins (`Copper`) and camp resources (`Camp Funds`, `Food`, `Timber`, `Stone`, `Weapons`).
3. **Press `3` or `4` and hit Enter**: Browse your inventory, select an item number, and edit stack counts, enchantment levels (`+0` to `+20`), or swap it for any other item from the database.
4. **Press `6` and hit Enter**: Saves changes securely, recalculates HMAC checksums, and clears cloud desync files.
5. **Launch Crimson Desert**: Load your edited save slot in-game, verify changes, and perform a new save in-game to sync with Steam Cloud automatically.

---

## ✨ Key Features

- **Cross-Platform Auto-Detection**: Automatically locates save files on both **Linux** (Steam/Proton default paths) and **Windows** (`%LOCALAPPDATA%\Pearl Abyss\CD\save`).
- **Slot Identification with Timestamps**: Displays exact date and time of last save modification for each slot (e.g., `26/08/2026 at 14:59:02`).
- **💰 Money & Camp Resources Editing**: Edit player coins (`Copper`) and camp funds (`Camp Funds`, `Food`, `Timber`, `Stone`, `Weapons`).
- **Global Item Database (6,200+ Items)**: Cataloged database of over 6,200 items for easy search and item swapping.
- **Interactive Inventory Browser & Search**: Page-by-page inventory navigation or search items directly by name.
- **Stack Count Editing**: Change quantity of any consumable or crafting material.
- **Enchantment & Durability Modification**: Change weapon/armor enchantment levels (`+0` to `+20`), durability, and sharpness.
- **Item Swapping / Replacement**: Convert any item in your inventory into any other item from the database.
- **Anti-Corruption Protection (HMAC Recalculation)**: Automatically recalculates the save file's integrity signature (HMAC/Checksum) so the game never reports the save as corrupt.
- **Anti-Crash / Steam Cloud Sync Fix (`steam_autocloud.vdf`)**: Automatically removes obsolete cloud metadata to prevent Steam Cloud from overwriting your changes or crashing at startup.
- **Automated Timestamped Backups & One-Click Restore**: Creates `.bak` backups before writing modifications and allows quick restoration via the terminal menu.

---

## 🛡️ Safety & Backups

The editor creates a timestamped backup (`save.save.YYYYMMDD_HHMMSS.bak`) in the save folder prior to applying any modification. If you wish to revert changes, simply select **Option 7 (Restore Backup)** in the main menu.

---

## 📄 License

Distributed under the MIT License for educational and entertainment purposes.
