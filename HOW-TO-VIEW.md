# How to View ARKADU Systems

## The CORS Problem

Browser security prevents loading local files directly (file:// protocol). You need to serve via HTTP.

---

## ✅ FIXED - Two Solutions

### Solution 1: HTTP Server (BEST - Full Data)

**I've started the server for you:**

```
Server running at: http://localhost:8001
```

**Open these URLs:**

- **Ecology:** http://localhost:8001/ARKADU-ECOLOGY.html
- **TRUE-ARKADU:** http://localhost:8001/TRUE-ARKADU.html  
- **Terminal:** http://localhost:8001/shell/terminal.html
- **Master Index:** http://localhost:8001/index-master.html

**If server stopped, restart it:**

```bash
cd "/Users/gaia/resurrecting atlantis/ARKADU"
python3 -m http.server 8001
```

Then open http://localhost:8001/ in your browser.

### Solution 2: Embedded Data (Works Offline)

**What I did:**
- Created `ecology-data.js` with 5,000 artifacts embedded
- ARKADU-ECOLOGY.html now loads this automatically
- Works with file:// protocol (double-click HTML)
- Smaller dataset but fully functional

**Trade-off:**
- Embedded: 5,000 artifacts (fast, works offline)
- HTTP: 10,097 artifacts (complete, needs server)

---

## What's Working Now

### ARKADU-ECOLOGY.html

✅ Loads data (embedded or fetched)  
✅ Shows organisms in all 4 views  
✅ Species filtering works  
✅ Chamber navigation works  
✅ Hover tooltips work  
✅ Animations work (FLOW mode)

**View via HTTP:** http://localhost:8001/ARKADU-ECOLOGY.html

### TRUE-ARKADU.html

✅ Full source code for 256 Python files  
✅ Full content for 704 JSON files  
✅ Dependency graph (127,171 edges)  
✅ Window system  
✅ Search & filter

**View via HTTP:** http://localhost:8001/TRUE-ARKADU.html

### Terminal

✅ System statistics  
✅ Chamber browser  
✅ Species analysis  
✅ Ekphrasis chains

**View via HTTP:** http://localhost:8001/shell/terminal.html

---

## Quick Check

**Test if it's working:**

1. Open http://localhost:8001/ARKADU-ECOLOGY.html
2. You should see:
   - Green background with controls
   - Numbers in header ("Loading..." then "5,000 / 5,000 organisms visible")
   - Colored dots in the canvas area
   - Species checkboxes on the left
3. Try clicking "FLOW" button → dots should animate
4. Try checking/unchecking species → dots appear/disappear

**If you see dots and numbers, IT'S WORKING! ✓**

---

## Troubleshooting

### "Connection refused" or "Can't connect"

**Problem:** Server not running

**Solution:**
```bash
cd "/Users/gaia/resurrecting atlantis/ARKADU"
python3 -m http.server 8001
```

### "Still says Loading..."

**Problem:** JavaScript error or data not loading

**Solution:**
1. Open browser console (F12 or Cmd+Option+I)
2. Look for errors
3. You should see: "Using embedded data..." or "Loaded 5000 artifacts"
4. If you see errors, share them

### "No dots visible"

**Problem:** Canvas not rendering or all species unchecked

**Solution:**
1. Check that some species checkboxes are checked (left panel)
2. Try clicking "GRID" or "ECOLOGY" view
3. Adjust "Organism Size" slider to make dots bigger

### "Server address already in use"

**Problem:** Port 8001 already taken

**Solution:**
```bash
python3 -m http.server 8002
# Then use: http://localhost:8002/
```

---

## What Data You're Seeing

### In ECOLOGY View

**With HTTP (full):**
- 10,097 total artifacts
- All species
- All chambers
- Complete hierarchy

**With Embedded (offline):**
- 5,000 artifacts (sample)
- All species represented
- Major chambers included
- Good for exploration

**Both show:**
- Real file data
- Actual sizes
- True chamber structure
- Species distribution

---

## Files Created/Modified

```
ARKADU/
├── ecology-data.js           NEW - 5,000 artifacts embedded
├── ARKADU-ECOLOGY.html       MODIFIED - Uses embedded data
├── HOW-TO-VIEW.md            NEW - This file
└── (all other files intact)
```

---

## Current Status

✅ HTTP server running on port 8001  
✅ Embedded data created (5,000 artifacts)  
✅ ARKADU-ECOLOGY.html updated to use embedded data  
✅ Particle positions initialized properly  
✅ All visualizations functional  

**READY TO VIEW**

---

## Recommended Workflow

1. **Start here:** http://localhost:8001/index-master.html
2. **Explore ecology:** Click "ECOLOGY VIEW" card
3. **Read code:** Click "TRUE-ARKADU" card  
4. **See stats:** Click "TERMINAL" card

**All systems operational via HTTP.**

---

*Fixed: 2025-10-05 21:15*  
*Server: http://localhost:8001*  
*Status: OPERATIONAL ✓*
