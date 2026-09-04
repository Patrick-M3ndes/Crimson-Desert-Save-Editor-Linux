# ⚔️ Crimson Desert - Item & Currency Save Editor (Linux & Windows)

[🇧🇷 Versão em Português](README.md) | [🇺🇸 English Version](README_EN.md)

A lightweight, fast, and high-precision Python save editor for **Crimson Desert** compatible with **Linux & Windows**.

> 🟢 **Status**: Tested and **working perfectly** on game version **2.01.00**!

---

## 📌 Overview

This tool was built to run directly in your terminal (Linux & Windows), allowing you to inspect your save file, modify player and camp currencies, change item quantities (stack counts), replace items with any item from a 6,200+ database, and safely manage timestamped backups.

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

## 🛡️ Protection & Steam Sync Mechanisms

### 1. Anti-Corruption Integrity Protection
Crimson Desert validates save files using an HMAC integrity signature. If you edit a save file without recalculating this signature, the game engine will reject it as corrupted. This editor **automatically recalculates and re-signs the HMAC key** upon saving, ensuring the game accepts your save seamlessly.

### 2. Steam Cloud Conflict Prevention (Anti-Crash)
When saving changes, the editor clears the local cloud metadata file (`steam_autocloud.vdf`). This prevents Steam from detecting a cloud conflict before launch and overwriting your edited save or crashing on the title screen.

### 3. Automatic Steam Cloud Re-Synchronization
After making edits in the save editor:
1. Launch Crimson Desert and load your edited save slot.
2. Verify your new items or currencies in-game, then perform a **new save (manual or quick save)** inside the game.
3. Upon saving in-game, Steam will generate fresh metadata and **automatically sync your modified save to the Steam Cloud**.

---

## 🛠️ System Requirements

- **Operating System**: Linux (Ubuntu, Debian, Fedora, Arch Linux, Pop!_OS, etc.) OR Windows 10/11.
- **Python**: Version 3.8 or higher (`python --version` or `python3 --version`).
- **Git**: (Optional, to clone repository).

---

## 🚀 Installation & Running Guide

### 🐧 Linux (Terminal)

```bash
# 1. Clone repository
git clone https://github.com/Patrick-M3ndes/Crimson-Desert-Save-Editor-Linux-Windows.git
cd Crimson-Desert-Save-Editor-Linux-Windows

# 2. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run Save Editor
python main.py
```

---

### 🪟 Windows (PowerShell / Command Prompt)

```powershell
# 1. Clone repository
git clone https://github.com/Patrick-M3ndes/Crimson-Desert-Save-Editor-Linux-Windows.git
cd Crimson-Desert-Save-Editor-Linux-Windows

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run Save Editor
python main.py
```

> 💡 **Tip**: Whenever you open a new terminal window to run the script, remember to activate the virtual environment first (`source .venv/bin/activate` on Linux or `.venv\Scripts\activate` on Windows).

---

## 🎮 Interactive Menu Overview

When running `python main.py`, the terminal menu will appear:

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

---

## 🛡️ Safety & Backups

The editor creates a timestamped backup (`save.save.YYYYMMDD_HHMMSS.bak`) in the save folder prior to applying any modification. If you wish to revert changes, simply select **Option 7 (Restore Backup)** in the main menu.

---

## 📄 License

Distributed under the MIT License for educational and entertainment purposes.
