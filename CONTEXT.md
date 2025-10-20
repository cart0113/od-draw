# CONTEXT.md

This file provides guidance to AI assistants when working with code in this repository.

## CRITICAL PYTHON EXECUTION REQUIREMENTS

**THIS IS THE MOST IMPORTANT INSTRUCTION - FAILURE TO FOLLOW WILL CAUSE ERRORS:**

- **ALWAYS USE `python-main`** - NEVER use `python` or `python3`
- **ALWAYS USE `uv-main`** - NEVER use `pip` or `uv`
- **ALWAYS USE `ruff-main`** - NEVER use `ruff`
- These are custom executables that must be used for ALL Python operations
- No exceptions to this rule - `python-main` is the ONLY Python interpreter to use
- For package installation, use `uv-main pip install` instead of `pip install`
- For formatting, use `ruff-main` directly or `/Users/ajcarter/bin/run-ruff.sh` (which uses ruff-main)

## Important Workspace Management

- **VERY IMPORTANT**: Always delete screenshots after viewing to keep the workspace clean
- Remember to clean up any temporary files used during development

## Code Style Guidelines

1. No fallback behavior - Assume data is in the correct structure:
   - Use `dict['key']` instead of `dict.get('key')`
   - **EXTREMELY IMPORTANT**: NEVER add backward compatibility code when refactoring
   - **EXTREMELY IMPORTANT**: NEVER maintain both old and new attribute/method names
   - **EXTREMELY IMPORTANT**: When asked to change names or refactor, remove ALL traces of old names
   - No default values in code
   - No default parameters in function signatures unless explicitly requested
   - Every parameter should be required rather than optional with defaults
   - Code should be correct by construction

2. Error handling:
   - Let errors surface naturally
   - Don't add defensive/protective code unless explicitly requested
   - No try/except blocks for anticipated failures

3. Testing:
   - Do not run tests unless explicitly requested
   - Do not test or run Python scripts unless explicitly requested
   - Wait for user to run tests and report results
   - **VERY IMPORTANT**: After editing any Python file (.py), run `/Users/ajcarter/bin/run-ruff.sh` on it to format the code (this uses ruff-main)
   - Only run ruff on .py files, not on markdown or other file types

4. Code conciseness:
   - Write direct, minimal code
   - Avoid extra abstractions or layers
   - No comments unless specifically requested
   - **IMPORTANT**: When logic becomes complex or exceeds ~10-15 lines, break it into separate methods with clear, descriptive names
   - Keep methods focused on a single responsibility

5. Avoid excessive verification:
   - Don't suggest extra validation steps
   - Skip unnecessary type checking
   - Trust the correctness of inputs
   - Don't add Python type hints in code unless explicitly requested
   - It's acceptable to include type information in function docstrings

6. Python import practices:
   - **IMPORTANT**: Do NOT import all symbols into top-level __init__.py files unless explicitly requested
   - This is considered bad practice because:
     * It pollutes the namespace and makes it unclear where symbols come from
     * It can create circular import issues and increase startup time
   - Keep __init__.py minimal and explicit about what is exposed in the module's public API
   - Only import specific symbols into __init__.py if the user explicitly asks for it
   - **IMPORTANT**: All __init__.py files should be empty - use full import paths instead
   - Example of correct import style:
     ```python
     from od_draw.diagram.base import Diagram
     from od_draw.shapes.base import Rectangle, Circle, Triangle
     from od_draw import colors
     ```
   - Do NOT use convenience imports like `from od_draw import Diagram` or `import od_draw.shapes`

7. No unsolicited explanations:
   - Don't explain code unless asked
   - Skip summary explanations after edits
   - Focus on implementation, not justification
   - **VERY IMPORTANT**: When auto accept is enabled, NEVER prompt for confirmation or ask questions - just execute the requested actions directly
   - **VERY IMPORTANT**: When auto accept is on, do NOT ask "Should I..." or "Would you like me to..." - just do it

8. Code implementation boundaries:
   - **VERY IMPORTANT**: Don't try to write more code than specified by the user
   - Only implement what the user has provided enough information for
   - Ask follow-up questions if there's insufficient information rather than guessing (unless auto accept is enabled)
   - It's acceptable if code doesn't fully work when implementation details haven't been specified

## Incremental Development Approach

- **VERY IMPORTANT**: Projects start with incomplete information - never attempt to build a fully working application from an underspecified prompt
- When specifications are incomplete, either ask specific questions or leave functionality unimplemented
- Do not guess or implement speculative features - this creates code that's difficult to remove later
- Allow the user to incrementally build the project by adding details over time ("building a castle")
- The user will test and verify code functionality - don't worry if implementation is incomplete
- Focus solely on implementing what has been explicitly specified

## Git Commits

- **VERY VERY IMPORTANT**: NEVER commit changes unless explicitly requested by the user
- **CRITICAL**: Do NOT commit even if you think it's helpful or the logical next step
- Even if asked to commit once in a session, do NOT commit again without being explicitly asked
- Each commit requires a new explicit request - previous permission does not extend to future commits
- Wait for explicit confirmation before committing, even if changes are ready
- The user must explicitly say "commit" or "git commit" - do not infer this from context
- Make regular, human-like commits without "Committed by Claude Code" mentions
- Write commit messages like a human developer would
- **VERY IMPORTANT**: Never add AI attribution in commit messages
- **VERY IMPORTANT**: Never include lines like "Generated with Claude Code" or "Co-Authored-By: Claude" in commit messages
- When asked for "pre-refactor checkpoint commits," understand that the code may not be working, but should be committed to easily track changes with git diff

## Working with Logic Problems

