# ARKADU 🏛️
## Noah's Ark ⊗ Xanadu: Media Archaeology + Organic Visualization Engine

https://hartswf0.github.io/arkadu/approach-fusion-voronoi.html


> **📖 For complete documentation of all 45+ visualizations, 6 organic algorithms, and ecology systems, see [README-MASTER.md](README-MASTER.md)**

**ARKADU** is a media archaeology system that excavates, catalogs, visualizes, and explores digital artifacts across technocultural strata. It combines the collecting ethos of Noah's Ark with Ted Nelson's Xanadu vision of bidirectional transclusion and deep linking.

### Quick Navigation
- 🏠 **[Master Index](index-master.html)** - Launch all 45+ visualizations
- 📖 **[Complete Documentation](README-MASTER.md)** - Full system guide
- ⚔️ **[Approach 6: Voronoi Warfare](approach-6-depth-test.html)** - Most beautiful algorithm
- 🪨 **[Approach 3: Organic BSP](approach-3-depth-test.html)** - Production recommended
- 🗻 **[Stratigraphic Deep](strata-deep.html)** - Full depth exploration

---

## System Stats

| Metric | Value |
|--------|-------|
| **Artifacts** | 10,094 files |
| **Storage** | 56.48 GB |
| **Visualizations** | 45+ HTML systems |
| **Algorithms** | 6 organic approaches |
| **Ekphrasis Chains** | 223 (JSON→Python→Media) |

---

## Concept

ARKADU treats your media project as an **archaeological site** with multiple **strata** (layers). Each file is an **artifact** that leaves **traces** through **networks** of **circulation**. The system:

- **[excavates]** `<technocultural strata>` by scanning directories
- **[documents]** `<artifacts>` with complete `<metadata>`
- **[reconstructs]** `<provenance>` by analyzing HTML references
- **[maps]** `<circulation>` networks between files
- **[compares]** `<obsolescence>` vs `<persistence>` patterns
- **[evaluates]** `<affordances>` for GitHub storage strategies

This embodies the **Media Archaeologist** ontology: investigating media artifacts across time, comparing formats, and documenting their flows through institutions (GitHub, external hosts, local archives).

---

## Quick Start

### 1. Excavate Your Media
```bash
cd "/Users/gaia/resurrecting atlantis"
python3 ARKADU/arkadu-scan.py .
```

This generates `media-manifest.json` containing:
- Full catalog of all images, videos, audio files
- File metadata (size, modification time, type)
- Animal kingdom classifications (CAT, HORSE, ELEPHANT, etc.)
- Stratum assignments (WHISKER_LAYER, TRUNK_LAYER, etc.)
- Provenance links (which HTML files use which media)
- GitHub storage analysis and recommendations

### 2. View in Browser
```bash
# Open viewer.html in a browser
open ARKADU/viewer.html
```

Or serve it locally:
```bash
python3 -m http.server 8000
# Then visit: http://localhost:8000/ARKADU/viewer.html
```

---

## What Was Discovered

Your **Resurrecting Atlantis** project contains:

| Metric | Value |
|--------|-------|
| **Images** | 6,537 |
| **Videos** | 734 |
| **Audio Files** | 426 |
| **Total Size** | 52.75 GB |
| **HTML Files** | 14 |
| **Linked Artifacts** | 10 |
| **Orphaned Artifacts** | 7,687 (99.9%) |

### Animal Kingdoms (Top Strata)
1. **DOG** — 1,202 artifacts
2. **CAT** — 1,154 artifacts  
3. **JELLYFISH** — 1,080 artifacts
4. **TIGER** — 999 artifacts
5. **HONEYBADGER** — 898 artifacts
6. **SHARK** — 801 artifacts
7. **LIZARD** — 514 artifacts
8. **ELEPHANT** — 410 artifacts

---

## GitHub Storage Strategy

### The Problem
- GitHub file limit: **100 MB per file**
- GitHub repo soft limit: **1 GB recommended**
- Your project: **52.75 GB total**
- Large files: **163 files >50MB**, **119 files >100MB**

### The Solution: **Selective Archival**

#### Keep in Git (with Git LFS)
- Key "header_prompt" videos (one per track, <10 MB each)
- Clapper cards and thumbnails
- Shared assets referenced across multiple HTML files
- `media-manifest.json` (the index of everything)
- Estimated size: **~500 MB**

#### Host Externally
- Full slideshow compilations (`slideshows/*.mp4`)
- Large compilation (`boy_video.mp4` @ 162 MB)
- Animal-specific working directories (CAT/WHISKER/MEDIA/, etc.)
- Options:
  - **Internet Archive** (free, permanent, mission-aligned)
  - **Cloudflare R2** (affordable object storage)
  - **YouTube** (unlisted videos for public access)
  - **GitHub Releases** (large .zip archives)

