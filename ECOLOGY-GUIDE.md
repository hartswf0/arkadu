# ARKADU ECOLOGY - Visual Ecosystem Guide

## What This Is

**ARKADU ECOLOGY** visualizes your media as a **living ecosystem** where:
- Each file is an **organism** (colored dot/particle)
- File types are **species** (.mp4, .png, .json, .py)
- Directories are **chambers** (habitats/grid worlds)
- Files can be seen **flowing, clustering, nesting**
- You can **filter by species** and explore the ecology

---

## 4 View Modes

### 1. GRID VIEW 🔲
**Chambers as grid worlds with organisms**

- Each chamber is a tile/grid
- Organisms (files) placed in grid cells
- Colored by species (file type)
- Size = file size

**Use for:**
- Seeing density of files in chambers
- Comparing chamber populations
- Finding which chambers have which species

**Controls:**
- Click chamber name (left panel) to focus on it
- Filter species (checkboxes) to see only certain types

### 2. NESTED VIEW 📦
**Hierarchical chambers within chambers**

- Kingdoms contain phylums contain classes
- Recursive nesting visualization
- Organisms shown as tiny squares
- Depth configurable (1-5 levels)

**Use for:**
- Understanding hierarchy
- Seeing nested structure
- Comparing depths

**Controls:**
- Adjust "Chamber Depth" slider to see deeper levels
- Each nested box contains its children

### 3. FLOW VIEW 💫
**Organisms flowing through ecosystem (ANIMATED)**

- Particles move continuously
- Bounce off edges
- Represent living system
- Colored by species

**Use for:**
- Visualizing ecosystem as alive
- Seeing distribution dynamically
- Getting sense of scale/motion

**Controls:**
- Runs automatically (animated)
- Filter species to see certain types flow
- Particle size slider adjusts organism size

### 4. ECOLOGY VIEW 🌐
**Species clusters showing ecosystem structure**

- Each species forms a cluster
- Arranged in circle
- Shows relationships
- Living ecosystem metaphor

**Use for:**
- Comparing species populations
- Seeing ecosystem balance
- Understanding species distribution

**Controls:**
- Species automatically cluster
- Filter to show/hide species
- Hover over organisms for details

---

## Controls Explained

### Species Filter (Left Panel)

**Checkboxes for each file type:**
- ☑ .mp4 (Magenta) - Videos
- ☑ .png (Cyan) - PNG images
- ☑ .jpg (Blue) - JPG images
- ☑ .wav (Yellow) - Audio WAV
- ☑ .mp3 (Orange) - Audio MP3
- ☑ .json (Pink) - Data files
- ☑ .py (Green) - Python code
- ☑ .html (Teal) - Web pages
- ☑ .md (Lime) - Markdown docs
- ☑ .js (Yellow-green) - JavaScript

**Check/uncheck to filter:**
- ✓ Checked = species visible
- ☐ Unchecked = species hidden

### View Depth Slider

**Chamber Depth: 1-5**
- **1** = Kingdoms (ANT, CAT, DOG, HORSE...)
- **2** = Phylums (CAT/WHISKER, CAT/PAW...)
- **3** = Classes (CAT/WHISKER/MEDIA...)
- **4** = Orders
- **5** = Families

**Use to:**
- Navigate hierarchy
- See deeper nesting
- Focus on specific level

### Particle Size Slider

**Organism Size: 1-10**
- Small = harder to see, less cluttered
- Large = easier to see, more visible

**Adjust for:**
- Visibility
- Aesthetic preference
- Screen resolution

### Chamber List

**Click chamber names to focus:**
- Shows only that chamber
- Grid view zooms to chamber
- Click again to un-focus

---

## Color Coding

### Species Colors

```
Videos:
  .mp4  → Magenta/Purple

Images:
  .png  → Cyan
  .jpg  → Blue

Audio:
  .wav  → Yellow
  .mp3  → Orange

Data:
  .json → Pink

Code:
  .py   → Green
  .js   → Yellow-Green

Web:
  .html → Teal

Docs:
  .md   → Lime
```

