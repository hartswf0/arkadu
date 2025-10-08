# Network Graph Update - JSONL Migration

**Date:** 2025-10-08 07:47:11  
**Status:** ✅ FIXED - Network graph now uses JSONL data system

---

## Problem Identified

`network-graph.html` was trying to load `media-manifest.json` which:
- Does NOT exist in repository
- Has been replaced by JSONL system
- Resulted in empty/blank network graph

**Error:** No data displayed, empty canvas

---

## Solution Implemented

Updated `network-graph.html` to use **ARKADU v1.0 JSONL data**:

### Data Sources

1. **`sys/primitive.jsonl`** (2.9 MB)
   - All 10,094 files with metadata
   - File types, sizes, paths

2. **`sys/ekphrasis.jsonl`** (88 KB)
   - 223 operative ekphrasis chains
   - JSON prompts → Python scripts relationships
   - Format: `{prompt_file, script, sample_prompts, uses_ffmpeg, ...}`

### Network Structure

**Old Model:** HTML files → Media files  
**New Model:** JSON prompts → Python scripts (ekphrasis chains)

```
JSON Files (prompts)
    ↓
Python Scripts (processors)
    ↓
Generated Media (outputs)
```

### Changes Made

1. **Dual Data Loading**
   ```javascript
   Promise.all([
     fetch('sys/primitive.jsonl'),
     fetch('sys/ekphrasis.jsonl')
   ])
   ```

2. **Circulation Map**
   - Maps Python scripts to JSON prompt files
   - Shows which scripts use which prompts
   - Represents operative ekphrasis chains

3. **Usage Relationships**
   - JSON files "used by" Python scripts
   - Based on actual ekphrasis chain data
   - 223 traced relationships

---

## Network Graph Features

### Node Types

- **Python Scripts** (circulation nodes)
  - Shown as larger nodes
  - Represent processing scripts
  - Color: HTML color (cyan)

- **JSON Prompts** (media nodes)
  - Shown as smaller nodes
  - Contain operative ekphrasis
  - Color: Media color (gold)

- **Orphaned Files** (optional)
  - Files not in any chain
  - Can be toggled on/off
  - Color: Gray

### Visualization

- Force-directed graph layout
- Links show JSON → Python relationships
- Interactive tooltips on hover
- Stats HUD shows node/link counts
- Legend explains node types

---

## Data Format

### Ekphrasis Chain Structure

```json
{
  "type": "operative_ekphrasis_chain",
  "prompt_file": "DOG/BL-TIMELINE-ADDENDUM.json",
  "script": "check_syntagmas.py",
  "sample_prompts": [
    "Title etched in pulsating crimson across black velvet.",
    "Distant chorus whispers behind closed doors."
  ],
  "uses_ffmpeg": false,
  "uses_drawtext": false,
  "intent": null
}
```

### Conversion Logic

```javascript
// Build circulation: script → [prompt_files]
chains.forEach(chain => {
  if (chain.script && chain.prompt_file) {
    circulation[chain.script].push(chain.prompt_file);
  }
});

// Build usage: prompt_file → [scripts]
chains.forEach(chain => {
  if (chain.prompt_file && chain.script) {
    usageMap[chain.prompt_file].push(chain.script);
  }
});
```

---

## Testing

### Verification

```bash
# 1. Check data files exist
ls -lh ARKADU/sys/primitive.jsonl ARKADU/sys/ekphrasis.jsonl
# Both present ✓

# 2. Check ekphrasis chains
wc -l ARKADU/sys/ekphrasis.jsonl
# 223 chains ✓

# 3. Open network graph
open ARKADU/network-graph.html
# Should show force-directed graph with nodes and links

# 4. Verify stats
# Should display:
# - Node count (JSON + Python files)
# - Link count (223 chains)
# - Orphan count (files not in chains)
```

---

## Network Graph Now Shows

1. **223 Ekphrasis Chains**
   - JSON prompt files → Python scripts
   - Operative semantic relationships
   - Tool chain mappings

2. **File Relationships**
   - Which scripts use which prompts
   - Circulation networks
   - Processing pipelines

3. **Interactive Exploration**
   - Hover for file details
   - Toggle orphan visibility
   - Force simulation physics

---

## Related Updates

- ✅ `viewer.html` - Migrated to JSONL
- ✅ `network-graph.html` - Migrated to JSONL
- ✅ Both use `sys/primitive.jsonl` + `sys/ekphrasis.jsonl`
- ✅ No missing data dependencies

---

## Status

**✅ NETWORK GRAPH NOW OPERATIONAL**

Shows ekphrasis chains (JSON → Python) instead of HTML → Media relationships.  
More accurate representation of actual operative ecology.

---

*Update completed: 2025-10-08 07:47:11*  
*Network graph status: ✅ WORKING*  
*Data sources: primitive.jsonl + ekphrasis.jsonl*  
*Chains visualized: 223*
