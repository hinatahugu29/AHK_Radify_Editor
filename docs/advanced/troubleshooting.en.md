# Troubleshooting

This page explains how to resolve common issues when using Radify Menu Editor.

## Editor Launch Issues

### Python Not Recognized

**Symptom**: `python: command not found` or similar error

**Solutions**:

1. Verify Python is installed
   ```bash
   python --version
   ```

2. Try `python3` command
   ```bash
   python3 main.py
   ```

3. Add Python to PATH environment variable

### Module Not Found

**Symptom**: `ModuleNotFoundError: No module named 'customtkinter'`

**Solution**:

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install customtkinter Pillow
```

### Editor Window Doesn't Appear

**Symptom**: Script starts but window doesn't display

**Solutions**:

1. Check error messages (displayed in console)
2. Check display settings (issues may occur with scaling other than 100%)
3. Update CustomTkinter to latest version
   ```bash
   pip install --upgrade customtkinter
   ```

## File Loading Issues

### Configuration File Won't Load

**Symptom**: "Failed to load configuration file"

**Solutions**:

1. Check for JSON syntax errors
   - Validate with [JSONLint](https://jsonlint.com/)
   - Check comma positions, unclosed quotes

2. Verify file permissions
   - Ensure file is not read-only

3. Restore from backup
   ```bash
   copy backups\autosave_*.json menu_config.json
   ```

### Images Won't Load

**Symptom**: Icon images don't display or error

**Solutions**:

1. Verify image files exist
2. Verify image format is supported (PNG, JPG, BMP, ICO)
3. Verify file path doesn't contain Japanese or special characters
4. Try opening image in another app to check if corrupted

## Script Output Issues

### AHK Script Won't Export

**Symptom**: No files created when export button pressed

**Solutions**:

1. Verify write permissions for output folder
2. Verify sufficient free space at output location  
3. Verify path doesn't contain Japanese or special characters

### Output Script Doesn't Work

**Symptom**: Generated .ahk file double-click doesn't show menu

**Solutions**:

1. Verify AutoHotkey v2 is installed
   ```bash
   autohotkey --version
   ```

2. Right-click script → "Edit Script" to check errors

3. Verify required library files are present
   - `Radify.ahk`
   - `Lib/Gdip_All.ahk`

4. Verify image resources were copied correctly

## Performance Issues

### Editor is Slow

**Symptom**: Operations lag, response is sluggish

**Solutions**:

1. Check memory usage (Task Manager)
2. Simplify menu by deleting unnecessary items
3. Delete unused images from image list
4. Restart PC

## AutoHotkey Script Issues

### Menu Won't Display

**Symptom**: Menu doesn't appear when hotkey pressed

**Solutions**:

1. Verify script is running (AHK icon in taskbar)
2. Check for hotkey conflicts with other apps
3. Run script as administrator
4. Try changing hotkey

### Icons Don't Display

**Symptom**: Menu appears but icons don't display

**Solutions**:

1. Verify `images/` folder is in same location as script
2. Verify image filenames are correct
3. Try changing image paths to absolute paths

### Actions Don't Execute

**Symptom**: Nothing happens when item clicked

**Solutions**:

1. Check for syntax errors in action code
2. Add MsgBox for debugging
   ```ahk
   MsgBox "Action executed"
   Run "notepad.exe"
   ```
3. Verify paths and commands are correct

## Screen Capture Issues

### Capture Doesn't Work

**Symptom**: Nothing happens when screen capture button pressed

**Solutions**:

1. Run editor as administrator
2. Check if security software is interfering
3. Use alternative screen capture tool to create images

## Common Error Messages

### "JSON decode error"

**Cause**: JSON syntax error in configuration file

**Solutions**:

1. Restore from backup
2. Validate with [JSONLint](https://jsonlint.com/)
3. Manually fix (check commas, quotes)

### "Permission denied"

**Cause**: No write permissions for file

**Solutions**:

1. Run as administrator
2. Remove read-only attribute from file
3. Save to different location

### "File not found"

**Cause**: Specified file doesn't exist

**Solutions**:

1. Verify file path
2. Review relative vs absolute paths
3. Verify file actually exists

## Support Information

### Help Resources

- [GitHub Repository](https://github.com/hinatahugu29/AHK_Radify_Editor)
- [Issues](https://github.com/hinatahugu29/AHK_Radify_Editor/issues)
- [Discussions](https://github.com/hinatahugu29/AHK_Radify_Editor/discussions)

### Bug Reports

Information to include when reporting on GitHub Issues:

1. **Environment**:
   - OS (Windows 10/11)
   - Python version
   - AutoHotkey version

2. **Issue Details**:
   - What you did
   - Expected behavior
   - Actual behavior

3. **Reproduction Steps**:
   - Step-by-step procedure

4. **Error Messages**:
   - Complete error message

5. **Screenshots**:
   - Attach images if possible

## Next Steps

If issues persist:

1. [Open an Issue on GitHub](https://github.com/hinatahugu29/AHK_Radify_Editor/issues/new)
2. [Ask in Discussions](https://github.com/hinatahugu29/AHK_Radify_Editor/discussions)
3. Review documentation again
   - [Installation](../getting-started/installation.md)
   - [Basic Usage](../user-guide/basic-usage.md)
