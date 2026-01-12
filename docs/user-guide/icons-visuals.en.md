# Icons & Visuals

This page explains how to customize the appearance of your menus.

## Icon Settings

### How to Select Icons

#### Method 1: From File

1. Select an item
2. Click "Select Icon" in right panel
3. Choose image file (PNG, JPG, ICO)

!!! tip "Supported Formats"
    PNG, JPG, JPEG, BMP, ICO, GIF formats are supported.

#### Method 2: Screen Capture

**The signature feature of Radify Menu Editor** - screen capture:

1. Click "Screen Capture" button
2. Editor minimizes
3. Drag mouse to select area
4. Automatically cropped, resized, and applied as icon

!!! success "Convenient Usage"
    Capture app icons and buttons directly for instantly recognizable menus.

#### Method 3: From Existing Image List

1. Open "Image List" tab in right panel
2. Click desired image
3. Click "Use this image"

### Icon Size

Icons are automatically resized to optimal size:

- Default: 64x64px
- Recommended: 32x32 ~ 128x128px

!!! note "Transparent PNG Recommended"
    PNG images with transparent backgrounds display cleanly.

## Label Settings

### Label Text

Enter text to display in the "Label" field of the right panel.

```
Examples: Notepad
         Google Search
         Volume Up
```

### Label Display/Hide

- Icon only
- Label only  
- Both (default)

Toggle in right panel checkboxes.

### Font Settings

Global menu font settings:

1. Open "Menu Options"
2. Select font family
3. Adjust font size

```
Recommended Fonts:
- Yu Gothic UI
- Meiryo UI
- Segoe UI
```

## Color Themes

### Skin Selection

Select skin in "Menu Options" of right panel:

- **Default**: Standard colors
- **Dark**: Dark theme
- **Light**: Light theme
- **Custom**: Customizable

### Glow Effect

Enable/disable item glow (glowing effect):

- **Enable Glow**: Check to enable
- Glow color depends on skin

!!! tip "Improved Visibility"
    Glow effect makes items more visible against dark backgrounds.

## Preview Customization

### Zoom Level

Adjust preview display magnification:

- Slider adjustment: 50% ~ 200%
- Shortcuts:
  - `Ctrl +`: Zoom in
  - `Ctrl -`: Zoom out
  - `Ctrl 0`: Reset

### Background Color

Change preview background color to check in an environment close to actual usage.

## Global Menu Settings

### Menu Options

Configure the following in "Menu Options" dialog:

#### Item Size

```
itemSize: 60
```

Base size of item icons (in pixels)

#### Ring Spacing

```
ringSpacing: 80
```

Distance between rings (in pixels)

#### Menu Name

```
menu_name: myMainMenu
```

Variable name used in AutoHotkey script

### Appearance Mode

- **Light**: Light mode (bright background)
- **Dark**: Dark mode (dark background)
- **System**: Follow system settings

## Icon Resource Management

### Organizing Images

Recommended organization of images in `images/` folder:

```
images/
├── apps/          # Application icons
├── system/        # System function icons
├── custom/        # Custom icons
└── emoji/         # Emoji icons
```

## Visual Best Practices

### Consistent Design

- Use icons of same style
- Unify color scheme
- Unify size (auto-resized, but originals should be similar size)

### Ensure Visibility

- Be mindful of contrast with background
- Avoid icons that are too small
- Labels should be short and clear

### Theme-Based Icon Sets

Align icon themes by function:

- **File Operations**: Folder, document icons
- **Web-Related**: Browser, SNS icons
- **System**: Gear, settings icons
- **Media**: Play, stop icons

## Next Steps

- [Script Export](export.md)
- [Custom Actions](../advanced/custom-actions.md)
