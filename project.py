from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys
import math
from math import *
import numpy as np


def evalFnX(val):
    return -c2[0] + val*sc


def evalFnY(val):
    return -c2[1] + val*sc


scale = 1
sc = 1
TranslateFlag = 0
zoomLevel = 0

x_min, x_max = -17, 17
y_min, y_max = -10, 10
y_diff = 10
x_diff = 17

c1 = [0, 0]
c2 = [0, 0]
oldCenter = [0, 0]

xAxisLimits = [c2[0]-x_diff*scale, -c2[0] + x_diff*scale]
yAxisLimits = [c2[1]-y_diff*scale, -c2[1] + y_diff*scale]
print(xAxisLimits, yAxisLimits)

mposX = 0
mposY = 0
mosX, mosY = 0, 0

darkgrey = [0.4, 0.4, 0.4]
red = [1.0, 0.0, 0.0]
green = [0.0, 1.0, 0.0]
blue = [0.0, 0.0, 1.0]
cyan = [0.0, 1.0, 1.0]
magenta = [1.0, 0.0, 1.0]
yellow = [1.0, 1.0, 0.0]
white = [1.0, 1.0, 1.0]
black = [0.0, 0.0, 0.0]
darkred = [0.5, 0.0, 0.0]
darkgreen = [0.0, 0.5, 0.0]
darkblue = [0.0, 0.0, 0.5]
darkcyan = [0.0, 0.5, 0.5]
darkmagenta = [0.5, 0.0, 0.5]
darkyellow = [0.5, 0.5, 0.0]
lightgrey = [0.8, 0.8, 0.8]
print("global")

mousePosString = ""

plotPointsList = []

linesList = []
linesListFlag = 0
circlesList = []
dynamicCircle = dict()
polygonsList = []
polygonsListFlag = 0
parabolasList = []
ellipseList = []
hyperbolaList = []
InstructionSet = []
dynamicCircleFlag = 0

zoomFlag = 0
temp = c2

mouseState = 0
keyboardinputflag = 0
inputString = ""
transInput = ""
drawFlag = 0
_error = ""

errorCodes = {
    400: "Entered invalid input",
    404: "Not Found"
}


def display_error(code):
    global _error
    _error = errorCodes[code]


def trans(p):
    global c2, FuncX, FuncY
    print(p, type(p))
    try:
        if type(p) == type(""):
            x, y = map(int, p.split())
        else:
            x, y = p[0], p[1]
        c2 = [x, y]
    except:
        display_error(400)


def strToPoint(s):
    return list(map(int, s.split()))


