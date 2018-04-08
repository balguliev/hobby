from vpython import *

# Constants
arc_radius = 2
theta1 = -pi / 6
theta2 = pi / 6

scene.caption = """
    Click to place object.
    After the object is placed, click and hold to target a ray. Let go to see its path.
    Hold shift and drag to move the camera and use it as a convex mirror
    Refresh the page to reset"""
    
# Define a bounding box for when we find points
box_left, box_right = arc_radius * cos(theta1), arc_radius
box_bottom, box_top = arc_radius * sin(theta1), arc_radius * sin(theta2)


arc = shapes.arc(radius=arc_radius, angle1=theta1, angle2=theta2)
extrusion(path=[vec(0, 0, 0.1), vec(0, 0, -0.1)], shape=arc) # Create mirror
diag = int(hypot(scene.width, scene.height))

scene.autoscale = False  # Fix focus on mirror
scene.userspin = False  # So all items locked in xy plane

box(pos=vector(0, 0, 0), length=diag, width=0.01, height=0.01, color=color.cyan)  # Optical axis
origin = sphere(pos=vec(0, 0, 0), radius=0.03)  # Origin, center of curvature
focus = sphere(pos=vec(1, 0, 0), radius=0.03)  # Focus

origin_label = label(pos=origin.pos, text="Origin", box=False, yoffset=1)
focus_label = label(pos=focus.pos, text="Focus", box=False, yoffset=1)


def hypot(x, y):
    return sqrt(x ** 2 + y ** 2)


def sign(x):
    return -1 if x < 0 else 1


def angle_from_ihat(vect: vector):
    theta = atan2(vect.y, vect.x)
    return theta if theta > 0 else theta + 2*pi


def ray_from_points(x1, y1, x2, y2, color=color.yellow):
    return cylinder(pos=vec(x1, y1, 0), axis=vec(x2 - x1, y2 - y1, 0), length=diag, radius=0.02, color=color)


def intersection(p1, p2, r=arc_radius):
    """From http://mathworld.wolfram.com/Circle-LineIntersection.html"""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    D = x1 * y2 - x2 * y1
    dr = hypot(dx, dy)
    disc = r ** 2 * dr ** 2 - D ** 2
    dr2, disqrt = dr ** 2, sqrt(disc)
    if disc > 0:
        x = (D * dy - sign(dy) * dx * disqrt) / dr2
        y = (-D * dx - abs(dy) * disqrt) / dr2
        if box_left < x < box_right and box_bottom < y < box_top:
            return x, y  # return this point if it fits on the arc

        x = (D * dy + sign(dy) * dx * disqrt) / dr2
        y = (-D * dx + abs(dy) * disqrt) / dr2
        if box_left < x < box_right and box_bottom < y < box_top:
            return x, y  # return this point if it fits on the arc


def make_reflection(direction: vector):
    x, y = object.pos.x, object.pos.y
    intersect = intersection((x, y), (x + direction.x, y + direction.y))
    if intersect:
        intersect_vect = vec(*intersect, 0)
        normal = -intersect_vect
        line_vect = -direction
        theta = diff_angle(line_vect, normal)
        
        if angle_from_ihat(line_vect) < angle_from_ihat(normal):
            line_vect = line_vect.rotate(angle=2 * theta)
        else:
            line_vect = line_vect.rotate(angle=-2 * theta)
        
        sphere(pos=intersect_vect, radius=0.04)  # Shows point of reflection
        arrow(pos=intersect_vect, axis=normal * 0.15)  # Shows normal vect.
        length = (object.pos + normal).mag
        cylinder(pos=object.pos, axis=direction, length=length, radius=0.02, color=color.green)  # Ray from object to mirror
        cylinder(pos=intersect_vect, axis=line_vect, length=diag, radius=0.02, color=color.red) # Ray from mirror to 'infinity'


ev = scene.waitfor('click')
object = sphere(pos=ev.pos, radius=0.05, color=color.green)

# Hide labels after object is placed
origin_label.visible=False
focus_label.visible=False

# Used to 
drag = False
ray = None


def down():
    global drag, ray

    x, y = scene.mouse.pos.x, scene.mouse.pos.y
    ray = ray_from_points(object.pos.x, object.pos.y, x, y)
    ray.color = color.cyan
    drag = True

def move():
    global drag, ray
    if drag:  # mouse button is down
        ray.axis = scene.mouse.pos - object.pos

def up():
    global drag, ray
    drag = False
    ray.visible = False
    make_reflection(scene.mouse.pos - object.pos)

scene.bind("mousedown", down)
scene.bind("mousemove", move)
scene.bind("mouseup", up)
