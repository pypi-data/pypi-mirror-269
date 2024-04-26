# EscFormatter

## Description

This Python package provides a class named `Esc` that enables the execution of ANSI escape commands in the console. It offers functionalities for advanced text formatting, changing font colors in the console, applying text styles, and positioning the cursor.

## Usage Example

```python
from escformatter.esc import Esc

# Create an instance of Esc
e = Esc()

# Register cleanup to reset console styles and colors to default
e.register_cleanup()

# Display 'Hello, World!' in red
print(e.fg_red + 'Hello, World!')
