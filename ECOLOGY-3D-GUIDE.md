# ARKADU 3D ECOLOGY — Transect Engine

## What This Is

**A true 3D spatial environment for performing ecological transects across a media archive.**

Not folders. Not lists. Not hierarchies.

**A living landscape where chambers exist as geological strata that you orbit, slice, and traverse.**

---

## Core Concept: Chambers as Ecological Entities

### Each Chamber Is:

1. **A Species** - A unique form with its own characteristics
2. **A Habitat** - Contains other chambers (nested glyphs)
3. **A Stratum** - Exists at a specific depth (taxonomy level)
4. **A Node** - Connected via parent-child relationships and mycelial threads

### Visual Metaphor:

```
ROOT (Y=0)
  ↓
KINGDOMS (Y=250)    ← Depth 0: Biomes floating in orbit
  ↓
PHYLUMS (Y=500)     ← Depth 1: Nested structures
  ↓
CLASSES (Y=750)     ← Depth 2: Terminal chambers
```

**You orbit around this vertical stack, seeing all layers simultaneously.**

---

## The Four Modes

### 1. BIOME VIEW (Default)

**See the entire ecosystem as an orbiting structure**

- All chambers visible at once
- Arranged in circular formations per depth
- Rotate automatically or drag to orbit
- Zoom to inspect closely

**Purpose:** Feel the whole ecology, understand scale and distribution

### 2. STRATA VIEW

**Focus on horizontal slicing**

- Emphasizes depth layers
- Connections between depths become visible
- Parent-child relationships highlighted
- Like looking at geological core sample

**Purpose:** Understand taxonomic descent and branching

### 3. MYCELIUM

**Show ekphrasis chains as purple threads**

- Purple curved lines = prompt → script → media chains
- Reveals generative relationships
- Shows how text became image/video
- Network of transformation visible

**Purpose:** See operative ekphrasis ecology, trace media generation

### 4. TRANSECT MODE

**Horizontal plane slices through the space**

- Red translucent plane at adjustable Y height
- Shows only chambers that intersect the plane
- Reveals cross-sectional structure
- Like an ecologist's field transect

**Purpose:** Study distribution at specific depth, compare siblings

---

## Interaction Design

### Organic Gestures (No Menus)

**Mouse Drag:** Orbit around the structure
- Horizontal drag = rotate around Y axis
- Vertical drag = tilt view up/down

**Mouse Wheel:** Zoom in/out
- Closer = see chamber details and nested glyphs
- Farther = see whole ecosystem structure

**Click Chamber:** Focus and transclude
- Chamber highlighted (cyan border)
- Right panel slides open with full details
- Other chambers dim slightly
- Connections to this chamber emphasized

**No clicking through folders** - all navigation is spatial

### Bloom on Select

When you click a chamber:
1. **Border glows cyan** (focused state)
2. **Nested glyphs visible** inside (children as small colored squares)
3. **Transect panel opens** with complete details
4. **Related chambers connected** with emphasized lines

The chamber "blooms" to reveal its interior structure.

---

## Visual Encoding

### Color = Species (Dominant File Type)

```
Blue (#4dd9cc)      → Images (PNG/JPG)
Coral (#d97b8f)     → Video (MP4)
Amber (#e8b849)     → Audio/Code (MP3/PY)
Purple (#9d7be8)    → Data (JSON)
Green (#6bbd8f)     → Web (HTML)
```

Each chamber colored by its most common file type.

### Size = Population

- Chamber size ∝ √(artifact count)
- Larger boxes = more files
- See density distribution instantly

### Position = Taxonomy

- **X/Z plane:** Siblings arranged in circle
- **Y axis:** Depth in taxonomy (0, 250, 500)
- **Spatial proximity** = taxonomic relationship

### Nested Glyphs = Children

Inside each chamber, small colored squares show children:
- Up to 9 glyphs visible
- Each glyph colored by child's dominant species
- Hover to see name
- Click to zoom to that child

**This is the key innovation:** You see chambers-within-chambers without descending.

---

## The Transect Panel (Right Side)

### Opens When Chamber Clicked

**Displays:**
- Chamber name & metadata
- Depth, artifact count, total size
- Dominant species
- **Nested Chamber Glyphs** - Click to jump to child
- **Mycelial Connections** - Ekphrasis chain count
- **Parent Link** - Click to ascend

**This is transclusion** - the chamber's full contents brought into view without navigation.

---

## Controls (Bottom Right)

### Live Adjustment Sliders

**Rotation:** 0-20
- Auto-rotation speed
- Set to 0 to stop, drag manually

**Depth Separation:** 100-500px
- Vertical spacing between depth layers
- Compress to see flat, expand to see stacked

**Chamber Scale:** 5-30
- Multiplier for chamber sizes
- Larger = easier to see details
- Smaller = see more chambers at once

**Transect Height:** -200 to 600
- Y position of transect plane (if enabled)
- Slice at any height to see cross-section

All changes are **live** - no reload needed.

---

## Taxonomic Awareness

