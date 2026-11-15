# room-model

A measured 3D model of a home office + music room redesign, used to check that furniture fits and to preview the
look before buying anything. The owner is not an engineer and judges the product, not the code: explain in plain
language, test in a real browser before saying something works, and say what was and was not tested.

This repo is public. Do not commit photos of the home, names of household members, or secrets.

## What is here

| Path | What it is |
|---|---|
| `office-room.html` | The whole product: one page (three.js). Published as a Claude artifact, see below. |
| `tools/test_page.js` | Browser test (Playwright): opens the page, clicks every view and option, drags an item, adds and removes one, saves screenshots, prints errors. Run from the repo root: `node tools/test_page.js`. |
| `tools/export_scene.js` | Saves the exact scene from the page (`scene.glb`) plus camera and light info (`shot.json`) for a chosen view and light preset. |
| `tools/render_still.py` | Renders that scene in Blender (`pip install bpy`, Cycles on CPU, a few minutes per 1600px still). |
| `tools/photoreal.py` | Sends a Blender still to image models on Wiro and saves photoreal versions. Costs money; needs the owner's OK. |
| `renders/` | Stills made so far (Blender input and the image-model results). |

Published page: https://claude.ai/artifact/D6EtJ3Wj3bvSaLt24nTvWk . To update it, read that artifact first, then
publish `office-room.html` to the same URL. Keep the repo and the artifact in step: change the file here, test,
publish, commit.

## The room (inches)

- Axes: x runs along the back wall from the TV wall (x=0) to the window wall (x=150). z runs from the back wall
  (z=0) to the door wall (z=131). The scene is scaled to meters so it is true size in a headset.
- Measured: back wall 150 ("accurate to the inch"); window wall 131 = 52 (back-wall side) + 57 window + 22;
  sill 40; window top 81.5; ceiling 96; recessed lights 2 x 2, about 30 diagonally in from each corner; ceiling fan
  dead centre of the main rectangle, dropping 18.
- Entry nook: x -28..20, z 102..159. It is 48 wide and 57 deep, sticking 28 past the door wall and 28 past the TV
  wall, so the TV wall is only 102 long. The way into the room is the gap between the corner at (20, 131) and
  whatever stands at the end of the TV wall. The closet opening is on the door wall. The room door is on the nook's
  far wall (z=159), hinged at the x=-26 side, swinging in.
- Measured belongings: media console 63.5 x 15 x 25.5 (on the floor, owner is open to a smaller one that still
  hides the router and the TV/soundbar cables); Yamaha keyboard 53 wide x 12 deep, music stand top at 40 (keys drawn
  at 31); two 28" monitors, the left one vertical; 65" TV; an ergonomic office chair that stays.
- From the floor plan: the office closet opening (about 62 wide, starting 4 from the entry corner) and the door
  position. Guessed from photos, not measured: chair size, the two ocean canvases (24 x 16), the glass cabinet (IKEA Detolf's
  listed size), guitar sizes.

## The rest of the house

Added 2026-11-15 from the owner's floor plan image (a real-estate style plan with printed room sizes). `HOUSE` in the
page holds every other room as a polygon in plan pixels (about 1.205 inches per pixel; `P(px,py)` converts to inches;
north is up on the plan, which is -x here, and east is -z). The office is the plan's lower-right bedroom: its
159 x 178 footprint and window position matched the plan to the inch, and the 28-inch jog turned out to be the
primary bedroom's closet. `HOUSE.openings` cuts doors, cased openings and windows into any wall they lie on.

Rooms: living + dining, kitchen, foyer, hall, two baths, primary bedroom, second bedroom, garage, closets, plus
porch and patio slabs. Room sizes are the plan's printed figures; door and window positions are read off the
drawing (good to a few inches); ceilings are assumed 96 and window heights copy the office. The other rooms are
empty shells: no kitchen counters, bath fixtures, fireplace or furniture until the owner supplies measurements or
photos. Catalog items can be added to any room, but the fit check only covers the office.

