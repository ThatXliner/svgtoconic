from svgpathtools import *
from typing import Iterator
from sympy import *


def convert_paths(paths: list[Path]) -> Iterator[Path]:
    for path in paths:
        for seg in path:
            if isinstance(seg, CubicBezier):
                for item in cubicIntoQuadratics(seg):
                    yield item
        else:
            # TODO: Handle other types of segments
            yield seg


def cubicIntoQuadratics(cubic: CubicBezier) -> Iterator[QuadraticBezier]:
    """I don't know how this works but it does"""

    def midPointApprox(cubic: CubicBezier) -> QuadraticBezier:
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
        yield midPointApprox(cubic)
    elif tdiv >= 0.5:
        cubicSplit = splitCubic(cubic, tdiv)
        yield midPointApprox(cubicSplit[0])
        yield midPointApprox(cubicSplit[1])
    else:
        cubicSplit = splitCubic(cubic, tdiv)
        yield midPointApprox(cubicSplit[0])
        for item in cubicIntoQuadratics(cubicSplit[1]):
            yield item


def evalCubic(cubic: CubicBezier, t: float) -> float:
    """Evaluates the cubic Bezier at the given t."""
    return (
        ((1 - t) ** 3) * cubic.start
        + 3 * ((1 - t) ** 2) * t * cubic.control1
        + 3 * (1 - t) * (t**2) * cubic.control2
        + (t**3) * cubic.end
    )


def splitCubic(cubic: CubicBezier, t: float) -> tuple[CubicBezier, CubicBezier]:
    """splits the cubic at the given t, using De Casteljau's"""
    splitPoint = evalCubic(cubic, t)
    secondPoints = [
        cubic.start + t * (cubic.control1 - cubic.start),
        cubic.control1 + t * (cubic.control2 - cubic.control1),
        cubic.control2 + t * (cubic.end - cubic.control2),
    ]
    thirdPoints = [
        secondPoints[0] + t * (secondPoints[1] - secondPoints[0]),
        secondPoints[1] + t * (secondPoints[2] - secondPoints[1]),
    ]
    return (
        CubicBezier(cubic.start, secondPoints[0], thirdPoints[0], splitPoint),
        CubicBezier(splitPoint, thirdPoints[1], secondPoints[2], cubic.end),
    )


# Opens the SVG in a new browser window
if __name__ == "__main__":
    paths, _attribs = svg2paths("test.svg")
    newPath = Path()
    for path in convert_paths(paths):
        newPath.append(path)
    disvg(newPath)
    constant = Matrix([Symbol('x'), Symbol('y'), 1])
    for quadratic in newPath:
        continue
        a, b, c = quadratic.start, quadratic.control, quadratic.end
        u = Matrix([b.imag - c.imag, c.real - b.real, b.real * c.imag - b.imag - c.real])
        v = Matrix([c.imag - a.imag, a.real - c.real, c.real * a.imag - c.imag * a.real])
        w = Matrix([a.imag - b.imag, b.real - a.real, a.real * b.imag - a.imag * b.real])
        q = 2 * (u * w.T  + w * u.T) - v * v.T
        print(simplify((constant.T * q * constant)[0]))