### Always Know Where You Are

**HUD (Top Left) Shows:**
- **Current Depth:** Which layer you're observing
- **Focus:** Which chamber is selected
- **Taxonomy:** Full lineage path

**Example:**
```
Current Depth: Depth 1
Focus: WHISKER
Taxonomy: L0: CAT > L1: WHISKER
```

### Ancestry Trails

When chamber focused:
- Parent shown in taxonomy
- Children shown as nested glyphs
- Siblings visible in same circular ring
- Full descent path reconstructable

---

## Real 3D Spatial Implementation

### Not Fake 3D

This uses real 3D math:
1. Chambers positioned in (x, y, z) space
2. Camera rotates around origin
3. 3D → 2D projection with perspective
4. Z-sorting for correct occlusion
5. Scale based on distance (perspective)

### Rotation Math

```javascript
// Rotate around Y axis (horizontal orbit)
x' = x * cos(rotY) - z * sin(rotY)
z' = x * sin(rotY) + z * cos(rotY)

// Rotate around X axis (tilt)
y' = y * cos(rotX) - z' * sin(rotX)
z'' = y * sin(rotX) + z' * cos(rotX)

// Project to 2D
scale = cameraZ / (cameraZ + z'')
screenX = centerX + x' * scale
screenY = centerY - y' * scale
```

This creates **true depth perception** - chambers farther away are smaller and occluded.

---

## Comparing the 3 Systems

### ecology-pro.html
- Click through folders
- One chamber at a time
- Traditional file explorer mindset
- Species filtering
- Good for: Detailed browsing

### ecology-spatial.html
- Multiple views (Landscape, Strata, Flow, Galaxy)
- All kingdoms visible
- Still somewhat flat
- Good for: Overview and patterns

### ecology-3d.html ⭐ THIS
- **True 3D continuous space**
- **Orbit around vertical stack**
- **Chambers-within-chambers visible**
- **Transect slicing**
- **Mycelial threads**
- **No navigation - pure exploration**
- Good for: **Spatial comprehension, ecological understanding**

---

## Use Cases

### 1. Understanding Distribution

**Task:** Where are the video files concentrated?

**Action:**
1. Look for coral-colored chambers
2. Orbit to see all angles
3. Notice DOG kingdom has many coral chambers at depth 2
4. Transect slice at Y=500 to see all depth-2 videos

### 2. Tracing Generation

**Task:** How did this image get created?

**Action:**
1. Enable MYCELIUM mode
2. Find chamber containing the image
3. Follow purple thread backward
4. See JSON prompt → Python script → Image output
5. Click each to see details

### 3. Comparing Kingdoms

**Task:** How does CAT compare to JELLYFISH?

**Action:**
1. Zoom out to see both kingdoms
2. Note sizes (CAT larger)
3. Note colors (CAT more blue, JELLYFISH more purple)
4. Count nested glyphs (CAT has more children)
5. No need to click into either - see from outside

### 4. Finding Sparse Strata

**Task:** Which areas have few files?

**Action:**
1. Orbit entire structure
2. Look for small chambers
3. Enable TRANSECT mode
4. Slice at each depth
5. See which rings have gaps

---

## Technical Architecture

### Data Loading

```javascript
1. Load primitive.jsonl (10,094 artifacts)
2. Load ekphrasis.jsonl (223 chains)
3. Build chamber hierarchy (auto-detect from paths)
4. Position chambers in 3D space
   - Circular arrangement per depth
   - Y = depth * depthSeparation
5. Calculate dominant species per chamber
6. Render continuously at 60 FPS
```

### Performance

- **Canvas rendering** (not DOM)
- **Z-sorting** for correct depth
- **60 FPS** smooth rotation
- **Handles 312 chambers** easily
- **Hover detection** via bounding box test
- **Adaptive detail** (labels only when close)

### Memory Footprint

- ~30 MB in browser
- All chamber data in RAM
- Canvas 2D (not WebGL, lighter)
- No texture loading (vector only)

---

## Aesthetic Principles

### 1. Organic Minimalism

- Clean geometric forms (squares, circles)
- Natural flow (orbiting, not snapping)
- Depth and translucency
- No clutter

### 2. Translucency & Depth

- Chambers semi-transparent
- Opacity based on distance
- Shadow effect for depth
- Overlapping creates layers

### 3. Spatial Relation Over List

- Proximity = relationship
- Vertical = taxonomic descent
- Horizontal = sibling clusters
- Lines = explicit connections

### 4. Color as Signal

- Not decoration
- Immediate species recognition
- Consistent across all views
- Follows natural associations (blue=water=image flow)

---

## The Transect Metaphor

### What Is an Ecological Transect?

In field ecology, a **transect** is:
- A line or plane through an environment
- Used to sample and count species
- Reveals distribution patterns
- Repeated at different locations to compare

### Digital Transect Here:

- **Horizontal plane** (adjustable Y height)
- **Slices through 3D chamber space**
- **Shows cross-section** at that depth
- **Reveals patterns:**
  - Which chambers exist at this level?
  - How are they distributed?
  - What species dominate?
  - Are there gaps or clusters?

