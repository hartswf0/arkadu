# ARKADU Scale System

## What is the Scale?

The **ARKADU Scale** is a verification system that measures and validates the **volume** (count) and **mass** (bytes) of every file in the repository, organized by hierarchy and media type (species).

## Quick Start

```bash
# Run the scale to measure everything
python3 scale-verify.py

# View the full report
cat sys/scale-report.txt

# Check verification data
cat sys/scale-verification.json
```

## What It Measures

### Volume (Count)
- **Definition**: Number of files
- **Unit**: Files
- **Purpose**: Shows how many artifacts exist in each territory

### Mass (Weight)  
- **Definition**: Total bytes
- **Unit**: Bytes (displayed as MB/GB)
- **Purpose**: Shows physical storage size of territories

### Species (Media Type)
- **Definition**: File extension/type
- **Examples**: `.png`, `.mp4`, `.json`, `.py`
- **Purpose**: Categorizes files by format

### Dominant Species
- **Definition**: Species with highest (volume × mass) product
- **Purpose**: Identifies what type of media dominates a territory

## How It Works

```
primitive.jsonl (10,094 files)
  ↓
Build hierarchy tree
  ↓
For each territory:
  - Count files (volume)
  - Sum bytes (mass)
  - Track species breakdown
  - Find dominant species
  ↓
Export to scale-verification.json
```

## Measurements Verified

From **10,094 total files** (56.5 GB):

### Top Kingdoms by Mass

| Kingdom | Volume | Mass | Dominant |
|---------|--------|------|----------|
| LIZARD | 594 | 25.2 GB | `.mp4` |
| MANTA | 204 | 10.0 GB | `.mp4` |
| CAT | 1,981 | 7.3 GB | `.jpg` |
| DOG | 1,230 | 3.4 GB | `.png` |

### Global Species Distribution

| Species | Volume | Mass |
|---------|--------|------|
| `.mp4` | 735 files | 41.1 GB (72.7%) |
| `.png` | 5,966 files | 6.4 GB (11.3%) |
| `.wav` | 350 files | 4.1 GB (7.2%) |
| `.jpg` | 1,316 files | 3.0 GB (5.3%) |

## Integration with Voronoi Visualization

The scale measurements feed directly into `voronoi-depth-test.html`:

```javascript
// Dual sizing metric from scale data
node.totalSize = node.totalFiles + (node.totalBytes / MB)

// CAT example:
// 1,981 files + (7,833 MB / 1) = 9,814 totalSize
```

This ensures:
- ✅ Voronoi cell sizes reflect actual data
- ✅ Large kingdoms (LIZARD) dominate the view
- ✅ Small kingdoms (KOALA) are proportionally tiny
- ✅ Color tinting reflects dominant species

## Files Generated

- `sys/scale-report.txt` - Human-readable report
- `sys/scale-verification.json` - Machine-readable data
- `SCALE-VERIFICATION.md` - Technical verification document

## Verification Status

✅ **VERIFIED** - The visualization matches the scale:
- Volume tracking: Accurate
- Mass tracking: Accurate  
- Species tracking: Accurate
- Dominant species: Calculated correctly
- Visual sizing: Proportional to measurements

## Use Cases

1. **Verify visualization accuracy** - Compare voronoi sizes to scale data
2. **Find large files** - Identify territories with high mass
3. **Analyze species distribution** - See what file types dominate
4. **Track changes over time** - Re-run scale after adding files
5. **Debug sizing issues** - Check if a territory's totalSize makes sense

## Theory: Why Volume + Mass?

A territory's "importance" comes from both:
- **How many things** it contains (volume)
- **How big those things are** (mass)

Example:
- **Territory A**: 1,000 tiny JSON files (10 MB total)
  - High volume, low mass
- **Territory B**: 10 large video files (10 GB total)  
  - Low volume, high mass

The **balanced metric** `volume + mass/MB` ensures both matter:
- Territory A totalSize: 1,000 + 10 = 1,010
- Territory B totalSize: 10 + 10,000 = 10,010

Territory B is ~10× larger in the visualization, reflecting its greater "weight" in the repository.

## Maintenance

Re-run the scale whenever:
- ✅ New files are added
- ✅ Files are moved between territories
- ✅ Large files are committed
- ✅ Visualization sizes seem incorrect

```bash
# Quick verification
python3 scale-verify.py | grep "Top 3"
```

---

**Scale Calibration**: ✅ ZEROED  
**Data Source**: `primitive.jsonl`  
**Last Run**: 2025-10-06
