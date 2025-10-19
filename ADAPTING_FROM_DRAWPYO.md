# Adapting from drawpyo

This document details our experience adapting code from the excellent [drawpyo](https://github.com/MerrimanInd/drawpyo) open-source project for use in od-draw.

## Why We Used drawpyo

We chose to build upon drawpyo's foundation for several compelling reasons:

1. **Proven Draw.io Compatibility**: drawpyo has already solved the complex problem of generating valid Draw.io XML files that work correctly with diagrams.net/Draw.io
2. **Well-Designed Architecture**: The object-oriented design with clear separation between File, Page, and Object layers aligned well with our needs
3. **Robust XML Generation**: The XMLBase class provides solid XML escaping and tag generation
4. **Open Source**: drawpyo is MIT licensed and openly available for use and modification
5. **Active Development**: The project is maintained and has addressed real-world Draw.io format requirements

## Project Information

- **Project**: drawpyo
- **Repository**: https://github.com/MerrimanInd/drawpyo
- **Author**: Merrimanind
- **License**: MIT License
- **Version Used**: 0.2.2 (installed via pip)
- **Purpose**: Python library for programmatically generating Draw.io diagrams

## What We Learned About drawpyo

### Architecture Overview

drawpyo has a well-thought-out architecture with three main layers:

1. **XML Layer** (`xml_base.py`): Base class for all XML-generating objects
2. **Document Layer** (`file.py`, `page.py`): File and page management
3. **Diagram Layer** (`diagram/`): Shapes, edges, groups, and other diagram elements

### Key Design Patterns

#### 1. XMLBase Pattern

Every Draw.io object inherits from `XMLBase`, which provides:
- Automatic ID generation using Python's `id()` function
- XML attribute dictionary via `attributes` property
- XML tag generation with proper escaping
- Support for UserObject tags (for filtering/grouping)

**What we copied**:
- The entire XMLBase class structure
- XML character escaping logic
- Tag generation pattern

**Source files**:
- `drawpyo/xml_base.py` → `od_draw/drawio/xml_base.py`

#### 2. Nested XML Structures

Draw.io files have a specific nested structure:
```xml
<mxfile>
  <diagram>
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Actual objects go here -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**What we learned**:
- Every Draw.io diagram MUST have two empty mxCell objects (ID 0 and 1)
- Pages are actually three nested XML tags (Diagram, mxGraphModel, root)
- Each tag level has specific attributes from the Draw.io specification

**What we copied**:
- The Page class with Diagram, MxGraph, and Root inner classes
- The two required empty mxCell objects
- Page formatting properties (grid, guides, tooltips, etc.)

**Source files**:
- `drawpyo/page.py` → `od_draw/drawio/page.py`

#### 3. File Management

The File class handles:
- Page collection and management
- Metadata (modified timestamp, agent string, etc.)
- XML generation combining all pages
- Writing to disk with proper encoding

**What we copied**:
- File class structure
- Page management methods (add_page, remove_page)
- XML generation that combines pages
- File writing logic with directory creation

**Source files**:
- `drawpyo/file.py` → `od_draw/drawio/file.py`

#### 4. Geometry System

Objects in Draw.io have geometry defined in a nested `<mxGeometry>` element.

**What we learned**:
- Geometry is a separate object with x, y, width, height
- It has a special `as="geometry"` attribute
- The Geometry class inherits from XMLBase to generate its own XML

**What we copied**:
- Geometry class structure
- Size property (tuple of width/height)
- Geometry as a nested XML element

**Source files**:
- `drawpyo/diagram/base_diagram.py` (Geometry class) → `od_draw/drawio/geometry.py`

#### 5. Style System

Draw.io styles are encoded as semicolon-separated strings:
```
baseStyle;attribute1=value1;attribute2=value2
```

**What we learned**:
- Styles are property dictionaries converted to strings
- baseStyle (if present) goes first without an equals sign
- Boolean values are represented as integers (0 or 1)
- Color values are hex strings (#RRGGBB)
- None/empty values should be excluded from the style string

**What we copied**:
- `style_str_from_dict()` function for converting style dicts to strings
- Style attribute handling in Object class
- Property-based style generation pattern

**Source files**:
- `drawpyo/diagram/base_diagram.py` (style_str_from_dict) → `od_draw/drawio/object.py`

#### 6. Object System

Objects (shapes) in Draw.io are `<mxCell>` elements with:
- Unique ID
- Value (text content)
- Style string
- Vertex flag (1 for shapes, 0 for edges)
- Nested geometry element
- Parent reference (usually 1 for the page root)

**What we copied**:
- Object class structure
- mxCell XML generation
- Style attribute properties (fillColor, strokeColor, etc.)
- Geometry integration
- Page linking

**Source files**:
- `drawpyo/diagram/objects.py` (Object class) → `od_draw/drawio/object.py`

## What We Didn't Copy

We intentionally simplified drawpyo for od-draw's specific needs:

### 1. Edge/Connector System
- **Not copied**: `edges.py` with Edge, TargetEdge, WaypointEdge classes
- **Reason**: od-draw focuses on basic shapes; edges/connectors can be added later if needed

### 2. Group System
- **Not copied**: Group class for managing object collections
- **Reason**: Not needed for our current use case

### 3. Container/Parent System
- **Not copied**: Complex parent-child relationships, autoexpanding containers
- **Reason**: Simplified to basic shape rendering without nesting

### 4. Shape Libraries
- **Not copied**: TOML-based shape libraries, library import system
- **Reason**: od-draw has its own shape system; we just need basic Draw.io output

### 5. Text Formatting
- **Not copied**: TextFormat class with font, size, color, alignment
- **Reason**: Basic shapes only; text formatting can be added incrementally

### 6. Template System
- **Not copied**: Creating objects from templates, style string parsing
- **Reason**: Not needed for our backend-focused architecture

### 7. Extended Objects
- **Not copied**: `extended_objects.py` with specialized shape types
- **Reason**: Using od-draw's own shape definitions

### 8. Advanced Style Features
- **Not copied**: Line patterns, dashed patterns, sketch/comic styling
- **Reason**: Keeping it simple; can add later if needed

## Code Modifications and Improvements

While drawpyo provided an excellent foundation, we made several improvements:

### 1. Type Hints

**Original drawpyo**:
```python
def __init__(self, file_name="Diagram.drawio", file_path="."):
    self.pages = []
```

**Our version**:
```python
def __init__(
    self,
    file_name: str = "Diagram.drawio",
    file_path: str = path.join(path.expanduser("~"), "Diagrams"),
) -> None:
    self.pages: list[Page] = []
```

We added comprehensive type hints throughout:
- Function parameter types
- Return type annotations
- Property type hints
- Modern Python 3.10+ union syntax (`Optional[X]` → `X | None`)

### 2. Docstrings

**Original drawpyo**:
```python
def add_page(self, page):
    """Add a page to the file.

    Args:
        page (drawpyo.diagram.Page): A Page object
    """
```

**Our version**:
```python
def add_page(self, page: Page) -> None:
    """
    Add a page to this file.

    Args:
        page: Page object to add
    """
```

Improvements:
- Google-style docstrings
- Clearer descriptions
- Type information in signatures (not just docstrings)
- More context about what each method does

### 3. Code Organization

We reorganized the code structure:
- Split Geometry into its own module
- Kept only essential functionality
- Removed unused imports
- Clearer module-level docstrings explaining origin

### 4. Naming Improvements

Some renaming for clarity:
- `xml_ify()` → `_xml_escape()` (more descriptive)
- Made XML escape mapping a module constant
- Changed `host` from "Drawpyo" to "od-draw"

### 5. Modern Python Features

Used Python 3.10+ features:
- `dict[str, Any]` instead of `Dict[str, Any]`
- `list[Page]` instead of `List[Page]`
- Union types with `|` instead of `Union`
- TYPE_CHECKING for forward references

### 6. Simplified Initialization

**Original drawpyo Object**:
```python
def __init__(self, value="", position=(0, 0), **kwargs):
    # Many complex initialization steps
    # Parent handling, autoexpanding, etc.
```

**Our version**:
```python
def __init__(
    self,
    page: Optional["Page"] = None,
    value: str = "",
    shape: str = "rectangle",
    **kwargs: Any,
) -> None:
    # Streamlined for basic use case
```

We removed:
- Parent/child relationship handling
- Autoexpanding containers
- Template object copying
- Complex geometry calculations

### 7. Integration with od-draw

We modified the backend to work seamlessly with od-draw:
- Removed drawpyo import dependency
- Used relative imports from `od_draw.drawio`
- Adapted to od-draw's Shape classes
- Integrated with od-draw's config system

## Mapping: drawpyo → od-draw

| drawpyo File | od-draw File | What We Copied |
|-------------|-------------|----------------|
| `xml_base.py` | `drawio/xml_base.py` | Complete XMLBase class, XML escaping |
| `file.py` | `drawio/file.py` | File class, page management, writing |
| `page.py` | `drawio/page.py` | Page, Diagram, MxGraph, Root classes |
| `diagram/base_diagram.py` | `drawio/geometry.py` | Geometry class |
| `diagram/base_diagram.py` | `drawio/object.py` | style_str_from_dict function |
| `diagram/objects.py` | `drawio/object.py` | Object class (simplified) |

## Technical Details We Learned

### 1. Draw.io XML Format Requirements

- Files must have `host`, `modified`, `agent`, `version`, `type` attributes
- Version "21.6.5" corresponds to Draw.io spec version
- Every page needs two empty mxCell objects with IDs 0 and 1
- Object parent references usually point to ID 1 (the page root)

### 2. XML Character Escaping

Must escape: `>`, `<`, `&`, `"`, `'`

Draw.io uses standard XML entities:
- `>` → `&gt;`
- `<` → `&lt;`
- `&` → `&amp;`
- `"` → `&quot;`
- `'` → `&apos;`

### 3. Style String Format

Format: `baseStyle;attr1=val1;attr2=val2;...`

Important attributes:
- `shape`: Shape type (rectangle, ellipse, etc.)
- `fillColor`: Fill color (#RRGGBB or "none")
- `strokeColor`: Border color (#RRGGBB or "none")
- `strokeWidth`: Border width (integer)
- `rounded`: Round corners (0 or 1)
- `whiteSpace`: Text wrapping ("wrap", "nowrap")

### 4. Geometry Attributes

- `x`, `y`: Position relative to parent
- `width`, `height`: Object dimensions
- `as`: Always "geometry" for object geometry

### 5. Object Vertex Flag

- `vertex="1"`: This is a shape/node
- `vertex="0"`: This is an edge/connector (not used in our simplified version)

## Attribution and License

We are deeply grateful to the drawpyo project and its contributors:

- **Original Project**: [drawpyo](https://github.com/MerrimanInd/drawpyo)
- **Author**: Merrimanind
- **License**: MIT License
- **Copyright**: Copyright (c) Merrimanind

### Our Modifications

The code in `od_draw/drawio/` is adapted from drawpyo with the following changes:
- Added comprehensive type hints
- Improved docstrings
- Simplified for basic shape rendering
- Integrated with od-draw's architecture
- Reorganized into separate modules

### License Compliance

drawpyo is licensed under the MIT License, which permits:
- Commercial use
- Modification
- Distribution
- Private use

We acknowledge drawpyo as the source and maintain attribution in:
- Module-level docstrings in all adapted files
- This ADAPTING_FROM_DRAWPYO.md document
- Comments in the code where specific functions/classes were copied

## Why We Chose to Internalize Rather Than Depend

We could have kept drawpyo as a dependency, but chose to copy and adapt for several reasons:

### 1. **Control Over Features**
- drawpyo has many features we don't need (edges, groups, templates)
- We wanted a minimal implementation focused on basic shapes
- Easier to maintain and understand with less code

### 2. **Type Safety**
- We wanted comprehensive type hints throughout
- Adding type hints to an external dependency would be harder
- Modern Python type annotations improve IDE support

### 3. **Integration**
- Tighter integration with od-draw's architecture
- No need to convert between different object models
- Simpler imports and dependencies

### 4. **Future Evolution**
- We may need to extend the Draw.io support in ways specific to od-draw
- Having the code internally makes experimentation easier
- Can optimize for our specific use case

### 5. **Dependency Management**
- One fewer external dependency to manage
- No version compatibility concerns
- Smaller installation footprint

### 6. **Learning Opportunity**
- Understanding the Draw.io format deeply
- Knowledge transfer to the od-draw team
- Better equipped to debug issues

## What This Means for od-draw

### Current Capabilities

With the adapted drawpyo code, od-draw can now:
- Generate valid Draw.io XML files
- Create pages with multiple shapes
- Set shape colors, sizes, and positions
- Support rectangles and ellipses
- Export diagrams editable in diagrams.net

### Future Possibilities

The foundation from drawpyo makes it easier to add:
- More shape types (triangles, polygons, custom shapes)
- Edge/connector support
- Text formatting
- Containers and groups
- Style templates
- Advanced Draw.io features

### Maintenance Notes

When maintaining the `od_draw/drawio/` package:
- Refer back to drawpyo for Draw.io format questions
- Check drawpyo updates for new Draw.io spec changes
- Keep attribution comments in the code
- Document any significant deviations from drawpyo

## Conclusion

Adapting from drawpyo has been an excellent decision. We gained:
- A solid, tested foundation for Draw.io export
- Deep understanding of the Draw.io XML format
- Well-architected code to build upon
- Confidence that our output will work with Draw.io

We're grateful to the drawpyo project for solving the hard problems and sharing their work openly. This is open source collaboration at its best - building upon each other's work to create better tools for everyone.

## Resources

- **drawpyo GitHub**: https://github.com/MerrimanInd/drawpyo
- **drawpyo Documentation**: https://github.com/MerrimanInd/drawpyo/tree/main/docs
- **Draw.io/diagrams.net**: https://www.diagrams.net/
- **Draw.io Format Specification**: https://drawio-app.com/blog/
- **mxGraph (underlying format)**: Historical documentation for Draw.io's XML format

---

*This document was created as part of od-draw's development to acknowledge our debt to drawpyo and document what we learned from their excellent work.*
