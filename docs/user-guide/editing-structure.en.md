# Editing Menu Structure

This page explains how to create and edit complex menu structures.

## Understanding Hierarchy

Radify Menu Editor organizes menus with the following hierarchy:

```
Main Menu
├── Ring 1
│   ├── Item 1
│   ├── Item 2
│   └── Item 3
├── Ring 2
│   ├── Item 4
│   └── Item 5 (→ To Submenu)
└── Ring 3
    └── Item 6

Submenu A
├── Ring 1
│   ├── Item 7
│   └── Item 8
└── Ring 2
    └── Item 9
```

## Multi-Ring Structure

### Adding Multiple Rings

Add multiple rings to give your menu depth:

1. Click "Add New Ring" multiple times
2. Adjust each ring's radius to set placement

!!! tip "Automatic Ring Numbering"
    Rings are automatically numbered 1, 2, 3... from inside.

### Adjusting Ring Radius

Adjust "Ring Spacing" in the right panel to set distance between rings.

```
Inner Ring: Radius 100px
Middle Ring: Radius 180px
Outer Ring: Radius 260px
```

## Creating Submenus

### Adding a Submenu

1. Select an item that will have a submenu button
2. Click "Add Submenu" button
3. Enter submenu name
4. New submenu is added to tree view

### Setting Links to Submenus

1. Select item in main menu
2. Select destination in "Submenu" dropdown in right panel
3. Action is automatically configured

!!! info "Submenu Actions"
    Links to submenus are auto-generated as special actions.

### Editing Submenus

1. Select submenu in tree view
2. Add/edit rings and items as with normal menus

## Advanced Item Placement

### Fixing Positions

To place specific items at specific positions:

1. Rearrange item order
2. Check position in preview
3. Fine-tune as needed

### Empty Slots

To create empty slots in a ring:

1. Add a dummy item
2. Leave label empty
3. Don't set an action (or set a do-nothing action)

!!! warning "Note"
    Empty slots still exist internally as items.

## Best Practices

### Menu Depth

- Place most frequently used functions in main menu
- Keep submenus to about 2 levels
- Avoid too deep hierarchies

### Number of Rings

- 3-4 rings per menu is appropriate
- Too many reduces visibility

### Number of Items

- 6-8 items per ring is ideal
- Over 12 becomes difficult to select

### Naming Conventions

- Use clear label names
- Submenu names should reflect content
- Consistent naming for easier management

## Next Steps

- [Action Settings](actions.md)
- [Icons & Visuals](icons-visuals.md)
