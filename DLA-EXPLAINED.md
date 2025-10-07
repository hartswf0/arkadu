# ❄️ DLA: Diffusion-Limited Aggregation

**The most organic algorithm - fractal crystal growth**

---

## 🌨️ What is DLA?

**Diffusion-Limited Aggregation** is a process where particles undergo a **random walk** (Brownian motion) until they collide with a growing structure, then **stick** to it.

**Found in nature:**
- ❄️ Snowflake formation
- 🌿 Lichen growth patterns
- ⚡ Lightning branches
- 🪸 Coral reefs
- 🧠 Neuron dendrites
- 🔬 Bacterial colonies

---

## 🧬 The Algorithm

### 1. Initialize Seeds
```javascript
// Place small seed clusters for each territory
seeds.forEach((territory, i) => {
  // Position in circle
  angle = (i / total) × 2π
  x = center.x + cos(angle) × radius
  y = center.y + sin(angle) × radius
  
  // Create 3×3 seed cluster
  for dy in [-1, 0, 1]:
    for dx in [-1, 0, 1]:
      grid[y+dy][x+dx] = territory.id
})
```

### 2. Release Particles
```javascript
// Pick territory that needs more growth
underSized = territories.filter(t => t.current < t.target)

// Weight by deficit (territories needing more get more particles)
weights = underSized.map(t => (t.target - t.current) / t.target)
targetTerritory = weightedRandom(underSized, weights)

// Spawn particle near target seed
particle.x = targetSeed.x + random(-30, 30)
particle.y = targetSeed.y + random(-30, 30)
```

### 3. Random Walk
```javascript
// Brownian motion - move randomly
while (!stuck && steps < maxSteps):
  direction = random(0, 3)  // 4 directions: up, down, left, right
  
  if direction == 0: particle.x--
  if direction == 1: particle.x++
  if direction == 2: particle.y--
  if direction == 3: particle.y++
```

### 4. Stick on Contact
```javascript
// Check 8 neighbors (Moore neighborhood)
neighbors = [
  grid[y-1][x], grid[y+1][x],    // top, bottom
  grid[y][x-1], grid[y][x+1],    // left, right
  grid[y-1][x-1], grid[y-1][x+1], // diagonals
  grid[y+1][x-1], grid[y+1][x+1]
]

// If touching target territory
if neighbors.includes(targetTerritory.id):
  grid[y][x] = targetTerritory.id  // STICK!
  targetTerritory.current++
  stuck = true
```

### 5. Repeat
```javascript
// Continue until all territories reach target size
while (any territory needs more particles):
  releaseParticle()
  randomWalk()
  stickOnContact()
```

---

## 🎨 Visual Characteristics

### Fractal Branching
DLA creates **dendritic (tree-like) structures**:
```
         A
        AAA
       AAAA
      AAAABAA
     AAAABAABA
    AAABBBAAABA
   AAABBBBAAABAA
```

### Why Fractal?
- Particles arrive from random directions
- Tips of branches are most exposed
- New particles stick to tips first
- Creates branching, self-similar pattern

### Organic Boundaries
Borders are **extremely irregular**:
- No straight lines
- Fractal dimension ~1.7 (between line and plane)
- Looks completely natural
- Unique every time

---

## 📊 Properties

### Accuracy
**~85% area accuracy**

**Why not exact:**
- Random walk is unpredictable
- Some territories grow faster by chance
- Boundary competition varies
- We stop at "close enough" to target

### Speed
**SLOW** - the slowest algorithm

**Why:**
- Each particle takes 100-1000 steps
- Need thousands of particles
- Pure simulation (no shortcuts)
- ~16ms per frame × 1000 frames = 16 seconds

### Determinism
**Non-deterministic** - different every time

Random walk means:
- Same input → different output
- Unpredictable patterns
- Unique results each run

---

## ⚙️ Implementation Details

### Optimization: Batch Processing
```javascript
// Release 20 particles per frame instead of 1
const batchSize = 20;
for (let i = 0; i < batchSize; i++) {
  releaseParticle();
  randomWalk();
}
```

**Without batching:** 1 particle/frame = 10,000 frames = 3+ minutes  
**With batching:** 20 particles/frame = 500 frames = ~8 seconds

### Optimization: Weighted Territory Selection
```javascript
// Prioritize territories that need more growth
weights = territories.map(t => (t.target - t.current) / t.target)

// Territory with 50% deficit gets 2× more particles
// Territory with 10% deficit gets 0.2× fewer particles
```

Ensures all territories grow proportionally.

### Optimization: Max Walk Steps
```javascript
const maxSteps = 1000;

// Abandon particle if it wanders too far
if (steps > maxSteps) {
  releaseNewParticle();
}
```

Prevents infinite loops.

