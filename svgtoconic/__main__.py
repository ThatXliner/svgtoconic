from svgpathtools import *
paths, attribs = svg2paths('test.svg')

def cubicIntoQuadratics(cubic):
    prec = 0.1
    tdiv = (prec) / ((3 ** 0.5 / 18) * abs(cubic.end - 3 * cubic.control2 + 3 * cubic.control1 - cubic.start) * 0.5)
    tdiv = tdiv ** (1/3)
    if (tdiv >= 1):
        return (midPointApprox(cubic), )
    elif (tdiv >= 0.5):
        cubicSplit = splitCubic(cubic, tdiv)
        return (midPointApprox(cubicSplit[0]), midPointApprox(cubicSplit[1]))
    else:
        return (midPointApprox(cubicSplit[0]), cubicIntoQuadratics(cubicSplit[1]))
def midPointApprox(cubic): # approximates the cubic into the control point for a quadratic
    return QuadraticBezier(cubic.start, (3 * (cubic.control1 + cubic.control2) - (cubic.start + cubic.end)) / 4, cubic.end)
def evalCubic(cubic, t): # evals the cubic at the given t
    return ((1 - t) ** 3) * cubic.start + 3 * ((1 - t) ** 2) * t * cubic.control1 + 3 * (1 - t) * (t ** 2) * cubic.control2 + (t ** 3) * cubic.end
def splitCubic(cubic, t): # splits the cubic at the given t, using De Casteljau's
    splitPoint = evalCubic(cubic, t)
    secondPoints = [
        cubic.start + 0.25 * (cubic.control1 - cubic.start),
        cubic.control1 + 0.25 * (cubic.control2 - cubic.control1),
        cubic.control2 + 0.25 * (cubic.end - cubic.control2)
    ]
    thirdPoints = [
        secondPoints[0] + 0.25 * (secondPoints[1] - secondPoints[0]),
        secondPoints[1] + 0.25 * (secondPoints[2] - secondPoints[1]),
    ]
    return (CubicBezier(cubic.start, secondPoints[0], thirdPoints[0], splitPoint),
            CubicBezier(splitPoint, thirdPoints[1], secondPoints[2], cubic.end))
newPath = Path()
for path, attrib in zip(paths, attribs):
    for seg in path:
        if isinstance(seg, CubicBezier):
            for item in cubicIntoQuadratics(seg):
                # https://stackoverflow.com/questions/2009160/how-do-i-convert-the-2-control-points-of-a-cubic-curve-to-the-single-control-poi/14514491
                newPath.append(item)
disvg(newPath)
