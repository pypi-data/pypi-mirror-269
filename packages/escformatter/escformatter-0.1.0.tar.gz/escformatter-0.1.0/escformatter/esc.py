"""
Filename: esc.py
Author: Leonardo S. Amaral
Created: April 25, 2024

Description:
This file contains a Python class named `Esc` that allows executing ANSI escape commands in the console. It provides functionalities for advanced text formatting, changing font color of the console, text style, and cursor positioning.

Usage Example:
>>> e = Esc()
>>> e.register_cleanup()  # Registers resetting console styles and colors to default before exiting the application
>>> print(e.fg_red + 'Hello, World!')  # Displays 'Hello, World!' in red

Classes:
- `Esc`: Class to execute ANSI escape commands in the console.

Methods:
- `__init__(self) -> None`: Initializes the object and sets the cleanup state as not registered.
- `register_cleanup(self) -> None`: Registers a function to reset formatting upon program termination, if not already registered.
- `fg_rgb_color(self, r: Union[int, str], g: Union[int, str], b: Union[int, str]) -> str`: Returns an ANSI escape sequence to set the text color to RGB.
- `bg_rgb_color(self, r: Union[int, str], g: Union[int, str], b: Union[int, str]) -> str`: Returns an ANSI escape sequence to set the background color to RGB.
- `clear_line(self) -> str`: Returns an ANSI escape sequence to clear the current line.
- `clear_previous_line(self) -> str`: Returns an ANSI escape sequence to clear the previous line.
- `clear(self) -> str`: Returns an ANSI escape sequence to clear the screen.

Properties:
- Various properties to set font color (foreground) and background color using ANSI escape sequences.
- Properties to apply text styles such as bold, italic, underline, etc.
- Properties to reset color, intensity, and text style to default settings.

Static Methods:
- `_validate_normalize_color(value: Union[int, str]) -> str`: Validates and normalizes an RGB color value.

Constants:
- None

Exceptions:
- None
"""

import atexit
from typing import Union