### Why These Colors?

- **High contrast** against black background
- **Distinct** from each other
- **Intuitive** (green = code, cyan = images, etc.)
- **Neon/terminal aesthetic** (fits ARKADU style)

---

## Interaction

### Hover Over Organisms

**Tooltip appears showing:**
- File name
- Species (extension)
- Size (KB)
- Chamber (location)
- Full path

**Works in all view modes**

### Click Chambers

**In Chamber List:**
- Click to focus on that chamber
- Grid view shows only that chamber
- Click again to return to all chambers

### Filter Species

**Check/uncheck boxes:**
- Immediately filters view
- Organisms disappear/appear
- Header shows count (e.g., "5,234 / 10,097 organisms visible")

---

## Understanding the Ecology

### What Are "Organisms"?

**Each file = an organism:**
- Has a species (file type)
- Lives in a chamber (directory)
- Has a size (file size → organism size)
- Has a color (species color)
- Exists in ecosystem

### What Are "Chambers"?

**Directories = chambers:**
- Habitat for organisms
- Can contain multiple species
- Nested within each other
- Form hierarchy (taxonomy)

### What Are "Species"?

**File types = species:**
- .mp4, .png, .json, .py, etc.
- Distinct characteristics
- Different populations
- Can coexist in chambers

### Ecosystem Metaphor

**The visualization shows:**
- **Population**: How many of each species
- **Distribution**: Where species live
- **Density**: How crowded chambers are
- **Hierarchy**: How chambers nest
- **Diversity**: Mix of species in chambers

---

## Use Cases

### 1. Find Storage Hotspots

**Goal:** See where most data lives

**Steps:**
1. Go to GRID view
2. Look at chamber sizes
3. See which have most organisms
4. Check organism sizes (bigger = larger files)

**Insight:** Largest chambers = storage optimization targets

### 2. Analyze Species Distribution

**Goal:** See where each file type lives

**Steps:**
1. Go to ECOLOGY view
2. See species clusters
3. Check cluster sizes
4. Filter to single species
5. Go to GRID view to see distribution

**Insight:** Where do videos live vs images vs code?

### 3. Explore Hierarchy

**Goal:** Understand nested structure

**Steps:**
1. Go to NESTED view
2. Adjust depth slider (1-5)
3. See recursive nesting
4. Identify deep vs shallow chambers

**Insight:** How deep is your file hierarchy?

### 4. Compare Species Populations

**Goal:** How many files of each type?

**Steps:**
1. Look at Species Filter counts
2. Go to ECOLOGY view
3. Compare cluster sizes
4. Filter different combinations

**Insight:** Videos few but large, images many but small

### 5. Visualize System as Alive

**Goal:** See ecosystem dynamically

**Steps:**
1. Go to FLOW view
2. Watch organisms move
3. Filter different species
4. Adjust particle size

**Insight:** System feels organic, alive, flowing

---

## Technical Details

### Data Source

**Reads from:** `ARKADU/sys/primitive.jsonl`

**Contains:**
- 10,097 artifacts (files)
- Full metadata (path, size, extension, depth)
- Pattern detection
- Prompt detection

### Rendering

**Canvas-based:**
- HTML5 Canvas for graphics
- 60 FPS in FLOW view
- Instant rendering in static views
- Smooth interactions

### Performance

**Handles:**
- 10,000+ particles
- Real-time filtering
- Smooth animations
- Instant species toggle

### Species Detection

**Automatic:**
- Reads file extension from data
- Maps to color palette
- Counts per species
- Filters on demand

---

## View Mode Details

### GRID Mode Algorithm

1. Load chambers at selected depth
2. If chamber selected → show only that one
3. Else → tile all chambers
4. For each chamber:
   - Draw border and label
   - Filter organisms by selected species
   - Arrange in grid (sqrt algorithm)
   - Draw organisms as circles
   - Size by file size

