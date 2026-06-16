"""
Lesson 2: 2D Transformations
=============================
A transformation is a mathematical operation that moves or changes a shape.
We store shapes as lists of (x, y) points and apply math to each point.

The three fundamental transformations:
  • Translation  — slide a shape left/right/up/down
  • Scaling      — make a shape bigger or smaller
  • Rotation     — spin a shape around a point

Libraries used:
  - Pillow  (pip install Pillow)
  - math    (built-in)
"""

import math
from PIL import Image, ImageDraw

# ── Canvas setup ─────────────────────────────────────────────────────────────

def new_canvas(width=600, height=400, color=(30, 30, 30)):
    img  = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_polygon(draw, points, color, label=""):
    """Draw a filled polygon from a list of (x,y) points."""
    draw.polygon(points, fill=color, outline=(255, 255, 255))
    if label:
        cx = sum(p[0] for p in points) // len(points)
        cy = sum(p[1] for p in points) // len(points)
        draw.text((cx - 20, cy - 8), label, fill=(255, 255, 255))

# ── Define a simple arrow shape (list of vertices) ───────────────────────────

ARROW = [
    (0,  -40),   # tip
    (20,  10),
    (8,   10),
    (8,   40),
    (-8,  40),
    (-8,  10),
    (-20, 10),
]

# ── Transformation functions ──────────────────────────────────────────────────

def translate(points, tx, ty):
    """Slide every point by (tx, ty)."""
    return [(x + tx, y + ty) for x, y in points]

def scale(points, sx, sy, cx=0, cy=0):
    """
    Scale every point by (sx, sy).
    cx, cy  = the center of scaling (defaults to origin).
    """
    return [(cx + (x - cx) * sx,
             cy + (y - cy) * sy) for x, y in points]

def rotate(points, angle_degrees, cx=0, cy=0):
    """
    Rotate every point by angle_degrees around (cx, cy).
    Positive angle = counter-clockwise.
    """
    theta = math.radians(angle_degrees)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    result = []
    for x, y in points:
        # Shift to origin
        dx, dy = x - cx, y - cy
        # Rotate
        nx = dx * cos_t - dy * sin_t
        ny = dx * sin_t + dy * cos_t
        # Shift back
        result.append((cx + nx, cy + ny))
    return result
