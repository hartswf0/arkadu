# ARKADU Primitive Scan Report
**Generated:** 2025-10-05T20:37:45-04:00

## System Overview

**Total Files Scanned:** 10,094 files (excluding venv/cache)

### By Kingdom (Top-level folders)

```
CAT:          1,981 files  ████████████████████
DOG:          1,233 files  ████████████
JELLYFISH:    1,178 files  ████████████
TIGER:        1,108 files  ███████████
HONEYBADGER:    980 files  ██████████
ANT:            879 files  █████████
SHARK:          801 files  ████████
LIZARD:         594 files  ██████
ELEPHANT:       458 files  █████
MANTA:          204 files  ██
IMPALA:         174 files  ██
BOY:             52 files  █
HORSE:           25 files  █
WHALE:           17 files
SPIDER:          11 files
```

---

## Operative Ekphrasis Discovery

### JSON Prompt Files: 576 files

JSON files containing `operativeEkphrasis` field (actual prompts used for generation):

**Sample files:**
- `departure.json`
- `notice-me.json`
- `resurrecting-atlantis.json`
- `CAT/storyboard.json`
- `CAT/storyboard-sequence.json`

**Sample prompts found:**
- "Title etched in pulsating crimson across black velvet."
- "A dimly lit plain bedroom in a high-rise apartment."
- "POET, wearing a black t-shirt, reads a poem aloud."
- "Infinity symbol made of pale light, slowly fraying at both ends."

### Python Scripts: 253 files

Scripts that process media, including:
- Video assembly (`add_scrolling_header_to_intros.py`)
- Audio processing (`create_professional_vintage_mix.py`)
- Image generation (`improved_codex_overlay.py`)
- Timeline management (`timeline_generator.py`)

### Ekphrasis Chains: 223 traced

**JSON prompts → Python scripts → Generated media**

Example chain:
```
DOG/BL-TIMELINE-ADDENDUM.json
  → check_syntagmas.py
  Prompts: "Title etched in pulsating crimson across black velvet..."
```

---

## Filename Schemas Detected

### CAT/WHISKER Pattern
```
WGY058_RI__Memory_Storage_Retrieval__POET_and_MOTHE_3374175a-9c48-4672-8f62-9583f38f5cb0_0.png

Structure:
  WGY[shot_num]_[operator_code]__[operation_name]__[description]_[uuid]_[variant].[ext]
```

### HORSE Pattern
```
01_SH_OutOfLife_000000_header_prompt.mp4

Structure:
  [track_num]_[track_code]_[title]_[timestamp]_header_prompt.mp4
```

---

## Actual Tool Chains Found

### Example: Audio Processing
```python
# create_professional_vintage_mix.py
subprocess.run([
    'ffmpeg',
    '-i', 'LIZARD/WhereYouGoWhenYouLeave_VoiceTrack.wav',
    '-filter:a', 'highpass=f=200,lowpass=f=3500,equalizer...',
    'output.mp4'
])
```

**Intent:** "Deep, pitched-down voice with vintage AM radio characteristics"

### Example: Text Overlay
```python
# add_scrolling_header_to_intros.py
drawtext={font}:text='{title_text}':x={x}:y={y}:fontcolor={color}
```

**Intent:** "Adds a dynamic, scrolling header bar to intro videos"

---

## Hierarchy Depth Analysis

Most files are at **depth 2-3**:

```
CAT/                    Kingdom (depth 1)
├─ WHISKER/            Phylum (depth 2)  ← Most files here
│  └─ MEDIA/           Class (depth 3)
├─ EYE/                Phylum
│  └─ cache/           Class
└─ PAW/                Phylum
```

---

## Data Outputs

### `ARKADU/sys/primitive.jsonl`
One line per file with:
- `path`, `size`, `ext`, `depth`, `mtime`, `name`
- `pattern`: Detected filename schema
- `prompts`: If JSON, whether it contains operative ekphrasis

### `ARKADU/sys/ekphrasis.jsonl`
One line per chain with:
- `prompt_file`: JSON with prompts
- `script`: Python script that reads it
- `sample_prompts`: First 3 prompts
- `uses_ffmpeg`, `uses_drawtext`: Tool detection
- `intent`: Script docstring

---

## What This Reveals

### 1. **Prompts Are Everywhere**
576 JSON files contain actual prompts used to generate images/videos via AI tools (likely Midjourney/Stable Diffusion based on UUID patterns).

### 2. **Semantic Filenames**
Filenames encode metadata:
- Shot numbers (`WGY058`)
- Operator codes (`RI`, `CS`, `DS`)
- Operations (`Memory_Storage_Retrieval`)
- UUIDs (generation tracking)
- Variants (iteration numbers)

### 3. **Multi-Stage Workflows**
```
Prompt (JSON) 
  → AI generation (external)
  → Python assembly (local)
  → ffmpeg processing (local)
  → Final media output
```

### 4. **Operative Ekphrasis = Text→Code→Media**
The prompts aren't just descriptions—they're **operational instructions** that flow through code to produce specific visual/audio results.

---

## Next Steps

1. **Chamber Hierarchy Scan** - Map full Kingdom→Species taxonomy
2. **Family Detection** - Find duplicate/variant clusters
3. **River Tracing** - Build complete provenance graph
4. **Totem Extraction** - Parse all semantic markers from filenames
5. **UI Terminal** - Visualize the ekphrasis ecology

---

**Files Generated:**
- `ARKADU/sys/primitive.jsonl` (10,094 entries)
- `ARKADU/sys/ekphrasis.jsonl` (223 chains)
