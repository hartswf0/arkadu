# ARKADU OS - Quick Start Guide

## 30-Second Start

```bash
cd "/Users/gaia/resurrecting atlantis"

# Run full system scan (takes ~30 seconds)
bash ARKADU/bin/scan

# View in browser
open ARKADU/shell/terminal.html
```

---

## What You'll See

### STATUS Tab
- Total artifacts: **10,097 files**
- Total storage: **56.48 GB**
- Ekphrasis chains: **223 traced**
- Top kingdoms by size (LIZARD, REAL, SHARK...)

### CHAMBERS Tab
Browse the taxonomic hierarchy:
- **Kingdom** (depth 1): ANT, CAT, DOG, HORSE, etc.
- **Phylum** (depth 2): CAT/WHISKER, LIZARD/VOICE_VARIATIONS
- **Class** (depth 3): CAT/WHISKER/MEDIA, CAT/EYE/cache

### SPECIES Tab
File types by storage:
- `.mp4` - 735 files, 41.08 GB (video)
- `.png` - 5,966 files, 6.40 GB (images)
- `.wav` - 350 files, 4.06 GB (audio)

### EKPHRASIS Tab
Operative ekphrasis chains:
```
JSON (prompts) → Python (assembly) → Media (output)
```

---

## Understanding the Output

### What Are Chambers?
**Chambers** = directories organized by taxonomic rank:
- Depth 1 = **Kingdom** (CAT, DOG, HORSE)
- Depth 2 = **Phylum** (CAT/WHISKER, CAT/PAW)
- Depth 3 = **Class** (CAT/WHISKER/MEDIA)

### What Are Species?
**Species** = file types (extensions):
- `.mp4`, `.png`, `.jpg`, `.wav`, `.json`, `.py`, etc.

### What Are Ekphrasis Chains?
**Operative ekphrasis** = text prompts flowing through code into generated media:

```
CAT/storyboard.json
  Prompt: "A dimly lit plain bedroom in a high-rise apartment."
  ↓
timeline_generator.py
  (Reads JSON, assembles images into video)
  ↓
slideshow.mp4
  (Generated output)
```

---

## Data Files Explained

### `ARKADU/sys/primitive.jsonl`
One line per file with:
```json
{
  "path": "CAT/WHISKER/file.png",
  "size": 1234567,
  "ext": ".png",
  "depth": 3,
  "pattern": {"schema": "CAT_WHISKER", "shot_num": "058"}
}
```

### `ARKADU/sys/taxonomy.jsonl`
Taxonomic IDs for each file:
```json
{
  "taxonomic_id": "CAT.WHISKER.MEDIA.png.a1b2c3d4",
  "taxonomy": {
    "kingdom": "CAT",
    "phylum": "WHISKER",
    "class": "MEDIA",
    "species": ".png"
  }
}
```

### `ARKADU/sys/chambers.jsonl`
Chamber summaries:
```json
{
  "chamber": "CAT/WHISKER",
  "rank": "phylum",
  "file_count": 1154,
  "total_bytes": 1234567890,
  "dominant_species": [".png", ".jpg"]
}
```

### `ARKADU/sys/ekphrasis.jsonl`
Traced chains:
```json
{
  "prompt_file": "CAT/storyboard.json",
  "script": "timeline_generator.py",
  "sample_prompts": ["A dimly lit bedroom..."],
  "uses_ffmpeg": true
}
```

---

## Common Tasks

### Find Largest Files
```bash
jq 'select(.size > 100000000) | {path, size}' ARKADU/sys/primitive.jsonl
```

### Count Files by Kingdom
```bash
jq -r '.path' ARKADU/sys/primitive.jsonl | cut -d'/' -f1 | sort | uniq -c
```

### List All Prompt Files
```bash
jq 'select(.prompts.has_prompts == true) | .path' ARKADU/sys/primitive.jsonl
```

### Find Chambers with Most Files
```bash
jq 'select(.depth == 2) | {chamber, file_count}' ARKADU/sys/chambers.jsonl | sort -t: -k2 -nr | head
```

### Show Ekphrasis Chains Using ffmpeg
```bash
jq 'select(.uses_ffmpeg == true)' ARKADU/sys/ekphrasis.jsonl
```

---

## Analysis Commands

```bash
# Full statistical analysis
python3 ARKADU/kern/analyze.py

# Re-scan specific sections
python3 ARKADU/kern/primitive_scan.py    # Files only
python3 ARKADU/kern/taxonomy_scan.py     # Hierarchy only
python3 ARKADU/kern/ekphrasis_trace.py   # Chains only
```

---

## Troubleshooting

### "Cannot find sys/*.jsonl files"
**Solution:** Run the scan first:
```bash
bash ARKADU/bin/scan
```

### "Terminal shows no data"
**Solution:** Check browser console for errors. Make sure you're serving via HTTP:
```bash
cd "/Users/gaia/resurrecting atlantis"
python3 -m http.server 8000
# Then visit: http://localhost:8000/ARKADU/shell/terminal.html
```

### "Scan takes too long"
The scan processes ~10,000 files. Expected times:
- Primitive scan: ~15 seconds
- Taxonomy scan: ~10 seconds
- Ekphrasis trace: ~5 seconds
- **Total: ~30 seconds**

---

## Next Steps

1. **Review the data** in terminal.html
2. **Read SYSTEM-REPORT.md** for detailed findings
3. **Decide on storage strategy** (what to keep in Git vs external)
4. **Generate .gitignore** based on scan results
5. **Archive large files** to Internet Archive

---

## Key Insights

### Storage Hotspots
- **LIZARD/** - 9.88 GB of audio temp files (could be cleaned)
- **MANTA/final/** - 6.91 GB of final videos (archive candidates)
- **CAT/EYE/** - 5.77 GB of working images (archive candidates)

### File Type Distribution
- **Videos** = 73% of storage (735 files, 41 GB)
- **Images** = 12% of storage (7,282 files, 9 GB)
- **Audio** = 7% of storage (350 files, 4 GB)

### Operative Ekphrasis
- **576 prompt files** containing ~15,000+ prompts
- **223 chains** connecting prompts → code → media
- **36 actively used** prompt files
- **6 scripts** using ffmpeg for video generation

---

## Support

- **Full documentation:** `ARKADU/README.md`
- **System report:** `ARKADU/SYSTEM-REPORT.md`
- **Primitive scan report:** `ARKADU/PRIMITIVE-SCAN-REPORT.md`
- **Original excavation:** `ARKADU/EXCAVATION-REPORT.md`

---

*ARKADU OS v1.0 - Media Archaeology Operating System*
