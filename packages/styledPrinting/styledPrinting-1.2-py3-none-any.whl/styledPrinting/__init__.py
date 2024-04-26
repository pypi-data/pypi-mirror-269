class Color:
    @staticmethod
    def black(text: str) -> str:
        """Returns the text in black color

        Args:
            text (str): The text to be in black color

        Returns:
            str: The text in black color
        """
        return f"\033[30m{text}\033[0m"

    @staticmethod
    def red(text: str) -> str:
        """Returns the text in red color

        Args:
            text (str): The text to be in red color

        Returns:
            str: The text in red color
        """
        return f"\033[31m{text}\033[0m"

    @staticmethod
    def green(text: str) -> str:
        """Returns the text in green color

        Args:
            text (str): The text to be in green color

        Returns:
            str: The text in green color
        """
        return f"\033[32m{text}\033[0m"

    @staticmethod
    def yellow(text: str) -> str:
        """Returns the text in yellow color

        Args:
            text (str): The text to be in yellow color

        Returns:
            str: The text in yellow color
        """
        return f"\033[33m{text}\033[0m"

    @staticmethod
    def blue(text: str) -> str:
        """Returns the text in blue color

        Args:
            text (str): The text to be in blue color

        Returns:
            str: The text in blue color
        """
        return f"\033[34m{text}\033[0m"

    @staticmethod
    def purple(text: str) -> str:
        """Returns the text in purple color

        Args:
            text (str): The text to be in purple color

        Returns:
            str: The text in purple color
        """
        return f"\033[35m{text}\033[0m"

    @staticmethod
    def cyan(text: str) -> str:
        """Returns the text in cyan color

        Args:
            text (str): The text to be in cyan color

        Returns:
            str: The text in cyan color
        """
        return f"\033[36m{text}\033[0m"

    @staticmethod
    def white(text: str) -> str:
        """Returns the text in white color

        Args:
            text (str): The text to be in white color

        Returns:
            str: The text in white color
        """
        return f"\033[37m{text}\033[0m"


class Background:
    @staticmethod
    def red(text: str) -> str:
        """Returns the text with red background

        Args:
            text (str): The text to have red background

        Returns:
            str: The text with red background
        """
        return f"\033[41m{text}\033[0m"

    @staticmethod
    def green(text: str) -> str:
        """Returns the text with green background

        Args:
            text (str): The text to have green background

        Returns:
            str: The text with green background
        """
        return f"\033[42m{text}\033[0m"

    @staticmethod
    def yellow(text: str) -> str:
        """Returns the text with yellow background

        Args:
            text (str): The text to have yellow background

        Returns:
            str: The text with yellow background
        """
        return f"\033[43m{text}\033[0m"

    @staticmethod
    def blue(text: str) -> str:
        """Returns the text with blue background

        Args:
            text (str): The text to have blue background

        Returns:
            str: The text with blue background
        """
        return f"\033[44m{text}\033[0m"

    @staticmethod
    def purple(text: str) -> str:
        """Returns the text with purple background

        Args:
            text (str): The text to have purple background

        Returns:
            str: The text with purple background
        """
        return f"\033[45m{text}\033[0m"

    @staticmethod
    def cyan(text: str) -> str:
        """Returns the text with cyan background

        Args:
            text (str): The text to have cyan background

        Returns:
            str: The text with cyan background
        """
        return f"\033[46m{text}\033[0m"

    @staticmethod
    def white(text: str) -> str:
        """Returns the text with white background

        Args:
            text (str): The text to have white background

        Returns:
            str: The text with white background
        """
        return f"\033[47m{text}\033[0m"


class Style:
    @staticmethod
    def bold(text: str) -> str:
        """Returns the text in bold

        Args:
            text (str): The text to make bold

        Returns:
            str: The text in bold
        """
        return f"\033[1m{text}\033[0m"

    @staticmethod
    def underline(text: str) -> str:
        """Returns the text underlined

        Args:
            text (str): The text to underline

        Returns:
            str: The text underlined
        """
        return f"\033[4m{text}\033[0m"

    @staticmethod
    def blink(text: str) -> str:
        """Returns the text blinking

        Args:
            text (str): The text to blink

        Returns:
            str: The text blinking
        """
        return f"\033[5m{text}\033[0m"

    @staticmethod
    def inverted(text: str) -> str:
        """Returns the text inverted

        Args:
            text (str): The text to invert

        Returns:
            str: The text inverted
        """
        return f"\033[7m{text}\033[0m"

    @staticmethod
    def concealed(text: str) -> str:
        """Returns the text concealed

        Args:
            text (str): The text to conceal

        Returns:
            str: The text concealed
        """
        return f"\033[8m{text}\033[0m"

    @staticmethod
    def strike(text: str) -> str:
        """Returns the text striked

        Args:
            text (str): The text to strike

        Returns:
            str: The text striked
        """
        return f"\033[9m{text}\033[0m"


