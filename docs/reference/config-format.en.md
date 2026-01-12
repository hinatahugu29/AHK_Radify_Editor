# Configuration File Format

This page explains the format of configuration files used by Radify Menu Editor.

## menu_config.json

JSON file containing menu structure and all settings.

### Basic Structure

```json
{
  "image_dir": "images",
  "main_menu": [...],
  "submenus": {...},
  "menu_options": {...},
  "favorites": [...]
}
```

### Top-Level Fields

#### image_dir

```json
"image_dir": "images"
```

Path to directory containing icon images (relative path).

#### main_menu

```json
"main_menu": [
  {
    "ring": 1,
    "items": [...]
  },
  {
    "ring": 2,
    "items": [...]
  }
]
```

Array defining main menu ring structure.

#### submenus

```json
"submenus": {
  "ToolsMenu": [...],
  "SettingsMenu": [...]
}
```

Submenu definitions. Keys are submenu names, values are ring arrays.

#### menu_options

```json
"menu_options": {
  "skin": "Default",
  "EnableGlow": true,
  "itemSize": 60,
  "ringSpacing": 80,
  "menu_name": "myMainMenu",
  "gui_font_family": "",
  "gui_font_size": 12,
  "appearance_mode": "Dark"
}
```

Global menu settings.

## Ring Structure

### Ring Object

```json
{
  "ring": 1,
  "items": [...]
}
```

- **ring**: Ring number (starts from 1, inside to outside)
- **items**: Array of items placed in this ring

## Item Structure

### Basic Item

```json
{
  "label": "Notepad",
  "icon": "images/notepad.png",
  "action": "Run \"notepad.exe\""
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|---|---|---|---|
| `label` | String | Yes | Label text displayed on item |
| `icon` | String | No | Icon image path (relative or absolute) |
| `action` | String | No | AutoHotkey code executed on click |

### Submenu Link

```json
{
  "label": "Tools",
  "icon": "images/tool-box.png",
  "submenu": "ToolsMenu"
}
```

- **submenu**: Destination submenu name (matches key in `submenus`)

## Menu Options Details

### skin

```json
"skin": "Default"
```

Skin name to use.

Available values:
- `"Default"`
- `"Dark"`
- `"Light"`
- `"Custom"`

### EnableGlow

```json
"EnableGlow": true
```

Enable/disable item glow (glowing) effect.

- `true`: Enabled
- `false`: Disabled

### itemSize

```json
"itemSize": 60
```

Item icon size (in pixels).

Recommended range: 40 ~ 100

### ringSpacing

```json
"ringSpacing": 80
```

Distance between rings (in pixels).

Recommended range: 60 ~ 120

### menu_name

```json
"menu_name": "myMainMenu"
```

Menu object variable name used in AutoHotkey script.

Naming convention: Alphanumeric and underscore only, cannot start with number

## Complete Example

### Simple Menu

```json
{
  "image_dir": "images",
  "main_menu": [
    {
      "ring": 1,
      "items": [
        {
          "label": "Notepad",
          "icon": "images/notepad.png",
          "action": "Run \"notepad.exe\""
        },
        {
          "label": "Calculator",
          "icon": "images/calculator.png",
          "action": "Run \"calc.exe\""
        },
        {
          "label": "Google",
          "icon": "images/google.png",
          "action": "Run \"https://www.google.com\""
        }
      ]
    }
  ],
  "submenus": {},
  "menu_options": {
    "skin": "Default",
    "EnableGlow": true,
    "itemSize": 60,
    "ringSpacing": 80,
    "menu_name": "myMainMenu",
    "gui_font_family": "",
    "gui_font_size": 12,
    "appearance_mode": "Dark"
  },
  "favorites": []
}
```

## Manual Editing

### Importance of Backup

Always create a backup before manual editing.

```bash
copy menu_config.json menu_config.backup.json
```

### JSON Validation

Verify JSON syntax is correct after editing.

Online tools:
- [JSONLint](https://jsonlint.com/)
- [JSON Formatter](https://jsonformatter.curiousconcept.com/)

## Next Steps

- [Templates](templates.md)
- [Module Structure](modules.md)