class Esc:
    """Class to execute ANSI escape commands in the console:
    - Advanced text formatting;
    - Changing font color of the console;
    - Text style;
    - Cursor positioning.

    ### Usage example:
    >>> e = Esc()
    >>> e.register_cleanup() # Registers resetting console styles and colors to default before exiting the application
    >>> print(e.fg_red + 'Hello, World!')  # Displays 'Hello, World!' in red
    """

    def __init__(self) -> None:
        """Initialize the object and set the cleanup state as not registered."""
        self._cleanup_registered = False

    @property
    def reset_all(self) -> str:
        """Returns an ANSI escape sequence to reset all settings to default."""
        return '\033[0m'

    @property
    def reverse(self) -> str:
        """Returns an ANSI escape sequence to invert colors between text and background."""
        return '\033[7m'

    @property
    def reverse_off(self) -> str:
        """Returns an ANSI escape sequence to deactivate color inversion between text and background."""
        return '\033[27m'
    
    @property
    def slow_blink(self) -> str:
        """Returns an ANSI escape sequence to enable slow blink text mode."""
        return '\033[5m'

    @property
    def slow_blink_off(self) -> str:
        """Returns an ANSI escape sequence to disable slow blink text mode."""
        return '\033[25m'

    @property
    def fast_blink(self) -> str:
        """Returns an ANSI escape sequence to enable fast blink text mode."""
        return '\033[6m'

    @property
    def fast_blink_off(self) -> str:
        """Returns an ANSI escape sequence to disable fast blink text mode."""
        return '\033[26m'

    @property
    def reset_intensity(self) -> str:
        """Returns an ANSI escape sequence to reset text intensity, reverting bold and faint styles to normal."""
        return '\033[22m'

    @property
    def bold(self) -> str:
        """Returns an ANSI escape sequence to enable bold text mode."""
        return '\033[1m'

    @property
    def faint(self) -> str:
        """Returns an ANSI escape sequence to enable faint text mode."""
        return '\033[2m'

    @property
    def faint_off(self) -> str:
        """Returns an ANSI escape sequence to disable faint text mode."""
        return '\033[22m'

    @property
    def italic(self) -> str:
        """Returns an ANSI escape sequence to enable italic text mode."""
        return '\033[3m'

    @property
    def italic_off(self) -> str:
        """Returns an ANSI escape sequence to disable italic text mode."""
        return '\033[23m'

    @property
    def underline(self) -> str:
        """Returns an ANSI escape sequence to enable underline mode."""
        return '\033[4m'
    
    @property
    def dunderline(self) -> str:
        """Returns an ANSI escape sequence to disable bold text mode and enable double underline mode."""
        return '\033[21m'

    @property
    def underline_off(self) -> str:
        """Returns an ANSI escape sequence to disable underline mode."""
        return '\033[24m'

    @property
    def crossed_out(self) -> str:
        """Returns an ANSI escape sequence to enable crossed-out text mode."""
        return '\033[9m'

    @property
    def crossed_out_off(self) -> str:
        """Returns an ANSI escape sequence to disable crossed-out text mode."""
        return '\033[29m'

    @property
    def hide(self) -> str:
        """Returns an ANSI escape sequence to hide text."""
        return '\033[8m'

    @property
    def reveal(self) -> str:
        """Returns an ANSI escape sequence to reveal text after being hidden."""
        return '\033[28m'

    @property
    def overlined(self) -> str:
        """Returns an ANSI escape sequence to enable overlined text mode."""
        return '\033[53m'

    @property
    def overlined_off(self) -> str:
        """Returns an ANSI escape sequence to disable overlined text mode."""
        return '\033[55m'
    
    @property
    def framed(self) -> str:
        """Returns an ANSI escape sequence to enable framed text mode."""
        return '\033[51m'

    @property
    def encircled(self) -> str:
        """Returns an ANSI escape sequence to enable encircled text mode."""
        return '\033[52m'

    @property
    def bordered_off(self) -> str:
        """Returns an ANSI escape sequence to disable framed and encircled text mode."""
        return '\033[54m'

    @property
    def fg_reset(self) -> str:
        """Returns an ANSI escape sequence to reset the font color to default."""
        return '\033[39m'

    @property
    def fg_black(self) -> str:
        """Returns an ANSI escape sequence to set the font color to black."""
        return '\033[30m'

    @property
    def fg_red(self) -> str:
        """Returns an ANSI escape sequence to set the font color to red."""
        return '\033[31m'

    @property
    def fg_green(self) -> str:
        """Returns an ANSI escape sequence to set the font color to green."""
        return '\033[32m'

    @property
    def fg_yellow(self) -> str:
        """Returns an ANSI escape sequence to set the font color to yellow."""
        return '\033[33m'

    @property
    def fg_blue(self) -> str:
        """Returns an ANSI escape sequence to set the font color to blue."""
        return '\033[34m'

    @property
    def fg_magenta(self) -> str:
        """Returns an ANSI escape sequence to set the font color to magenta."""
        return '\033[35m'

    @property
    def fg_cyan(self) -> str:
        """Returns an ANSI escape sequence to set the font color to cyan."""
        return '\033[36m'

    @property
    def fg_white(self) -> str:
        """Returns an ANSI escape sequence to set the font color to white."""
        return '\033[37m'

    @property
    def fg_light_black(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light black."""
        return '\033[90m'

    @property
    def fg_light_red(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light red."""
        return '\033[91m'

    @property
    def fg_light_green(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light green."""
        return '\033[92m'

    @property
    def fg_light_yellow(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light yellow."""
        return '\033[93m'

    @property
    def fg_light_blue(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light blue."""
        return '\033[94m'

    @property
    def fg_light_magenta(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light magenta."""
        return '\033[95m'

    @property
    def fg_light_cyan(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light cyan."""
        return '\033[96m'

    @property
    def fg_light_white(self) -> str:
        """Returns an ANSI escape sequence to set the font color to light white."""
        return '\033[97m'

    @property
    def bg_reset(self) -> str:
        """Returns an ANSI escape sequence to reset the background color to default."""
        return '\033[49m'

    @property
    def bg_black(self) -> str:
        """Returns an ANSI escape sequence to set the background color to black."""
        return '\033[40m'

    @property
    def bg_red(self) -> str:
        """Returns an ANSI escape sequence to set the background color to red."""
        return '\033[41m'

    @property
    def bg_green(self) -> str:
        """Returns an ANSI escape sequence to set the background color to green."""
        return '\033[42m'

    @property
    def bg_yellow(self) -> str:
        """Returns an ANSI escape sequence to set the background color to yellow."""
        return '\033[43m'

    @property
    def bg_blue(self) -> str:
        """Returns an ANSI escape sequence to set the background color to blue."""
        return '\033[44m'

    @property
    def bg_magenta(self) -> str:
        """Returns an ANSI escape sequence to set the background color to magenta."""
        return '\033[45m'

    @property
    def bg_cyan(self) -> str:
        """Returns an ANSI escape sequence to set the background color to cyan."""
        return '\033[46m'

    @property
    def bg_white(self) -> str:
        """Returns an ANSI escape sequence to set the background color to white."""
        return '\033[47m'

    @property
    def bg_light_black(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light black."""
        return '\033[100m'

    @property
    def bg_light_red(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light red."""
        return '\033[101m'

    @property
    def bg_light_green(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light green."""
        return '\033[102m'

    @property
    def bg_light_yellow(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light yellow."""
        return '\033[103m'

    @property
    def bg_light_blue(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light blue."""
        return '\033[104m'

    @property
    def bg_light_magenta(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light magenta."""
        return '\033[105m'

    @property
    def bg_light_cyan(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light cyan."""
        return '\033[106m'

    @property
    def bg_light_white(self) -> str:
        """Returns an ANSI escape sequence to set the background color to light white."""
        return '\033[107m'

    @staticmethod
    def _validate_normalize_color(value: Union[int, str]) -> str:
        """Validates and normalizes an RGB color value.

        This method accepts integer values or strings representing integers. If an integer value is provided,
        it will be checked to ensure it falls within the range of 0 to 255. If a string is provided, it will
        be checked to ensure it contains only digits. If yes, the string will be converted to an integer and normalized.
        If the conversion to integer fails or if the string contains non-numeric characters, the default value of 0
        will be returned.

        ### Args:
            value (Union[int, str]): The color value to be validated and normalized.

        ### Returns:
            str: The normalized color value, represented as a string.
        """
        if isinstance(value, str):
            if value.isdigit():
                return str(max(0, min(int(value), 255)))
            else:
                try:
                    int_value = int(value)
                    return str(max(0, min(int_value, 255)))
                except ValueError:
                    return '0'
        elif isinstance(value, int):
            return str(max(0, min(value, 255)))
        else:
            return '0'

    def fg_rgb_color(self, r: Union[int, str], g: Union[int, str], b: Union[int, str]) -> str:
        """Returns an ANSI escape sequence to set the text color to RGB.

        This method takes RGB color values and returns an ANSI escape sequence that sets the text color
        to the color specified by the red (R), green (G), and blue (B) values.

        ### Args:
            r (Union[int, str]): The value for the red component of the color (0-255 or a string representing an integer).
            g (Union[int, str]): The value for the green component of the color (0-255 or a string representing an integer).
            b (Union[int, str]): The value for the blue component of the color (0-255 or a string representing an integer).

        ### Returns:
            str: The ANSI escape sequence to set the text color to the specified RGB color.
        """
        r = self._validate_normalize_color(r)
        g = self._validate_normalize_color(g)
        b = self._validate_normalize_color(b)
        return f'\033[38;2;{r};{g};{b}m'
    
    def bg_rgb_color(self, r: Union[int, str], g: Union[int, str], b: Union[int, str]) -> str:
        """Returns an ANSI escape sequence to set the background color to RGB.

        This method takes RGB color values and returns an ANSI escape sequence that sets the background color
        to the color specified by the red (R), green (G), and blue (B) values.

        ### Args:
            r (Union[int, str]): The value for the red component of the color (0-255 or string representing an integer).
            g (Union[int, str]): The value for the green component of the color (0-255 or string representing an integer).
            b (Union[int, str]): The value for the blue component of the color (0-255 or string representing an integer).

        ### Returns:
            str: The ANSI escape sequence to set the background color to the specified RGB color.
        """
        r = self._validate_normalize_color(r)
        g = self._validate_normalize_color(g)
        b = self._validate_normalize_color(b)
        return f'\033[48;2;{r};{g};{b}m'
    
    @property
    def b(self) -> str:
        """Returns the ANSI escape sequence for the backspace character.

        The backspace character moves the cursor one position to the left on the current line, without erasing any characters.

        ### Returns:
            str: The ANSI escape sequence for the backspace character ('\\b').
        """
        return '\010'
    
    @property
    def t(self) -> str:
        """Returns the ANSI escape sequence for the tab character.

        The tab character moves the cursor to the next tab stop.

        ### Returns:
            str: The ANSI escape sequence for the tab character ('\\t').
        """
        return '\011'

    @property
    def cr(self) -> str:
        """Returns the ANSI escape sequence for the carriage return character.

        The carriage return character moves the cursor to the beginning of the current line.

        ### Returns:
            str: The ANSI escape sequence for the carriage return character ('\\r').
        """
        return '\r'
    
    @property
    def lf(self) -> str:
        """Returns the ANSI escape sequence for the line feed character.

        The line feed character moves the cursor to the beginning of the next line.

        ### Returns:
            str: The ANSI escape sequence for the line feed character ('\\n').
        """
        return '\n'

    @property
    def clear_line(self) -> str:
        """Returns an ANSI escape sequence to clear the current line.

        This escape sequence removes all text from the current line without moving the cursor to a new line.

        ### Returns:
            str: The ANSI escape sequence to clear the current line.
        """
        return '\015\033[K'

    @property
    def clear_previous_line(self) -> str:
        """Returns an ANSI escape sequence to clear the previous line.

        This escape sequence moves the cursor to the previous line, removes the current line, and then
        clears all text from the previous line without moving the cursor to a new line.

        ### Returns:
            str: The ANSI escape sequence to clear the previous line.
        """
        return '\033[F\033[K'

    @property
    def clear(self) -> str:
        """Returns an ANSI escape sequence to clear the screen.

        This escape sequence removes all text from the screen and repositions the cursor to the top-left corner of the screen.

        ### Returns:
            str: The ANSI escape sequence to clear the screen.
        """
        return '\033[1J'

    def _register_cleanup_callback(self) -> None:
        """Internal method to be registered with atexit for cleanup."""
        print(self.reset_all, end='')

    def register_cleanup(self) -> None:
        """Registers a function to reset formatting upon program termination, if not already registered.

        This method registers a callback function to reset the console formatting to its default state 
        using ANSI escape codes when the program exits. The callback function is only registered once 
        to avoid redundant cleanup operations.

        ### Returns:
            None
        """
        if not self._cleanup_registered:
            atexit.register(self._register_cleanup_callback)
            self._cleanup_registered = True

if __name__ == '__main__':
    esc = Esc()
    esc.register_cleanup()

    print(esc.fg_red, end='')
    print(esc.bg_blue, end='')
    print(esc.bold, end='')
    print('Lorem impsum')
    print(esc.reset_intensity, end='')
    print(esc.fg_reset, end='')
    print(esc.bg_reset, end='')
    print('Lorem impsum')