"""
od_draw.colors: Color management for od-draw diagrams.

Supports hex colors with optional alpha channel for SVG/PNG rendering.
"""

from typing import Optional, Tuple, Union


class Color:
    """Represents a color with optional alpha (transparency) channel.

    Examples:
        color = Color("#FF0000")  # Red
        color = Color("#FF0000", 0.5)  # Red with 50% opacity
        color = Color("#FF000080")  # Red with 50% opacity (hex alpha)
    """

    def __init__(self, hex_color: str, alpha: Optional[float] = None) -> None:
        """Initialize a color.

        Args:
            hex_color: Hex color string (e.g., "#FF0000" or "#FF000080")
            alpha: Optional alpha value between 0 and 1. If not provided,
                   will be extracted from hex_color if it has 8 digits.
        """
        self.hex_color = hex_color.upper()

        # Parse hex color
        if self.hex_color.startswith("#"):
            hex_digits = self.hex_color[1:]
        else:
            hex_digits = self.hex_color

        # Extract RGB and alpha from hex
        if len(hex_digits) == 6:
            # RGB only
            self.rgb = self._hex_to_rgb(hex_digits)
            self.alpha = alpha if alpha is not None else 1.0
        elif len(hex_digits) == 8:
            # RGBA
            self.rgb = self._hex_to_rgb(hex_digits[:6])
            hex_alpha = int(hex_digits[6:8], 16) / 255.0
            # If alpha parameter provided, it overrides hex alpha
            self.alpha = alpha if alpha is not None else hex_alpha
        else:
            raise ValueError(f"Invalid hex color: {hex_color}. Must be 6 or 8 digits.")

        # Validate alpha range
        if not 0 <= self.alpha <= 1:
            raise ValueError(f"Alpha must be between 0 and 1, got {self.alpha}")

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color string to RGB tuple."""
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)

    def to_hex(self, include_alpha: bool = False) -> str:
        """Convert to hex string.

        Args:
            include_alpha: If True, includes alpha channel in output

        Returns:
            Hex color string (e.g., "#FF0000" or "#FF000080")
        """
        r, g, b = self.rgb
        if include_alpha:
            alpha_hex = format(int(self.alpha * 255), '02X')
            return f"#{r:02X}{g:02X}{b:02X}{alpha_hex}"
        return f"#{r:02X}{g:02X}{b:02X}"

    def to_rgba(self) -> Tuple[int, int, int, float]:
        """Convert to RGBA tuple."""
        return (*self.rgb, self.alpha)

    def with_alpha(self, alpha: float) -> "Color":
        """Create a new Color with a different alpha value.

        Args:
            alpha: New alpha value between 0 and 1

        Returns:
            New Color instance with the same RGB but different alpha
        """
        return Color(self.to_hex(include_alpha=False), alpha)

    def __repr__(self) -> str:
        return f"Color('{self.to_hex(include_alpha=True)}')"

    def __str__(self) -> str:
        return self.to_hex(include_alpha=True)


# Helper type for color inputs
ColorInput = Union[Color, str, Tuple[Union[Color, str], float]]


def parse_color(color_input: ColorInput) -> Color:
    """Parse various color input formats into a Color object.

    Args:
        color_input: Can be:
            - Color object
            - Hex string (6 or 8 digits)
            - Tuple of (Color or hex string, alpha)

    Returns:
        Color object

    Examples:
        parse_color("#FF0000")
        parse_color(colors.RED)
        parse_color(("#FF0000", 0.5))
        parse_color((colors.RED, 0.5))
    """
    if isinstance(color_input, Color):
        return color_input
    elif isinstance(color_input, str):
        return Color(color_input)
    elif isinstance(color_input, tuple):
        color_part, alpha = color_input
        if isinstance(color_part, Color):
            return color_part.with_alpha(alpha)
        else:
            return Color(color_part, alpha)
    else:
        raise TypeError(f"Invalid color input type: {type(color_input)}")


# Predefined colors based on SHELLACK color palette
# Basic ANSI Colors
BLACK = Color("#000000")
RED = Color("#FF0000")
GREEN = Color("#00FF00")
YELLOW = Color("#FFFF00")
BLUE = Color("#0000FF")
MAGENTA = Color("#FF00FF")
CYAN = Color("#00FFFF")
WHITE = Color("#FFFFFF")

# Bright Colors
BRIGHT_BLACK = Color("#555555")
BRIGHT_RED = Color("#FF5555")
BRIGHT_GREEN = Color("#55FF55")
BRIGHT_YELLOW = Color("#FFFF55")
BRIGHT_BLUE = Color("#5555FF")
BRIGHT_MAGENTA = Color("#FF55FF")
BRIGHT_CYAN = Color("#55FFFF")
BRIGHT_WHITE = Color("#FFFFFF")

# Gray Scale Colors
LIGHT_GRAY = Color("#D3D3D3")
GRAY = Color("#808080")
SLATE_GRAY = Color("#708090")
DARK_GRAY = Color("#A9A9A9")
CHARCOAL = Color("#36454F")

# Reds
RED_SALMON = Color("#FA8072")
RED_CORAL = Color("#FF7F50")
RED_TOMATO = Color("#FF6347")
RED_CRIMSON = Color("#DC143C")
RED_FIRE_BRICK = Color("#B22222")
RED_DARK = Color("#8B0000")

# Pinks
PINK = Color("#FFC0CB")
PINK_HOT = Color("#FF69B4")
PINK_DEEP = Color("#FF1493")
PINK_FUCHSIA = Color("#FF00FF")

# Oranges
ORANGE = Color("#FFA500")
ORANGE_DARK = Color("#FF8C00")
ORANGE_BURNT = Color("#CC5500")
ORANGE_AMBER = Color("#FFBF00")
ORANGE_COPPER = Color("#B87333")

# Yellows
YELLOW_GOLD = Color("#FFD700")
YELLOW_MUSTARD = Color("#FFDB58")
YELLOW_HONEY = Color("#FFC30B")
YELLOW_LEMON = Color("#FFF44F")

# Greens
GREEN_LIME = Color("#00FF00")
GREEN_FOREST = Color("#228B22")
GREEN_MINT = Color("#98FF98")
GREEN_EMERALD = Color("#50C878")
GREEN_SEA = Color("#2E8B57")
GREEN_OLIVE = Color("#808000")
GREEN_SAGE = Color("#9DC183")

# Blues
BLUE_SKY = Color("#87CEEB")
BLUE_ROYAL = Color("#4169E1")
BLUE_NAVY = Color("#000080")
BLUE_SAPPHIRE = Color("#0F52BA")
BLUE_STEEL = Color("#4682B4")
BLUE_MIDNIGHT = Color("#191970")

# Cyans
CYAN_TURQUOISE = Color("#40E0D0")
CYAN_TEAL = Color("#008080")
CYAN_AQUA = Color("#00FFFF")

# Purples
PURPLE = Color("#800080")
PURPLE_LAVENDER = Color("#E6E6FA")
PURPLE_ORCHID = Color("#DA70D6")
PURPLE_AMETHYST = Color("#9966CC")
PURPLE_VIOLET = Color("#8F00FF")

# Browns
BROWN = Color("#A52A2A")
BROWN_TAN = Color("#D2B48C")
BROWN_SIENNA = Color("#A0522D")
BROWN_CHOCOLATE = Color("#D2691E")
BROWN_MAHOGANY = Color("#C04000")

# Special/Utility
TRANSPARENT = Color("#FFFFFF", 0.0)
