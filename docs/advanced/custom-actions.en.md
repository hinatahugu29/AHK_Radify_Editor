# Custom Actions

This page explains how to create advanced actions utilizing the full power of AutoHotkey v2.

## AutoHotkey v2 Basics

### Direct Code Writing

In Radify Menu Editor, you can write AutoHotkey v2 code directly in the action field.

The editor automatically wraps it as an anonymous function, so just write like this:

```ahk
MsgBox "Hello, World!"
```

Actually generated in script:

```ahk
item.action := (*) => {
    MsgBox "Hello, World!"
}
```

## Advanced Action Examples

### Conditional Logic

#### Change Behavior by Window State

```ahk
if WinExist("ahk_exe notepad.exe")
    WinActivate
else
    Run "notepad.exe"
```

#### Change Behavior by Time of Day

```ahk
hour := A_Hour
if (hour >= 9 && hour < 17)
    Run "work_app.exe"
else
    Run "personal_app.exe"
```

### Loops

#### Operate Multiple Windows Sequentially

```ahk
windows := ["ahk_exe notepad.exe", "ahk_exe calc.exe"]
for exe in windows {
    if WinExist(exe)
        WinActivate
}
```

### Variables and Arrays

#### Variable-ize Frequently Used Paths

```ahk
myDocs := A_MyDocuments
myWork := myDocs "\Work"
Run myWork
```

## Advanced Window Operations

### Adjust Window Position and Size

```ahk
if WinExist("ahk_exe notepad.exe") {
    WinActivate
    WinMove 0, 0, 800, 600  ; x, y, width, height
}
```

### Window Half-Size

```ahk
WinActivate "A"
WinGetPos &x, &y, &w, &h
screenW := A_ScreenWidth
WinMove 0, 0, screenW // 2, A_ScreenHeight
```

## Advanced Clipboard Usage

### Process Clipboard Contents

```ahk
old := A_Clipboard
A_Clipboard := StrUpper(old)  ; Convert to uppercase
Sleep 100
Send "^v"
Sleep 100
A_Clipboard := old  ; Restore
```

## File Operations

### Text File Read/Write

```ahk
; Write
FileAppend "Log: " A_Now "`n", "C:\log.txt"

; Read
content := FileRead("C:\data.txt")
MsgBox content
```

### File Existence Check

```ahk
if FileExist("C:\important_file.txt")
    MsgBox "File exists"
else
    MsgBox "File not found"
```

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

- [Managing Multiple Menus](multiple-menus.md)
- [Troubleshooting](troubleshooting.md)

## Reference Resources

- [AutoHotkey v2 Official Documentation](https://www.autohotkey.com/docs/v2/)
- [AutoHotkey v2 Tutorial](https://www.autohotkey.com/docs/v2/Tutorial.htm)
- [AutoHotkey v2 Command Reference](https://www.autohotkey.com/docs/v2/lib/)
