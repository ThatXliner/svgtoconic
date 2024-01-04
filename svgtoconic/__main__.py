from svgpathtools import *
from typing import Iterator
from sympy import *


def convert_paths(paths: list[Path]) -> Iterator[Path]:
    for path in paths:
        for seg in path:
            if isinstance(seg, CubicBezier):
                for item in cubic2quadratic(seg):
                    yield item
            else:
                # TODO: Handle other types of segments
                yield seg


def cubic2quadratic(cubic: CubicBezier) -> Iterator[QuadraticBezier]:
    """I don't know how this works but it does"""

    def helper(cubic: CubicBezier) -> QuadraticBezier:
        """approximates the cubic Bezier into the control point for a quadratic"""
        return QuadraticBezier(
            cubic.start,
            (3 * (cubic.control1 + cubic.control2) - (cubic.start + cubic.end)) / 4,
            cubic.end,
        )

    prec = 0.1
    tdiv = (prec) / (
        (3**0.5 / 18)
        * abs(cubic.end - 3 * cubic.control2 + 3 * cubic.control1 - cubic.start)
        * 0.5
    )
    tdiv = tdiv ** (1 / 3)
    if tdiv >= 1:
        yield helper(cubic)
    elif tdiv >= 0.5:
        cubicSplit = split_cubic(cubic, tdiv)
        yield helper(cubicSplit[0])
        yield helper(cubicSplit[1])
    else:
        cubicSplit = split_cubic(cubic, tdiv)
        yield helper(cubicSplit[0])
        for item in cubic2quadratic(cubicSplit[1]):
            yield item


def eval_cubic_bezier(cubic: CubicBezier, t: float) -> float:
    """Evaluates the cubic Bezier at the given t."""
    return (
        ((1 - t) ** 3) * cubic.start
        + 3 * ((1 - t) ** 2) * t * cubic.control1
        + 3 * (1 - t) * (t**2) * cubic.control2
        + (t**3) * cubic.end
    )


def split_cubic(cubic: CubicBezier, t: float) -> tuple[CubicBezier, CubicBezier]:
    """splits the cubic at the given t, using De Casteljau's"""
    split_point = eval_cubic_bezier(cubic, t)
    second_points = [
        cubic.start + t * (cubic.control1 - cubic.start),
        cubic.control1 + t * (cubic.control2 - cubic.control1),
        cubic.control2 + t * (cubic.end - cubic.control2),
    ]
    third_points = [
        second_points[0] + t * (second_points[1] - second_points[0]),
        second_points[1] + t * (second_points[2] - second_points[1]),
    ]
    return (
        CubicBezier(cubic.start, second_points[0], third_points[0], split_point),
        CubicBezier(split_point, third_points[1], second_points[2], cubic.end),
    )


# Opens the SVG in a new browser window
if __name__ == "__main__":
    paths, _attribs = svg2paths("goomba.svg")
    new_path = Path()
    for path in convert_paths(paths):
        new_path.append(path)
    disvg(new_path)
    constant = Matrix([Symbol("x"), Symbol("y"), 1])
    for quadratic in new_path:
        continue
        a, b, c = quadratic.start, quadratic.control, quadratic.end
        u = Matrix(
            [b.imag - c.imag, c.real - b.real, b.real * c.imag - b.imag - c.real]
        )
        v = Matrix(
            [c.imag - a.imag, a.real - c.real, c.real * a.imag - c.imag * a.real]
        )
        w = Matrix(
            [a.imag - b.imag, b.real - a.real, a.real * b.imag - a.imag * b.real]
        )
        q = 2 * (u * w.T + w * u.T) - v * v.T
        print(simplify((constant.T * q * constant)[0]))