#### Recommended `.gitignore`
```gitignore
# Exclude all videos by default
*.mp4
*.mov
*.avi
*.webm

# But keep header prompts
!*_header_prompt.mp4
!slideshows/

# Exclude large compilations
boy_video.mp4

# Exclude animal working directories
CAT/WHISKER/MEDIA/
ELEPHANT/TRUNK/
DOG/NOSE/
*/MEDIA/

# Keep the manifest and tools
!media-manifest.json
!ARKADU/
```

---

## File Structure

```
ARKADU/
├── arkadu-scan.py      # Python scanner that excavates all media
├── viewer.html         # Interactive web interface for viewing manifest
├── README.md           # This file
└── (generates)
    └── media-manifest.json   # Complete provenance database
```

---

## The Media Archaeologist Ontology

ARKADU implements the 10-layer ontology you described:

```
<Media Archaeologist>
├─ [investigates] <media> <artifacts>
│   └─ [gathers] <evidence> from <primary sources>
├─ [excavating] <technocultural strata>
│   └─ [composed-of] <layers> (Animal kingdoms)
├─ [reconstruct] <past configurations>
│   └─ [modeled-with] <narratives> (provenance links)
├─ [compare] <obsolescence> with <persistence>
│   └─ [identify] orphaned vs actively-used artifacts
├─ [document] <observations>
│   └─ [annotated-with] <metadata> (dates, sizes, types)
└─ [circulations] across <networks>
    └─ [visible-through] manifest mappings
```

Each scan produces a **stratum report** showing which artifacts persist (actively used), which face obsolescence (orphaned), and how they circulate through your HTML network.

---

## Advanced Usage

### Filter Orphaned Files
The viewer allows filtering orphans by:
- Animal kingdom (e.g., "CAT", "HORSE")
- File type (e.g., "PNG", "MP4")
- Path fragments (e.g., "clapper", "header")

### Export Strategies
Generate custom exports:
```python
# In arkadu-scan.py, add custom export methods
def export_by_animal(self, animal):
    """Export manifest for specific animal stratum"""
    artifacts = self.strata[animal]
    # ... export logic

def export_github_safe_list(self):
    """Export only files safe for GitHub (<50 MB)"""
    safe = [a for a in all_artifacts if a['size'] < 50_000_000]
    # ... export logic
```

### Update Provenance After Changes
Rerun the scanner any time you:
- Add new HTML files
- Reference new media in existing HTML
- Add new media to animal directories

```bash
python3 ARKADU/arkadu-scan.py .
```

The manifest updates automatically.

---

## Xanadu Features

### Bidirectional Links
When HTML file A references image B:
- Image B knows it's used by A (`used_by` field)
- HTML A knows it uses B (`circulation` mapping)

This enables:
- Finding all dependents of a file before deleting
- Tracking which HTML files break if media is moved
- Building dependency graphs

### Transclusion Tracking
The system detects:
- `<img src="...">` references
- `<video src="...">` references  
- `<source src="...">` references
- CSS `url()` references (future)
- JavaScript dynamic loading (future)

### Deep Provenance
Each artifact tracks:
- **Creation time** (file modification date)
- **Format** (file extension, MIME type)
- **Size** (bytes)
- **Location** (stratum, animal kingdom)
- **Usage** (which HTML files reference it)
- **Status** (linked vs orphaned)

---

## Philosophy

ARKADU recognizes that:

1. **Software is archaeological**  
   Every codebase is a site with layers of decisions, abandoned experiments, and evolved patterns.

2. **Media has provenance**  
   Like artifacts in a museum, digital files have histories: who made them, where they've been, what they've been used for.

3. **Circulation reveals meaning**  
   Orphaned files tell a story (working files? deprecated designs?). Heavily-linked files reveal core concepts.

4. **Obsolescence ≠ Worthless**  
   Old media often persists in new forms. The "clapper cards" are remediated into slideshows. The pattern continues.

5. **Documentation is care**  
   By cataloging these 7,697 artifacts, we honor their existence. They're not "junk files" — they're the residue of creative labor.

---

## Next Steps

### For GitHub
1. Create `.gitignore` using the pattern above
2. Add small/critical files to Git
3. Upload large files to Internet Archive
4. Update `media-manifest.json` with external URLs
5. Modify HTML to load from manifest (offline-first)

### For Future Excavations
1. Add video duration extraction (using `ffprobe`)
2. Add image dimension extraction (using `PIL`)
3. Build visual provenance graph (using D3.js or Cytoscape)
4. Create "time machine" view (artifacts by modification date)
5. Add search interface for finding specific files

### For Xanadu Dreams
1. Implement bidirectional hyperlinking in HTML
2. Add version tracking (Git integration)
3. Create transclusion viewer (see file usage in context)
4. Build parallel document comparison tool
5. Enable collaborative annotation of artifacts

---

## Credits

**Concept:** Media Archaeology + Xanadu + Noah's Ark  
**Implementation:** ARKADU Engine  
**Site:** Resurrecting Atlantis  
**Excavated:** October 2025  

> "Every <artifact> leaves <traces>. Every <trace> tells a story.  
> This is that story — 7,697 chapters long."

---

## License

This tool is part of the Resurrecting Atlantis project.  
Media archaeology should be open, accessible, and shared freely.