class Cursor:
    @staticmethod
    def moveUp(times: int = 1) -> None:
        """Moves the cursor up X lines

        Args:
            times (int, optional): The number of lines to move up. Defaults to 1.
        """
        print(f"\033[{times}A", end="")

    @staticmethod
    def moveDown(times: int = 1) -> None:
        """Moves the cursor down X lines

        Args:
            times (int, optional): The number of lines to move down. Defaults to 1.
        """
        print(f"\033[{times}B", end="")

    @staticmethod
    def moveLineStart() -> None:
        """Moves the cursor to the start of the line"""
        print("\033[1G", end="")

    @staticmethod
    def moveLineEnd() -> None:
        """Moves the cursor to the end of the line"""
        print("\033[K", end="")

    @staticmethod
    def moveLeft(times: int = 1) -> None:
        """Moves the cursor left X times

        Args:
            times (int, optional): The number of times to move left. Defaults to 1.
        """
        print(f"\033[{times}D", end="")

    @staticmethod
    def moveRight(times: int = 1) -> None:
        """Moves the cursor right X times

        Args:
            times (int, optional): The number of times to move right. Defaults to 1.
        """
        print(f"\033[{times}C", end="")

    @staticmethod
    def clearLine() -> None:
        """Clears the current line"""
        print("\033[2K", end="")

    @staticmethod
    def clearScreen() -> None:
        """Clears the screen"""
        print("\033[2J", end="")

    @staticmethod
    def saveCursorPosition() -> None:
        """Saves the current cursor position"""
        print("\033[s", end="")

    @staticmethod
    def restoreCursorPosition() -> None:
        """Restores the saved cursor position"""
        print("\033[u", end="")

    @staticmethod
    def hideCursor() -> None:
        """Hides the cursor"""
        print("\033[?25l", end="")

    @staticmethod
    def showCursor() -> None:
        """Shows the cursor"""
        print("\033[?25h", end="")

    @staticmethod
    def move(x: int = 0, y: int = 0, relative: bool = False) -> None:
        """Moves the cursor to the position x, y

        Args:
            x (int, optional): The x position. Defaults to 0.
            y (int, optional): The y position. Defaults to 0.
            relative (bool, optional): If the position is relative to the current position. Defaults to False.

        Usage:
        ```python
        Cursor.move(3, 4) # Move the cursor to the position 3, 4

        Cursor.move(3, 4, relative=True) # Move the cursor 3 to the right and 4 down, so the cursor will be at 6, 8; Given that the cursor is at 3, 4
        ```
        """
        if relative:
            if x > 0:
                print(f"\033[{x}C", end="")
            elif x < 0:
                print(f"\033[{abs(x)}D", end="")
            if y > 0:
                print(f"\033[{y}B", end="")
            elif y < 0:
                print(f"\033[{abs(y)}A", end="")
        else:
            print(f"\033[{y};{x}H", end="")


class Prefix:
    @staticmethod
    def info() -> str:
        """Returns the INFO prefix

        Returns:
            str: The INFO prefix
        """
        return f"[{Color.blue(' INFO ')}]"

    @staticmethod
    def ok() -> str:
        """Returns the OK prefix

        Returns:
            str: The OK prefix
        """
        return f"[{Color.green('  OK  ')}]"

    @staticmethod
    def warn() -> str:
        """Returns the WARN prefix

        Returns:
            str: The WARN prefix
        """
        return f"[{Color.yellow(' WARN ')}"

    @staticmethod
    def fail() -> str:
        """Returns the FAIL prefix

        Returns:
            str: The FAIL prefix
        """
        return f"[{Color.red(' FAIL ')}]"