def drawFromStr(string):
    global parabolasList, linesList, circlesList, ellipseList, hyperbolaList
    l = list(string.split("|"))
    if l[0].lower().strip() == "parabola":
        try:
            cen, a = l[1], l[2]
            try:
                limX = l[3]
            except:
                limX = 30
            try:
                color = list(map(float, l[4][1:-1].split(",")))
            except:
                color = darkcyan
            try:
                siz = l[5]
            except:
                siz = 4
            if type(cen) == type(""):
                cen = strToPoint(cen)
                InstructionSet.append(
                    ["parabola", cen, float(a), float(limX), color, int(siz)])

                # parabolasList.append([cen, float(a), float(limX), color, int(siz)])
        except:
            display_error(400)
    if l[0].lower().strip() == "line":
        try:
            # drawLine(p1,p2,color,size=siz)
            p1, p2 = l[1], l[2]
            if type(p1) == type(""):
                p1 = strToPoint(p1)
            if type(p2) == type(""):
                p2 = strToPoint(p2)
            try:
                color = list(map(float, l[3][1:-1].split(",")))
            except:
                color = darkcyan
            try:
                siz = int(l[4])
            except:
                siz = 4
            InstructionSet.append(["line", p1, p2, color, siz])
            # linesList.append([p1, p2, color, siz])
        except:
            display_error(400)
    if l[0].lower().strip() == "circle":
        try:
            # def drawCircle(c, radius, color=[0, 0, 0]):
            cen, r = l[1], l[2]
            d = dict()
            if type(cen) == type(""):
                cen = strToPoint(cen)
            try:
                color = list(map(float, l[3][1:-1].split(",")))
            except:
                color = darkred
            # circlesList.append([cen, float(r), color])
            InstructionSet.append(["circle", cen, float(r), color])
            d["c"] = cen
            d["r"] = r
        except:
            display_error(400)
    if l[0].lower().strip() == "ellipse":
        try:
            # def drawEllipseGeneral(center, xL, yL, color):
            cen, xL, yL = l[1], float(l[2]), float(l[3])
            if type(cen) == type(""):
                cen = strToPoint(cen)
            try:
                color = list(map(float, l[4][1:-1].split(",")))
            except:
                color = darkgreen
            # ellipseList.append([cen, xL, yL, color])
            InstructionSet.append(["ellipse", cen, xL, yL, color])
        except:
            display_error(400)
    if l[0].lower().strip() == "hyperbola":
        try:
            # def drawHyperbolaMidPoint(c, a, b, limitX, color=[0, 0, 0]):
            cen, a, b = l[1], float(l[2]), float(l[3])
            try:
                limitX = float(l[4])
            except:
                limitX = 30
            if type(cen) == type(""):
                cen = strToPoint(cen)
            try:
                color = list(map(float, l[5][1:-1].split(",")))
            except:
                color = darkmagenta
            # hyperbolaList.append([cen, a, b, limitX, color])
            InstructionSet.append(["hyperbola", cen, xL, yL, color])

        except:
            display_error(400)


def drawHyperbola(c, a, b, limitX=30, color=[0, 0, 0]):
    x0, y0 = c[0], c[1]
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    p = (((a+0.5)**2)/(a*a)) - (1/(b*b)) - 1
    x = a
    y = 0
    while x <= (a*a) / (((a*a)-(b*b))**0.5):
        if p <= 0:
            p += (2*x / (a*a))
            x += 1
        p -= (1+2*y)/(b*b)
        y += 1
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 + y))
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 - y))
        glVertex2f(evalFnX(x0 - x), evalFnY(y0 - y))
        glVertex2f(evalFnX(x0 - x), evalFnY(y0 + y))
        if x >= limitX:
            break
    p = (((x+1)**2)/(a*a)) - (((y+0.25)**2)/(b*b)) - 1
    while x < limitX:
        if p >= 0:
            y += 1
            p -= (2*y)/(b*b)
        x += 1
        p += (2*x + 1)/(a*a)
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 + y))
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 - y))
        glVertex2f(evalFnX(x0 - x), evalFnY(y0 - y))
        glVertex2f(evalFnX(x0 - x), evalFnY(y0 + y))
    glEnd()


def drawEllipse(center, rx, ry, color):
    output = []
    if rx < 0 or ry < 0:
        print("major or minor axis length cannot be negative")
        return 0
    xc, yc = center[0], center[1]
    x = 0
    y = ry
    d1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    while (dx < dy):
        glVertex2f(evalFnX(x+xc), evalFnY(y+yc))
        glVertex2f(evalFnX(-x+xc), evalFnY(y+yc))
        glVertex2f(evalFnX(x+xc), evalFnY(-y+yc))
        glVertex2f(evalFnX(-x+xc), evalFnY(-y+yc))
        if (d1 < 0):
            x += 1
            dx = dx + (2 * ry * ry)
            d1 = d1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)
    d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) +
          ((rx * rx) * ((y - 1) * (y - 1))) -
          (rx * rx * ry * ry))
    while (y >= 0):
        glVertex2f(evalFnX(x+xc), evalFnY(y+yc))
        glVertex2f(evalFnX(-x+xc), evalFnY(y+yc))
        glVertex2f(evalFnX(x+xc), evalFnY(-y+yc))
        glVertex2f(evalFnX(-x+xc), evalFnY(-y+yc))
        if (d2 > 0):
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)
    glEnd()
    return output