**Enable with:** TRANSECT MODE button
**Adjust with:** Transect Height slider
**Visual:** Red translucent plane with chambers intersecting it

---

## Cultivation Metaphor

### You Are an Archivist-Ecologist

Not managing files. **Cultivating an ecology.**

**Your tools:**
- **Orbit** - Walk around the field
- **Zoom** - Kneel to inspect closely
- **Transect** - Cut a soil core sample
- **Mycelium** - Reveal underground networks
- **Bloom** - Open a specimen to see interior

**Your understanding grows through:**
- Spatial memory (I know CAT is over there)
- Pattern recognition (Videos cluster at depth 2)
- Relationship mapping (WHISKER descends from CAT)
- Network awareness (This prompt generated that video)

### Not Hierarchy - Topology

Traditional: ROOT → FOLDER → SUBFOLDER → FILE
- Linear descent
- One path to each item
- No lateral connections
- Feels like navigating a maze

Ecological: BIOME ⊃ HABITAT ⊃ SPECIES ⊃ SPECIMENS
- Spatial coexistence
- Multiple perspectives possible
- Connections visible
- Feels like exploring a landscape

---

## Keyboard/Mouse Map

```
DRAG         → Orbit camera
SCROLL       → Zoom in/out
CLICK        → Focus chamber (transclude)
ESC/X        → Close transect panel

(No keyboard shortcuts needed - all spatial)
```

---

## Comparison to Traditional Interfaces

### File Explorer (Finder/Explorer)
```
ROOT
└── CAT
    ├── WHISKER
    │   ├── file1.png
    │   └── file2.mp4
    └── PAW
        └── file3.json
```
- Nested lists
- One folder at a time
- Click to descend
- Click back to ascend
- No spatial memory
- No pattern visibility

### ARKADU 3D Ecology
```
     (orbit view)
    ╱───────────╲
   │     CAT     │ ← Y=0
   │  [WHISKER]  │   nested glyphs visible
   │    [PAW]    │
    ╲───────────╱
         ↓
    ╱──────╲
   │WHISKER│ ← Y=250
    ╲──────╱
```
- Spatial arrangement
- All depths visible
- No clicking to navigate
- Orbit to explore
- Spatial memory builds
- Patterns immediately visible

---

## Future Enhancements

### Possible Extensions

1. **VR/AR Mode**
   - Walk through chambers
   - Reach out and touch
   - Life-size or miniature

2. **Time Dimension**
   - Animate file creation over time
   - Watch ecology grow
   - Seasonal patterns

3. **Gravity Simulation**
   - Chambers attract/repel
   - Form natural clusters
   - Emergent organization

4. **Audio Spatialization**
   - Each chamber emits sound
   - Closer = louder
   - Species-specific tones

5. **Collaborative Exploration**
   - Multiple users in same space
   - See others' cursors
   - Shared annotations

6. **Generative Terrain**
   - Chambers grow/shrink
   - Connections strengthen/weaken
   - Living system

---

## How to Use (Step by Step)

### First Time Opening

1. **Wait for load** (5-10 seconds)
   - 10,094 artifacts being positioned
   - Progress bar shows status

2. **See the biome**
   - Chambers orbiting slowly
   - Three distinct depth layers
   - Colors indicate species

3. **Drag to explore**
   - Move mouse to orbit
   - All chambers visible from different angles

4. **Click a large chamber** (probably CAT or DOG)
   - Right panel opens
   - See metadata and nested glyphs
   - Notice children shown as small squares

5. **Click a nested glyph**
   - Jump to that child chamber
   - Now focused on depth 1
   - Parent still visible above

6. **Try MYCELIUM mode**
   - Click button in HUD
   - Purple threads appear
   - Ekphrasis chains revealed

7. **Enable TRANSECT**
   - Horizontal slice appears
   - Adjust height slider
   - See cross-sections at different depths

### Daily Usage

**Just orbit and click.** That's it.

No menu navigation. No folder clicking. Pure spatial exploration.

---

## Access

**URL:** http://localhost:8001/ecology-3d.html

**Requirements:**
- Modern browser (Chrome, Firefox, Safari, Edge)
- HTTP server running on port 8001
- Mouse or trackpad

**Performance:**
- Smooth on most hardware
- 60 FPS target
- Tested with 312 chambers, 10K+ artifacts

---

## Status

✅ **FULLY OPERATIONAL**

**Currently loaded:**
- 10,094 artifacts
- 312 chambers (automatic hierarchy)
- 223 ekphrasis chains
- Real 3D positioning
- Live transclusion
- Mycelial network

**Ready for:**
- Ecological fieldwork
- Spatial comprehension
- Pattern discovery
- Taxonomic study
- Transect analysis
- Media archaeology

---

*ARKADU 3D ECOLOGY v1.0*  
*Transect Engine • Spatial Archive • Chamber Ecology*  
*See the Archive as a Living Landscape*
