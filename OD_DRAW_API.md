# od-draw API Design and Architecture

This document explains the design philosophy, architecture, and API patterns for od-draw, a Python library for creating diagrams with multiple backend support.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Core Design Philosophy](#core-design-philosophy)
3. [Architecture](#architecture)
4. [Package Structure](#package-structure)
5. [Key Components](#key-components)
6. [Backend System](#backend-system)
7. [Configuration System](#configuration-system)
8. [CLI Design](#cli-design)
9. [Usage Patterns](#usage-patterns)
10. [Extension Points](#extension-points)

## Project Overview

od-draw is a Python library for creating diagrams programmatically with support for multiple output formats:

- **SVG** - Scalable Vector Graphics for web and documentation
- **PNG** - Raster images for presentations and reports
- **Draw.io** - Editable diagrams compatible with diagrams.net/Draw.io

The library is designed to be:
- **Simple** - Minimal API surface, easy to learn
- **Flexible** - Support multiple backends without changing code
- **Configurable** - User preferences via `~/.od-draw-config`
- **Pythonic** - Follow Python best practices and conventions

## Core Design Philosophy

### 1. Two-Layer Architecture

The library has two distinct layers:

**Low-Level Layer (`od_draw.shapes`)**
- Primitive shape objects (Rectangle, Circle, Block)
- Position, size, and styling attributes
- No rendering logic
- No backend awareness

**High-Level Layer (`od_draw.diagram`)**
- Diagram container
- Shape management
- Backend coordination
- Rendering orchestration

This separation allows:
- Easy addition of new shapes without touching rendering
- Backend implementation changes without affecting shapes
- Clear separation of concerns

### 2. Backend Abstraction

All backends implement the `Backend` protocol:

```python
class Backend(ABC):
    @abstractmethod
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        pass

    @abstractmethod
    def show(self, shapes: List[Shape], **kwargs):
        pass
```

This allows:
- New backends without changing existing code
- Consistent API across all output formats
- Easy testing and mocking

### 3. Configuration as a Major Component

The `~/.od-draw-config` file is a **critical system component**, not an afterthought:

- Controls viewer applications for each format
- Sets default rendering options
- Platform-specific defaults that "just work"
- TOML format for human readability

## Architecture

```
┌─────────────────────────────────────────────────┐
│              User Diagram Class                 │
│         (inherits from Diagram)                 │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            od_draw.diagram.Diagram               │
│  - Contains shapes list                         │
│  - Manages backend selection                    │
│  - Coordinates rendering                        │
└──────────────┬──────────────────┬────────────────┘
               │                  │
               ▼                  ▼
┌──────────────────────┐  ┌──────────────────────┐
│  od_draw.shapes      │  │  od_draw.backends    │
│  - Shape primitives  │  │  - SVGBackend        │
│  - Block             │  │  - PNGBackend        │
│  - Circle            │  │  - DrawIOBackend     │
│  - Rectangle         │  │                      │
└──────────────────────┘  └──────────────┬───────┘
                                         │
                                         ▼
                              ┌──────────────────────┐
                              │  od_draw.config      │
                              │  - Load TOML config  │
                              │  - Platform defaults │
                              │  - Viewer settings   │
                              └──────────────────────┘
```

## Package Structure

```
od_draw/
├── __init__.py          # Package root, exports cli()
├── cli.py               # Click-based CLI
├── config.py            # Configuration loading
├── shapes/              # Low-level shape primitives
│   ├── __init__.py      # Exports factory functions
│   ├── base.py          # Shape base classes
│   └── factory.py       # Factory functions (block, circle, rectangle)
└── diagram/             # High-level diagram abstraction
    ├── __init__.py      # Exports Diagram class
    ├── base.py          # Diagram class
    └── backends/        # Backend implementations
        ├── __init__.py  # Exports all backends
        ├── base.py      # Backend protocol/ABC
        ├── svg.py       # SVG backend
        ├── png.py       # PNG backend (Pillow)
        └── drawio.py    # Draw.io backend (drawpyo)
```

## Key Components

### Shape Classes (`od_draw.shapes.base`)

**Base Shape Class:**
```python
class Shape:
    def __init__(self, x, y, width, height, fill, stroke, stroke_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
```

**Derived Classes:**
- `Rectangle` - Basic rectangular shape
- `Circle` - Circular shape with radius
- `Block` - Alias for Rectangle (common diagram terminology)

**Design Notes:**
- Shapes are data containers, not renderers
- All measurements in the same units (pixels by default)
- Optional styling (fill, stroke) with sensible defaults
- No rendering logic - that's the backend's job

### Factory Functions (`od_draw.shapes.factory`)

Factory functions provide a convenient API:

```python
def block(x0, y0, width, height, fill, stroke, stroke_width):
    return Block(x=x0, y=y0, width=width, height=height, ...)
```

**Why Factory Functions:**
- More intuitive parameter names (`x0` vs `x`)
- Consistent API across shapes
- Easy to add validation/preprocessing
- Can return different classes based on parameters

### Diagram Class (`od_draw.diagram.base`)

The Diagram class is the main container:

```python
class Diagram:
    def __init__(self, width=800, height=600, units="px"):
        self.width = width
        self.height = height
        self.units = units
        self.shapes = []
        self._backend = None

    def add_shape(self, shape):
        self.shapes.append(shape)

    def render(self, output_path, backend=None, **kwargs):
        # Select backend based on file extension or explicit choice
        # Delegate to backend.render()

    def show(self, backend='svg', **kwargs):
        # Use configured viewer to display
        # Delegate to backend.show()
```

**Design Notes:**
- Simple container semantics
- Backend selection automatic or explicit
- Passes through kwargs to backends for flexibility
- No rendering logic - pure orchestration

## Backend System

### Backend Protocol

All backends implement:

```python
class Backend(ABC):
    @abstractmethod
    def render(self, shapes: List[Shape], output_path: str, **kwargs):
        """Render shapes to file at output_path"""
        pass

    @abstractmethod
    def show(self, shapes: List[Shape], **kwargs):
        """Display shapes in configured viewer"""
        pass
```

### SVG Backend (`svg.py`)

**Rendering:**
- Iterates through shapes
- Converts each to SVG elements
- Writes XML to file

**Showing:**
- Creates temporary file
- Uses configured `svg_viewer` from config
- Opens with `subprocess.run([viewer, temp_file])`

**Implementation Notes:**
- Simple text generation (no XML library needed)
- Direct shape-to-SVG mapping
- Fill and stroke attributes map directly

### PNG Backend (`png.py`)

**Rendering:**
- Uses Pillow (PIL)
- Creates Image object
- Draws shapes using ImageDraw
- Saves to file

**Showing:**
- Creates temporary PNG file
- Uses configured `png_viewer` from config
- Opens with `subprocess.run([viewer, temp_file])`

**Implementation Notes:**
- Requires Pillow dependency
- Handles color conversion
- Stroke width conversion to int

### Draw.io Backend (`drawio.py`)

**Rendering:**
- Uses drawpyo library
- Creates File and Page objects
- Converts shapes to drawpyo Objects
- Writes to .drawio XML format

**Showing:**
- Creates temporary .drawio file
- Uses configured `drawio_viewer` from config
- Opens with `subprocess.run([viewer, temp_file])`

**Implementation Notes:**
- Builds on drawpyo for Draw.io compatibility
- Maps shape attributes to drawpyo properties
- Supports editing in Draw.io/diagrams.net

## Configuration System

### Configuration File (`~/.od-draw-config`)

**Location:** `~/.od-draw-config` in user's home directory

**Format:** TOML

**Example:**
```toml
# Viewer commands
svg_viewer = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
png_viewer = "open"
drawio_viewer = "open"

# Default options
default_backend = "svg"
default_width = 1024
default_height = 768
```

### Configuration Loading (`config.py`)

**Loading Process:**
1. Get platform-specific defaults
2. Load `~/.od-draw-config` if it exists
3. Merge user config over defaults
4. Cache in global variable

**Platform Defaults:**
- **macOS:** `open` for all viewers
- **Linux:** `xdg-open` for all viewers
- **Windows:** `start` for all viewers

**Error Handling:**
- Missing config file → use defaults
- Invalid TOML → use defaults (silent fallback)
- Missing viewer executable → command fails with clear error

### Why Configuration is Critical

1. **User Control** - Users choose their preferred applications
2. **Platform Flexibility** - Works across macOS/Linux/Windows
3. **Workflow Integration** - Integrates with existing tools
4. **No Hardcoding** - No assumptions about installed software
5. **Future Expansion** - Easy to add more config options

## CLI Design

### Click-Based CLI

**Why Click:**
- Better help formatting
- Type validation built-in
- Cleaner decorator syntax
- Better error messages
- Industry standard

**Command Structure:**
```python
@click.command()
@click.option("--render-diagram", help="Name of diagram class")
@click.option("--kwarg", multiple=True, help="key=value arguments")
@click.option("--show-ruler", is_flag=True)
@click.option("--output", help="Output file path")
@click.option("--backend", type=click.Choice(["svg", "png", "drawio"]))
@click.option("--show", is_flag=True)
def cli(...):
    # Implementation
```

### Auto-Detection Logic

**Single Diagram:**
- If file contains exactly one Diagram subclass
- Automatically use it without `--render-diagram`
- User convenience for simple cases

**Multiple Diagrams:**
- If file contains multiple Diagram subclasses
- Require `--render-diagram ClassName`
- List available classes to help user

**No Diagrams:**
- Show error message
- Exit cleanly

### Kwarg Processing

**Format:** `--kwarg key=value`

**Processing:**
```python
kwargs = {}
for kv in kwarg:  # kwarg is tuple from click multiple=True
    key, value = kv.split("=", 1)
    kwargs[key] = value
```

**Passed to:** Diagram class constructor

**Use Case:** Parameterizing diagrams from command line

## Usage Patterns

### Basic Usage

```python
from od_draw import shapes, diagram, cli

class MyDiagram(diagram.Diagram):
    def __init__(self, width=800, height=600, units="px"):
        super().__init__(width=width, height=height, units=units)

        rect = shapes.block(x0=100, y0=100, width=200, height=100,
                          fill="#ff0000", stroke="#000000", stroke_width=2)
        self.add_shape(rect)

if __name__ == '__main__':
    cli()
```

### Command Line Usage

```bash
# Auto-detect single diagram
python-main my_diagram.py --show

# Specify diagram name
python-main my_diagram.py --render-diagram MyDiagram --output out.svg

# Pass kwargs to diagram constructor
python-main my_diagram.py --kwarg width=1024 --kwarg height=768

# Use different backend
python-main my_diagram.py --show --backend png
```

### Programmatic Usage

```python
from od_draw import shapes, diagram

# Create diagram
d = diagram.Diagram(width=800, height=600)

# Add shapes
d.add_shape(shapes.block(x0=10, y0=10, width=100, height=50))
d.add_shape(shapes.circle(x0=200, y0=50, radius=30))

# Render to file
d.render("output.svg")

# Show in viewer
d.show()

# Use specific backend
d.render("output.png", backend="png")
```

### Configuration-Based Workflow

1. User creates `~/.od-draw-config`:
```toml
svg_viewer = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
default_width = 1920
default_height = 1080
```

2. Create diagram normally:
```python
class MyDiagram(diagram.Diagram):
    def __init__(self):
        super().__init__()  # Uses config defaults
        # Add shapes...
```

3. Show diagram:
```bash
python-main diagram.py --show  # Opens in Chrome automatically
```

## Extension Points

### Adding New Shapes

1. Create shape class in `shapes/base.py`:
```python
class Triangle(Shape):
    def __init__(self, x, y, base, height, **kwargs):
        super().__init__(x, y, base, height, **kwargs)
        self.base = base
```

2. Add factory function in `shapes/factory.py`:
```python
def triangle(x0, y0, base, height, fill=None, stroke=None, stroke_width=1):
    return Triangle(x=x0, y=y0, base=base, height=height, ...)
```

3. Update backends to handle Triangle:
```python
# In each backend's render method
if isinstance(shape, Triangle):
    return self._triangle_to_svg(shape)  # or _draw_triangle, etc.
```

### Adding New Backends

1. Create backend file in `diagram/backends/`:
```python
class PDFBackend(Backend):
    def render(self, shapes, output_path, **kwargs):
        # Implement PDF rendering
        pass

    def show(self, shapes, **kwargs):
        # Implement PDF viewing
        pass
```

2. Export from `diagram/backends/__init__.py`:
```python
from .pdf import PDFBackend
```

3. Add to Diagram class backend selection:
```python
elif backend == 'pdf' or output_path.endswith('.pdf'):
    self._backend = PDFBackend()
```

4. Add config option:
```python
# In config.py platform defaults
"pdf_viewer": "open",  # or platform-specific
```

### Adding Configuration Options

1. Add to `config.py` defaults:
```python
defaults = {
    "default_backend": "svg",
    "default_width": 800,
    "default_height": 600,
    "new_option": "default_value",  # New option
    **get_platform_defaults(),
}
```

2. Use in code:
```python
from od_draw.config import get_config

config = get_config()
value = config["new_option"]
```

3. Document in `docs/configuration.rst` and `CONFIG.md`

### Adding CLI Options

1. Add Click option:
```python
@click.option("--new-option", help="Description")
def cli(..., new_option):
    # Handle new option
```

2. Process and use:
```python
if new_option:
    kwargs["new_option"] = new_option
```

## Best Practices for Contributors

1. **Maintain Layer Separation**
   - Shapes should never import backends
   - Backends should handle any shape type
   - Diagram orchestrates, doesn't render

2. **Follow No-Fallback Philosophy**
   - Don't add defensive code without reason
   - Let errors surface naturally
   - Trust type system and structure

3. **Keep It Simple**
   - Avoid over-abstraction
   - Direct, minimal code
   - Clear naming

4. **Configuration First**
   - User preferences via config file
   - Not hardcoded assumptions
   - Platform-appropriate defaults

5. **Document User-Facing Changes**
   - Update relevant .rst files
   - Update CONFIG.md for config changes
   - Update this file for API changes

## Common Patterns

### Pattern: Shape Creation

```python
# In diagram __init__
def __init__(self):
    super().__init__()

    # Create and add in one line
    self.add_shape(shapes.block(x0=10, y0=10, width=100, height=50))

    # Or store reference
    my_shape = shapes.circle(x0=100, y0=100, radius=30)
    self.add_shape(my_shape)
```

### Pattern: Conditional Backend Selection

```python
# Diagram.render() method
if backend == 'svg' or output_path.endswith('.svg'):
    self._backend = SVGBackend()
elif backend == 'png' or output_path.endswith('.png'):
    self._backend = PNGBackend()
# ... etc
```

### Pattern: Config with Defaults

```python
from od_draw.config import get_config

config = get_config()
viewer = config.get("svg_viewer", "open")  # Fallback to "open"
```

## Future Enhancements

Potential areas for expansion:

1. **More Shapes** - Arrows, connectors, polygons, text
2. **Layout Engine** - Automatic positioning/alignment
3. **Themes** - Predefined color schemes and styles
4. **Templates** - Common diagram patterns
5. **Animation** - For SVG/web output
6. **Interactive** - Clickable elements in SVG
7. **Cloud Export** - Direct upload to services
8. **Validation** - Check diagram constraints

## Questions for Future Development

When extending od-draw, consider:

1. Does this belong in shapes or diagram layer?
2. Is this backend-specific or universal?
3. Should this be configurable?
4. Is this a new shape or shape variant?
5. Does this maintain the simple API?
6. Is this documented for users?

## Summary

od-draw is designed around these principles:

- **Simplicity** - Easy to use, easy to understand
- **Separation** - Clear layer boundaries
- **Flexibility** - Multiple backends, one API
- **Configuration** - User control via config file
- **Extensibility** - Clear patterns for additions

When working with od-draw, always consider these principles and maintain the clean architecture that makes the library approachable and maintainable.
