# Script Export

This page explains how to export created menus as AutoHotkey scripts.

## Export Feature

### Basic Export Steps

1. **"File" → "Export AHK Script"** from menu bar
2. Select output folder
3. Click "OK"

Upon export completion, the following files/folders are created:

```
MyRadifyMenu/
├── MyMenu.ahk           # Main script
├── Radify.ahk           # Radify library
├── Lib/
│   └── Gdip_All.ahk     # GDI+ library
└── images/              # Icons used
    ├── icon1.png
    ├── icon2.png
    └── ...
```

## Output Files

### Main Script (.ahk)

AutoHotkey v2 script containing menu configuration.

Main contents:

- Radify library include
- Menu structure definition
- Action definitions for each item
- Hotkey settings (launch key)

### Radify.ahk

Core library for ring menu rendering. Do not modify this file.

### Lib/Gdip_All.ahk

Advanced graphics rendering library using GDI+.

### images/

All icon images used in the menu are automatically copied.

## Running Output Script

### Basic Execution

1. Double-click `.ahk` file in output folder
2. AutoHotkey icon appears in taskbar
3. Open menu with configured hotkey (default: `Ctrl+Space`)

### Customizing Hotkey

Open script and edit hotkey section:

```ahk
; Default
^Space::myMainMenu.Show()

; Example change: Win+Z key
#z::myMainMenu.Show()
```

!!! tip "Hotkey Notation"
    - `^`: Ctrl
    - `!`: Alt
    - `+`: Shift
    - `#`: Win

## Creating Portable Package

### Complete Portable Environment

The output folder contains all necessary files, so it can be used for:

#### Portable on USB Drive

1. Copy output folder to USB drive
2. Run on any Windows PC (AutoHotkey v2 required)

#### Use on Other PCs

1. ZIP compress output folder
2. Share via email or cloud
3. Extract and run

### Dependencies

**AutoHotkey v2** installation is required for execution.

Compiling to standalone executable (.exe) allows execution without AutoHotkey installation (described later).

## Script Customization

### Auto-Start on Launch

Register in Windows startup:

1. Open Run dialog with `Win+R`
2. Enter `shell:startup`
3. Create script shortcut and place in startup folder

### Switching Multiple Menus

Call different menus with different hotkeys:

```ahk
^Space::myMainMenu.Show()
^!Space::mySubMenu.Show()
```

## Compiling to EXE

### Using Ahk2Exe

Use `Ahk2Exe` included with AutoHotkey v2 to convert script to executable:

1. Launch Ahk2Exe
2. **Source (script file)**: Select main script
3. **Destination (.exe file)**: Specify output location
4. **Base File**: Select AutoHotkey32.exe or AutoHotkey64.exe
5. Click **Convert**

!!! warning "Note"
    When compiling, `Lib/` folder and `images/` folder must also be placed in same location as EXE.

### Distribution Package

For distribution, bundle the following in a folder:

```
MyRadifyMenu_Portable/
├── MyMenu.exe
├── Radify.ahk
├── Lib/
│   └── Gdip_All.ahk
└── images/
    └── ...
```

## Version Control

### Configuration File Backup

Editor auto-creates backups, but manual saving is also recommended:

1. Copy `menu_config.json`
2. Save with date or version number
   - `menu_config_v1.0.json`
   - `menu_config_20260113.json`

## Best Practices

### Regular Export

Export current state as backup before major menu changes.

### Documentation

For complex menu structures, documenting structure and usage in README.txt is helpful.

## Troubleshooting

### Script Won't Start

1. Verify AutoHotkey v2 is installed
2. Verify script file extension is `.ahk`
3. Check error messages (right-click → "Edit Script" to view contents)

### Icons Don't Display

1. Verify `images/` folder is in same directory
2. Verify image files actually exist
3. Verify paths are correctly written as relative paths

### Actions Don't Execute

1. Check action definitions in script
2. Check for syntax errors
3. Debug with `MsgBox`

## Next Steps

- [Custom Actions](../advanced/custom-actions.md)
- [Managing Multiple Menus](../advanced/multiple-menus.md)
- [Troubleshooting](../advanced/troubleshooting.md)
