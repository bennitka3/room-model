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
- Guessed from photos, not measured: closet opening width and position (72 wide, starting 6 from the entry corner),
  door position on the far wall, chair size, the two ocean canvases (24 x 16), the glass cabinet (IKEA Detolf's
  listed size), guitar sizes.

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
6. Other rooms, once measured. A phone scan is fine for layout; tape-measure anything where an inch matters.

## Which model

Small tweaks (add or resize a catalog item, change a measurement in `R`, move something in `defaults()`, wording)
are fine on a cheaper model. Use the strongest model for new systems: VR hosting, room-shape changes, the render
pipeline.
