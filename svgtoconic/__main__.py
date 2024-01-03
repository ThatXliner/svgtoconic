from xml.dom.minidom import parse
from pathlib import Path
import re


def get_all_control_points(path_d):
    """Extracts control points for all path types in an SVG path's d attribute.

    Args:
        path_d (str): The d attribute of an SVG path element.

    Returns:
        list: A list of control points, where each control point
            is a tuple of (x, y) values. Additionally, each entry includes:
                - type: String indicating the path command type (e.g., "M", "C", "L").
                - data: List of additional data specific to the command (e.g., [radius] for arcs).
    """

    control_points = []

    # Define regex patterns for different path commands and their control points:
    regex_patterns = {
        "M": r"M\s*([\d.,]*)(?=[^\d])",  # Moveto: single (x, y) pair
        "L": r"L\s*([\d.,]*)(?=[^\d])",  # Lineto: single (x, y) pair
        "C": r"(?i)C\s*([\d.,]*)(?=[^\d])",  # Cubic Bézier: multiple (x, y) pairs
        "Q": r"(?i)Q\s*([\d.,]*)(?=[^\d])",  # Quadratic Bézier: multiple (x, y) pairs
        "A": r"(?i)A\s*([\d.,]*)(?=[^\d])",  # Elliptical arc: radius, rotation, flags, start/end angles
        "Z": r"Z",  # Close path: no explicit control points
    }

    for command_type, pattern in regex_patterns.items():
        if command_type == "Z":
            continue  # No control points for close path
        for match in re.finditer(pattern, path_d):
            data = match.group(1).split(",")  # Extract data based on command type
            print(command_type, data)
            coordinates = [
                float(coord) for coord in data
            ]  # Convert coordinates to floats

            # Depending on the command type, extract relevant control points and information:
            if command_type == "M" or command_type == "L":
                control_points.append(
                    {
                        "type": command_type,
                        "data": [],
                        "points": [(coordinates[0], coordinates[1])],
                    }
                )
            elif command_type == "C":
                control_points.append(
                    {
                        "type": command_type,
                        "data": [],
                        "points": [
                            (coordinates[i], coordinates[i + 1])
                            for i in range(0, len(coordinates), 2)
                        ],
                    }
                )
            elif command_type == "Q":
                control_points.append(
                    {
                        "type": command_type,
                        "data": [],
                        "points": [(coordinates[0], coordinates[1])],
                    }
                )
            elif command_type == "A":
                # Add specific arc data
                control_points.append(
                    {
                        "type": command_type,
                        "data": data[
                            :6
                        ],  # Extract radius, rotation, flags, start/end angles
                        "points": [],  # Arcs don't have direct control points
                    }
                )
            elif command_type == "Z":
                pass  # No control points for close path

    return control_points


# def get_svg_commands(svg_file: str):
#     return re.search(r'd="(.+?)"', svg_file).group(1)


if __name__ == "__main__":
    dom = parse("test.svg")
    for node in dom.getElementsByTagName("path"):
        print(node.getAttribute("d"))
        output = []
        for x in get_all_control_points(node.getAttribute("d")):
            output.extend(x["points"])
        print(output)
        print()
        print(" ".join(map(lambda x: " ".join(map(lambda y: str(y * 3), x)), output)))
