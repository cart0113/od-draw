Configuration
=============

od-draw uses a configuration file located at ``~/.od-draw-config`` to customize behavior.

Configuration File Location
---------------------------

The configuration file should be placed at:

.. code-block:: bash

    ~/.od-draw-config

This file uses TOML format for configuration options.

Configuration Options
---------------------

svg_viewer
~~~~~~~~~~

The command to use for viewing SVG files when using ``--show``.

**Default:** ``open`` (macOS), ``xdg-open`` (Linux), ``start`` (Windows)

**Example:**

.. code-block:: toml

    svg_viewer = "firefox"

png_viewer
~~~~~~~~~~

The command to use for viewing PNG files when using ``--show``.

**Default:** ``open`` (macOS), ``xdg-open`` (Linux), ``start`` (Windows)

**Example:**

.. code-block:: toml

    png_viewer = "gimp"

drawio_viewer
~~~~~~~~~~~~~

The command to use for viewing Draw.io files when using ``--show``.

**Default:** ``open`` (macOS), ``xdg-open`` (Linux), ``start`` (Windows)

**Example:**

.. code-block:: toml

    drawio_viewer = "/Applications/draw.io.app/Contents/MacOS/draw.io"

default_backend
~~~~~~~~~~~~~~~

The default backend to use when rendering diagrams.

**Default:** ``svg``

**Options:** ``svg``, ``png``, ``drawio``

**Example:**

.. code-block:: toml

    default_backend = "svg"

default_width
~~~~~~~~~~~~~

The default width for diagrams in pixels.

**Default:** ``800``

**Example:**

.. code-block:: toml

    default_width = 1024

default_height
~~~~~~~~~~~~~~

The default height for diagrams in pixels.

**Default:** ``600``

**Example:**

.. code-block:: toml

    default_height = 768

Example Configuration File
--------------------------

.. code-block:: toml

    # ~/.od-draw-config

    # Viewer commands
    svg_viewer = "firefox"
    png_viewer = "open"
    drawio_viewer = "/Applications/draw.io.app/Contents/MacOS/draw.io"

    # Default rendering options
    default_backend = "svg"
    default_width = 1024
    default_height = 768

Platform-Specific Defaults
--------------------------

od-draw automatically selects appropriate defaults based on your operating system:

macOS
~~~~~

.. code-block:: toml

    svg_viewer = "open"
    png_viewer = "open"
    drawio_viewer = "open"

Linux
~~~~~

.. code-block:: toml

    svg_viewer = "xdg-open"
    png_viewer = "xdg-open"
    drawio_viewer = "xdg-open"

Windows
~~~~~~~

.. code-block:: toml

    svg_viewer = "start"
    png_viewer = "start"
    drawio_viewer = "start"

Using Configuration in CLI
--------------------------

The configuration file affects the behavior of the ``--show`` flag:

.. code-block:: bash

    # Uses the configured svg_viewer
    python-main my_diagram.py --show --backend svg

    # Uses the configured png_viewer
    python-main my_diagram.py --show --backend png

Configuration Priority
----------------------

Configuration values are resolved in the following order (highest to lowest priority):

1. Command-line arguments
2. Configuration file (``~/.od-draw-config``)
3. Platform-specific defaults

Creating Your Configuration
---------------------------

To create a configuration file:

.. code-block:: bash

    # Create the file
    touch ~/.od-draw-config

    # Edit with your preferred editor
    nano ~/.od-draw-config

Then add your desired configuration options in TOML format.
