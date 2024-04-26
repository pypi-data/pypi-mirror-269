# Pyxels

Pyxels is a low-level image data manipulation library for Python. It is designed to be fast and efficient, and to provide a simple interface for working with image data. 

Pyxels is currently in early development, and may not yet be ready for general use.

## Installation

To install Pyxels, you can use pip:

```bash
pip install pyxels
```

## Usage

### pyxels.RGB

The `pyxels.RGB` class represents a color in the RGB color space. It has three attributes: `red`, `green`, and `blue`, which are all integers between 0 and 255. It supports addition, subtraction, multiplication, and division with other `pyxels.RGB` instances, as well as comparison with other `pyxels.RGB` instances.

```python
from pyxels import RGB

# Create a new RGB color
color = RGB(255, 0, 0)

# Add two RGB colors
new_color = color + RGB(0, 255, 0)

# Blend two RGB colors
blended_color = color.blend(new_color, 0.42)

# Check if two RGB colors are equal
print(f"The colors are {'equal' if color == new_color else 'not equal'}")

# Convert an RGB color to a hex string
print(color.to_hex())

# Load an RGB color from a hex string
color = RGB.from_hex("#C0FFEE")

# Set the least significant bit of each color channel
other_color = RGB(254, 127, 63)
other_color.set_lsb(RGB(1, 0, 1))

# Get the least significant bit of each color channel
lsb = other_color.get_lsb()

# Bitwise XOR two RGB colors
xor_color = color ^ new_color
```

## License

Pyxels is released under the MIT license. See [LICENSE](LICENSE) for more information.