from pydantic import BaseModel, Field
from pydantic import field_validator, model_validator
from typing import Any


class MazeConfig(BaseModel):
    """
    Configuration model for the maze generator.

    Attributes:
        width (int): Width of the maze (must be >= 1).
        height (int): Height of the maze (must be >= 1).
        entry (tuple[int, int]): Entry coordinates (row, col).
        exit (tuple[int, int]): Exit coordinates (row, col).
        output_file (str): Output file path for the maze.
        perfect (bool): If True, generates a perfect maze (no loops).
        seed (int | None): Random seed for reproducible generation.
    """

    width: int = Field(..., ge=1)
    height: int = Field(..., ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(..., min_length=1)
    perfect: bool
    seed: int | None = None

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> tuple[int, int]:
        """
        Parse coordinate input from string or tuple into a tuple of integers.

        Args:
            value (Any): Input value representing coordinates.

        Returns:
            tuple[int, int]: Parsed (x, y) coordinates.

        Raises:
            ValueError: If format is invalid or values are not integers.
        """
        if value is None or value == "":
            raise ValueError("You entered no coordinates")

        if isinstance(value, tuple):
            return value

        if not isinstance(value, str):
            raise ValueError("The value needs to be a str")

        splited = value.split(",")
        if len(splited) != 2:
            raise ValueError("Wrong format of exit and entry coordinates")

        try:
            return (int(splited[0].strip()), int(splited[1].strip()))
        except ValueError:
            raise ValueError("Coordinates must contain integers only")

    @model_validator(mode="after")
    def valid_input(self) -> "MazeConfig":
        """
        Validate maze configuration consistency.

        Ensures:
            - Entry and exit are not the same.
            - Entry and exit are within maze bounds.

        Returns:
            MazeConfig: The validated configuration object.

        Raises:
            ValueError: If constraints are violated.
        """
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")

        nx, ny = self.entry
        ex, ey = self.exit

        if not (0 <= nx < self.width and 0 <= ny < self.height):
            raise ValueError("entry out of bounds")

        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("exit out of bounds")

        return self


def normalize_config(raw: dict[str, str]) -> dict[str, Any]:
    """
    Convert raw configuration dictionary from file into typed values.

    Args:
        raw (dict[str, str]): Raw key-value pairs from config file.

    Returns:
        dict[str, Any]: Normalized configuration with correct types.
    """

    def parse_bool(v: str) -> bool:
        """
        Convert string boolean to Python boolean.

        Args:
            v (str): String representation of boolean ("True" or "False").

        Returns:
            bool: Parsed boolean value.

        Raises:
            ValueError: If value is not valid boolean string.
        """
        if v == "True":
            return True
        if v == "False":
            return False
        raise ValueError(f"Invalid boolean: {v}")

    return {
        "width": int(raw["WIDTH"]),
        "height": int(raw["HEIGHT"]),
        "entry": raw["ENTRY"],
        "exit": raw["EXIT"],
        "output_file": raw["OUTPUT_FILE"],
        "perfect": parse_bool(raw["PERFECT"]),
        "seed": int(raw["SEED"]) if "SEED" in raw else None
    }


def parsing_config_file(path: str) -> dict[str, str]:
    """
    Parse a configuration file into a dictionary.

    Args:
        path (str): Path to configuration file.

    Returns:
        dict[str, str]: Raw key-value pairs from file.

    Raises:
        ValueError: If file format is invalid or duplicate keys exist.
        OSError: If file cannot be opened.
    """
    config: dict[str, str] = {}

    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError("Invalid way of assigning a key, value")

                key, value = line.split("=", 1)

                if key in config:
                    raise ValueError(f"Duplicates are not allowed {key}")

                config[key] = value

    except OSError:
        raise OSError("Problem with the file")

    return config


def load_config(path: str) -> MazeConfig:
    """
    Load and validate maze configuration from file.

    Args:
        path (str): Path to configuration file.

    Returns:
        MazeConfig: Fully validated configuration object.
    """
    raw = parsing_config_file(path)
    normalized = normalize_config(raw)
    return MazeConfig(**normalized)


if __name__ == "__main__":
    import sys

    try:
        config = load_config(sys.argv[1])
        print(config)

    except Exception as e:
        print(f"[CONFIG ERROR] {e}")
        exit(1)
