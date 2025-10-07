# ARKADU DECKS — Spatial Navigation System

## What This Is

**DECKS = The Void/Frame against which chambers and species are rendered**

This system implements TWO spatial navigation models for exploring ARKADU's 10,097 artifacts across nested chamber hierarchies.

---

## Core Ontology

```
DECK          → The spatial layer itself (the void, the backdrop, the stage)
  ↓ contains
CHAMBERS      → Worlds/rooms that exist ON a deck
  ↓ contains
SPECIES       → Media types that live IN chambers (.png, .mp4, .json, etc.)
  ↓ contains
GRAINS        → Individual files (the atoms)
```

**Key insight:** DECKS are not containers—they are SUBSTRATE. Everything else is content rendered against the void.

---

## MODEL 1: DEPTH DECKS (Vertical Archaeology)

**Metaphor:** Archaeological strata stacked vertically

### How It Works

```
╔═══════════════════════════════════╗
║ DECK 0: SURFACE (Kingdoms)       ║  ← You are here
║ ┌─────┐  ┌─────┐  ┌─────┐       ║
║ │ CAT │  │ DOG │  │ ANT │       ║
║ └─────┘  └─────┘  └─────┘       ║
╚═══════════════════════════════════╝
         ↓ DESCEND into CAT
╔═══════════════════════════════════╗
║ DECK 1: CAT LAYER                ║  ← Now here
║ ┌────────┐  ┌─────┐              ║
║ │WHISKER │  │ PAW │              ║
║ └────────┘  └─────┘              ║
╚═══════════════════════════════════╝
         ↓ DESCEND into WHISKER
╔═══════════════════════════════════╗
║ DECK 2: WHISKER LAYER            ║  ← Now here
║  🔵🔵🔵  🔴🔴  🟡🟡🟡          ║  Species grains
║  PNG    MP4   JSON               ║
╚═══════════════════════════════════╝
```

### Navigation

- **← Left Arrow** or **◀ PREV** → Go to parent deck (ascend)
- **→ Right Arrow** or **NEXT ▶** → Go to first child deck (descend)
- **↑ Up Arrow** or **↑ UP** → Go to parent deck (ascend)
- **Click portal** → Descend into that specific chamber
- **Click grain** → Inspect artifact

### Visual System

**Three panels always visible:**
- **Prev** (parent deck, 30% left, 85% scale, 30% opacity)
- **Curr** (current deck, centered, 100% scale, full opacity)
- **Next** (child deck preview, 30% right, 85% scale, 30% opacity)

**This creates depth perception** - you can see where you came from and where you can go.

### Use Case

- **Archaeological excavation** - digging through nested layers
- **Hierarchical exploration** - clear parent→child structure
- **System archaeology** - treating file system as geological strata

---

## MODEL 2: PARALLEL DECKS (Horizontal Multiverse)

**Metaphor:** Parallel universes arranged spatially

### How It Works

```
     DECK: CAT           DECK: DOG           DECK: ANT
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │ WHISKER     │    │ BARK        │    │ COLONY      │
  │ 🔵🔵🔵     │    │ 🔴🔴🔴     │    │ 🔵🔵🔵     │
  │ PAW         │    │ BONE        │    │ QUEEN       │
  │ 🟡🟡       │    │ 🟡🟡       │    │ 🟣🟣       │
  └─────────────┘    └─────────────┘    └─────────────┘
       ↑                  ↑                   ↑
    All visible, one focused
```

### Navigation

- **◀ Left** → Pan to previous sibling deck
- **▶ Right** → Pan to next sibling deck
- **ENTER** → Descend into focused deck (chambers become new decks)
- **Click deck** → Focus on that deck
- **Arrow keys** → Navigate between decks

### Nested Transformation

When you ENTER a deck, its chambers become new decks:

```
Before (Kingdom level):
CAT deck | DOG deck | ANT deck

After (ENTER CAT):
WHISKER deck | PAW deck | TAIL deck
  ↑ Chambers are now decks
```

### Visual System

**Multiple decks arranged horizontally:**
- **Focused deck** → Full opacity, glowing border, centered
- **Other decks** → 50% opacity, blurred, visible alongside

**You can see ecosystem relationships** between siblings.

### Use Case