def Circle(center, radius, color=[0, 0, 0]):
    x, y = center[0], center[1]
    radius = abs(radius)
    vertices = []
    for i in range(0, 180):
        angle_theta = i
        vertices.append([evalFnX(x + radius * cos(radians(angle_theta))),
                        evalFnY(y + radius * sin(radians(angle_theta)))])
    return vertices


def keyboard(*args):
    ESCAPE = '\033'
    global c2, sc, TranslateFlag, hyperbolaList, linesList, ellipseList, circlesList, keyboardinputflag, drawFlag, inputString, transInput, oldCenter, temp, zoomFlag, zoomLevel, plotPointsList, polygonsList, parabolasList, InstructionSet
    if args[0] == b'\r':
        if TranslateFlag == 1:
            TranslateFlag = 0
            trans(inputString)
            inputString = ""
        elif drawFlag == 1:
            drawFlag = 0
            drawFromStr(inputString)
            inputString = ""
    elif TranslateFlag == 1:
        inputString += args[0].decode("utf-8")
    elif drawFlag == 1:
        inputString += args[0].decode("utf-8")
    elif args[0] == b'[':
        keyboardinputflag = 1
    elif args[0] == b']':
        inputString += "]"
        keyboardinputflag = 0
        inputString = ""
    elif keyboardinputflag:
        inputString += args[0].decode("utf-8")
    elif args[0] == b't' or args[0] == b'T':
        TranslateFlag = 1
        inputString = ""
    elif args[0] == b'd' or args[0] == b'D':
        inputString = ""
        drawFlag = 1
    elif args[0] == b'z' or args[0] == b'Z':
        if sc >= 1:
            sc += 1
        elif sc < 1:
            sc += 0.1
        zoomLevel -= 1
    elif args[0] == b'o' or args[0] == b'O':
        if sc > 1:
            sc -= 1
            zoomLevel += 1
        elif sc <= 1:
            if sc >= 0.2:
                sc -= 0.1
                zoomLevel += 1
    elif args[0] == b'r' or args[0] == b'R':
        InstructionSet = []
    elif args[0] == b'u' or args[0] == b'U':
        InstructionSet.pop()
    print(args)
    glutPostRedisplay()
    glutSwapBuffers()


def getPixel(x, y):
    pxcolor = glReadPixels(x, y, 1.0, 1.0, GL_RGB, GL_FLOAT)
    return list(np.frombuffer(pxcolor, np.float32))


def distBtw2Pts(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


def mouse(*args):
    global TranslateFlag, c2, mposX, mposY, mousePosString, mosX, mosY, mouseState
    if len(args) == 2:
        mposX = round((c2[0] + ((-17 + args[0] * (34/1535))/sc)), 2)
        mposY = round((c2[1] + ((10 - args[1] * (20/863))/sc)), 2)
        mosX = args[0]
        mosY = args[1]
    else:
        mposX = round((c2[0] + ((-17 + args[2] * (34/1535))/sc)), 2)
        mposY = round((c2[1] + ((10 - args[3] * (20/863))/sc)), 2)
        mouseState = args[1]
        mosX = args[2]
        mosY = args[3]
    mousePosString = str([mposX, mposY])
    glutPostRedisplay()
    glutSwapBuffers()
    print("mouse args", args)


def glut_print(x,  y,  font,  text, color=[1, 0, 0]):
    blending = False
    if glIsEnabled(GL_BLEND):
        blending = True
    # glEnable(GL_BLEND)
    glColor3f(color[0], color[1], color[2])
    glWindowPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ctypes.c_int(ord(ch)))
    if not blending:
        glDisable(GL_BLEND)


cent = [0, 0]
regularPolyFlag = 0
newPolygonPts = []