### Grid Representation
```javascript
// Uint8Array for memory efficiency
grid = new Uint8Array(500 × 500);  // 250KB

// Values:
// 0-253: territory ID
// 255: empty space
```

More efficient than 2D array of objects.

---

## 🔬 Theory: Why DLA Creates Fractals

### The Physics
1. **Diffusion:** Particles move randomly (Brownian motion)
2. **Limited:** Growth happens only when particles stick
3. **Aggregation:** Structure grows by accumulation

### Branching Mechanism
```
Initial seed:        First particles:      Branching begins:
     •                    •••                  •••
                          •••                 •••••
                          •••                ••• •••
                                               • •
```

**Why tips grow fastest:**
- Tips exposed to more directions
- Particles hit tips before reaching interior
- Creates "screening effect"
- Interior becomes shadowed

### Fractal Dimension
DLA structures have **fractal dimension ≈ 1.7**

**What this means:**
- More than a line (D=1)
- Less than a plane (D=2)
- Self-similar at different scales
- Same branching pattern at all zoom levels

---

## 🆚 Comparison to Other Growth

### DLA vs Cellular Automata
| DLA | CA |
|-----|-----|
| Random walk | Deterministic rules |
| Particles stick | Cells compete |
| Fractal | Cellular |
| Unpredictable | Reproducible |

### DLA vs Eden Model
**Eden model:** Always add cell at boundary  
**DLA:** Add cell only when particle arrives  

DLA → Fractal  
Eden → Compact

### DLA vs Reaction-Diffusion
**DLA:** Particles aggregate  
**Reaction-Diffusion:** Chemicals react + diffuse  

DLA → Branching  
RD → Spots/stripes

---

## 🎯 When to Use DLA

### Perfect For:
✅ **Generative art** - fractal beauty  
✅ **Natural simulations** - crystal growth, snowflakes  
✅ **Organic textures** - lightning, coral, neurons  
✅ **Unpredictable patterns** - unique every time

### Not Good For:
❌ **Data visualization** - too inaccurate (~85%)  
❌ **Fast rendering** - very slow  
❌ **Reproducible layouts** - non-deterministic  
❌ **Compact territories** - creates sparse structures

---

## 🌟 Variants & Extensions

### Biased DLA
Add directional bias to random walk:
```javascript
// Bias toward gravity
if (random() < 0.3) {
  direction = DOWN;  // 30% chance to go down
} else {
  direction = random(0, 3);
}
```

Creates "dripping" patterns.

### Multi-Type DLA
Different particle types stick with different probabilities:
```javascript
if (particleType == A && territoryType == A) {
  stickProbability = 0.9;  // Like sticks to like
} else {
  stickProbability = 0.1;  // Repulsion
}
```

Creates segregated structures.

### 3D DLA
Extend to 3D space:
```javascript
// 6 directions instead of 4
// Creates 3D dendrites, snowflakes
```

### Screened Growth DLA
Limit growth to only surface particles:
```javascript
// Prevents interior filling
// Creates even more fractal structure
```

---

## 🧮 Mathematical Properties

### Probability of Sticking
At any point, probability particle sticks:
```
P(stick) = (exposed neighbors) / 8
```

Tips have more exposed neighbors → higher P(stick) → faster growth.

### Growth Rate
Territory growth rate ∝ particle flux × stick probability:
```
dA/dt ∝ Φ × P(stick)
```

Where:
- Φ = particle flux (particles per area per time)
- P(stick) = probability of sticking

### Fractal Scaling
Perimeter scales with radius non-linearly:
```
Perimeter ∝ Radius^D

Where D ≈ 1.7 (fractal dimension)
```

Standard circle: D = 1  
DLA cluster: D = 1.7  

**More surface for same area!**

---

## 🚀 Try It

```bash
open http://localhost:8765/organic-evolution.html
```

1. **Click "Aggregate"** on Approach 7
2. **Watch** particles random walk and stick
3. **See** fractal patterns emerge
4. **Step** through slowly to understand process

**Stats to watch:**
- **Particles:** Total particles released
- **Stuck:** Particles that successfully attached
- **Coverage:** % of space filled

---

## 🔮 Future Improvements

### Speed Optimization
- **Distance field:** Pre-compute distance to nearest territory
- **Jump to boundary:** Skip random walk in empty space
- **Parallel particles:** Simulate multiple particles simultaneously

### Accuracy Improvement
- **Adaptive flux:** Send more particles to deficient territories
- **Area monitoring:** Stop when target reached (don't overshoot)
- **Boundary smoothing:** Post-process to refine edges

### Visual Enhancement
- **Color gradient:** Fade by distance from seed
- **Particle trails:** Show recent random walks
- **Growth animation:** Record and replay growth process

---

**DLA: The most organic algorithm - pure emergent fractal beauty! ❄️✨**