**VERY IMPORTANT - FOLLOW THIS ADVICE OR YOU WILL DIE**

1. When facing logic problems that aren't immediately solvable:
   - **Ask for help early** rather than guessing repeatedly
   - Don't create increasingly complex workarounds for simple logical errors
   - Avoid adding unnecessary fallback or error-checking code when the core logic is wrong
   - After a few unsuccessful attempts, explicitly state you're struggling with the problem

2. Signs you should ask for help:
   - You've made multiple attempts to fix the same logic issue without success
   - You find yourself creating complex workarounds instead of solving the root problem
   - Your solutions are becoming increasingly complex without clear improvement
   - You're adding defensive or fallback code to handle edge cases that shouldn't exist

3. Correct approach to logic problems:
   - First, state clearly that you're having trouble with the specific logic
   - Explain your current understanding of the problem
   - Describe what you've tried and why it didn't work
   - Ask specific questions about the logic you're struggling with
   - Request clarification rather than implementing guessed solutions

4. When struggling with logic problems:
   - After 2-3 unsuccessful attempts, create a detailed explanation file
   - Use the format {date}_{problem_desc}.md (e.g., 20250513_recursion_issue.md)
   - Include the problematic code snippets in the file
   - Explain your current understanding of how the code works
   - Detail the specific challenges you're facing and your attempts to solve them
   - Highlight any edge cases or inconsistencies you've identified

5. Remember that AI assistants often struggle with certain types of logic problems
   - Complex conditional logic
   - Recursive algorithms
   - State management
   - Rendering and layout calculations

## Refactoring

**CRITICAL**: When refactoring, ALWAYS remove all unnecessary code. Do not leave old implementations, unused functions, or dead code behind. Clean refactoring means complete removal of obsolete code.

1. Distinguish between API implementation vs API usage refactoring:
   - When refactoring the API itself (core logic), understanding multiple files together may be necessary
   - When updating API calls across many files, take it one file at a time

2. For large-scale API usage refactoring:
   - Complete the API implementation changes first
   - Then update caller files one at a time, finishing each file before moving to the next
   - Don't attempt to make partial changes across multiple files simultaneously

3. Remove all unnecessary code:
   - **EXTREMELY IMPORTANT**: Delete old implementations completely when replacing them
   - Remove unused imports after refactoring
   - Delete obsolete helper functions that are no longer called
   - Remove commented-out code blocks
   - Clean up temporary debugging code
   - Example: When converting PNG backend from PIL to SVG conversion, delete ALL the old PIL drawing code

4. Efficient multi-file refactoring strategy:
   - Check for patterns in API usage before starting
   - Create a clear plan with files prioritized
   - Focus on one type of change at a time
   - Communicate if a task is taking longer than expected

## Design Patterns

1. ClassFallbackConstructor Pattern (formerly PseudoDataclass Pattern):
   - **IMPORTANT**: I prefer the ClassFallbackConstructor Pattern for configurable classes
   - This pattern uses class attributes for defaults and Ellipsis (...) as sentinel values in __init__
   - See design_pattern_class_fallback_constructor.md for full details
   - Allows detection of explicitly passed parameters vs. defaults
   - Supports clean inheritance with overridable class attributes

2. CompositionMixin Pattern:
   - **IMPORTANT**: I prefer the CompositionMixin Pattern for building flexible component architectures
   - This pattern allows users to choose between inheritance and composition approaches
   - Uses protocols (e.g., CanRender, CanTick) to define behavior contracts
   - Implements behaviors in mixin classes that delegate to apply_* class methods
   - See composition_mixin_pattern.md for full details
   - Enables small, focused classes that handle specific traits/functions
   - Avoids forcing architectural decisions on API users

## Project Overview

od-draw is a Python library for creating diagrams with multiple backend support (SVG, PNG, Draw.io). It provides a simple, intuitive API for building diagrams programmatically with the flexibility to render to different output formats.

**IMPORTANT**: For comprehensive information about the od-draw API design, architecture, and implementation patterns, read [OD_DRAW_API.md](OD_DRAW_API.md). This document contains detailed explanations of:
- Two-layer architecture (shapes vs diagram)
- Backend system design
- Configuration system (critical component)
- CLI design patterns
- Extension points for new shapes and backends
- Usage patterns and best practices

## Code Structure

The project is organized into focused modules:

- `od_draw/shapes/`: Low-level shape primitives (Rectangle, Circle, Block)
- `od_draw/diagram/`: High-level diagram abstraction and backend management
- `od_draw/diagram/backends/`: Backend implementations (SVG, PNG, Draw.io)
- `od_draw/cli.py`: Command-line interface for rendering diagrams
- `examples/`: Example diagrams demonstrating od-draw features
- `tests/`: Test suite
- `docs/`: Sphinx documentation with Furo theme

## Development Workflow

### Building and Installing

```bash
# Install for development
uv-main pip install -e ".[dev,docs]"
```

### Running Examples

**VERY IMPORTANT**: Always use `python-main` to run examples, never `python` or `python3`:

```bash
python-main examples/simple_diagram.py --render-diagram MyDiagram --output diagram.svg
```

### Building Documentation

```bash
cd docs
make html
```

## Architecture

The architecture separates concerns between shapes, diagrams, and backends:

- **Shapes**: Low-level primitives with position, size, and styling
- **Diagram**: Container managing shapes and coordinating backend rendering
- **Backends**: Pluggable renderers that convert shapes to specific output formats

Key architectural points:
- Diagrams contain shapes and delegate rendering to backends
- Backends implement the Backend protocol for consistent interface
- CLI provides command-line access to diagram rendering
- Backend selection can be explicit or inferred from file extension