def GoMenu(value):
    global newPolygonPts, dynamicCircle, dynamicCircleFlag, cent, regularPolyFlag, InstructionSet
    if value == 1:
        InstructionSet.append(["point", mposX, mposY])
        # plotPointsList.append([mposX, mposY])
    elif value == 2:
        newPolygonPts.append([mposX, mposY])
    elif value == 3:
        InstructionSet.append(["poly"]+newPolygonPts)
        # polygonsList.append(newPolygonPts)
        newPolygonPts = []
    elif value == 4:
        cent = [mposX, mposY]
        dynamicCircleFlag = 1
    elif value == 6:
        glutDestroyWindow(glutGetWindow())
        exit()
    # if value !=6:
    glutPostRedisplay()


def detailsPrint():
    glut_print(10, 50, GLUT_BITMAP_TIMES_ROMAN_24,
               "Input :"+inputString, darkblue)
    # mosX+5, 805-mosY
    glut_print(10, 10, GLUT_BITMAP_TIMES_ROMAN_24, mousePosString, red)
    glut_print(1350, 810, GLUT_BITMAP_TIMES_ROMAN_24,
               "Center: (" + str(c2[0])+","+str(c2[1])+")", darkmagenta)
    glut_print(1350, 780, GLUT_BITMAP_TIMES_ROMAN_24,
               "Scale: "+str(sc), darkmagenta)
    glut_print(1350, 750, GLUT_BITMAP_TIMES_ROMAN_24,
               "Zoom level: "+str(zoomLevel), darkmagenta)
    glut_print(10, 780, GLUT_BITMAP_TIMES_ROMAN_24, _error, darkmagenta)


def draw():
    global c1, plotPointsList, zoomFlag, c2, dynamicCircleFlag, mouseState, dynamicCircle, cent, regularPolyFlag, InstructionSet
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(3)
    drawPlane()
    plotPoint([c2[0]*sc, c2[1]*sc], blue, 7)
    for instruct in InstructionSet:
        try:
            name = instruct[0].strip().lower()
            i = instruct[1:]
            if name == "parabola":
                drawParabolaMidPoint(i[0], i[1], i[2], i[3], i[4])
            elif name == "ellipse":
                drawEllipse(i[0], i[1], i[2], i[3])
            elif name == "hyperbola":
                drawHyperbola(i[0], i[1], i[2], i[3], i[4])
            elif name == "line":
                drawLine(i[0], i[1], i[2])
            elif name == "point":
                plotPoint(i, red)
            elif name == "poly":
                drawPolyWithPts(i, darkgreen)
            elif name == "circle":
                drawPolyWithPts(Circle(i[0], i[1], i[2]))
        except :
            pass
    if dynamicCircleFlag == 1:
        temp = Circle(cent, distBtw2Pts(cent, [mposX, mposY]), [0, 0, 0])
        drawPolyWithPts(temp, [0, 0, 0])
        if mouseState == 1:
            dynamicCircleFlag = 0
            mouseState = 0
            InstructionSet.append(
                ["circle", cent, distBtw2Pts(cent, [mposX, mposY]), [0, 0, 0]])
    detailsPrint()
    print("InstructionSet", InstructionSet)
    glFlush()


def DrawPoly(center, n, s, color=[0, 0, 0]):
    glPointSize(5)
    glColor3f(color[0], color[1], color[2])
    glTranslatef(evalFnX(center[0]), evalFnY(center[1]), 0)
    cx, cy = 0, 0
    sideAngle = 360/n
    sideAngleH = sideAngle/2
    sideAngleHRadians = math.radians(sideAngleH)
    bv1x = cx-s/2
    bv1y = cy - (s/2)*(1/math.tan(sideAngleHRadians))
    bv2x = cx+s/2
    bv2y = bv1y
    drawLine((bv1x, bv1y), (bv2x, bv2y), color)
    for i in range(n-1):
        glRotatef(sideAngle, 0, 0, 1)
        drawLine((bv1x, bv1y), (bv2x, bv2y), color)
    glRotatef(sideAngle, 0, 0, 1)
    glTranslatef(evalFnX(-center[0]), evalFnY(-center[1]), 0)


