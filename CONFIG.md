# od-draw Configuration

od-draw uses a configuration file to customize its behavior. This document provides comprehensive information about configuration options and usage.

## Configuration File

### Location

The configuration file is located at:

```
~/.od-draw-config
```

### Format

The configuration file uses TOML format. TOML is a simple, human-readable configuration file format.

## Configuration Options

### Viewer Commands

These options control which programs are used to view different file formats when using `--show`:

#### `svg_viewer`

Command to view SVG files.

**Type:** String
**Default:** Platform-dependent (`open` on macOS, `xdg-open` on Linux, `start` on Windows)

**Example:**
```toml
svg_viewer = "firefox"
```

#### `png_viewer`

Command to view PNG files.

**Type:** String
**Default:** Platform-dependent (`open` on macOS, `xdg-open` on Linux, `start` on Windows)

**Example:**
```toml
png_viewer = "gimp"
```

#### `drawio_viewer`

Command to view Draw.io files.

**Type:** String
**Default:** Platform-dependent (`open` on macOS, `xdg-open` on Linux, `start` on Windows)

**Example:**
```toml
drawio_viewer = "/Applications/draw.io.app/Contents/MacOS/draw.io"
```

### Default Rendering Options

#### `default_backend`

The default backend to use when no backend is specified.

**Type:** String
**Default:** `"svg"`
**Options:** `"svg"`, `"png"`, `"drawio"`

**Example:**
```toml
default_backend = "svg"
```

#### `default_width`

Default width for diagrams in pixels.

**Type:** Integer
**Default:** `800`

**Example:**
```toml
default_width = 1024
```

#### `default_height`

Default height for diagrams in pixels.

**Type:** Integer
**Default:** `600`

**Example:**
```toml
default_height = 768
```

## Platform-Specific Defaults

### macOS

```toml
svg_viewer = "open"
png_viewer = "open"
drawio_viewer = "open"
```

### Linux

```toml
svg_viewer = "xdg-open"
png_viewer = "xdg-open"
drawio_viewer = "xdg-open"
```

### Windows

```toml
svg_viewer = "start"
png_viewer = "start"
drawio_viewer = "start"
```

## Example Configuration Files

### Minimal Configuration

```toml
# ~/.od-draw-config
svg_viewer = "firefox"
```

### Complete Configuration

```toml
# ~/.od-draw-config

# Viewer commands
svg_viewer = "firefox"
png_viewer = "open"
drawio_viewer = "/Applications/draw.io.app/Contents/MacOS/draw.io"

# Default rendering options
default_backend = "svg"
default_width = 1024
default_height = 768
```

### Developer Configuration

```toml
# ~/.od-draw-config

# Use VS Code for viewing
svg_viewer = "code"
png_viewer = "code"

# Larger default canvas
default_width = 1920
default_height = 1080

# Prefer PNG for quick previews
default_backend = "png"
```

## Usage with CLI

The configuration file affects CLI behavior automatically:

```bash
# Uses configured svg_viewer
python-main my_diagram.py --show --backend svg

# Uses configured default_backend if not specified
python-main my_diagram.py --show

# Command-line args override config
python-main my_diagram.py --show --backend png
```

## Configuration Priority

Settings are resolved in the following order (highest to lowest priority):

1. **Command-line arguments** - Explicitly passed flags and options
2. **Configuration file** - Values from `~/.od-draw-config`
3. **Platform defaults** - OS-specific defaults
4. **Built-in defaults** - Hardcoded fallback values

## Creating Your Configuration

### Quick Start

```bash
# Create the configuration file
touch ~/.od-draw-config

# Edit with your preferred editor
nano ~/.od-draw-config
```

### Testing Your Configuration

```bash
# Test with a simple diagram
python-main -c "
from od_draw import shapes, diagram
d = diagram.Diagram()
d.add_shape(shapes.block(x0=10, y0=10))
d.show()
"
```

## Advanced Configuration

### Custom Viewer Scripts

You can use custom scripts as viewers:

```toml
svg_viewer = "/Users/username/bin/my-svg-viewer.sh"
```

Example viewer script:
```bash
#!/bin/bash
# my-svg-viewer.sh
/Applications/Firefox.app/Contents/MacOS/firefox "$1" &
```

### Environment Variables

Viewer commands can reference environment variables:

```toml
svg_viewer = "${BROWSER}"
```

## Troubleshooting

### Configuration Not Loading

1. Verify file location: `ls -la ~/.od-draw-config`
2. Check file format: Ensure valid TOML syntax
3. Check file permissions: `chmod 644 ~/.od-draw-config`

### Viewer Not Working

1. Test viewer command directly: `firefox test.svg`
2. Use absolute paths for executables
3. Check that the viewer supports the file format

### Invalid Configuration

If the configuration file contains errors, od-draw will:
1. Print a warning message
2. Fall back to platform defaults
3. Continue operation

## Future Configuration Options

Future versions may support:

- Custom shape libraries
- Style presets
- Template diagrams
- Export options
- Network diagram servers
