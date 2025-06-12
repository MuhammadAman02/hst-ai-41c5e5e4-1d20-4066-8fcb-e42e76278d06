from typing import Tuple

def check_collision(rect1: Tuple[float, float, float, float], 
                   rect2: Tuple[float, float, float, float]) -> bool:
    """
    Check collision between two rectangles.
    Each rect is (x, y, width, height)
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

def point_in_rect(point: Tuple[float, float], 
                  rect: Tuple[float, float, float, float]) -> bool:
    """Check if a point is inside a rectangle."""
    px, py = point
    x, y, w, h = rect
    return x <= px <= x + w and y <= py <= y + h