def drawPolyWithPts(l, color=[0, 0, 0]):
    for i in range(len(l)):
        drawLine(l[i-1], l[i], color, 4)


def plotPoint(p, color=[0, 0, 0], size=4):
    print("plotPoint", p)
    glPointSize(size)
    glBegin(GL_POINTS)
    glColor3f(color[0], color[1], color[2])
    glVertex2f(evalFnX(p[0]), evalFnY(p[1]))
    glEnd()


def drawPlane():
    for i in range(-17, 18):
        for j in range(-10, 11):
            for k in range(1, 5):
                drawCoLine((-i, j+0.2*k), (i, j+0.2*k), lightgrey, size=1)
                drawCoLine((i+0.2*k, -j), (i+0.2*k, j), lightgrey, size=1)
    for i in range(-17, 18):
        for j in range(-10, 11):
            drawCoLine((-i, j), (i, j), size=1)
            drawCoLine((i, -j), (i, j), size=1)
    centerX = evalFnX(c2[0])
    centerY = evalFnY(c2[1])
    print("centerXY", centerX, centerY)
    if zoomLevel == 0:
        z = 1
    else:
        z = zoomLevel
    drawLine([-20*abs(z)+centerX, 0], [centerX+20*abs(z), 0], darkblue, size=3)
    drawLine([0, centerY-15*abs(z)], [0, centerY+15*abs(z)], darkblue,  size=3)


def drawLine(p1, p2, color=[0, 0, 0], size=4):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    glColor3f(color[0], color[1], color[2])
    glLineWidth(size)
    glBegin(GL_LINES)
    glVertex2f(evalFnX(x1), evalFnY(y1))
    glVertex2f(evalFnX(x2), evalFnY(y2))
    glEnd()


def drawCoLine(p1, p2, color=[0, 0, 0], scale=1, size=2):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    glColor3f(color[0], color[1], color[2])
    glLineWidth(size)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def drawAxes(p1, p2, color=[0, 0, 0], scale=1, size=2):
    x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
    glColor3f(color[0], color[1], color[2])
    glLineWidth(size)
    glBegin(GL_LINES)
    glVertex2f(evalFnX(x1), evalFnY(y1))
    glVertex2f(evalFnX(x2), evalFnY(y2))
    glEnd()


def drawParabolaMidPoint(c, a, limitX, color=[0, 0, 0], size=4):
    x0, y0 = c[0], c[1]
    glColor3f(color[0], color[1], color[2])
    glPointSize(size)
    glBegin(GL_POINTS)
    p = 1 - 2*a
    x = 0
    y = 0
    while 2*a >= y:
        if p >= 0:
            x += 1
            p -= 4*a
        y += 1
        p += 1+2*y
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 + y))
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 - y))
        if x >= limitX:
            break
    p = (y+0.5)**2 - 4*a*(x+1)
    while x < limitX:
        if p < 0:
            y += 1
            p += 2*y
        x += 1
        p -= 4*a
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 + y))
        glVertex2f(evalFnX(x0 + x), evalFnY(y0 - y))
    glEnd()


if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(50, 50)
    glutInitWindowSize(1000, 720)
    glutCreateWindow("Co-ordinate plane")
    glutFullScreen()
    glClearColor(1, 1, 1, 0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-17, 17, -10, 10)

    # subMenuLine = glutCreateMenu(line_menu)

    mainMenu = glutCreateMenu(GoMenu)
    glutAddMenuEntry("Plot Point", 1)
    glutAddMenuEntry("select points", 2)
    glutAddMenuEntry("Draw polygon with selected pts", 3)
    glutAddMenuEntry("Draw Circle", 4)
    glutAddMenuEntry("Exit", 6)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    glutDisplayFunc(draw)
    print("mainLoop")
    glutKeyboardFunc(keyboard)
    glutMotionFunc(mouse)
    glutPassiveMotionFunc(mouse)
    glutMouseFunc(mouse)
    glutMainLoop()
