# ARKADU NAVIGATOR - Advanced Hyperlink & Transclusion Explorer

## What This Is

**A complete file navigation system with transclusion and hyperlink following.**

Unlike the basic terminal, the Navigator lets you:
- **See complete file content** (transclusion)
- **Click to follow links** between files (hyperlinks)
- **Navigate bidirectionally** (inbound/outbound)
- **Explore chains visually** (JSON→Python→Media)
- **Search everything instantly**
- **Track your navigation history**

---

## What Was Missing Before

### Old Terminal Problems
❌ Only showed statistics (no file content)  
❌ No way to see what file references what  
❌ No clickable navigation  
❌ No transclusion (couldn't read files)  
❌ Chains were just text lists  

### NEW Navigator Solutions
✅ Shows complete file source code  
✅ Click any file reference to open it  
✅ See both inbound and outbound connections  
✅ Full transclusion (read entire files)  
✅ Interactive chain visualization  
✅ Search across all files  
✅ Recent files sidebar  

---

## How to Access

### ⚠️ CRITICAL: Use HTTP, Not file://

**WRONG (doesn't work):**
```
Double-clicking navigator.html → file:// → CORS errors
```

**CORRECT (works perfectly):**
```
http://localhost:8001/navigator.html
```

### Start Server First

```bash
cd "/Users/gaia/resurrecting atlantis/ARKADU"
python3 -m http.server 8001
```

Then open: **http://localhost:8001/navigator.html**

---

## Features

### 1. Full File Transclusion

**What it means:** You can see the COMPLETE content of any file.

**How it works:**
- Click "Python Scripts" → list of all 256 Python files
- Click any Python file → window shows:
  - Complete source code (every line)
  - Documentation (docstrings)
  - Imports (all dependencies)
  - Subprocess calls (ffmpeg, etc.)

**Example:**
```
Click: create_professional_vintage_mix.py
→ See complete 147 lines of source
→ See all ffmpeg subprocess calls
→ See all file references
```

### 2. Hyperlink Navigation

**What it means:** Click any file reference to jump to that file.

**How it works:**
- When viewing a file, see "References (Outbound)"
- Lists all files THIS file references
- Click any reference → jumps to that file
- See "Referenced By (Inbound)" → what files reference THIS one
- Click to navigate backwards

**Example:**
```
Viewing: timeline_generator.py
→ See "References: storyboard.json"
→ Click storyboard.json
→ Navigator opens that JSON file
→ See all 89 prompts inside
→ See what OTHER files reference it
→ Click to navigate to those
```

### 3. Bidirectional Links

**What it means:** See both directions of connections.

**Outbound (What I Reference):**
- Files this file reads/imports/uses
- Click to see those files

**Inbound (What References Me):**
- Files that read/import/use this file
- Click to see those files

**Example:**
```
storyboard.json shows:
  Referenced By (Inbound): 3 files
    → timeline_generator.py (python_reference)
    → create_montage.py (json_reference)
    → assemble_final.py (json_reference)
  
  Click any → jump to that file
  See how they use storyboard.json
```

### 4. Ekphrasis Chain Visualization

**What it means:** See and navigate complete JSON→Python→Media chains.

**How it works:**
- Click "Ekphrasis Chains" in sidebar
- See all 223 chains visualized
- Each chain shows: JSON file → Python script → Media tool
- Click any file in chain to open it
- See the prompts being used
- See the code that processes them

**Example:**
```
Chain 47:
  storyboard.json → timeline_generator.py → ffmpeg

Click storyboard.json:
  → See 89 operative ekphrasis prompts
  → "Title etched in pulsating crimson..."
  
Click timeline_generator.py:
  → See complete source code
  → See ffmpeg subprocess calls
  → See how it reads the JSON
  → See the drawtext commands
```

### 5. Search Everything

**What it means:** Instant search across all files.

**How it works:**
- Type in search box at top
- Searches file names and paths
- Shows matching results instantly
- Click any result to open that file

**Example:**
```
Search: "vintage"
→ Shows: create_professional_vintage_mix.py
→ Click to open and read complete source
```

### 6. Recent Files History

**What it means:** Quick access to files you've already opened.

**How it works:**
- Every file you open is tracked
- Shows last 10 files in sidebar
- Click to reopen instantly
- Navigate your path through the system

---

## Interface Layout

```
┌──────────────────────────────────────────────────────────────┐
│ ARKADU NAVIGATOR | Hyperlink & Transclusion Explorer   [Search]│
├──────────┬────────────────────────────────┬─────────────────┤
│          │                                │  CONTEXT &      │
│ FILE     │      MAIN VIEW                 │  CONNECTIONS    │
│ TYPES    │                                │                 │
│          │  • File content (transclusion) │  Outbound: 12   │
│ Python   │  • Source code                 │  Inbound: 5     │
│ JSON     │  • Documentation               │                 │
│ Chains   │  • Imports                     │  References:    │
│          │  • Subprocess calls            │  - file1.json   │
│ RECENT   │                                │  - file2.py     │
│ FILES    │                                │                 │
│          │                                │  Chains: 3      │
│ file1.py │                                │  - Chain 1      │
│ file2.js │                                │  - Chain 2      │
└──────────┴────────────────────────────────┴─────────────────┘
│ Breadcrumb: path/to/current/file.py                   Stats  │
└──────────────────────────────────────────────────────────────┘
```

---

## Use Cases

### Use Case 1: Trace Video Generation

**Goal:** Understand how videos are created

**Steps:**
1. Open Navigator
2. Click "Ekphrasis Chains"
3. Find chain with video output
4. Click the JSON file → see prompts
5. Click the Python script → see complete source
6. See subprocess calls to ffmpeg
7. See exact commands used

**Result:** Complete understanding of pipeline

### Use Case 2: Find All Uses of a File

**Goal:** See what uses storyboard.json

**Steps:**
1. Search "storyboard.json"
2. Click to open it
3. Look at right panel: "Referenced By (Inbound)"
4. See list of all files that reference it
5. Click each to see how they use it

**Result:** Complete usage map

### Use Case 3: Explore Code Dependencies

**Goal:** See what a Python script imports and uses

**Steps:**
1. Click "Python Scripts"
2. Click any script
3. See "Imports" section
4. See "References (Outbound)" section
5. Click any reference to explore
6. Navigate the dependency graph

**Result:** Complete dependency understanding

### Use Case 4: Read Complete Source

**Goal:** Read every line of a Python file

**Steps:**
1. Search or browse to Python file
2. Click to open
3. See "Source Code" section
4. Complete file content displayed
5. Scroll through all lines
6. See documentation, imports, calls

**Result:** Full code comprehension

### Use Case 5: Discover Connections

**Goal:** Find unexpected relationships

**Steps:**
1. Start with any file
2. Look at connections panel
3. Follow inbound/outbound links
4. Discover files you didn't know existed
5. Map the actual system structure

**Result:** System archaeology complete

---

## Data Loaded

**The Navigator loads:**
- 256 Python files (3.5 MB) - **Complete source code**
- 704 JSON files (32 MB) - **Full content**
- 960 graph nodes - **All files**
- 127,171 edges - **Every connection**
- 223 ekphrasis chains - **Complete chains**

**Total:** 63.3 MB of complete, uncompressed data

---

## Performance

**Load time:** ~4 seconds (first load)  
**Navigation:** Instant (all data in memory)  
**Search:** Real-time filtering  
**Memory:** ~200 MB browser memory  
**Smoothness:** No lag, instant response  

---

## Comparison to Other Tools

### vs Terminal (shell/terminal.html)
- **Terminal:** Shows stats only
- **Navigator:** Shows complete files + stats

### vs TRUE-ARKADU
- **TRUE-ARKADU:** Window system, multiple files
- **Navigator:** Single-file focus, connection panel, chains

### vs ECOLOGY
- **ECOLOGY:** Visual dots/particles
- **Navigator:** Text-based file content

**Use Navigator when you want to:**
- Read complete source code
- Follow hyperlinks between files
- Trace chains interactively
- Understand connections
- Search for specific files

---

## Technical Details

### Architecture

**3-Panel Layout:**
1. **Left Sidebar:** File types, recent files
2. **Main View:** Current file content (transclusion)
3. **Right Panel:** Connections, links, chains

**Data Flow:**
```
HTTP Fetch → JSON Parse → Index Build → Interactive UI
           ↓
  Python files (full source)
  JSON files (full content)
  Graph (all edges)
  Chains (complete)
```

**Navigation:**
```
Click file → Load content → Show in main → Extract connections → Show in panel
           ↓                              ↓
      Add to history              Find inbound/outbound
           ↓                              ↓
     Update sidebar              Render clickable links
```

### Connection Detection

**Outbound (What I Reference):**
- Extracted from graph edges where `source === current_file`
- Shows: target file, edge type, path
- Clickable to navigate

**Inbound (What References Me):**
- Extracted from graph edges where `target === current_file`
- Shows: source file, edge type, path
- Clickable to navigate

**Chains:**
- Filtered from all 223 chains
- Shows only chains involving current file
- Interactive visualization

---

## Keyboard Shortcuts

*Future feature - not yet implemented*

Planned:
- `Ctrl+F` - Focus search
- `Ctrl+B` - Back in history
- `Ctrl+L` - Show connections
- `Ctrl+E` - Show chains
- `Escape` - Clear selection

---

## Known Limitations

1. **Must use HTTP server** - Cannot open via file://
2. **Large files may be slow** - 32 MB JSON takes a moment
3. **No syntax highlighting** - Raw source code display
4. **No line numbers** - Plain text view
5. **No editing** - Read-only viewer

**These are acceptable trade-offs for complete data access.**

---

## Future Enhancements

Possible additions:
- [ ] Syntax highlighting for code
- [ ] Line numbers in source view
- [ ] Multi-file comparison
- [ ] Export connection graphs
- [ ] Visual graph rendering
- [ ] Timeline view of chains
- [ ] Filter by file type in connections
- [ ] Bookmark important files
- [ ] Notes/annotations on files
- [ ] Dark/light theme toggle

---

## Status

✅ **OPERATIONAL**

**Currently showing:**
- 256 Python files (complete source)
- 704 JSON files (full content)
- 960 nodes, 127,171 connections
- 223 ekphrasis chains
- Full transclusion
- Bidirectional navigation
- Interactive search

**Ready for:**
- Code archaeology
- Dependency exploration
- Chain tracing
- Hyperlink navigation
- System comprehension

---

## Access Now

**Open this URL:**
```
http://localhost:8001/navigator.html
```

**Or from master index:**
```
http://localhost:8001/index-master.html
→ Click "NAVIGATOR" card
```

---

*ARKADU Navigator v1.0*  
*Hyperlink Following | Transclusion | Bidirectional Links*  
*Complete System Navigation*
