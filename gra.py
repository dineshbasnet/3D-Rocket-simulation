import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Globals
y_trans = -0.7  # Y-axis translation of the rocket
fly = False
theta_x = 0
theta_y = 0
theta_z = 0
dt = 0.3
x_trans = 0.0
scale_factor = 1.0
view_offset = 0.0  # Keeps track of the rocket's distance in space

# Fly the rocket
def flyRocket():
    global y_trans, view_offset
    if fly:
        y_trans += 0.025  # Adjust the speed of upward movement
        view_offset += 0.05  # Move the rocket further into space

# Reset the rocket
def reset():
    global y_trans, fly, dt, x_trans, scale_factor, theta_x, theta_y, theta_z, view_offset
    fly = False
    dt = 0.3
    y_trans = -0.7  # Reset Y translation
    x_trans = 0.0
    scale_factor = 1.0
    theta_x = 0
    theta_y = 0
    theta_z = 0
    view_offset = 0.0  # Reset view offset

# Handle keyboard input
def specialInput(key, _, __):  # Removed x, y and replaced with _
    global fly, dt, x_trans, scale_factor, theta_x, theta_y, theta_z, y_trans
    if key == GLUT_KEY_UP:
        fly = True
    elif key == GLUT_KEY_DOWN:
        reset()
    elif key == GLUT_KEY_LEFT:
        dt = 0.0
    elif key == GLUT_KEY_RIGHT:
        dt = 0.3
    elif key == GLUT_KEY_PAGE_UP:
        scale_factor += 0.1
    elif key == GLUT_KEY_PAGE_DOWN:
        scale_factor = max(0.5, scale_factor - 0.1)
    elif key == GLUT_KEY_F1:
        x_trans -= 0.1
    elif key == GLUT_KEY_F2:
        x_trans += 0.1
    elif key == b'+':  # Scaling up
        scale_factor += 0.1
    elif key == b'-':  # Scaling down
        scale_factor = max(0.5, scale_factor - 0.1)
    elif key == GLUT_KEY_F3:  # Move up
        y_trans += 0.1
    elif key == GLUT_KEY_F4:  # Move down
        y_trans -= 0.1
    elif key == GLUT_KEY_F5:
        theta_x += 5
    elif key == GLUT_KEY_F6:
        theta_x -= 5
    elif key == GLUT_KEY_F7:
        theta_y += 5
    elif key == GLUT_KEY_F8:
        theta_y -= 5
    elif key == GLUT_KEY_F9:
        theta_z += 5
    elif key == GLUT_KEY_F10:
        theta_z -= 5
    glutPostRedisplay()

# Flame rendering using circles for a more realistic effect
def render_flame():
    glPushMatrix()
    glTranslatef(0.0, y_trans - 1.00, 0.0)  # Position flames under the rocket

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    for i in range(20):  # Create 20 flame particles
        glPushMatrix()

        # Random placement of flame particles
        x_offset = random.uniform(-0.05, 0.05)  # Small horizontal variation
        y_offset = random.uniform(-0.1, -0.3)  # Move flames downward
        circle_size = random.uniform(0.05, 0.15)  # Random size

        glTranslatef(x_offset, y_offset, 0.0)  # Move flame particle

        # Random flame colors (red, orange, yellow shades)
        r = random.uniform(0.8, 1.0)
        g = random.uniform(0.2, 0.5)
        b = random.uniform(0.0, 0.1)
        glColor4f(r, g, b, 1.0)  # Semi-transparent flame effect

        # Draw a small circle (ellipse-like shape)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0.0, 0.0)  # Center of the circle
        for angle in range(0, 361, 30):  # Approximate a circle
            rad = math.radians(angle)
            glVertex2f(math.cos(rad) * circle_size, math.sin(rad) * circle_size)
        glEnd()

        glPopMatrix()

    glDisable(GL_BLEND)
    glPopMatrix()

# Render the background stars and planet
def render_background():
    glPushMatrix()
    glTranslatef(0.0, 0.0, -2.0)  # Position the stars and planets in the background
    
    # Draw stars (static background)
    glPointSize(2)
    glBegin(GL_POINTS)
    for _ in range(100):  # Draw 100 random stars
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-5, -2))
    glEnd()
    
    # Draw a planet (static position)
    glPushMatrix()
    glTranslatef(1.5, 1.0, -4.5)  # Position the planet in space
    glColor3f(0.3, 0.5, 0.7)  # Blueish color for the planet
    glutSolidSphere(0.2, 50, 50)  # Draw a sphere for the planet
    glPopMatrix()

    glPopMatrix()

# Rocket rendering
def rocket():
    glPushMatrix()
    glTranslatef(x_trans, y_trans, 0.0)
    glScalef(scale_factor, scale_factor, scale_factor)
    glRotatef(theta_x, 1, 0, 0)
    glRotatef(theta_y, 0, 1, 0)
    glRotatef(theta_z, 0, 0, 1)

    # Rocket nose cone
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.0, 0.68, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glutSolidCone(0.15, 0.4, 50, 30)
    glPopMatrix()

    # Rocket body
    glColor3f(0.7, 0.7, 0.7)
    glPushMatrix()
    glTranslatef(0.0, -0.02, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    quadobj = gluNewQuadric()
    gluCylinder(quadobj, 0.15, 0.15, 0.7, 50, 30)
    glPopMatrix()

    # Black stripe
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glutSolidTorus(0.01, 0.15, 10, 50)
    glPopMatrix()

    # Rocket fins
    glColor3f(0.3, 0.3, 0.3)
    for angle in [0, 90]:
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0.0, 0.08, 0.0)
        glScalef(0.9, 0.4, 0.06)
        glutSolidCube(0.5)
        glPopMatrix()

    glPopMatrix()

    # Render flame when flying
    if fly:
        render_flame()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Render the background stars and planet
    render_background()

    # Rocket rendering
    rocket()

    glutSwapBuffers()

# Idle function for animation
def idle():
    global theta_y
    if theta_y >= 360:
        theta_y = 0
    theta_y += dt
    if fly:
        flyRocket()
    glutPostRedisplay()

# Initialize and set up the window
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)  # Increased window size
    glutInitWindowPosition(200, 100)
    glutCreateWindow(b"Rocket Simulation with 3D Transformations and Space Background")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2, 2, -2, 2, -10, 10)  # Orthographic projection for better space effect
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(0, 0, -5)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(specialInput)
    glutKeyboardFunc(specialInput)  # Handles '+' and '-' keys
    glutMainLoop()

if __name__ == "__main__":
    main()
