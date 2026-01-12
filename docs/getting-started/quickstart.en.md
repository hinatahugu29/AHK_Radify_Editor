# Quick Start

This guide explains how to create your first ring menu using Radify Menu Editor.

## Launching the Editor

Run the following command in the project folder:

```bash
python main.py
```

## Understanding the Screen Layout

The editor consists of three main panels:

### Left Panel: Tree View
- Displays menu hierarchy
- Drag & drop to rearrange

### Center Panel: Preview
- Real-time menu appearance preview
- Live Sync feature provides instant reflection

### Right Panel: Property Editor
- Edit details of selected items
- Configure icons, labels, and actions

## Creating Your First Menu

### Step 1: Add a New Ring

1. Click the **"Add New Ring"** button at the top of the left panel
2. A ring is added and displayed in the tree

!!! tip "What is a Ring?"
    A ring is a unit for arranging items in a circle. Menus can consist of multiple rings.

### Step 2: Add an Item

1. Select the ring you added
2. Click the **"Add New Item"** button
3. An item is added to the ring

### Step 3: Configure the Item

Configure the following in the right panel:

#### Label
Enter the text to display on the item.

```
Example: Notepad
```

#### Icon
1. Click "Select Icon"
2. Choose an image file, or
3. "Screen Capture" to capture directly from screen

!!! tip "Screen Capture"
    The screen capture feature lets you capture app icons and buttons directly.

#### Action
Set what happens when the item is clicked.

##### Method 1: Use Templates

1. Click the "Template Search" button
2. Select a template like "Launch App"
3. Enter parameters (e.g., `notepad.exe`)

##### Method 2: Write Code Directly

For advanced users. You can write AutoHotkey v2 code directly:

```ahk
Run "notepad.exe"
```

### Step 4: Preview

The menu you created is displayed in real-time on the center canvas.

- Icon placement
- Font size
- Colors and style

Everything is reflected instantly.

### Step 5: Save

1. **"File" → "Save"** from the menu bar
2. Or press `Ctrl+S`

!!! info "Auto-Save"
    The editor auto-saves periodically, but manual saving is also recommended.

## Export as AHK Script

You can export the created menu as an AutoHotkey script.

1. **"File" → "Export AHK Script"** from the menu bar
2. Select output folder
3. Required files are automatically copied:
   - Main script (.ahk)
   - Library files (Lib/)
   - Image resources (images/)

### Running the Script

Just double-click the `.ahk` file in the output folder to run it.

!!! success "Complete!"
    Your first ring menu is now complete!

## Next Steps

After learning the basic creation method, also refer to these guides:

- [Editing Menu Structure](../user-guide/editing-structure.md) - Creating complex hierarchies
- [Action Settings](../user-guide/actions.md) - Advanced action definitions
- [Icons & Visuals](../user-guide/icons-visuals.md) - Appearance customization

## FAQ

### Q: The created menu doesn't appear

A: Verify that AutoHotkey v2 is installed. Also try right-clicking the script → "Run as administrator."

### Q: Icons don't display

A: Verify that image file paths are correct. If using relative paths, place images in the same folder as the script.

### Q: Actions don't execute

A: Check for syntax errors in action code. We recommend starting with templates.
