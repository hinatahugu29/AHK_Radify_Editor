# Action Settings

This page explains how to configure actions that execute when menu items are clicked.

## Types of Actions

Radify Menu Editor supports various actions:

- **Launch Applications**: Open programs or files
- **Send Keys**: Automate keyboard operations
- **Window Operations**: Minimize, maximize windows, etc.
- **System Commands**: Shutdown, restart, etc.
- **Script Execution**: Run AutoHotkey code
- **Show Submenu**: Navigate to another menu

## Using Templates

### Searching Templates

1. Select an item
2. Click "Template Search" in right panel
3. Search by category or keyword
4. Click desired template

### Commonly Used Templates

#### Launch Application

```ahk
Run "notepad.exe"
```

With parameters:

```ahk
Run "notepad.exe C:\memo.txt"
```

#### Open Webpage

```ahk
Run "https://www.google.com"
```

#### Open Folder

```ahk
Run "C:\Users\YourName\Documents"
```

#### Send Keys

```ahk
Send "^c"  ; Ctrl+C
```

```ahk
Send "^v"  ; Ctrl+V
```

#### Minimize Window

```ahk
WinMinimize "A"
```

## Writing Code Directly

### Basic Syntax

You can write AutoHotkey v2 code directly in the action field:

```ahk
MsgBox "Hello, World!"
```

!!! note "Auto-Wrapping"
    The editor automatically wraps code as an anonymous function `(*) => { ... }`, so just write the code.

### Multi-Line Code

Execute multiple processes sequentially:

```ahk
WinActivate "ahk_exe notepad.exe"
Send "Hello from Radify!"
```

### Conditional Logic

Change behavior based on window state:

```ahk
if WinExist("ahk_exe notepad.exe")
    WinActivate
else
    Run "notepad.exe"
```

### Using Variables

```ahk
myPath := "C:\MyFolder"
Run myPath
```

## Advanced Actions

### Toggle Hotkey

```ahk
static toggle := false
toggle := !toggle
if toggle
    MsgBox "ON"
else
    MsgBox "OFF"
```

### Clipboard Operations

```ahk
A_Clipboard := "Copied text"
MsgBox "Copied to clipboard"
```

### File Read/Write

```ahk
FileAppend "Log: " A_Now "`n", "C:\log.txt"
```

## Linking to Submenus

### Manual Setup

```ahk
ShowSubmenu("SubmenuName")
```

### Select from Dropdown

1. "Submenu" dropdown in right panel
2. Select destination submenu
3. Action is auto-configured

## Error Handling

### Try-Catch

```ahk
try {
    Run "nonexistent.exe"
} catch as err {
    MsgBox "Error: " err.Message
}
```

## Best Practices

### Clear Code

- Use comments
- Descriptive variable names
- Split complex processes

### Path Handling

Use absolute paths or environment variables for reliability.

### Error-Resistant Code

Check existence before execution:

```ahk
if FileExist("C:\myapp.exe")
    Run "C:\myapp.exe"
else
    MsgBox "App not found"
```

## Next Steps

- [Icons & Visuals](icons-visuals.md)
- [Script Export](export.md)
- [Custom Actions](../advanced/custom-actions.md)
