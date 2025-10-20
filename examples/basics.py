"""
Basic examples demonstrating od_draw shapes and features.
"""

from od_draw.diagram.base import Diagram
from od_draw.shapes.base import Triangle, Square, Rectangle, Polygon, Line
from od_draw import colors


class Polygons(Diagram):
    """Diagram showcasing polygon shapes."""

    def __init__(self, **kwargs):
        super().__init__(width=800, height=600, **kwargs)

        # Triangle - basic with solid border
        Triangle(
            diagram=self,
            x=50,
            y=50,
            width=100,
            height=100,
            border_thickness=2,
            border_color=colors.BLUE_ROYAL,
            background_color=(colors.BLUE_SKY, 0.3),
        )

        # Square - with rotation and different border colors per side
        Square(
            diagram=self,
            x=200,
            y=50,
            size=100,
            border_thickness=(2, 4, 2, 4),  # top, right, bottom, left
            border_color=(
                colors.RED,
                colors.GREEN,
                colors.BLUE,
                colors.YELLOW,
            ),
            background_color=colors.PINK_HOT,
            rotation=15,
        )

        # Rectangle - dashed border with transparency
        Rectangle(
            diagram=self,
            x=350,
            y=50,
            width=150,
            height=100,
            border_thickness=3,
            border_style="dashed",
            border_color=colors.ORANGE,
            background_color=(colors.ORANGE_AMBER, 0.5),
        )

        # Custom Polygon - pentagon
        pentagon_points = [
            (600, 50),
            (650, 80),
            (630, 140),
            (570, 140),
            (550, 80),
        ]
        Polygon(
            diagram=self,
            points=pentagon_points,
            border_thickness=2,
            border_color=colors.PURPLE,
            background_color=(colors.PURPLE_LAVENDER, 0.6),
            rotation=0,
        )

        # Another triangle with dotted border
        Triangle(
            diagram=self,
            x=50,
            y=200,
            width=120,
            height=80,
            border_thickness=2,
            border_style="dotted",
            border_color=colors.GREEN_FOREST,
            background_color=colors.GREEN_MINT,
        )

        # Rotated rectangle
        Rectangle(
            diagram=self,
            x=250,
            y=200,
            width=100,
            height=150,
            border_thickness=3,
            border_color=colors.BROWN_CHOCOLATE,
            background_color=(colors.BROWN_TAN, 0.4),
            rotation=30,
        )

        # Square with no fill
        Square(
            diagram=self,
            x=400,
            y=250,
            size=80,
            border_thickness=4,
            border_color=colors.CYAN_TEAL,
            background_color=None,
        )

        # Custom polygon - star shape
        star_points = [
            (600, 200),  # top
            (615, 235),  # inner right
            (650, 250),  # right
            (620, 275),  # inner bottom right
            (630, 310),  # bottom right
            (600, 290),  # inner bottom
            (570, 310),  # bottom left
            (580, 275),  # inner bottom left
            (550, 250),  # left
            (585, 235),  # inner left
        ]
        Polygon(
            diagram=self,
            points=star_points,
            border_thickness=2,
            border_color=colors.YELLOW_GOLD,
            background_color=colors.YELLOW,
        )


class Lines(Diagram):
    """Diagram showcasing line features."""

    def __init__(self, **kwargs):
        super().__init__(width=800, height=600, **kwargs)

        # Simple line
        Line(
            diagram=self,
            x0=50,
            y0=50,
            x1=200,
            y1=50,
            thickness=2,
            color=colors.BLACK,
        )

        # Line with arrow-out on right end
        Line(
            diagram=self,
            x0=50,
            y0=100,
            x1=200,
            y1=100,
            thickness=3,
            color=colors.BLUE_ROYAL,
            right_end_style="arrow-out",
        )

        # Line with arrow-in on right end
        Line(
            diagram=self,
            x0=50,
            y0=150,
            x1=200,
            y1=150,
            thickness=3,
            color=colors.RED,
            right_end_style="arrow-in",
        )

        # Line with circle ends
        Line(
            diagram=self,
            x0=50,
            y0=200,
            x1=200,
            y1=200,
            thickness=3,
            color=colors.GREEN_FOREST,
            left_end_style="circle",
            right_end_style="circle",
        )

        # Line with square ends
        Line(
            diagram=self,
            x0=50,
            y0=250,
            x1=200,
            y1=250,
            thickness=3,
            color=colors.ORANGE,
            left_end_style="square",
            right_end_style="square",
        )

        # Dashed line with arrows
        Line(
            diagram=self,
            x0=250,
            y0=50,
            x1=400,
            y1=150,
            thickness=2,
            color=colors.PURPLE,
            style="dashed",
            left_end_style="arrow-out",
            right_end_style="arrow-out",
        )

        # Dotted line
        Line(
            diagram=self,
            x0=250,
            y0=200,
            x1=400,
            y1=300,
            thickness=2,
            color=colors.CYAN_TEAL,
            style="dotted",
        )

        # Line with transparency
        Line(
            diagram=self,
            x0=450,
            y0=50,
            x1=600,
            y1=50,
            thickness=8,
            color=(colors.RED, 0.5),
            right_end_style="arrow-out",
        )

        # Diagonal line with mixed end styles
        Line(
            diagram=self,
            x0=450,
            y0=100,
            x1=600,
            y1=250,
            thickness=4,
            color=colors.BLUE_NAVY,
            left_end_style="circle",
            right_end_style="arrow-out",
        )

        # Thick line with square start and arrow end
        Line(
            diagram=self,
            x0=650,
            y0=100,
            x1=750,
            y1=300,
            thickness=5,
            color=colors.BROWN_MAHOGANY,
            left_end_style="square",
            right_end_style="arrow-in",
        )

        # Crossing lines demonstration
        Line(
            diagram=self,
            x0=100,
            y0=350,
            x1=300,
            y1=550,
            thickness=3,
            color=(colors.YELLOW_GOLD, 0.7),
            style="solid",
            left_end_style="circle",
            right_end_style="arrow-out",
        )

        Line(
            diagram=self,
            x0=100,
            y0=550,
            x1=300,
            y1=350,
            thickness=3,
            color=(colors.PINK_HOT, 0.7),
            style="dashed",
            left_end_style="arrow-out",
            right_end_style="circle",
        )