- **Comparing multiple kingdoms** simultaneously
- **Seeing ecosystem structure** spatially
- **Non-hierarchical navigation** - jump between any visible deck
- **Spatial memory building** - "CAT is to the left of DOG"

---

## Data Source

**Loads from actual ARKADU data:**
- `/sys/primitive.jsonl` → 10,097 artifacts
- Builds chamber hierarchy automatically from file paths
- Respects actual data structure (CAT: 1,981 files, DOG: 1,233, etc.)
- Species extracted from file extensions

**Data format respected:**
```json
{
  "path": "CAT/WHISKER/MEDIA/file.png",
  "name": "file.png",
  "size": 2345678,
  "ext": "png",
  "depth": 3
}
```

---

## Interface Components

### Left Sidebar: Navigation

**Kingdoms List**
- Shows all depth-0 chambers (kingdoms)
- Click to jump directly to that kingdom
- Sorted by artifact count (largest first)
- Active kingdom highlighted

**Species Filter**
- Checkboxes for each file type (.png, .mp4, .json, etc.)
- Click to toggle filter
- Shows count per species
- Color-coded by species type

### Center: Deck Stage

**DEPTH Mode (default):**
- Carousel of 3 decks (prev/curr/next)
- Grid background (spatial reference)
- Species clusters (colored dot groups)
- Portal chambers (doorways to sub-decks)
- Controls at bottom (navigation)

**PARALLEL Mode:**
- Multiple decks visible side-by-side
- 3D perspective view
- Focused deck highlighted
- Click to change focus
- Enter to descend

### Right Sidebar: Inspector

**Shows selected grain details:**
- Artifact name
- Species (file type)
- Size (KB)
- Chamber location
- Full path

**Future:** Will show connections, chains, references

### Top Header

**Brand** + **Mode Toggle** + **Stats**
- Switch between DEPTH/PARALLEL modes
- See total chambers, artifacts, current depth

### Bottom Footer

**Breadcrumb** + **Status**
- Current path (e.g., "CAT > WHISKER > MEDIA")
- Selection info

---

## Color System

### Species Colors

```
Blue (#4dd9cc)    → .png, .jpg (images)
Coral (#d97b8f)   → .mp4 (video)
Amber (#e8b849)   → .mp3, .py (audio, code)
Purple (#9d7be8)  → .json (data)
Green (#6bbd8f)   → .html (web)
Dim (#6b8a96)     → .txt, other
```

**Why these colors?**
- High contrast against dark void
- Distinct from each other
- Intuitive associations (blue=images, red=video)
- Neon/cyberpunk aesthetic

---

## Technical Implementation

### Data Loading

```javascript
// Loads real ARKADU data
fetch('/sys/primitive.jsonl')
  → Parse JSONL
  → Build chamber hierarchy from paths
  → Extract species from extensions
  → Render decks
```

### Chamber Building

```javascript
// Automatic hierarchy from file paths
"CAT/WHISKER/MEDIA/file.png"
  → Chamber: "CAT" (depth 0)
  → Chamber: "CAT/WHISKER" (depth 1)
  → Chamber: "CAT/WHISKER/MEDIA" (depth 2)
  → Artifact: file.png (in MEDIA chamber)
```

### Deck Rendering

```javascript
// Each deck = canvas with:
- Grid background (spatial reference)
- Species clusters (positioned algorithmically)
- Portal chambers (navigation doorways)
- Grains (individual files, max 100 per species for performance)
```

### State Management

```javascript
state = {
  mode: 'depth' | 'parallel',
  chambers: [],      // All chambers
  artifacts: [],     // All artifacts
  current: 'CAT',    // Current chamber ID
  path: ['CAT'],     // Navigation path
  filters: Set(),    // Active species filters
  selected: null     // Selected grain
}
```

---

## Keyboard Shortcuts

**Universal:**
- `←` Left Arrow → Go to previous/parent
- `→` Right Arrow → Go to next/child
- `↑` Up Arrow → Go to parent

**DEPTH Mode:**
- `←` → Ascend to parent deck
- `→` → Descend to first child deck
- `↑` → Ascend to parent deck

**PARALLEL Mode:**
- `←` → Pan left to previous sibling
- `→` → Pan right to next sibling
- `↑` → (planned: exit to parent level)

---

## How DECKS Work

### The Void Concept

**DECK is not a container—it's a STAGE:**

