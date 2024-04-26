from dataclasses import dataclass
from typing import Iterator, Protocol, SupportsInt, TypeAlias, cast, override

from typing_extensions import Buffer, SupportsIndex


class SupportsTrunc(Protocol):
    def __trunc__(self) -> int: ...


ReadableBuffer: TypeAlias = Buffer
ConvertibleToInt: TypeAlias = (
    str | ReadableBuffer | SupportsInt | SupportsIndex | SupportsTrunc
)


class ClampedUint8(int):
    """
    Represents an unsigned 8-bit integer that is clamped between 0 and 255.
    """

    def __new__(cls, value):
        return super().__new__(cls, min(max(value, 0), 255))


@dataclass
class RGB:
    """
    Represents a color in the RGB color model.

    Attributes:
        red (int | ClampedUint8): The red component of the color.
        green (int | ClampedUint8): The green component of the color.
        blue (int | ClampedUint8): The blue component of the color.
    """

    def __init__(
        self,
        red: int | ClampedUint8,
        green: int | ClampedUint8,
        blue: int | ClampedUint8,
    ):
        """
        Initializes a new instance of the RGB class.

        Args:
            red (int | ClampedUint8): The red component of the color.
            green (int | ClampedUint8): The green component of the color.
            blue (int | ClampedUint8): The blue component of the color.
        """
        self.red = ClampedUint8(red)
        self.green = ClampedUint8(green)
        self.blue = ClampedUint8(blue)
        super().__init__()

    @classmethod
    def from_hex(cls, value: str) -> "RGB":
        """
        Creates an RGB color from a hexadecimal string.

        Args:
            value (str): The hexadecimal string representing the color.

        Returns:
            RGB: The RGB color created from the hexadecimal string.
        """
        return cls(
            ClampedUint8(int(value[1:3], 16)),
            ClampedUint8(int(value[3:5], 16)),
            ClampedUint8(int(value[5:7], 16)),
        )

    @override
    def __str__(self) -> str:
        """
        Returns a string representation of the RGB color.

        Returns:
            str: The string representation of the RGB color.
        """
        return f"#{self.red:02x}{self.green:02x}{self.blue:02x}"

    @override
    def __repr__(self) -> str:
        """
        Returns a string representation of the RGB color.

        Returns:
            str: The string representation of the RGB color.
        """
        return f"RGB({self.red}, {self.green}, {self.blue})"

    @override
    def __eq__(self, other: object) -> bool:
        """
        Checks if the RGB color is equal to another RGB color.

        Args:
            other (object): The other object to compare.

        Returns:
            bool: True if the RGB colors are equal, False otherwise.
        """
        if not isinstance(other, RGB):
            return NotImplemented
        return (
            self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
        )

    @override
    def __hash__(self) -> int:
        """
        Returns the hash value of the RGB color.

        Returns:
            int: The hash value of the RGB color.
        """
        return hash((self.red, self.green, self.blue))

    def __iter__(self) -> Iterator[ClampedUint8]:
        """
        Returns an iterator over the RGB color components.

        Returns:
            Iterator[ClampedUint8]: An iterator over the RGB color components.
        """
        return iter(
            (
                cast(ClampedUint8, self.red),
                cast(ClampedUint8, self.green),
                cast(ClampedUint8, self.blue),
            )
        )

    def __getitem__(self, index: int) -> ClampedUint8:
        """
        Returns the RGB color component at the specified index.

        Args:
            index (int): The index of the RGB color component.

        Returns:
            ClampedUint8: The RGB color component at the specified index.
        """
        return cast(ClampedUint8, (self.red, self.green, self.blue)[index])

    def to_hex(self) -> str:
        """
        Converts the RGB color to a hexadecimal string.

        Returns:
            str: The hexadecimal string representation of the RGB color.
        """
        return str(self)

    def __add__(self, other: "RGB") -> "RGB":
        """
        Adds two RGB colors together.

        Args:
            other (RGB): The other RGB color to add.

        Returns:
            RGB: The result of adding the two RGB colors together.
        """
        return RGB(
            ClampedUint8(self.red + other.red),
            ClampedUint8(self.green + other.green),
            ClampedUint8(self.blue + other.blue),
        )

    def __sub__(self, other: "RGB") -> "RGB":
        """
        Subtracts one RGB color from another.

        Args:
            other (RGB): The other RGB color to subtract.

        Returns:
            RGB: The result of subtracting the other RGB color from this RGB color.
        """
        return RGB(
            ClampedUint8(self.red - other.red),
            ClampedUint8(self.green - other.green),
            ClampedUint8(self.blue - other.blue),
        )

    def __mul__(self, other: "RGB") -> "RGB":
        """
        Multiplies two RGB colors together.

        Args:
            other (RGB): The other RGB color to multiply.

        Returns:
            RGB: The result of multiplying the two RGB colors together.
        """
        return RGB(
            ClampedUint8(self.red * other.red),
            ClampedUint8(self.green * other.green),
            ClampedUint8(self.blue * other.blue),
        )

    def __truediv__(self, other: "RGB") -> "RGB":
        """
        Divides one RGB color by another.

        Args:
            other (RGB): The other RGB color to divide by.

        Returns:
            RGB: The result of dividing this RGB color by the other RGB color.
        """
        return RGB(
            ClampedUint8(self.red // other.red),
            ClampedUint8(self.green // other.green),
            ClampedUint8(self.blue // other.blue),
        )

    def __floordiv__(self, other: "RGB") -> "RGB":
        """
        Divides one RGB color by another using floor division.

        Args:
            other (RGB): The other RGB color to divide by.

        Returns:
            RGB: The result of dividing this RGB color by the other RGB color using floor division.
        """
        return RGB(
            ClampedUint8(self.red // other.red),
            ClampedUint8(self.green // other.green),
            ClampedUint8(self.blue // other.blue),
        )

    def __mod__(self, other: "RGB") -> "RGB":
        """
        Computes the modulo of one RGB color by another.

        Args:
            other (RGB): The other RGB color to compute the modulo with.

        Returns:
            RGB: The result of computing the modulo of this RGB color by the other RGB color.
        """
        return RGB(
            ClampedUint8(self.red % other.red),
            ClampedUint8(self.green % other.green),
            ClampedUint8(self.blue % other.blue),
        )

    def __and__(self, other: "RGB") -> "RGB":
        """
        Performs a bitwise AND operation between two RGB colors.

        Args:
            other (RGB): The other RGB color to perform the bitwise AND operation with.

        Returns:
            RGB: The result of performing the bitwise AND operation between the two RGB colors.
        """
        return RGB(
            self.red & other.red, self.green & other.green, self.blue & other.blue
        )

    def __or__(self, other: "RGB") -> "RGB":
        """
        Performs a bitwise OR operation between two RGB colors.

        Args:
            other (RGB): The other RGB color to perform the bitwise OR operation with.

        Returns:
            RGB: The result of performing the bitwise OR operation between the two RGB colors.
        """
        return RGB(
            self.red | other.red, self.green | other.green, self.blue | other.blue
        )

    def __xor__(self, other: "RGB") -> "RGB":
        """
        Performs a bitwise XOR operation between two RGB colors.

        Args:
            other (RGB): The other RGB color to perform the bitwise XOR operation with.

        Returns:
            RGB: The result of performing the bitwise XOR operation between the two RGB colors.
        """
        return RGB(
            self.red ^ other.red, self.green ^ other.green, self.blue ^ other.blue
        )

    def __invert__(self) -> "RGB":
        """
        Performs a bitwise inversion of the RGB color.

        Returns:
            RGB: The result of performing the bitwise inversion of the RGB color.
        """
        return RGB(~self.red & 0xFF, ~self.green & 0xFF, ~self.blue & 0xFF)

    def set_lsb(self, bits: "RGB") -> "RGB":
        """
        Sets the least significant bits of the RGB color with the corresponding bits from another RGB color.

        Args:
            bits (RGB): The RGB color containing the least significant bits to set.

        Returns:
            RGB: The result of setting the least significant bits of the RGB color.
        """
        return RGB(
            (self.red & ~1) | (bits.red & 1),
            (self.green & ~1) | (bits.green & 1),
            (self.blue & ~1) | (bits.blue & 1),
        )

    def get_lsb(self) -> "RGB":
        """
        Gets the least significant bits of the RGB color.

        Returns:
            RGB: The RGB color containing the least significant bits.
        """
        return RGB(self.red & 1, self.green & 1, self.blue & 1)

    def blend(self, other: "RGB", factor: float) -> "RGB":
        """
        Blends the RGB color with another RGB color using a specified blending factor.

        Args:
            other (RGB): The other RGB color to blend with.
            factor (float): The blending factor between 0 and 1.

        Returns:
            RGB: The result of blending the RGB color with the other RGB color.
        """
        if factor < 0:
            factor = 0
        elif factor > 1:
            factor = 1

        return RGB(
            ClampedUint8(round(self.red * (1 - factor) + other.red * factor)),
            ClampedUint8(round(self.green * (1 - factor) + other.green * factor)),
            ClampedUint8(round(self.blue * (1 - factor) + other.blue * factor)),
        )

    def to_grayscale(self) -> "RGB":
        """
        Converts the RGB color to grayscale.

        Returns:
            RGB: The grayscale representation of the RGB color.
        """
        luminance = int(0.299 * self.red + 0.587 * self.green + 0.114 * self.blue)
        return RGB(luminance, luminance, luminance)

    def distance(self, other: "RGB") -> float:
        """
        Computes the Euclidean distance between the RGB color and another RGB color.

        Args:
            other (RGB): The other RGB color.

        Returns:
            float: The Euclidean distance between the RGB color and the other RGB color.
        """
        return (
            (self.red - other.red) ** 2
            + (self.green - other.green) ** 2
            + (self.blue - other.blue) ** 2
        ) ** 0.5

    def lighten(self, amount: int) -> "RGB":
        """
        Lightens the RGB color by a specified amount.

        Args:
            amount (int): The amount to lighten the RGB color.

        Returns:
            RGB: The result of lightening the RGB color.
        """
        return RGB(
            ClampedUint8(self.red + amount),
            ClampedUint8(self.green + amount),
            ClampedUint8(self.blue + amount),
        )

    def darken(self, amount: int) -> "RGB":
        """
        Darkens the RGB color by a specified amount.

        Args:
            amount (int): The amount to darken the RGB color.

        Returns:
            RGB: The result of darkening the RGB color.
        """
        return RGB(
            ClampedUint8(self.red - amount),
            ClampedUint8(self.green - amount),
            ClampedUint8(self.blue - amount),
        )
