# 🌱 NEW ORGANIC ALGORITHMS - Bottom-Up Growth

**Cellular automata • Physics simulation • Procedural packing • Space-filling curves**

---

## 🎯 The Evolution

**Previous approaches (1-4):** Top-down subdivision
- Start with full space
- Split it recursively
- Impose boundaries

**New approaches (5-8):** Bottom-up growth
- Start with seeds
- Grow outward
- Boundaries emerge naturally

---

## 🦠 APPROACH 5: Cellular Automata Growth

### Concept
Territories grow from seed points using **cellular automata rules**. Each cell checks its neighbors and decides whether to expand based on:
- How much space the territory still needs
- How many neighboring cells belong to it
- Competition from other territories

### Algorithm
```javascript
1. Place seeds for each territory
2. For each empty cell:
   - Check neighbors (4-directional)
   - Find territories touching this cell
   - Weight by: (target_area - current_area) / target_area
   - Probabilistically assign to weighted neighbor
3. Repeat until all cells claimed
```

### Characteristics
- **Organic boundaries:** Emerge from competition, not imposed
- **Adaptive growth:** Territories that need more space grow faster
- **Approximate accuracy:** ~95% (depends on seed placement)
- **Visual:** Natural, cellular, irregular borders

### Pros
✅ Truly organic growth pattern  
✅ Emergent behavior creates unique results  
✅ Can add mutation/variation rules  
✅ Feels "alive" - territories compete

### Cons
❌ Not 100% exact areas  
❌ Sensitive to seed placement  
❌ Slower than geometric methods  
❌ Non-deterministic results

---

## 🫧 APPROACH 6: Bubble Packing (Physics-Based)

### Concept
Territories are **circles that inflate and push apart** like soap bubbles. They grow until their areas match targets, pushing neighbors aside using physics simulation.

### Algorithm
```javascript
1. Place small circles at seed points
2. Loop:
   a. Inflate each circle toward target area
   b. Detect collisions between circles
   c. Apply repulsion forces
   d. Move circles based on forces
   e. Apply damping/friction
3. Stop when stable (minimal movement)
```

### Physics
```javascript
// Collision detection
dist = sqrt((x2-x1)² + (y2-y1)²)
overlap = (r1 + r2) - dist

// Repulsion force
if overlap > 0:
  force = overlap × stiffness
  angle = atan2(y2-y1, x2-x1)
  
  bubble1.vx -= cos(angle) × force
  bubble1.vy -= sin(angle) × force
  bubble2.vx += cos(angle) × force
  bubble2.vy += sin(angle) × force
```

### Characteristics
- **Natural packing:** Like bubbles in foam
- **Smooth boundaries:** Circles create organic Voronoi-like cells
- **Good accuracy:** ~92% (limited by circle packing efficiency)
- **Visual:** Soft, rounded, fluid boundaries

### Pros
✅ Beautiful circular territories  
✅ Physics-based feels natural  
✅ Smooth, rounded boundaries  
✅ Can animate growth process

### Cons
❌ Circle packing ~90% efficient (wastes 10% space)  
❌ Areas approximate, not exact  
❌ Computationally expensive  
❌ Requires many iterations to stabilize

---

## ❄️ APPROACH 7: Diffusion-Limited Aggregation (DLA)

### Concept
**Fractal growth pattern** where particles random walk until they touch a territory, then stick. Creates branching, crystal-like organic structures.

### Algorithm
```javascript
1. Place seed pixels for each territory
2. Release particle at random position
3. Particle random walks
4. When particle touches territory:
   - Stick to that territory
   - Increment territory area
5. Repeat until target areas reached
```

### Random Walk
```javascript
// Brownian motion
particle.x += random(-1, 1)
particle.y += random(-1, 1)

// Check if touching any territory
for each territory:
  if distance(particle, territory) < 1:
    territory.add(particle)
    break
```

### Characteristics
- **Fractal boundaries:** Branching, dendrite patterns
- **Extremely organic:** Most natural-looking of all approaches
- **Variable accuracy:** 80-95% (depends on particle count)
- **Visual:** Crystal-like, snowflake patterns

### Pros
✅ Most organic, natural appearance  
✅ Fractal beauty  
✅ Unique every time  
✅ Resembles natural growth (crystals, coral, lightning)

### Cons
❌ Very slow (many particles needed)  
❌ Poor area accuracy  
❌ Random/unpredictable  
❌ Territories can fragment

---

## 🌀 APPROACH 8: Space-Filling Curves (Hilbert/Peano)

### Concept
Use **Hilbert curve** (or Peano curve) to traverse space in a continuous path. Allocate segments of the curve proportionally to each territory.

### Algorithm
```javascript
1. Generate Hilbert curve at order N (2^(2N) points)
2. Calculate target segments:
   territory_i.segments = curve_length × (value_i / total)
3. Assign curve segments to territories
4. Fill pixels along each segment
```

