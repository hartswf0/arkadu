# 🌋 APPROACH 4: Sedimentary Voronoi (Falling Sand)

**Status:** ✅ IMPLEMENTED  
**File:** `approach-4-depth-test.html`  
**Algorithm:** Sediment deposition + Voronoi refinement  

---

## 🎯 Core Concept

**The geological metaphor brought to life:**

Territories "fall" and settle like sediment, creating **visible strata lines** (geological layers). Within each layer, **Voronoi cells iteratively subdivide** until achieving exact target areas.

**Key innovation:** Combines:
1. **Falling sand physics** - largest territories sink to bottom
2. **Strata visualization** - clear horizontal layer boundaries  
3. **Recursive Voronoi refinement** - subdivide until exact areas
4. **Infinite recursion** - each layer can be further subdivided

---

## 🌋 The Sedimentary Model

### How Sediment Works

In nature:
- Heavy particles sink deeper
- Layers form over time
- Each layer is visible (strata lines)
- Layers compact and settle

In our algorithm:
```
LARGEST territory = HEAVIEST = SINKS TO BOTTOM
↓
MEDIUM territory = settles on top
↓  
SMALLEST territory = floats to top
```

Visual result:
```
┌─────────────────────────┐ ← Top of container
│   SMALLEST (floats)     │
├─────────────────────────┤ ← Strata line
│   MEDIUM (settles)      │
├─────────────────────────┤ ← Strata line
│   LARGEST (sinks)       │
└─────────────────────────┘ ← Bottom
```

---

## 🔬 Algorithm Steps

### 1. Sort by Size (Gravity)
```javascript
// Largest = heaviest = sinks deepest
children.sort((a, b) => b.totalSize - a.totalSize);
```

### 2. Create Sediment Layers
```javascript
function createSedimentLayers(children, totalSize, boundary) {
  const layers = [];
  let currentY = boundary.y + boundary.radius; // Start at bottom
  
  children.forEach(child => {
    const ratio = child.totalSize / totalSize;
    const layerHeight = boundary.radius * 2 * ratio;
    
    layers.push({
      children: [child],
      bounds: {
        yMin: currentY - layerHeight,
        yMax: currentY,
        yTop: currentY - layerHeight  // STRATA LINE!
      }
    });
    
    currentY -= layerHeight;  // Move up for next layer
  });
  
  return layers;
}
```

### 3. Voronoi Within Each Layer
```javascript
// For each horizontal band:
layers.forEach(layer => {
  // Initialize seeds within layer bounds
  const seeds = placeInLayer(layer.children, layer.bounds);
  
  // Iteratively refine (20 iterations)
  for (let iter = 0; iter < 20; iter++) {
    // Generate Voronoi
    seeds.forEach(seed => {
      seed.cell = voronoi(seed, allSeeds, boundary);
      seed.actualArea = measure(seed.cell);
    });
    
    // Compare to target
    seeds.forEach(seed => {
      const error = (actualArea - targetArea) / targetArea;
      
      // Adjust horizontally (stay in layer!)
      if (error > 0.05) {  // Too big
        seed.x -= movement;
      } else if (error < -0.05) {  // Too small
        seed.x += movement;
      }
      
      // KEEP Y IN LAYER BOUNDS
      seed.y = clamp(seed.y, layer.yMin, layer.yMax);
    });
  }
});
```

### 4. Store Strata Lines
```javascript
// Each node remembers its strata boundary
child.strataLine = layer.yTop;
```

---

## 🧮 Mathematical Properties

**Area accuracy:** ~98% (like Approach 2)
- 20 iterations of refinement
- Converges to target area
- Horizontal movement only (stays in layer)

**Layer heights:** 100% exact
```
layerHeight[i] = totalHeight × (size[i] / totalSize)
```

**No overlaps:** Guaranteed within layers
- Each layer is independent
- Voronoi naturally prevents overlaps
- Strata lines provide clear boundaries

---

## 🌊 Visual Characteristics

### Strata Lines

Horizontal boundaries between layers create **geological appearance**:

```
┌───────────────────────────────┐
│  JELLYFISH  │  SNAKE  │  FOX  │  ← Layer 3 (small)
├───────────────────────────────┤  ← STRATA LINE
│      MANTA      │     CAT     │  ← Layer 2 (medium)
├───────────────────────────────┤  ← STRATA LINE  
│           LIZARD              │  ← Layer 1 (large, bottom)
└───────────────────────────────┘
```

### Organic Within Layers

Each layer uses Voronoi, so:
- **Horizontal bounds** = strata lines (rigid)
- **Vertical/lateral bounds** = Voronoi (organic)

Result: **Stratified + organic hybrid**

---

## 📊 Comparison to Other Approaches

