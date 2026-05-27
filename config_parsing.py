from pydantic import BaseModel, Field
from pydantic import field_validator, model_validator
from typing import Any

class MazeConfig(BaseModel):
    width: int = Field(...,ge=1)
    height: int = Field(...,ge=1)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(...,min_length=1)
    perfect: bool

    @field_validator("entry", "exit", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> tuple[int, int]: 
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
            return(int(splited[0].strip()), int(splited[1].strip()))
        except ValueError:
            raise ValueError("Coordinates must contain integers only")
        

    @model_validator(mode="after")
    def valid_input(self) -> "MazeConfig":
        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")
        nx,ny = self.entry
        ex,ey = self.exit

        if not (0 <= nx < self.width and 0 <= ny < self.height):
            raise ValueError("entry out of bounds")
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("exit out of bounds")
            
        return self
    
def normalize_config(raw: dict) -> dict:
    def parse_bool(v: str) -> bool:
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
    }
#parsing the file
def parsing_config_file(path: str) -> dict:
    config: dict = {}
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if not "=" in line:
                    raise ValueError("Invalid way of assiging a key, value")

                key, value = line.split("=", 1)
                config[key] = value
    except OSError:
        raise OSError("Problem with the file")
    return config

def load_config(path: str) -> MazeConfig:
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