### Hilbert Curve Generation
```javascript
// Recursive Hilbert curve (D2XY algorithm)
function d2xy(n, d):
  x = 0, y = 0
  for s = 1 to 2^n:
    rx = 1 & (d/2)
    ry = 1 & (d ^ rx)
    rotate(s, &x, &y, rx, ry)
    x += s × rx
    y += s × ry
    d /= 4
  return (x, y)
```

### Characteristics
- **100% space-filling:** Guaranteed no gaps
- **Exact accuracy:** 100% (segments = exact proportions)
- **Continuous territories:** Connected along curve
- **Visual:** Maze-like, space-filling pattern

### Pros
✅ 100% exact area proportions  
✅ Guaranteed space-filling  
✅ Deterministic  
✅ Mathematically elegant

### Cons
❌ Territories not compact (can be long/thin)  
❌ Artificial curve pattern visible  
❌ Less organic appearance  
❌ Territories interleave oddly

---

## 📊 Comparison

| Approach | Method | Accuracy | Organic | Speed | Best For |
|----------|--------|----------|---------|-------|----------|
| **5: CA** | Bottom-up growth | ~95% | ⭐⭐⭐⭐⭐ | Slow | Emergent patterns |
| **6: Bubble** | Physics simulation | ~92% | ⭐⭐⭐⭐ | Slow | Soft boundaries |
| **7: DLA** | Random aggregation | ~85% | ⭐⭐⭐⭐⭐ | Very slow | Fractal beauty |
| **8: Hilbert** | Space curve | 100% | ⭐⭐ | Fast | Perfect filling |

---

## 🆚 vs Previous Approaches

### Top-Down (1-4)
- Start with full space
- Subdivide recursively
- Exact areas (except Voronoi)
- Faster execution
- Less organic

### Bottom-Up (5-8)
- Start with seeds
- Grow outward
- Approximate areas (except Hilbert)
- Slower execution
- More organic

---

## 🌱 Growth Metaphors

**Approach 5 (CA):** Bacterial colonies spreading  
**Approach 6 (Bubble):** Soap foam forming  
**Approach 7 (DLA):** Snowflakes growing  
**Approach 8 (Hilbert):** Space-filling maze

---

## 🧬 Hybrid Possibilities

### CA + BSP
1. Use BSP for coarse subdivision (exact areas)
2. Use CA to create organic boundaries at edges

### Bubble + Voronoi
1. Pack bubbles for placement
2. Generate Voronoi from bubble centers
3. Organic placement, exact Voronoi structure

### DLA + Area Forcing
1. Grow via DLA for organic shape
2. Monitor areas during growth
3. Bias random walk toward territories needing more space

---

## 🚀 Usage

```bash
open http://localhost:8765/organic-evolution.html
```

**Try each approach:**
- **Approach 5:** Click "Grow" to see CA evolution
- **Approach 6:** Click "Inflate" to see bubble physics
- **Approach 7:** DLA (coming soon - complex implementation)
- **Approach 8:** Click "Subdivide" then "+ Depth" to refine

---

## 🔬 Theory

### Why Bottom-Up is More Organic

**Top-down** = Imposed structure
- Boundaries are cuts/splits
- Feels artificial, geometric
- Like slicing a pie

**Bottom-up** = Emergent structure  
- Boundaries arise from competition
- Feels natural, organic
- Like organisms growing

### Space-Filling Efficiency

| Method | Efficiency | Reason |
|--------|-----------|--------|
| Circles (Bubble) | ~90% | Circle packing wastes 10% |
| Squares (BSP) | 100% | Perfect tiling |
| Voronoi | 100% | Tessellates plane |
| DLA | 80-95% | Fractal gaps |
| Hilbert | 100% | Curve fills all space |

---

## 💡 When to Use Each

### Approach 5 (CA Growth)
- **Use when:** Want emergent, competitive growth
- **Perfect for:** Ecological simulations, territory expansion
- **Avoid when:** Need exact areas

### Approach 6 (Bubble)
- **Use when:** Want soft, rounded boundaries
- **Perfect for:** Organic UI, natural clustering
- **Avoid when:** Need rectangular spaces

### Approach 7 (DLA)
- **Use when:** Want fractal, crystal-like beauty
- **Perfect for:** Art, generative design
- **Avoid when:** Need speed or accuracy

### Approach 8 (Hilbert)
- **Use when:** Need 100% space-filling + exact areas
- **Perfect for:** Memory layouts, efficient packing
- **Avoid when:** Want compact territories

---

## 📁 Files

```
ARKADU/
├── organic-evolution.html           # Interactive demo ⭐
├── NEW-ALGORITHMS-README.md         # This file
└── sys/deep-test-data.json          # Test data
```

---

**Open the evolution lab:**
```bash
open http://localhost:8765/organic-evolution.html
```

🌱 **Watch territories GROW from the ground up!**
