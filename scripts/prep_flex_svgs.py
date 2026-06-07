"""Prepare Fusion 360 / Shaper Origin SVG exports for KiCad import.

Reads the two flex-PCB-related SVGs from KiCad/OM-FlexGrid V4/OM-FlexGrid-Flex/
(the FFC stiffener rectangle and the main flex body cutout outline),
applies the SVG transform matrix to bake it into the path data, computes
the rotation needed to make the leftmost edge of each shape exactly
vertical, applies the same rotation to both so they stay aligned with
each other, and writes ready-for-KiCad SVGs.

Two output files end up next to the originals:
  V4-Stiffener-for-KiCad.svg     (filled rectangle, target the Stiffener user layer)
  V4-EdgeCuts-for-KiCad.svg      (outline polyline, target Edge.Cuts)

KiCad's File -> Import -> Graphics dialog reads these, lets you pick the
target layer, and places them with a chosen origin. After import:

  - Edge cuts: select the imported items and, if needed, change their
    layer to Edge.Cuts and stroke width to 0.05 mm (KiCad default for
    that layer).
  - Stiffener: the filled polygon imports as a closed shape on whatever
    user layer you choose (typically User.1 renamed to "Stiffener").
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import List, Tuple

HERE = Path(__file__).resolve().parent
FLEX_DIR = HERE.parent / "KiCad" / "OM-FlexGrid V4" / "OM-FlexGrid-Flex"

STIFFENER_IN = FLEX_DIR / "FFC-Stiffener_Faces.svg"
CUTOUT_IN = FLEX_DIR / "V4CurveCutout_Faces.svg"

STIFFENER_OUT = FLEX_DIR / "V4-Stiffener-for-KiCad.svg"
CUTOUT_OUT = FLEX_DIR / "V4-EdgeCuts-for-KiCad.svg"


# ------------------------------------------------------------------------
# SVG path parsing: just enough for the Fusion 360 / Shaper exports we have.
# We sample arcs into short line segments to keep the rotation + bbox math
# simple, then re-emit as a polyline ("M ... L ... L ... Z").
# ------------------------------------------------------------------------

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?")
CMD_RE = re.compile(r"[MLHVCSQTAZmlhvcsqtaz]")


def tokenize(d: str) -> List:
    """Return [(cmd, [floats]), ...]"""
    out = []
    i = 0
    while i < len(d):
        c = d[i]
        if c in "MLHVCSQTAZmlhvcsqtaz":
            cmd = c
            i += 1
            nums_buf = []
            # Gather all numbers until the next command letter
            j = i
            while j < len(d) and d[j] not in "MLHVCSQTAZmlhvcsqtaz":
                j += 1
            chunk = d[i:j]
            for m in NUM_RE.finditer(chunk):
                nums_buf.append(float(m.group(0)))
            out.append((cmd, nums_buf))
            i = j
        else:
            i += 1
    return out


def arc_endpoint_to_center(x1, y1, x2, y2, fa, fs, rx, ry, phi_deg):
    """Endpoint to center parameterization (SVG spec)."""
    if rx == 0 or ry == 0:
        return None
    phi = math.radians(phi_deg)
    cosp, sinp = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p = cosp * dx + sinp * dy
    y1p = -sinp * dx + cosp * dy
    rx, ry = abs(rx), abs(ry)
    lam = (x1p * x1p) / (rx * rx) + (y1p * y1p) / (ry * ry)
    if lam > 1:
        s = math.sqrt(lam)
        rx, ry = rx * s, ry * s
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    if den == 0:
        return None
    fac = max(0, num) / den
    coef = math.sqrt(fac)
    if fa == fs:
        coef = -coef
    cxp = coef * rx * y1p / ry
    cyp = -coef * ry * x1p / rx
    cx = cosp * cxp - sinp * cyp + (x1 + x2) / 2
    cy = sinp * cxp + cosp * cyp + (y1 + y2) / 2

    def angle(ux, uy, vx, vy):
        dot = ux * vx + uy * vy
        n = math.hypot(ux, uy) * math.hypot(vx, vy)
        if n == 0:
            return 0.0
        ang = math.acos(max(-1, min(1, dot / n)))
        if ux * vy - uy * vx < 0:
            ang = -ang
        return ang

    theta1 = angle(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    d_theta = angle((x1p - cxp) / rx, (y1p - cyp) / ry,
                    (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if fs == 0 and d_theta > 0:
        d_theta -= 2 * math.pi
    elif fs == 1 and d_theta < 0:
        d_theta += 2 * math.pi
    return cx, cy, rx, ry, theta1, d_theta, phi


def sample_arc(x1, y1, x2, y2, rx, ry, phi_deg, fa, fs, n=64):
    """Sample an SVG elliptical arc into n+1 (x,y) points."""
    p = arc_endpoint_to_center(x1, y1, x2, y2, fa, fs, rx, ry, phi_deg)
    if p is None:
        return [(x1, y1), (x2, y2)]
    cx, cy, rx, ry, theta1, d_theta, phi = p
    cosp, sinp = math.cos(phi), math.sin(phi)
    pts = []
    for i in range(n + 1):
        t = theta1 + d_theta * (i / n)
        x = cx + rx * math.cos(t) * cosp - ry * math.sin(t) * sinp
        y = cy + rx * math.cos(t) * sinp + ry * math.sin(t) * cosp
        pts.append((x, y))
    return pts


def apply_matrix(x, y, m):
    """Apply 2x3 matrix m = [a, b, c, d, e, f] to point (x, y)."""
    a, b, c, d, e, f = m
    return (a * x + c * y + e, b * x + d * y + f)


def parse_matrix(transform: str):
    """Extract matrix(a,b,c,d,e,f) into list of 6 floats. None if not present."""
    m = re.search(r"matrix\s*\(([^)]+)\)", transform or "")
    if not m:
        return None
    return [float(x) for x in NUM_RE.findall(m.group(1))]


def path_to_polyline(d: str, transform_matrix=None, arc_samples=64):
    """Parse SVG path d and return a list of subpaths (each a list of (x,y))."""
    tokens = tokenize(d)
    subpaths = []
    current = []
    cx, cy = 0.0, 0.0
    start_x, start_y = 0.0, 0.0

    def add(p):
        current.append(p)

    for cmd, args in tokens:
        rel = cmd.islower()
        c = cmd.upper()
        i = 0
        if c == "M":
            x, y = args[0], args[1]
            if rel:
                x += cx
                y += cy
            if current:
                subpaths.append(current)
            current = []
            cx, cy = x, y
            start_x, start_y = x, y
            add((cx, cy))
            i = 2
            # Subsequent pairs after M are implicit L commands
            while i + 1 < len(args):
                x, y = args[i], args[i + 1]
                if rel:
                    x += cx
                    y += cy
                cx, cy = x, y
                add((cx, cy))
                i += 2
        elif c == "L":
            while i + 1 < len(args):
                x, y = args[i], args[i + 1]
                if rel:
                    x += cx
                    y += cy
                cx, cy = x, y
                add((cx, cy))
                i += 2
        elif c == "H":
            for x in args:
                if rel:
                    x += cx
                cx = x
                add((cx, cy))
        elif c == "V":
            for y in args:
                if rel:
                    y += cy
                cy = y
                add((cx, cy))
        elif c == "A":
            while i + 6 < len(args):
                rx, ry, xrot, fa, fs, x, y = args[i:i + 7]
                if rel:
                    x += cx
                    y += cy
                pts = sample_arc(cx, cy, x, y, rx, ry, xrot, int(fa), int(fs),
                                 n=arc_samples)
                # Skip the first point (already added)
                for p in pts[1:]:
                    add(p)
                cx, cy = x, y
                i += 7
        elif c == "Z":
            if current and (cx, cy) != (start_x, start_y):
                add((start_x, start_y))
            cx, cy = start_x, start_y
            if current:
                subpaths.append(current)
                current = []
        # We only need M / L / H / V / A / Z for these Fusion exports.

    if current:
        subpaths.append(current)

    # Apply transform matrix
    if transform_matrix is not None:
        subpaths = [[apply_matrix(x, y, transform_matrix) for (x, y) in sub]
                    for sub in subpaths]
    return subpaths


# ------------------------------------------------------------------------
# Rotation: find the leftmost vertex of the shape, find the segment of the
# polyline that has the smallest x at one endpoint and is "long enough" to
# represent a real edge, then rotate everything so that segment is vertical.
# ------------------------------------------------------------------------

def collinear_runs(sub, tol_deg=2.0):
    """Group consecutive segments in a subpath into collinear runs.

    Returns a list of (start_x, start_y, end_x, end_y, length) tuples,
    one per straight-ish run. A "run" is a sequence of segments whose
    direction stays within tol_deg of each other. Arc samples (which are
    many tiny segments with slowly changing direction) end up as runs
    too, but their per-step direction change exceeds tol_deg, so they
    naturally split into many short runs that lose out to true straight
    edges in the longest-run selection.
    """
    runs = []
    if len(sub) < 2:
        return runs
    tol = math.radians(tol_deg)
    cur_start_x, cur_start_y = sub[0]
    prev_dir = None
    last_x, last_y = sub[0]
    for i in range(1, len(sub)):
        x, y = sub[i]
        dx, dy = x - last_x, y - last_y
        if dx == 0 and dy == 0:
            continue
        d = math.atan2(dy, dx)
        if prev_dir is None or _ang_diff(d, prev_dir) < tol:
            prev_dir = d if prev_dir is None else prev_dir
            last_x, last_y = x, y
        else:
            # End current run, start new
            length = math.hypot(last_x - cur_start_x, last_y - cur_start_y)
            if length > 0:
                runs.append((cur_start_x, cur_start_y, last_x, last_y, length))
            cur_start_x, cur_start_y = last_x, last_y
            prev_dir = d
            last_x, last_y = x, y
    # Close final run
    length = math.hypot(last_x - cur_start_x, last_y - cur_start_y)
    if length > 0:
        runs.append((cur_start_x, cur_start_y, last_x, last_y, length))
    return runs


def _ang_diff(a, b):
    """Smallest angular difference between two directions (radians)."""
    d = (a - b + math.pi) % (2 * math.pi) - math.pi
    return abs(d)


def find_leftmost_edge_angle(subpaths) -> float:
    """Return the angle (radians) of the leftmost STRAIGHT edge.

    Strategy: group each subpath's segments into collinear runs (runs of
    near-constant direction). True straight edges come out as long runs,
    sampled arcs come out as many short runs. Then find the global min-x
    of the shape, restrict to runs whose midpoint lies within a band of
    that min-x, and pick the longest such run.

    This reliably catches "the left side of the FFC tail" on the flex
    cutout shape: the tail has straight edges; the body has a long arc
    that gets sampled into short segments and loses the longest-run race.
    """
    pts = [p for sub in subpaths for p in sub]
    if not pts:
        return 0.0
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    # Wider band than before because we want to include the entire FFC
    # tail, which may sit a bit inboard of the absolute min-x once the
    # main body's curve sticks out a tiny bit further on its own.
    band = max(0.05, 0.05 * (max_x - min_x))

    all_runs = []
    for sub in subpaths:
        all_runs.extend(collinear_runs(sub, tol_deg=2.0))

    best = None
    for (x1, y1, x2, y2, length) in all_runs:
        mid_x = (x1 + x2) / 2
        if mid_x - min_x > band:
            continue
        if best is None or length > best[4]:
            best = (x1, y1, x2, y2, length)

    if best is None:
        # No straight run in the band -- the leftmost region is purely
        # curved. Fall back to the longest segment in the band regardless
        # of straightness.
        for sub in subpaths:
            for i in range(len(sub) - 1):
                (x1, y1), (x2, y2) = sub[i], sub[i + 1]
                mid_x = (x1 + x2) / 2
                if mid_x - min_x > band:
                    continue
                length = math.hypot(x2 - x1, y2 - y1)
                if best is None or length > best[4]:
                    best = (x1, y1, x2, y2, length)

    if best is None:
        return 0.0
    x1, y1, x2, y2, _ = best
    return math.atan2(y2 - y1, x2 - x1)


def rotate_points(subpaths, angle_rad: float, pivot=(0, 0)):
    px, py = pivot
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    out = []
    for sub in subpaths:
        rot = []
        for (x, y) in sub:
            dx, dy = x - px, y - py
            rot.append((c * dx - s * dy + px, s * dx + c * dy + py))
        out.append(rot)
    return out


def bbox(subpaths):
    xs = [p[0] for sub in subpaths for p in sub]
    ys = [p[1] for sub in subpaths for p in sub]
    return min(xs), min(ys), max(xs), max(ys)


def translate(subpaths, dx, dy):
    return [[(x + dx, y + dy) for (x, y) in sub] for sub in subpaths]


# ------------------------------------------------------------------------
# SVG emit
# ------------------------------------------------------------------------

def to_svg(subpaths, width_cm, height_cm, fill, stroke="black",
           stroke_width=0.01) -> str:
    paths = []
    for sub in subpaths:
        if not sub:
            continue
        d = "M " + " L ".join(f"{x:.6f},{y:.6f}" for x, y in sub) + " Z"
        paths.append(d)
    paths_str = "\n  ".join(
        f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>'
        for d in paths
    )
    return f'''<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width_cm}cm" height="{height_cm}cm"
     viewBox="0 0 {width_cm} {height_cm}" version="1.1">
  <!-- Generated by scripts/prep_flex_svgs.py for KiCad import. -->
  <!-- Leftmost edge is rotated to be perfectly vertical. -->
  {paths_str}
</svg>
'''


# ------------------------------------------------------------------------
# Main: process both SVGs and emit cleaned versions.
# ------------------------------------------------------------------------

def load_svg_path(path: Path):
    text = path.read_text(encoding="utf-8")
    d_match = re.search(r'<path[^>]*\sd="([^"]+)"', text)
    if not d_match:
        raise SystemExit(f"no <path d> found in {path}")
    d = d_match.group(1)
    t_match = re.search(r'<path[^>]*\stransform="([^"]+)"', text)
    m = parse_matrix(t_match.group(1)) if t_match else None
    return d, m


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rotate-cutout",
        type=float,
        default=None,
        help="Manual rotation angle in degrees for the cutout, overriding "
             "the auto-detected angle. Positive = counter-clockwise. Useful "
             "when the auto-detected leftmost edge isn't what you wanted; "
             "import once into KiCad, see what needs to change, re-run with "
             "this flag to dial in.",
    )
    args = parser.parse_args()

    print(f"reading {STIFFENER_IN}")
    s_d, s_m = load_svg_path(STIFFENER_IN)
    s_sub = path_to_polyline(s_d, s_m, arc_samples=32)
    print(f"  stiffener: {sum(len(s) for s in s_sub)} pts in {len(s_sub)} subpath(s)")

    print(f"reading {CUTOUT_IN}")
    c_d, c_m = load_svg_path(CUTOUT_IN)
    c_sub = path_to_polyline(c_d, c_m, arc_samples=128)
    print(f"  cutout: {sum(len(s) for s in c_sub)} pts in {len(c_sub)} subpath(s)")

    # Step 1: figure out the rotation that makes the cutout's leftmost edge vertical.
    angle = find_leftmost_edge_angle(c_sub)
    angle_deg = math.degrees(angle)
    target = math.pi / 2
    rot = target - angle
    if args.rotate_cutout is not None:
        rot = math.radians(args.rotate_cutout)
        print(f"  MANUAL OVERRIDE: rotating cutout by {args.rotate_cutout:+.3f} deg")
    # Normalize to (-pi, pi] for readability.
    while rot > math.pi:
        rot -= 2 * math.pi
    while rot < -math.pi:
        rot += 2 * math.pi
    print(f"  cutout's leftmost edge currently at {angle_deg:.3f} deg")
    print(f"  rotating both shapes by {math.degrees(rot):+.3f} deg to make it vertical")

    # Step 2: rotate both shapes by the SAME angle around (0,0) in cutout space.
    # The stiffener is a tiny rectangle in its own coord system; first detect if
    # its leftmost edge is already vertical -- if so, leave it alone, since the
    # user said they want the two shapes to "line up" (presumably in KiCad they
    # will place the stiffener over the FFC tail; the stiffener is intrinsically
    # axis-aligned in its own SVG and doesn't need cutout-frame rotation).
    s_angle = find_leftmost_edge_angle(s_sub)
    print(f"  stiffener's leftmost edge at {math.degrees(s_angle):+.3f} deg")
    if abs(math.degrees(s_angle) - 90) < 1e-3 or abs(math.degrees(s_angle) + 90) < 1e-3:
        print("  stiffener leftmost edge already vertical, no rotation applied")
        s_rot_sub = s_sub
    else:
        s_target = math.pi / 2
        s_rot_angle = s_target - s_angle
        while s_rot_angle > math.pi:
            s_rot_angle -= 2 * math.pi
        while s_rot_angle < -math.pi:
            s_rot_angle += 2 * math.pi
        print(f"  rotating stiffener by {math.degrees(s_rot_angle):+.3f} deg")
        s_rot_sub = rotate_points(s_sub, s_rot_angle)

    c_rot_sub = rotate_points(c_sub, rot)

    # Step 3: translate each to its own (0,0) origin and emit
    for label, sub, out_path, fill in [
        ("stiffener", s_rot_sub, STIFFENER_OUT, "black"),
        ("cutout",    c_rot_sub, CUTOUT_OUT,    "none"),
    ]:
        minx, miny, maxx, maxy = bbox(sub)
        sub_t = translate(sub, -minx, -miny)
        w = maxx - minx
        h = maxy - miny
        svg_text = to_svg(sub_t, w, h, fill=fill)
        out_path.write_text(svg_text, encoding="utf-8")
        print(f"  wrote {out_path.name}  (bbox {w:.4f} x {h:.4f} cm)")

    print("done.")


if __name__ == "__main__":
    main()
