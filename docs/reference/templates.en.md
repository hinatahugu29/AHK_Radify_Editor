# Templates

This page explains the Radify Menu Editor action template system.

## templates.json

Templates are managed in the `templates.json` file.

### Basic Structure

```json
{
  "categories": [
    {
      "category": "CategoryName",
      "templates": [...]
    }
  ]
}
```

## Template Format

### Template Object

```json
{
  "name": "Template Name",
  "code": "AutoHotkey Code",
  "description": "Description",
  "keywords": ["keyword1", "keyword2"]
}
```

#### Field Descriptions

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | String | Yes | Template display name |
| `code` | String | Yes | AutoHotkey code to insert |
| `description` | String | No | Template description |
| `keywords` | Array | No | Keywords for search |

## Built-in Templates

### Launch Application

```json
{
  "name": "Launch Application",
  "code": "Run \"notepad.exe\"",
  "description": "Launches a program",
  "keywords": ["run", "launch", "execute"]
}
```

### Open Webpage

```json
{
  "name": "Open Webpage",
  "code": "Run \"https://www.google.com\"",
  "description": "Opens URL in browser",
  "keywords": ["web", "url", "browser"]
}
```

### Send Keys

```json
{
  "name": "Send Keys",
  "code": "Send \"^c\"",
  "description": "Sends keyboard operations",
  "keywords": ["send", "keys", "shortcut"]
}
```

## Adding Custom Templates

### Steps

1. Open `templates.json` in text editor
2. Add new template to appropriate category
3. Save file
4. Restart editor

### Example: Adding New Template

```json
{
  "category": "Custom",
  "templates": [
    {
      "name": "Screenshot",
      "code": "Send \"#{PrintScreen}\"",
      "description": "Take screenshot with Win+PrintScreen",
      "keywords": ["screenshot", "capture", "print"]
    }
  ]
}
```

## Template Categories

### Standard Categories

- **Basic**: Commonly used basic actions
- **Apps**: Application launch related
- **Web**: Web related operations
- **System**: System operations
- **Windows**: Window operations
- **Media**: Volume control, etc.
- **Custom**: User-defined templates

## Best Practices

### Clear Naming

Template names should clearly indicate what they do.

```json
// Good
"name": "Launch Notepad"

// Bad
"name": "Template1"
```

### Descriptive Descriptions

Write specific descriptions in the `description` field.

```json
"description": "Launches Notepad. Activates if already running."
```

### Utilize Keywords

Add related keywords for easy searching.

```json
"keywords": ["notepad", "text", "editor", "txt"]
```

## Next Steps

- [Module Structure](modules.md)
- [Custom Actions](../advanced/custom-actions.md)
