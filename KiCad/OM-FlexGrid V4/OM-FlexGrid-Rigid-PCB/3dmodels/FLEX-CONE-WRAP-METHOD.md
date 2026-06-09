# Wrapping a Flex PCB onto its Cone in Blender (without the spiral)

How we wrapped the OpenMuscle FlexGrid flex PCB onto a tapered (forearm) cone in
Blender so that every cross section is a true flat circle, with no spiral and no
twist. Written after a long debugging session so it can be reproduced quickly.

## TL;DR

The flat flex was cut as a **curved crescent**, which is the **unrolled
(developed) shape of a cone** (an annular sector). The fix is to **roll it back
up around the crescent's own center of curvature (the cone apex)**, using the
inverse cone-development mapping. Wrapping it any other way (like a rectangle,
or with Blender's Curve modifier) produces a spiral.

## The trap (what does NOT work)

1. **Treating the flex as a rectangle**: mapping length to wrap-angle and width
   to the axis. This only works if the flat piece is a rectangle (rolls into a
   cylinder). A crescent rolled this way spirals.
2. **Blender Curve modifier (wrap along a circle)**: on a closed circular path
   it accumulates a built-in frame rotation. Measured twist on our part was
   about 357 degrees (a full barber pole). Do not use it for a closed wrap.
3. **Simple Deform > Bend**: on a flat sheet it curls the sheet in its own
   plane (a flat coil), not into an upright tube.

## The key realization

Look at the flat flex from the top. If the outline is a **crescent / banana
(curved long edges)**, it is an annular sector, i.e. a cone development. A clean
circle fit to one of its long edges will have a tiny residual (ours was
0.13 mm), which confirms the edge is a true arc and gives you the apex.

## The correct method

1. View the flat flex from top; confirm it is a crescent.
2. Fit a circle to one clean long edge (Kasa least squares). The center is the
   cone apex `O`; bin by X and take the min-Y (or max-Y) vertex per bin so you
   fit a single clean edge arc, not the filled region.
3. For every vertex compute polar coords about `O` in the flat plane:
   - `rho = distance from O`
   - `phi = angle about O`
4. Let `alpha = phi span` (total sweep of the sector) and `phi0 = mid phi`.
   For a band that closes fully around (360 degrees):
   - `sin(beta) = alpha / (2*pi)`  (beta = cone half-angle)
   - `cos(beta) = sqrt(1 - sin(beta)^2)`
5. Map each vertex onto the cone (axis along world Y):
   - wrap angle `theta = (phi - phi0) / sin(beta)`
   - cone radius `r = rho*sin(beta) + (z - z_neutral)`  (the z term re-adds flex thickness radially)
   - axial position `Y = rho*cos(beta)` (then center it)
   - world position `= ( r*sin(theta), Y, r*cos(theta) )`

Because `theta` depends only on `phi` and `Y`/`r` depend only on `rho`, a row of
constant `rho` becomes a perfect flat circle and a line of constant `phi`
becomes a straight meridian. No twist by construction.

## Diagnostics that actually tell the truth

- **Ring test (is it a circle?)**: take vertices at constant ORIGINAL world-Y
  (a true ring). Measure spread in world-Y (axial drift = spiral) and spread in
  radius (circle error). Clean wrap: both near zero. Ours: worldY 0.03 mm,
  radius 0.16 mm.
- **Edge circle fit residual**: confirms the flat edge is a real arc (annular
  sector). Low residual = it is a cone development.

Pitfalls that gave false readings during debugging:
- Grouping diagnostic vertices by LOCAL Y on a branched mesh (local Y is not
  constant-world-Y). Always group by world coordinates.
- `atan2` wraps at +/-180 degrees; a twist column sampled right at the seam
  reads a huge or tiny spread that is meaningless. Sample away from the seam.
- A finite selection window in X converts to an angle (delta_x / R), which looks
  like "twist." Account for the window width before believing a twist number.

## Results for OM-FlexGrid V4

- Fitted apex `O` (flat plane): about (1.3 mm, 609.0 mm); bottom-edge arc radius
  639.9 mm; fit residual 0.13 mm.
- The flex's TRUE cone: radius 42.9 to 47.4 mm (about 86 to 95 mm diameter),
  about 60 mm tall, half-angle 4.25 degrees, sweep alpha 26.6 degrees, wraps a
  full 360 degrees.
- Note: the cone first placed in Fusion (R 37.9 to 51.8, 102 mm, 7.7 degrees) did
  NOT match the flex's development. The flex itself tells you the real cone via
  the edge fit. If you want a cone object to sit under the flex, build it to the
  TRUE numbers above (or re-derive from the flex each time).

## Reusable Blender script

Run in Blender's scripting workspace (or via the Blender MCP). Assumes the flat
flex object is named `FlexPCB`, lies roughly flat, and that you want the cone
axis along world Y. Produces a new object `FlexPCB_wrapped`.

```python
import bpy, math, mathutils, bmesh
M = mathutils

SRC_NAME = "FlexPCB"          # flat flex (the crescent)
OUT_NAME = "FlexPCB_wrapped"  # result

src = bpy.data.objects[SRC_NAME]
P = [src.matrix_world @ v.co for v in src.data.vertices]
zs = [p.z for p in P]
z_neutral = (min(zs) + max(zs)) / 2

# --- 1) fit a circle (apex O) to one clean long edge ---
xs = [p.x for p in P]
xmin, xmax = min(xs), max(xs)
NB = 60
edge = {}
for p in P:                     # bottom edge = min-Y vertex per X bin
    b = int((p.x - xmin) / (xmax - xmin + 1e-9) * NB)
    if b not in edge or p.y < edge[b].y:
        edge[b] = p

def kasa(pts):                  # algebraic circle fit -> (cx, cy, R)
    n = len(pts)
    ex = [q.x for q in pts]; ey = [q.y for q in pts]
    z = [ex[i]**2 + ey[i]**2 for i in range(n)]
    Sx=sum(ex); Sy=sum(ey); Sxx=sum(a*a for a in ex); Syy=sum(a*a for a in ey)
    Sxy=sum(ex[i]*ey[i] for i in range(n))
    Sxz=sum(ex[i]*z[i] for i in range(n)); Syz=sum(ey[i]*z[i] for i in range(n)); Sz=sum(z)
    m=[[Sxx,Sxy,Sx,-Sxz],[Sxy,Syy,Sy,-Syz],[Sx,Sy,n,-Sz]]
    for i in range(3):
        pv=m[i][i]
        for j in range(i+1,3):
            f=m[j][i]/pv
            for k in range(4): m[j][k]-=f*m[i][k]
    C=m[2][3]/m[2][2]; B=(m[1][3]-m[1][2]*C)/m[1][1]; A=(m[0][3]-m[0][1]*B-m[0][2]*C)/m[0][0]
    cx=-A/2; cy=-B/2
    return cx, cy, math.sqrt(max(0, cx*cx+cy*cy-C))

Ox, Oy, Redge = kasa(list(edge.values()))

# --- 2) polar coords about O, sector sweep, cone half-angle ---
rho = [math.hypot(p.x-Ox, p.y-Oy) for p in P]
phi = [math.atan2(p.y-Oy, p.x-Ox) for p in P]
alpha = max(phi) - min(phi)
phi0 = (min(phi) + max(phi)) / 2
sinb = alpha / (2*math.pi)
cosb = math.sqrt(max(0, 1 - sinb*sinb))
hmid = (min(r*cosb for r in rho) + max(r*cosb for r in rho)) / 2

# --- 3) roll up onto the cone (axis = world Y) ---
old = bpy.data.objects.get(OUT_NAME)
if old: bpy.data.objects.remove(old, do_unlink=True)
dup = src.copy(); dup.data = src.data.copy(); dup.name = OUT_NAME
bpy.context.scene.collection.objects.link(dup)
mw = dup.matrix_world.copy(); mwi = mw.inverted()
me = dup.data
for v in me.vertices:
    w = mw @ v.co
    rp = math.hypot(w.x-Ox, w.y-Oy)
    ph = math.atan2(w.y-Oy, w.x-Ox)
    th = (ph - phi0) / sinb
    r  = rp*sinb + (w.z - z_neutral)
    Y  = rp*cosb - hmid
    v.co = mwi @ M.Vector((r*math.sin(th), Y, r*math.cos(th)))
me.update()
bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()

print("apex O (mm): %.1f, %.1f  edge R %.1f" % (Ox*1000, Oy*1000, Redge*1000))
print("cone half-angle %.2f deg, R %.1f..%.1f mm, wraps %.0f deg" % (
    math.degrees(math.asin(sinb)), min(rho)*sinb*1000, max(rho)*sinb*1000,
    math.degrees(alpha/sinb)))
```

## Notes and gotchas

- This is a destructive bake. Keep the flat `FlexPCB` as a hidden backup so you
  can re-run with different parameters.
- It is not a live modifier. Blender's deform modifiers cannot do this exact
  mapping without the twist, so a bake (or a Geometry Nodes equivalent) is the
  clean route. Re-baking is fast.
- If the flex should stay flat near the rigid board and only wrap past it, mask
  the roll-up by the vertex's `phi` (or original X) range.
- To add a small standoff so the flex sits just proud of the cone surface, add a
  constant to `r` (for example `+ 0.0005` for 0.5 mm).
- The two long edges of a true annular sector are concentric. If one edge fits
  cleanly and the other does not, the bad fit is usually a connector tail or
  outline feature, not the development. Fit the clean edge.
