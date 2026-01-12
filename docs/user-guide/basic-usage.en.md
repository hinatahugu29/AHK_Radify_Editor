# Basic Usage

This page explains the basic operations of Radify Menu Editor.

## UI Components

### Menu Bar

- **File**: Save, Load, New, Export
- **Edit**: Undo/Redo, Copy & Paste
- **View**: Preview Zoom, Theme Switch
- **Help**: Documentation, Version Info

### Toolbar

Main operation buttons located at the top of the left panel:

- **Add New Ring**: Add a new ring
- **Add New Item**: Add item to selected ring
- **Add Submenu**: Create a submenu
- **Delete**: Delete selected element
- **Up/Down**: Change item order

## Ring Management

### Adding a Ring

1. Click "Add New Ring" button
2. Ring is added to tree view
3. Circular arrangement appears in preview

### Ring Settings

When a ring is selected, the following can be configured in the right panel:

- **Ring Number**: Ring identifier (1, 2, 3... from inside)
- **Radius**: Distance from center
- **Division Count**: Number of slots on circumference

!!! tip "Adjusting Ring Radius"
    By adjusting radius, you can create multi-ring structures.

### Deleting a Ring

1. Select the ring to delete
2. Click "Delete" button
3. Select "Yes" in confirmation dialog

!!! warning "Caution"
    Deleting a ring will also delete all items contained in that ring.

## Item Management

### Adding an Item

1. Select the ring where you want to add an item
2. Click "Add New Item" button
3. New item is added to the ring

### Selecting an Item

- Click directly in tree view
- Click on preview canvas (if implemented)

### Rearranging Items

#### Method 1: Using Buttons

1. Select item to move
2. Click "Up" or "Down" button

#### Method 2: Drag & Drop

1. Drag item in tree view
2. Drop at desired position

!!! tip "Visual Rearrangement"
    Drag & drop is most intuitive and reflects in preview in real-time.

## Preview Features

### Zoom

Adjust preview size:

- **Zoom In**: `Ctrl` + `+`
- **Zoom Out**: `Ctrl` + `-`
- **Reset**: `Ctrl` + `0`

Or use the zoom slider in the preview panel.

### Hover Display

Hovering over items in preview displays their information.

## Copy & Paste

### Copying Items

1. Select item to copy
2. `Ctrl+C` or "Edit" → "Copy"

### Pasting Items

1. Select destination ring
2. `Ctrl+V` or "Edit" → "Paste"

!!! info "Duplicating"
    Pasting in the same ring duplicates the item.

## Undo/Redo

Manage editing history:

- **Undo**: `Ctrl+Z`
- **Redo**: `Ctrl+Y`

!!! note "History Retention"
    History is retained for up to 50 steps.

## Search Function

### Item Search

Enter text in the search box at the top of the right panel to search for items containing the text in labels or actions.

### Image Search

In the image list tab, search by image filename.

## Keyboard Shortcuts

| Shortcut | Function |
|---|---|
| `Ctrl+S` | Save |
| `Ctrl+N` | New Project |
| `Ctrl+O` | Open File |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+C` | Copy |
| `Ctrl+V` | Paste |
| `Delete` | Delete |
| `F5` | Refresh Preview |

## Next Steps

After understanding basic operations, also refer to these pages:

- [Editing Menu Structure](editing-structure.md)
- [Action Settings](actions.md)
- [Icons & Visuals](icons-visuals.md)
