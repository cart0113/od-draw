# od-draw

A Python library for creating diagrams with multiple backend support (SVG, PNG, Draw.io).

## Features

- Multiple backend support: SVG, PNG, Draw.io
- Simple, intuitive API for creating diagrams
- Built on top of drawpyo for Draw.io compatibility
- CLI for rendering diagrams from Python files
- Configurable via `~/.od-draw-config`

## Installation

```bash
pip install od-draw
```

## Quick Start

```python
from od_draw import shapes, diagram, cli

class MyDiagram(diagram.Diagram):
    def __init__(self, text="hi", width="100", height="100", units="px"):
        super().__init__()
        shapes.block(x0=0, y0=0, height=height, width=width)

if __name__ == '__main__':
    cli()
```

Run from command line:

```bash
# Auto-detects single diagram in file
python-main my_diagram.py --output diagram.svg

# Specify diagram when multiple exist
python-main my_diagram.py --render-diagram MyDiagram --output diagram.svg

# Show diagram in viewer
python-main my_diagram.py --show
```

## Configuration

Create a `~/.od-draw-config` file to customize behavior:

```toml
# Viewer commands
svg_viewer = "firefox"
png_viewer = "gimp"

# Default options
default_backend = "svg"
default_width = 1024
default_height = 768
```

See [CONFIG.md](CONFIG.md) for complete configuration documentation.

## Documentation

Full documentation is available in the `docs/` directory. Key topics:

- [Installation](docs/installation.rst)
- [Quick Start Guide](docs/quickstart.rst)
- [Configuration](docs/configuration.rst) - **Important: major system component**
- [API Reference](docs/api.rst)

## License

MIT License
