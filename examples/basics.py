"""
Basic examples demonstrating od_draw shapes and features.
"""

import od_draw
from od_draw import colors


class Polygons(od_draw.Diagram):
    """Diagram showcasing polygon shapes."""

    def __init__(self, **kwargs):
        super().__init__(width=800, height=600, **kwargs)

        # Triangle - basic with solid border
        triangle = od_draw.Triangle(
            x=50,
            y=50,
            width=100,
            height=100,
            border_thickness=2,
            border_color=colors.BLUE_ROYAL,
            background_color=(colors.BLUE_SKY, 0.3),
        )
        self.add_shape(triangle)

        # Square - with rotation and different border colors per side
        square = od_draw.Square(
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
        self.add_shape(square)

        # Rectangle - dashed border with transparency
        rectangle = od_draw.Rectangle(
            x=350,
            y=50,
            width=150,
            height=100,
            border_thickness=3,
            border_style="dashed",
            border_color=colors.ORANGE,
            background_color=(colors.ORANGE_AMBER, 0.5),
        )
        self.add_shape(rectangle)

        # Custom Polygon - pentagon
        pentagon_points = [
            (600, 50),
            (650, 80),
            (630, 140),
            (570, 140),
            (550, 80),
        ]
        pentagon = od_draw.Polygon(
            points=pentagon_points,
            border_thickness=2,
            border_color=colors.PURPLE,
            background_color=(colors.PURPLE_LAVENDER, 0.6),
            rotation=0,
        )
        self.add_shape(pentagon)

        # Another triangle with dotted border
        triangle2 = od_draw.Triangle(
            x=50,
            y=200,
            width=120,
            height=80,
            border_thickness=2,
            border_style="dotted",
            border_color=colors.GREEN_FOREST,
            background_color=colors.GREEN_MINT,
        )
        self.add_shape(triangle2)

        # Rotated rectangle
        rotated_rect = od_draw.Rectangle(
            x=250,
            y=200,
            width=100,
            height=150,
            border_thickness=3,
            border_color=colors.BROWN_CHOCOLATE,
            background_color=(colors.BROWN_TAN, 0.4),
            rotation=30,
        )
        self.add_shape(rotated_rect)

        # Square with no fill
        empty_square = od_draw.Square(
            x=400,
            y=250,
            size=80,
            border_thickness=4,
            border_color=colors.CYAN_TEAL,
            background_color=None,
        )
        self.add_shape(empty_square)

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
        star = od_draw.Polygon(
            points=star_points,
            border_thickness=2,
            border_color=colors.YELLOW_GOLD,
            background_color=colors.YELLOW,
        )
        self.add_shape(star)


class Lines(od_draw.Diagram):
    """Diagram showcasing line features."""

    def __init__(self, **kwargs):
        super().__init__(width=800, height=600, **kwargs)

        # Simple line
        line1 = od_draw.Line(
            x0=50,
            y0=50,
            x1=200,
            y1=50,
            thickness=2,
            color=colors.BLACK,
        )
        self.add_shape(line1)

        # Line with arrow-out on right end
        line2 = od_draw.Line(
            x0=50,
            y0=100,
            x1=200,
            y1=100,
            thickness=3,
            color=colors.BLUE_ROYAL,
            right_end_style="arrow-out",
        )
        self.add_shape(line2)

        # Line with arrow-in on right end
        line3 = od_draw.Line(
            x0=50,
            y0=150,
            x1=200,
            y1=150,
            thickness=3,
            color=colors.RED,
            right_end_style="arrow-in",
        )
        self.add_shape(line3)

        # Line with circle ends
        line4 = od_draw.Line(
            x0=50,
            y0=200,
            x1=200,
            y1=200,
            thickness=3,
            color=colors.GREEN_FOREST,
            left_end_style="circle",
            right_end_style="circle",
        )
        self.add_shape(line4)

        # Line with square ends
        line5 = od_draw.Line(
            x0=50,
            y0=250,
            x1=200,
            y1=250,
            thickness=3,
            color=colors.ORANGE,
            left_end_style="square",
            right_end_style="square",
        )
        self.add_shape(line5)

        # Dashed line with arrows
        line6 = od_draw.Line(
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
        self.add_shape(line6)

        # Dotted line
        line7 = od_draw.Line(
            x0=250,
            y0=200,
            x1=400,
            y1=300,
            thickness=2,
            color=colors.CYAN_TEAL,
            style="dotted",
        )
        self.add_shape(line7)

        # Line with transparency
        line8 = od_draw.Line(
            x0=450,
            y0=50,
            x1=600,
            y1=50,
            thickness=8,
            color=(colors.RED, 0.5),
            right_end_style="arrow-out",
        )
        self.add_shape(line8)

        # Diagonal line with mixed end styles
        line9 = od_draw.Line(
            x0=450,
            y0=100,
            x1=600,
            y1=250,
            thickness=4,
            color=colors.BLUE_NAVY,
            left_end_style="circle",
            right_end_style="arrow-out",
        )
        self.add_shape(line9)

        # Thick line with square start and arrow end
        line10 = od_draw.Line(
            x0=650,
            y0=100,
            x1=750,
            y1=300,
            thickness=5,
            color=colors.BROWN_MAHOGANY,
            left_end_style="square",
            right_end_style="arrow-in",
        )
        self.add_shape(line10)

        # Crossing lines demonstration
        line11 = od_draw.Line(
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
        self.add_shape(line11)

        line12 = od_draw.Line(
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
        self.add_shape(line12)
