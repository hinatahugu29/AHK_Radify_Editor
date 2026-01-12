# Technical Specifications

This page explains the technical specifications and implementation details of Radify Menu Editor.

## System Requirements

### Minimum Requirements

- **OS**: Windows 10 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 2GB or more
- **Disk Space**: 100MB or more (excluding configuration files and images)

### Recommended Requirements

- **OS**: Windows 11 (64-bit)
- **Python**: 3.10 or higher
- **RAM**: 4GB or more
- **Disk Space**: 500MB or more

## Technology Stack

### Frontend (GUI)

- **CustomTkinter 5.2.0+**: Modern UI elements
- **Tkinter**: Standard GUI library (Python standard library)

### Image Processing

- **Pillow (PIL) 10.0.0+**: Image loading, resizing, conversion

### Data Format

- **JSON**: Configuration file and template storage format

### Output Target

- **AutoHotkey v2**: Execution environment for generated scripts

## Architecture

### Design Patterns

#### Mixin Pattern

Main class `RadifyMenuEditor` inherits multiple Mixin classes:

```python
class RadifyMenuEditor(
    CTk,           # CustomTkinter base class
    UISetupMixin,  # UI construction
    PreviewMixin,  # Preview rendering
    FileIOMixin,   # File I/O
    ActionsMixin,  # User actions
    DialogsMixin,  # Dialog management
    ImageMixin     # Image processing
):
    pass
```

**Advantages**:
- High modularity
- Each function independently testable/modifiable
- Improved code readability

## Data Structures

### Configuration File (menu_config.json)

```json
{
  "image_dir": String,      // Image directory path
  "main_menu": Array,       // Main menu structure
  "submenus": Object,       // Submenu definitions
  "menu_options": Object,   // Menu options
  "favorites": Array        // Favorite items
}
```

### Ring Structure

```typescript
interface Ring {
  ring: number;           // Ring number (starts from 1)
  items: MenuItem[];      // Array of items
}
```

### Menu Item

```typescript
interface MenuItem {
  label: string;          // Display label
  icon?: string;          // Icon path (optional)
  action?: string;        // AHK code (optional)
  submenu?: string;       // Submenu name (optional)
}
```

## Preview Rendering Algorithm

### Circular Placement Calculation

Item placement positions calculated with:

```python
# Polar to Cartesian conversion
angle = (index / total_items) * 2 * π + offset
x = center_x + radius * cos(angle)
y = center_y + radius * sin(angle)
```

### Multi-Ring Placement

```python
for ring_num, ring_data in enumerate(rings, start=1):
    radius = base_radius + (ring_num - 1) * ring_spacing
    # Place each item
```

## Performance Optimization

### Image Caching

Cache loaded images in memory:

```python
self.image_cache = {}

def load_image(self, path):
    if path in self.image_cache:
        return self.image_cache[path]
    
    image = Image.open(path)
    self.image_cache[path] = image
    return image
```

### Delayed Preview Update

Delay preview updates during user input for smooth operation:

```python
def schedule_preview_update(self):
    if self.preview_update_timer:
        self.after_cancel(self.preview_update_timer)
    
    self.preview_update_timer = self.after(300, self.draw_preview)
```

## Security

### File Path Validation

Validate user input paths:

```python
def is_safe_path(self, path):
    # Convert to absolute path
    abs_path = os.path.abspath(path)
    # Check if within project directory
    return abs_path.startswith(self.project_dir)
```

!!! warning "Important"
    Generated AHK scripts contain user-entered code as-is. Use only trusted code.

## Limitations

### Technical Limitations

1. **Max Items**: Recommended 12 items per ring (no technical limit, but UI reason)
2. **Max Rings**: Recommended 5 rings
3. **Image Size**: Max 2048x2048px (for memory usage reduction)
4. **Undo History**: Max 50 steps

### Platform Limitations

- **Windows Only**: Tkinter implementation is platform-dependent
- **AutoHotkey v2 Only**: Not compatible with v1

## Performance Metrics

### Startup Time

- **First Launch**: About 2-3 seconds
- **Subsequent**: About 1-2 seconds (with cache)

### Memory Usage

- **Idle**: About 50-80MB
- **Editing**: About 100-150MB
- **Many Images Loaded**: About 200-300MB

## License

### Radify Menu Editor

- **License**: MIT License
- **Copyright**: © 2026 hinatahugu29

### Dependencies

- **CustomTkinter**: MIT License
- **Pillow**: HPND License
- **Tkinter**: PSF License (Python standard library)

## Versioning

### Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: Backward-compatible feature additions
- **PATCH**: Backward-compatible bug fixes

**Current Version**: 1.3.0

## Future Plans

### Planned Features

- Plugin system
- Theme customization
- Cloud sync
- Multi-language support (English, Chinese, etc.)
- Animation effect preview

## References

- [AutoHotkey v2 Documentation](https://www.autohotkey.com/docs/v2/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python Official Documentation](https://docs.python.org/3/)

---

**Last Updated**: January 2026  
**Documentation Version**: 1.0
