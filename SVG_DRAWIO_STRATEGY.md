# SVG and Draw.io Strategy

## Core Philosophy

**od_draw has two separate rendering backends with different capabilities:**

1. **Native SVG/PNG backend** (primary focus)
2. **Draw.io backend** (future work, currently stubbed)

These are **intentionally separate** with their own shape libraries and APIs.

## Architecture Decision

### Native Implementation (Current Focus)

- We create our own shape primitives (Triangle, Square, Rectangle, Polygon, Line, etc.)
- Direct SVG generation with full control over rendering
- PNG generation via Pillow using the same shape definitions
- This is our **primary focus** until the native API is fully working

### Draw.io Implementation (Future Work)

- Separate shape library specifically for Draw.io
- Generates `.drawio` XML format
- May have different capabilities and constraints than native shapes
- **Currently stubbed out with NotImplementedError**

## Conversion Strategy: Best Effort Only

### Native → Draw.io
When converting from native od_draw shapes to Draw.io format:
- Best effort conversion using available Draw.io primitives
- Some features may not translate perfectly
- No guarantee of pixel-perfect rendering

### Draw.io → Native
When converting from Draw.io shapes to native od_draw format:
- Best effort conversion to SVG primitives
- Some Draw.io-specific features may be lost
- No guarantee of identical appearance

## API Divergence is Expected

**The two backends will have different APIs over time:**

- Connection points between shapes may work differently
- Styling options may vary
- Layout and positioning behaviors may differ
- Draw.io has concepts (groups, layers, connection handles) that don't map to simple SVG shapes
- Native shapes have precise control that Draw.io may not support

## Expected User Workflow

**Users will typically choose ONE backend and stick with it:**

1. **Choose a backend** (native SVG/PNG or Draw.io)
2. **Create diagram** using that backend's shapes
3. **Iterate and refine** within the same backend
4. **Don't switch back and forth** between backends

The typical workflow is: create → render → look at output → iterate. Switching backends mid-project would likely cause conversion issues and loss of fidelity.

## Implementation Priority

### Phase 1: Native API (CURRENT)
- Get the native SVG/PNG backend fully working
- Complete shape library with all features
- Robust rendering and styling options
- Comprehensive examples and documentation

### Phase 2: Draw.io Backend (FUTURE)
- Only after Phase 1 is complete
- Implement Draw.io shape library
- Create conversion utilities
- Document limitations and differences

## Current Status

**Draw.io backend is NOT to be worked on currently.**

The Draw.io interface is stubbed out and raises `NotImplementedError`. Do not implement Draw.io functionality until explicitly requested. Focus all efforts on the native SVG/PNG backend.

## Why This Approach?

1. **Avoid sync nightmare**: Trying to keep two rendering engines pixel-perfect would be a maintenance burden
2. **Different use cases**: Draw.io is for editable diagrams; native is for rendered output
3. **Clear separation**: Users know what they're getting with each backend
4. **Focused development**: Get one thing working excellently before adding another
5. **Honest about capabilities**: No false promises about perfect conversion
