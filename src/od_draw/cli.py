"""
CLI for od-draw.
"""

import importlib.util
import inspect
from pathlib import Path
import click


@click.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--diagram", help="Name of the diagram class to render")
@click.option("--output-path", "-o", help="Output file path")
@click.option(
    "--backend",
    type=click.Choice(["svg", "png", "drawio"]),
    help="Backend to use for rendering (default: auto-detect from output extension)",
)
@click.option("--show", is_flag=True, help="Show the diagram instead of saving")
@click.option("--show-rulers", is_flag=True, help="Show rulers in the diagram")
@click.option("--show-grid", is_flag=True, help="Show grid in the diagram")
@click.option(
    "--margin", type=int, default=20, help="Margin around the diagram (in pixels, default: 20)"
)
@click.option("--margin-top", type=int, help="Top margin (overrides --margin)")
@click.option("--margin-bottom", type=int, help="Bottom margin (overrides --margin)")
@click.option("--margin-left", type=int, help="Left margin (overrides --margin)")
@click.option("--margin-right", type=int, help="Right margin (overrides --margin)")
@click.option("--units", default="px", help="Unit for measurements (default: px)")
@click.option("--kwarg", multiple=True, help="Additional keyword arguments in format key=value")
def cli(
    file,
    diagram,
    output_path,
    backend,
    show,
    show_rulers,
    show_grid,
    margin,
    margin_top,
    margin_bottom,
    margin_left,
    margin_right,
    units,
    kwarg,
):
    """Run od-draw diagrams from Python files."""
    calling_file = Path(file).resolve()

    # Load the module
    spec = importlib.util.spec_from_file_location("user_module", calling_file)
    if spec is None or spec.loader is None:
        click.echo(f"Error: Could not load file {calling_file}")
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Import Diagram base class
    from od_draw.diagram.base import Diagram

    # Find all Diagram subclasses
    diagram_classes = [
        name
        for name, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, Diagram) and obj is not Diagram
    ]

    # Determine which diagram to render
    if not diagram:
        if len(diagram_classes) == 0:
            click.echo("No Diagram classes found in file")
            return
        elif len(diagram_classes) == 1:
            diagram_class = getattr(module, diagram_classes[0])
            diagram_name = diagram_classes[0]
        else:
            click.echo("Multiple Diagram classes found. Please specify one with --diagram:")
            for name in diagram_classes:
                click.echo(f"  {name}")
            return
    else:
        if diagram not in diagram_classes:
            click.echo(f"Error: Diagram class '{diagram}' not found in file")
            click.echo(f"Available diagrams: {', '.join(diagram_classes)}")
            return
        diagram_class = getattr(module, diagram)
        diagram_name = diagram

    # Parse additional kwargs
    init_kwargs = {}
    if kwarg:
        for kv in kwarg:
            key, value = kv.split("=", 1)
            init_kwargs[key] = value

    # Create the diagram instance
    diagram_instance = diagram_class(**init_kwargs)

    # Prepare render kwargs
    render_kwargs = {}
    if show_rulers:
        render_kwargs["show_rulers"] = True
    if show_grid:
        render_kwargs["show_grid"] = True
    if margin:
        render_kwargs["margin"] = margin
    if margin_top is not None:
        render_kwargs["margin_top"] = margin_top
    if margin_bottom is not None:
        render_kwargs["margin_bottom"] = margin_bottom
    if margin_left is not None:
        render_kwargs["margin_left"] = margin_left
    if margin_right is not None:
        render_kwargs["margin_right"] = margin_right
    if units:
        render_kwargs["units"] = units

    # Show or render
    if show:
        diagram_instance.show(backend=backend or "svg", **render_kwargs)
    else:
        # Determine output path
        if not output_path:
            # Default output path: {diagram_name}.{backend} in current directory
            backend_ext = backend or "svg"
            output_path = Path(f"{diagram_name}.{backend_ext}")
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Render the diagram
        diagram_instance.render(str(output_path), backend=backend, **render_kwargs)
        click.echo(f"Rendered {diagram_name} to {output_path}")
