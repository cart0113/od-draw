"""
CLI for od-draw.
"""

import sys
import importlib.util
import inspect
from pathlib import Path
import click


@click.command()
@click.option("--render-diagram", help="Name of the diagram class to render")
@click.option("--kwarg", multiple=True, help="Keyword arguments in format key=value")
@click.option("--show-ruler", is_flag=True, help="Show ruler in the diagram")
@click.option("--output", help="Output file path")
@click.option(
    "--backend",
    type=click.Choice(["svg", "png", "drawio"]),
    default="svg",
    help="Backend to use for rendering",
)
@click.option("--show", is_flag=True, help="Show the diagram instead of saving")
def cli(render_diagram, kwarg, show_ruler, output, backend, show):
    calling_file = Path(sys.argv[0]).resolve()

    spec = importlib.util.spec_from_file_location("user_module", calling_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    from od_draw.diagram import Diagram

    diagram_classes = [
        name
        for name, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, Diagram) and obj is not Diagram
    ]

    if not render_diagram:
        if len(diagram_classes) == 0:
            click.echo("No Diagram classes found in file")
            return
        elif len(diagram_classes) == 1:
            diagram_class = getattr(module, diagram_classes[0])
        else:
            click.echo("Multiple Diagram classes found. Please specify one with --render-diagram:")
            for name in diagram_classes:
                click.echo(f"  {name}")
            return
    else:
        diagram_class = getattr(module, render_diagram)

    kwargs = {}
    if kwarg:
        for kv in kwarg:
            key, value = kv.split("=", 1)
            kwargs[key] = value

    if show_ruler:
        kwargs["show_ruler"] = True

    diagram = diagram_class(**kwargs)

    if show:
        diagram.show(backend=backend)
    else:
        output_path = output or f"diagram.{backend}"
        diagram.render(output_path, backend=backend)