```
Traditional thinking:
  Folder contains files

Deck thinking:
  Void against which chambers are rendered
  Chambers appear ON the deck
  Species live IN the chambers
  Grains exist as the chambers
```

**The deck is the backdrop, the frame, the spatial layer itself.**

### Spatial Memory

**Why this matters:**

Traditional file navigation:
```
/CAT/WHISKER/MEDIA/file.png
```
→ Abstract path, no spatial component

Deck navigation:
```
"I descended two decks into CAT,
 panned to the WHISKER chamber,
 entered MEDIA,
 and found the PNG cluster in the top-left"
```
→ Spatial memory, physical location

**Humans remember PLACES, not PATHS.**

---

## Comparison to Other ARKADU Systems

### vs Navigator (navigator.html)

**Navigator:**
- Text-based file list
- Hyperlink following
- Transclusion (full content)
- Connection panel

**Decks:**
- Spatial visualization
- Physical navigation
- Cluster view (grains as dots)
- Deck-based exploration

**Use Navigator for:** Reading complete files, following links
**Use Decks for:** Understanding structure, spatial exploration

### vs Ecology (ARKADU-ECOLOGY.html)

**Ecology:**
- 4 view modes (Grid, Nested, Flow, Ecology)
- Animated particles
- Species filtering
- Ecosystem metaphor

**Decks:**
- 2 navigation modes (Depth, Parallel)
- Deck-based layers
- Chamber-centric
- Archaeological metaphor

**Use Ecology for:** Visual ecosystem overview
**Use Decks for:** Hierarchical navigation

### vs TRUE-ARKADU

**TRUE-ARKADU:**
- Window system
- Full source code
- Dependency graph
- Multi-file view

**Decks:**
- Deck system
- Grain clusters
- Chamber navigation
- Single-focus view

**Use TRUE-ARKADU for:** Code reading
**Use Decks for:** Spatial exploration

---

## Future Enhancements

### Planned Features

**Connections Between Decks:**
- Draw SVG arcs between grains across decks
- Show ekphrasis chains vertically
- "This grain on deck 1 generated that grain on deck 2"

**Deck Rotation (Parallel mode):**
- 360° rotation around central axis
- More than 5 decks visible
- Carousel of sibling decks

**Zoom into Grains:**
- Click grain → grain becomes chamber
- Chamber becomes deck
- Infinite zoom (fractal navigation)

**Time Dimension:**
- Animate file creation over time
- Grains "born" and appear on decks
- Watch system grow through history

**3D Depth View:**
- Use WebGL for true 3D rendering
- Navigate in Z-axis (true depth)
- Rotate camera freely

**Multi-Deck Selection:**
- Select multiple decks
- Compare side-by-side
- Diff between decks

---

## Known Limitations

1. **Max 100 grains per species** (performance)
   - Shows sample of larger clusters
   - Full count displayed in label

2. **Max 3 depth levels** (clarity)
   - Deeper hierarchies collapsed
   - Can navigate deeper but shown at level 3

3. **Parallel mode shows max 5 decks** (screen space)
   - Can pan between more
   - Only 5 visible at once

4. **No connections drawn yet** (MVP)
   - Will add ekphrasis chains
   - Will show references between grains

---

## Access

**Open via HTTP server:**
```
http://localhost:8001/decks.html
```

**⚠️ MUST use HTTP, not file://**

Server already running on port 8001.

---

## Quick Start

1. **Open** http://localhost:8001/decks.html
2. **See DEPTH mode** by default
3. **Click arrows** or use keyboard to navigate decks
4. **Click PARALLEL** button to switch modes
5. **Click species chips** to filter by type
6. **Click grains** to inspect artifacts
7. **Click portals** to descend into chambers

---

## Status

✅ **OPERATIONAL**

**Currently loaded:**
- Real ARKADU data (10,097 artifacts)
- Automatic chamber hierarchy
- Both DEPTH and PARALLEL modes
- Species filtering
- Grain inspection
- Keyboard navigation

**Ready for:**
- Spatial exploration
- Hierarchical navigation
- Chamber archaeology
- Species visualization
- System comprehension

---

*ARKADU DECKS v1.0*  
*Spatial Navigation • Depth Archaeology • Parallel Multiverse*  
*DECKS = The Void Against Which All Is Rendered*
