from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Globals
y_trans = -0.7  # Y-axis translation of the rocket
fly = False
theta_x = 0
theta_y = 0
theta_z = 0
dt = 0.3
x_trans = 0.0
scale_factor = 1.0

# Fly the rocket
def flyRocket():
    global y_trans
    y_trans += 0.025  # Adjust the speed of upward movement

# Reset the rocket
def reset():
    global y_trans, fly, dt, x_trans, scale_factor, theta_x, theta_y, theta_z
    fly = False
    dt = 0.3
    y_trans = -0.7  # Reset Y translation
    x_trans = 0.0
    scale_factor = 1.0
    theta_x = 0
    theta_y = 0
    theta_z = 0

# Handle keyboard input
def specialInput(key, x, y):
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

# Flame rendering using cones for a more realistic effect
def render_flame():
    glPushMatrix()
    glTranslatef(0.0, y_trans - 1.00, 0.0)  # Adjusted to be closer to the rocket tail

    # Enable blending for transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Create several cones (layers) to simulate the flame
    for i in range(5):  # Create 5 layers of cones for flame
        scale = 0.2 + i * 0.05  # Increase size for each layer
        transparency = 1.0 - i * 0.15  # Decrease transparency with each layer

        # Random flame colors for flickering effect
        r = random.uniform(0.8, 1.0)
        g = random.uniform(0.2, 0.5)
        b = random.uniform(0.0, 0.1)

        glColor4f(r, g, b, transparency)  # Set color and transparency
        glPushMatrix()
        glScalef(scale, scale, scale)  # Increase size for each layer
        glRotatef(-90, 1.0, 0.0, 0.0)  # Rotate to point downwards
        glutSolidCone(0.2, 0.5, 20, 20)  # Draw the cone
        glPopMatrix()

    glDisable(GL_BLEND)
    glPopMatrix()

# Rocket rendering
def rocket():
    glPushMatrix()
    glTranslatef(x_trans, y_trans, 0.0)  # Only translate along the Y-axis (up/down)
    glScalef(scale_factor, scale_factor, scale_factor)
    glRotatef(theta_x, 1, 0, 0)
    glRotatef(theta_y, 0, 1, 0)
    glRotatef(theta_z, 0, 0, 1)
    
    # Rocket nose cone (white)
    glColor3f(1.0, 1.0, 1.0)  # White
    glPushMatrix()
    glTranslatef(0.0, 0.68, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glutSolidCone(0.15, 0.4, 50, 30)
    glPopMatrix()
    
    # Rocket body cylinder (metallic gray with stripes)
    glColor3f(0.7, 0.7, 0.7)  # Metallic gray
    glPushMatrix()
    glTranslatef(0.0, -0.02, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    quadobj = gluNewQuadric()
    gluCylinder(quadobj, 0.15, 0.15, 0.7, 50, 30)
    glPopMatrix()
    
    # Black stripe on the rocket body
    glColor3f(0.0, 0.0, 0.0)  # Black
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glutSolidTorus(0.01, 0.15, 10, 50)  # Thin black stripe
    glPopMatrix()
    
    # Rocket fins (dark gray)
    glColor3f(0.3, 0.3, 0.3)  # Dark gray
    glPushMatrix()
    glTranslatef(0.0, 0.08, 0.0)
    glScalef(0.9, 0.4, 0.06)
    glutSolidCube(0.5)
    glPopMatrix()
    
    glPushMatrix()
    glRotatef(90, 0, 5, 0)
    glTranslatef(0.0, 0.08, 0.0)
    glScalef(0.9, 0.4, 0.06)
    glutSolidCube(0.5)
    glPopMatrix()
    
    glPopMatrix()

    # Render the flame when the rocket is flying
    if fly:
        render_flame()

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
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
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(200, 100)
    glutCreateWindow(b"Rocket Simulation with 3D Transformations and Layered Flame")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(0, 0, -5)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(specialInput)
    glutKeyboardFunc(specialInput)  # Added to handle '+' and '-' for scaling
    glutMainLoop()

if __name__ == "__main__":
    main()