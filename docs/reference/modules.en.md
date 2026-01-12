# Module Structure

This page explains the source code structure and module design of Radify Menu Editor.

## Project Structure

```
AHK_Radify_Editor_Modular/
├── main.py                 # Entry point
├── modules/                # Core modules
│   ├── __init__.py
│   ├── core.py            # Main class
│   ├── ui_setup.py        # UI construction
│   ├── preview.py         # Preview rendering
│   ├── file_io.py         # File I/O
│   ├── actions.py         # User action handling
│   ├── dialogs.py         # Dialog management
│   ├── images.py          # Image processing
│   └── utils.py           # Utilities
├── menu_config.json        # Menu configuration
├── templates.json          # Action templates
└── images/                 # Icon resources
```

## Module Details

### main.py

**Role**: Application entry point

```python
from modules.core import RadifyMenuEditor

if __name__ == "__main__":
    app = RadifyMenuEditor()
    app.mainloop()
```

### modules/core.py

**Role**: Main application class

**Primary Class**: `RadifyMenuEditor`

**Inheritance**:
- `CTk` (CustomTkinter)
- `UISetupMixin`
- `PreviewMixin`
- `FileIOMixin`
- `ActionsMixin`
- `DialogsMixin`
- `ImageMixin`

**Key Methods**:
- `__init__()`: Initialization
- `create_new_project()`: Create new project
- `refresh_all()`: Update entire UI
- `check_dependencies()`: Check dependencies
- `on_closing()`: Cleanup on exit

### modules/ui_setup.py

**Role**: User interface construction

**Primary Class**: `UISetupMixin`

**Key Methods**:
- `build_ui()`: Build main UI
- `create_menu_bar()`: Create menu bar
- `create_toolbar()`: Create toolbar
- `create_tree_panel()`: Tree view panel
- `create_preview_panel()`: Preview panel
- `create_properties_panel()`: Properties panel

### modules/preview.py

**Role**: Ring menu preview rendering

**Primary Class**: `PreviewMixin`

**Key Methods**:
- `draw_preview()`: Draw entire preview
- `draw_ring()`: Draw specific ring
- `draw_item()`: Draw individual item
- `calculate_item_position()`: Calculate item coordinates

### modules/file_io.py

**Role**: File read/write operations

**Primary Class**: `FileIOMixin`

**Key Methods**:
- `load_config()`: Load configuration file
- `save_config()`: Save configuration file
- `create_backup()`: Create backup
- `export_ahk_script()`: Export AHK script
- `load_templates()`: Load templates

### modules/actions.py

**Role**: User action handling

**Primary Class**: `ActionsMixin`

**Key Methods**:
- `refresh_tree()`: Update tree view
- `on_tree_select()`: Handle tree selection
- `add_new_ring()`: Add new ring
- `add_new_item()`: Add new item
- `delete_selected()`: Delete selected element
- `copy_item()` / `paste_item()`: Copy & paste
- `undo()` / `redo()`: Editing history management

### modules/dialogs.py

**Role**: Dialog management

**Primary Class**: `DialogsMixin`

**Key Methods**:
- `show_menu_options_dialog()`: Menu options settings
- `show_template_dialog()`: Template search dialog
- `show_about_dialog()`: Version info
- `show_export_dialog()`: Export settings

### modules/images.py

**Role**: Image processing

**Primary Class**: `ImageMixin`

**Key Methods**:
- `load_image()`: Load image
- `resize_image()`: Resize image
- `capture_screen()`: Screen capture
- `refresh_image_list()`: Update image list

### modules/utils.py

**Role**: Utility functions

**Key Functions**:
- `sanitize_var_name()`: Sanitize variable names
- `escape_ahk_string()`: Escape AHK strings
- `validate_json()`: JSON validation
- `generate_unique_name()`: Generate unique names

## Mixin Design Rationale

### Advantages

1. **Separation of Concerns**: Each function in independent module
2. **Maintainability**: Edit only relevant module when fixing specific features
3. **Reusability**: Partial reuse in other projects possible
4. **Readability**: File sizes appropriately split for easier reading

## Extension Methods

### Adding New Features

1. Add new method to appropriate Mixin, or
2. Create new Mixin and inherit in `core.py`

Example: New feature Mixin

```python
# modules/new_feature.py
class NewFeatureMixin:
    def new_feature_method(self):
        # Implementation
        pass
```

```python
# modules/core.py
from .new_feature import NewFeatureMixin

class RadifyMenuEditor(CTk, UISetupMixin, ..., NewFeatureMixin):
    ...
```

## Next Steps

- [Custom Actions](../advanced/custom-actions.md)
- [Troubleshooting](../advanced/troubleshooting.md)
