from typing import Any


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    def __init__(self, message: str):
        super().__init__(message)


def semantic_analyze(result: dict[str, Any]) -> None:
    # ALlowed keys
    valid_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT",
                  "OUTPUT_FILE", "PERFECT", "SEED"]

    # Check for missing or invalid keys
    for key in valid_keys:
        if key not in result.keys() and key != "SEED":
            raise ConfigError(f"Missing key: {key}")
    for key in result.keys():
        if key not in valid_keys:
            raise ConfigError(f"Invalid key: {key}")

    # Width and Height
    try:
        width = int(result["WIDTH"])
    except ValueError:
        raise ConfigError(f"Invalid value for WIDTH: {result['WIDTH']}")
    if width <= 0:
        raise ConfigError(f"Invalid value for WIDTH: {result['WIDTH']}")

    try:
        height = int(result["HEIGHT"])
    except ValueError:
        raise ConfigError(f"Invalid value for HEIGHT: {result['HEIGHT']}")
    if height <= 0:
        raise ConfigError(f"Invalid value for HEIGHT: {result['HEIGHT']}")

    # Entry and Exit
    if ',' not in result["ENTRY"] or result["ENTRY"].count(',') != 1:
        raise ConfigError(f"Invalid value for ENTRY: {result['ENTRY']}")

    if ',' not in result["EXIT"] or result["EXIT"].count(',') != 1:
        raise ConfigError(f"Invalid value for EXIT: {result['EXIT']}")

    w_entry, h_entry = result["ENTRY"].split(',')
    w_exit, h_exit = result["EXIT"].split(',')
    try:
        w_entry = int(w_entry)
        h_entry = int(h_entry)
    except ValueError:
        raise ConfigError(f"Invalid value for ENTRY: {result['ENTRY']}")
    if w_entry < 0 or w_entry >= width or h_entry < 0 or h_entry >= height:
        raise ConfigError(f"Invalid value for ENTRY: {result['ENTRY']}")

    try:
        w_exit = int(w_exit)
        h_exit = int(h_exit)
    except ValueError:
        raise ConfigError(f"Invalid value for EXIT: {result['EXIT']}")
    if w_exit < 0 or w_exit >= width or h_exit < 0 or h_exit >= height:
        raise ConfigError(f"Invalid value for EXIT: {result['EXIT']}")

    # Perfect
    if result["PERFECT"] not in ["True", "False"]:
        raise ConfigError(f"Invalid value for PERFECT: {result['PERFECT']}")


def sintax_validation_parse(file_content: str) -> dict[str, Any]:
    lines = file_content.splitlines()
    result: dict[str, Any] = {}

    # Parse each line and validate syntax
    for line in lines:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        if '=' not in line or line.count('=') != 1:
            raise ConfigError(f"Invalid line: {line}")
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ConfigError(f"Invalid line: {line}")
        result[key] = value

    # Semantic analysis
    semantic_analyze(result)

    # After semantic analysis, convert values to appropriate types
    result["WIDTH"] = int(result["WIDTH"])
    result["HEIGHT"] = int(result["HEIGHT"])
    if result["PERFECT"] == "True":
        result["PERFECT"] = True
    else:
        result["PERFECT"] = False
    if "SEED" in result:
        result["SEED"] = int(result["SEED"])

    return result
