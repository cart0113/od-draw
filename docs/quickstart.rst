Quick Start
===========

Creating a Simple Diagram
--------------------------

.. code-block:: python

    from od_draw import shapes, diagram

    class MyDiagram(diagram.Diagram):
        def __init__(self, width=800, height=600, units="px"):
            super().__init__(width=width, height=height, units=units)

            # Add a rectangle
            rect = shapes.block(x0=100, y0=100, width=200, height=100,
                              fill="#ff0000", stroke="#000000")
            self.add_shape(rect)

            # Add a circle
            circ = shapes.circle(x0=400, y0=150, radius=50,
                               fill="#0000ff", stroke="#000000")
            self.add_shape(circ)

    # Create and render the diagram
    my_diag = MyDiagram()
    my_diag.render('output.svg')

Using Different Backends
-------------------------

SVG Backend
~~~~~~~~~~~

.. code-block:: python

    diagram.render('output.svg', backend='svg')

PNG Backend
~~~~~~~~~~~

.. code-block:: python

    diagram.render('output.png', backend='png')

Draw.io Backend
~~~~~~~~~~~~~~~

.. code-block:: python

    diagram.render('output.drawio', backend='drawio')

Using the CLI
-------------

.. code-block:: bash

    python-main my_diagram.py --render-diagram MyDiagram --output diagram.svg

With keyword arguments:

.. code-block:: bash

    python-main my_diagram.py --render-diagram MyDiagram --kwarg 'width=1000' --kwarg 'height=800'

Show the diagram instead of saving:

.. code-block:: bash

    python-main my_diagram.py --render-diagram MyDiagram --show