### Photo pass (2026-11-15)

From the owner's interior and yard photos, all by eye and not measured:

- `buildFixed()` draws fixtures: living-room fireplace on the west wall with the TV above, kitchen (sink run on the
  south wall, range and fridge on the north wall, terracotta floor), hall bath (shower across the window end, vanity
  and toilet on the east wall), primary bath (shower at the south end, vanity and toilet on the west wall), primary
  ceiling fan, mirrored closet doors.
- `houseItems()` places today's movable things: sectional, rugs, dining table and chairs, bed, nightstands, dresser,
  hall runner, the MGB and washer/dryer in the garage, barrel sauna, fire pit, patio chairs, umbrella. The keyboard
  and guitars really live in the living room today; they are left out there because the office proposal moves them.
- Window heights adjusted from photos: living sill 36, dining sill 44, bath windows 56 to 80.
- `buildLot()`: lot side lengths from the parcel map (70 street side, 59 back, 118 and 123 sides). The street is on
  the plan's south side (+x) and the driveway sits in the notch east of the garage. House position on the lot, lawn,
  patios, driveway and fence are placed by eye. The owner's photos are not in this repo (public).

### Aerial, layout options and interface (2026-11-15)

- **Lot from the aerial photo:** traced from the owner's straightened aerial, in which the house sits square to the
  image. The main roof is 135 px eave to eave for 576 inches of house, so 4.27 inches per pixel (`A(ax,ay)` in the
  page converts). The lot outline is drawn to the parcel map's lengths (70 ft street side, 59 ft back, 118 ft east
  side, 123 ft west side), because the owner wants known measurements to set the scale; the aerial only positions
  and squares it (the traced outline came out 68, 62 and 117 ft, so the two agree). Driveway, front planting bed, back patio with its path down
  the west side of the lawn, and the lawn are traced from it, good to roughly 3 ft. A first attempt from a rotated
  aerial produced a badly slanted lot and was discarded: do not trace from a rotated photo. The garage has no door
  into the house (owner confirmed). The plan's west "patio" looks like bare ground in the aerial.
- **Layout options** (`DESIGNS`, Design tab; "As planned" switches them off in one click). Each keeps its own saved
  item list in `layouts`.
  - Dear Modern: Cliff Tan's rules as reported in a Tatler Asia interview and a Bustle piece (bed must not face the
    door, command position for desk and sofa, no mirror pointing at the bed). Uses the 72 inch desk floated to face
    the door. Known problems are written in the option's notes (sofa overlaps the hall opening as drawn).
  - Emily Henderson: her published numbers (sofa about 7 ft from TV, 30-36 inch walkways, 36 inches around the bed,
    24 inches around the dining table, rug sizes) from her living room, bedroom and dining rules pages.
  - Open living: utility closet by the foyer removed (`OPEN_ROOMS`). Always flag that the closet may hold a furnace
    or water heater and a wall may be load-bearing; a contractor has to confirm.
  These are Claude's reading of published rules, not the designers' work. Only cite rules found on a fetched page.
- **Interface:** the owner asked for "apple simple UI UX but keep the functionality". One panel, four tabs (View,
  Design, Items, Check), system font, segmented controls, switches; the selected item's card floats over the view.
  Keep new controls inside this structure instead of adding sections.

### Layout rework, lights and camera (2026-11-15, later)

Owner feedback that shaped this, keep honouring it:

- Layout options may add new pieces, swap or remove existing ones, and should be detailed: "don't be restricted to
  the things we already have in there", except fixed things like the fireplace. They cover the yard too.
- He likes the desk facing the door (Dear Modern) but it must never block the loveseat's view of the TV.
- "I really am beginning to hate that tree in there": the tall plant is out of the office (now in the living room).
- "Closet doors should be a choice": Design tab has primary (mirrored / plain white) and office (open / sliding).
- Open living removes the whole island (utility closet and pantry); the pantry becomes a tall cabinet at the end
  of the kitchen's sink run, "the far left corner when you enter the kitchen from the foyer".
