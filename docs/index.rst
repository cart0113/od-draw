od-draw Documentation
====================

Welcome to od-draw's documentation!

od-draw is a Python library for creating diagrams with multiple backend support (SVG, PNG, Draw.io).

Features
--------

* Multiple backend support: SVG, PNG, Draw.io
* Simple, intuitive API for creating diagrams
* Built on top of drawpyo for Draw.io compatibility
* CLI for rendering diagrams from Python files

Quick Start
-----------

.. code-block:: python

    from od_draw import shapes, diagram, cli

    class MyDiagram(diagram.Diagram):
        def __init__(self, text="hi", width="100", height="100", units="px"):
            super().__init__()
            shapes.block(x0=0, y0=0, height=height, width=width)

    if __name__ == '__main__':
        cli()

Run from command line:

.. code-block:: bash

    python-main my_diagram.py --render-diagram MyDiagram --kwarg 'text=boo' --show-ruler

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   configuration
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