### NESTED Mode Algorithm

1. Start with kingdoms (depth 1)
2. For each kingdom:
   - Draw outer box
   - Draw organisms inside
   - Recurse into children (up to 3 levels)
   - Each child gets 1/4 of parent space
3. Alpha decreases with depth (fade effect)

### FLOW Mode Algorithm

1. Initialize particles with random velocities
2. Each frame:
   - Update positions (x += vx, y += vy)
   - Bounce off edges
   - Draw particles
   - Request next frame
3. Continuous animation loop

### ECOLOGY Mode Algorithm

1. Group particles by species
2. Arrange species in circle (polar coordinates)
3. For each species cluster:
   - Calculate cluster center
   - Arrange organisms in sub-circle
   - Draw with species color
   - Label cluster

---

## Future Enhancements

### Planned Features

- [ ] **Operative Ekphrasis Chains** - Show which code generated which media
- [ ] **Connections/Links** - Draw lines between related files
- [ ] **Time Animation** - Show files appearing over time (by mtime)
- [ ] **Interaction Simulation** - Files "eat" each other (code generates media)
- [ ] **Birth/Death** - Animation of file creation/deletion
- [ ] **Energy Flow** - Visualize data flowing through system
- [ ] **Zoom/Pan** - Navigate large hierarchies
- [ ] **Search** - Find specific files in visualization
- [ ] **Export** - Save frames as images
- [ ] **3D View** - Depth represented in Z axis

---

## Troubleshooting

### "No organisms visible"

**Problem:** All species unchecked

**Solution:** Check at least one species checkbox

### "Chamber list empty"

**Problem:** No chambers at selected depth

**Solution:** Adjust depth slider to 1

### "Tooltip not showing"

**Problem:** Not hovering directly over organism

**Solution:** Move mouse slowly over dots

### "FLOW view not animating"

**Problem:** Browser tab not active

**Solution:** Click on browser window to activate

### "Too many organisms, can't see"

**Problem:** Overcrowding

**Solution:**
- Filter to fewer species
- Reduce particle size slider
- Focus on single chamber
- Try NESTED view instead

---

## Integration with Other Tools

### Use with TRUE-ARKADU

1. Find interesting files in ECOLOGY view
2. Note file names
3. Switch to TRUE-ARKADU.html
4. Search for those files
5. Open in windows to read content

### Use with Terminal

1. Identify chambers in ECOLOGY
2. Note chamber names
3. Switch to shell/terminal.html
4. Navigate to those chambers
5. See detailed statistics

### Use with Analysis

1. Spot patterns in ECOLOGY
2. Run analysis scripts to quantify
3. Cross-reference findings
4. Generate reports

---

## Examples

### Example 1: Find Video Hotspots

```
1. Open ARKADU-ECOLOGY.html
2. Uncheck all species except .mp4
3. Go to GRID view
4. See which chambers have most videos
5. Result: MANTA/final has most (28 videos, 6.91 GB)
```

### Example 2: Explore Image Distribution

```
1. Check only .png and .jpg
2. Go to ECOLOGY view
3. See huge cluster (7,282 images)
4. Go to NESTED view
5. See images spread across all chambers
6. Insight: Images everywhere, videos concentrated
```

### Example 3: Code vs Data

```
1. Check only .py and .json
2. Go to GRID view with depth 1
3. See code and data distributed similarly
4. Go to ECOLOGY view
5. Result: 256 Python, 704 JSON (data > code)
```

---

## Status

✅ **OPERATIONAL**

**Currently showing:**
- 10,097 organisms
- 15 species
- 320 chambers
- 4 view modes
- Interactive filtering
- Real-time visualization

**Ready for:**
- Exploration
- Analysis
- Documentation
- Presentation

---

*ARKADU ECOLOGY v1.0*  
*Living Media Ecosystem Visualization*  
*Chambers · Species · Organisms · Flow*