- Never block the living room's back door (north wall) with seating.
- The barrel sauna stands against the west fence at the line where the patio meets the lawn, not by the house.
- The real sectional is an L: one arm along the window wall, one facing the TV, with a separate ottoman.

What was built: `DESIGNS` options now use `add`, `rm`, `put`; per-layout closet choices live in `opts`; new catalog
pieces come from real listings in `PRODUCTS` (four have sizes not confirmed on the product page and say so).
Lights from the owner's photos: `HOUSE_LIGHTS` plus fixtures in `buildFixed()`, a flickering fireplace, and a sun
that casts through windows (walls and ceilings cast shadows; shadows are redrawn only when something changes, and
sun shadows are off in overhead views). Sunlight comes from the back-yard side. Camera: the turning point is moved
to the floor spot being looked at after every drag, zoom or walk (`reanchor`), zoom goes toward the cursor, and
walking speed scales with camera height (Shift doubles it). Saved layouts are version 9; older saves are dropped.

## Rules for the model

1. Dimensional accuracy beats looks. Never say something fits until the fit check or a measurement shows it.
2. Every item is either the owner's own measurement or a real product found online, with its listed size and a link.
   Products live in `PRODUCTS` in the page; each catalog entry in `T` says where its size comes from, and the page
   shows that when an item is selected. Mark anything else as an estimate.
3. Style: walnut or dark wood, matte black hardware, charcoal and neutral gray fabric, warm practical lighting.
   A believable residential office, not a gaming room. Acoustic panels are optional and are not soundproofing.
4. The measured page is the ruler. Photoreal images are for mood: image models keep the layout but invent details.
5. Ask before anything that spends $1 or more, touches secrets, or cannot be undone.

## How the page is built

`R` = room measurements. `T` = catalog of item types (size, source, builder function). `defaults(deskWidth)` = the
starting layout. `items` = what is in the room now (saved per browser in localStorage). `fit()` = the fit check.
`WALLS` = where wall-mounted items can go. `window.__room` exposes `exportGLB()`, `shot()`, `setView()` for the tools.
Walls are single-sided so they disappear when the camera is outside the room.

## Photoreal route (worked on 2026-11-14)

1. `node tools/export_scene.js office-room.html out door day`
2. `python3 tools/render_still.py out out/still.jpg 160 1600`
3. `python3 tools/photoreal.py out/still.jpg out/ai gpt26-flare` (or `seedream55`, `gpt26-sunburst`)

Result of the first test: Seedream 5.5 and GPT Image 2.6 Flare and Sunburst all kept the camera, room shape and
every item's place and looked like photographs (about 4 to 7 cents each). Drift: the floor went darker brown in all
three; Sunburst added a laptop, screen wallpapers and trees outside; Flare added a wall outlet. The Blender still on
its own was rejected as "not even close to photoreal": correct light, but simple shapes.

## Roadmap, in order

1. Owner's corrections to the guessed items above.
2. Real listings for the catalog gaps: keyboard bench (X-style), monitor arm, desk lamp, roller shade, guitar
   hangers, planter. Found but not wired in yet: Threshold adjustable desk lamp, Deconovo Aria motorized shade,
   MOUNTUP dual arm, String Swing hanger.
3. "Render this view": the owner names a view and light setting in chat, Claude runs the photoreal route.
4. VR on a Quest: the artifact viewer blocks headset mode, so host this page elsewhere (for example GitHub Pages
   from this repo), then test in the headset. Untested so far.
5. Small items that sit on furniture and move with it.
6. Furnish the other rooms: fixtures (kitchen, baths, fireplace) and furniture, from the owner's measurements or
   photos. Extend the fit check beyond the office. Tape-measure anything where an inch matters.

## Which model

Small tweaks (add or resize a catalog item, change a measurement in `R`, move something in `defaults()`, wording)
are fine on a cheaper model. Use the strongest model for new systems: VR hosting, room-shape changes, the render
pipeline.
