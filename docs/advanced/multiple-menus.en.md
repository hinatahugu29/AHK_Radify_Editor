# Managing Multiple Menus

This page explains how to efficiently manage multiple ring menus.

## Need for Multiple Menus

### Use Cases

- **Purpose-Specific Menus**: Work, personal, etc.
- **App-Specific Menus**: Used only in specific applications
- **Hierarchical Menus**: Deep hierarchies with submenus
- **Theme-Based Menus**: Development, media editing, etc.

## Utilizing Submenus

### Creating Submenus

1. Select item in main menu
2. Click "Add Submenu" button
3. Enter submenu name
4. Add rings and items to submenu

### Submenu Structure

```json
{
  "main_menu": [
    {
      "ring": 1,
      "items": [
        {
          "label": "Dev Tools",
          "submenu": "DevMenu"
        }
      ]
    }
  ],
  "submenus": {
    "DevMenu": [
      {
        "ring": 1,
        "items": [
          {"label": "VS Code", "action": "Run \"code\""},
          {"label": "Git Bash", "action": "Run \"git-bash.exe\""}
        ]
      }
    ]
  }
}
```

## Multiple Configuration Files

### Separating Configuration Files

Create separate configuration files for each purpose:

```
configs/
├── menu_work.json      # Work
├── menu_personal.json  # Personal
└── menu_gaming.json    # Gaming
```

### Switching Configurations

In editor, select desired configuration file via "File" → "Open Configuration."

## Dynamic Menu Switching

### Switching in AutoHotkey Script

Integrate multiple menus in one script:

```ahk
#Include Radify.ahk

; Menu 1 definition
menu1 := RadifyMenu()
menu1.items := [...]

; Menu 2 definition
menu2 := RadifyMenu()
menu2.items := [...]

; Switch menus with hotkeys
^Space::menu1.Show()
^!Space::menu2.Show()
```

### Context-Dependent Menus

Switch menus based on active window:

```ahk
^Space::
{
    if WinActive("ahk_exe code.exe")
        devMenu.Show()
    else if WinActive("ahk_exe chrome.exe")
        webMenu.Show()
    else
        mainMenu.Show()
}
```

## Best Practices

### Naming Conventions

Use clear file and menu names:

```
menu_work_development.json
menu_personal_media.json
menu_gaming_shortcuts.json
```

### Documentation

Document each menu's purpose in README.md:

```markdown
# Menu Configuration

- **menu_main.json**: Main menu (general)
- **menu_dev.json**: Development tools
- **menu_media.json**: Media editing
```

## Troubleshooting

### Too Many Menus to Manage

- Consolidate menus
- Use submenus for hierarchy
- Delete infrequently used menus

## Next Steps

- [Troubleshooting](troubleshooting.md)
- [Custom Actions](custom-actions.md)