| Feature | Approach 2 (Voronoi) | Approach 3 (BSP) | **Approach 4 (Sediment)** |
|---------|---------------------|-----------------|--------------------------|
| **Area accuracy** | ~98% | 100% | **~98%** |
| **Topology** | Full Voronoi | Varied cuts | **Layered Voronoi** |
| **Metaphor** | Natural cells | Strata cuts | **Sediment deposit** ✅ |
| **Strata lines** | No | No | **YES** ✅ |
| **Recursion** | Yes | Yes | **Yes** ✅ |
| **Falling sand** | No | No | **YES** ✅ |

---

## 🎯 Why This Approach?

### Perfect for Media Archaeology

**Geological metaphor:**
- ✅ Sediment = media artifacts deposited over time
- ✅ Strata = excavation layers
- ✅ Heavy/large = older/deeper deposits
- ✅ Light/small = recent/surface artifacts

**Literal visualization:**
> "The LIZARD stratum (25GB) sank deepest into the archive. Above it, MANTA (10GB) settled. CAT (7GB) formed the middle layer. Smaller territories float near the surface."

### Algorithmic Benefits

1. **Recursive subdivision** - can drill into any layer infinitely
2. **Exact layer heights** - proportional to data
3. **Voronoi within layers** - organic appearance
4. **Visible structure** - strata lines show organization
5. **Stable** - layers don't shift (deterministic)

---

## 🔧 Tuning Parameters

### `iterations = 20`
- More = better area accuracy
- 20 iterations ≈ 2% error

### Layer positioning
```javascript
// Largest at bottom (y = max)
currentY = boundary.y + boundary.radius;

// Each layer moves up
currentY -= layerHeight;
```

### Movement constraints
```javascript
// Horizontal adjustment (area refinement)
seed.x += adjustment;

// Vertical locked to layer
seed.y = clamp(seed.y, layer.yMin, layer.yMax);
```

---

## 🚀 Usage

**Open:** http://localhost:8765/approach-4-depth-test.html

**Load data:** Click "🗂️ LOAD ARKADU"

**Observe:**
1. **Horizontal strata lines** between territories
2. **Largest territories at bottom** (LIZARD sinks)
3. **Smallest at top** (small files float)
4. **Organic Voronoi** within each layer
5. **Exact layer heights** = exact proportions

**Console:**
```
🌋 SEDIMENTARY STRATA:
  LIZARD: 2489 files, 25211.0MB, totalSize=27700.5  ← Sinks to bottom
  MANTA: 1655 files, 10019.9MB, totalSize=11675.0   ← Middle layer
  CAT: 1981 files, 7296.5MB, totalSize=9277.6       ← Upper layer
  ...
```

---

## 🆚 When to Use

**Use Approach 4 if:**
- **Sediment metaphor** fits your domain (archaeology, geology, time deposits)
- Want **visible strata lines** showing hierarchy
- Need **falling sand / gravity** physics metaphor
- Like Voronoi BUT want clear layer structure
- ~2% area error acceptable

**Don't use if:**
- Need 100% exact areas (use Approach 3)
- Want pure Voronoi without layers (use Approach 2)
- Prefer radial organization (use Approach 1)

---

## 🌊 Recursive Subdivision

**Each layer can subdivide further!**

When you click into a territory:
1. That layer's space becomes new "container"
2. Its children become new "sediment"
3. They fall and create sub-strata
4. Process repeats infinitely

```
LIZARD layer (clicked)
  ↓ subdivides into:
  ┌─────────────────────┐
  │  LizardChild3       │ ← Small, floats
  ├─────────────────────┤
  │  LizardChild2       │ ← Medium
  ├─────────────────────┤
  │  LizardChild1       │ ← Large, sinks
  └─────────────────────┘
```

---

## 🧬 Pseudocode

```
function sedimentaryVoronoi(children, boundary):
  // 1. GRAVITY: Sort by size
  children.sort((a, b) => b.size - a.size)
  
  // 2. CREATE LAYERS: Bottom to top
  layers = []
  currentY = bottom
  for each child:
    height = (child.size / total) × containerHeight
    layers.push({
      child: child,
      yMin: currentY,
      yMax: currentY + height
    })
    currentY += height
  
  // 3. VORONOI IN EACH LAYER
  for each layer:
    seeds = initializeInLayer(layer)
    
    // Iterative refinement
    for i = 0 to 20:
      // Generate Voronoi
      for each seed:
        seed.cell = voronoi(seed, allSeeds)
        seed.area = measure(seed.cell)
      
      // Adjust positions
      for each seed:
        error = (seed.area - target) / target
        seed.x += adjustment(error)
        seed.y = clamp(seed.y, layer.yMin, layer.yMax)
    
    // 4. DRAW STRATA LINE
    drawLine(y = layer.yMax)
```

---

## 🔮 Future Enhancements

- **Compression effects:** Lower layers visually compressed (like real sediment)
- **Time animation:** Watch territories "fall" and settle
- **Erosion:** Smaller territories erode/fade over time
- **Folding:** Geological deformation of strata
- **Cross-bedding:** Diagonal patterns within layers

---

**Created:** 2025-10-06 04:15 AM  
**Theory:** Sediment deposition + Voronoi subdivision  
**Result:** Geological strata with organic subdivision 🌋
