#!/usr/bin/env python3
"""
ARKADU Deep Scanner
Comprehensive analysis of ALL files:
- Full media catalog (from original manifest)
- Deep code analysis (read every .py file)
- JSON content analysis (read every .json file)
- Dependency mapping (which files reference which)
- Generation tracking (which code generates which files)
"""

import json
import re
import ast
from pathlib import Path
from collections import defaultdict

def load_original_manifest():
    """Load the original full media-manifest.json"""
    try:
        with open('media-manifest.json') as f:
            data = json.load(f)
        return data
    except:
        return {}

def deep_scan_python_file(py_path):
    """
    Deep analysis of Python file:
    - Read full source code
    - Extract file references (paths in strings)
    - Find subprocess calls (ffmpeg, etc.)
    - Parse imports
    - Find output file generation
    """
    try:
        source = py_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return None
    
    analysis = {
        'path': str(py_path),
        'size': py_path.stat().st_size,
        'lines': len(source.split('\n')),
        'source': source,  # Full source code
        'file_references': [],
        'subprocess_calls': [],
        'imports': [],
        'generates': [],
        'reads': []
    }
    
    # Extract docstring
    try:
        tree = ast.parse(source)
        analysis['docstring'] = ast.get_docstring(tree)
    except:
        analysis['docstring'] = None
    
    # Find file path references (any string that looks like a path)
    for match in re.finditer(r'["\']([^"\']+\.(mp4|png|jpg|wav|json|mp3|mov|avi))["\']', source, re.IGNORECASE):
        path = match.group(1)
        analysis['file_references'].append(path)
    
    # Find directory references
    for match in re.finditer(r'["\']([^"\']+/[^"\']+)["\']', source):
        path = match.group(1)
        if '/' in path and not path.startswith('http'):
            analysis['file_references'].append(path)
    
    # Find subprocess calls
    if 'subprocess' in source or 'ffmpeg' in source:
        for match in re.finditer(r'subprocess\.(run|call|Popen)\s*\((.*?)\)', source, re.DOTALL):
            analysis['subprocess_calls'].append({
                'type': match.group(1),
                'snippet': match.group(2)[:200]
            })
    
    # Find imports
    for match in re.finditer(r'^(?:from|import)\s+(\S+)', source, re.MULTILINE):
        analysis['imports'].append(match.group(1))
    
    # Detect file generation (open for writing, write, save, export)
    if re.search(r'open\([^)]+["\']w["\']', source):
        analysis['generates'].append('writes_files')
    if re.search(r'\.save\(|\.write\(|\.export\(', source):
        analysis['generates'].append('generates_output')
    
    # Detect file reading
    if re.search(r'open\([^)]+["\']r["\']', source):
        analysis['reads'].append('reads_files')
    if re.search(r'json\.load|\.read\(', source):
        analysis['reads'].append('reads_data')
    
    return analysis

def deep_scan_json_file(json_path):
    """
    Deep analysis of JSON file:
    - Read full content
    - Detect structure (array, object)
    - Count entries
    - Sample data
    - Find prompts/ekphrasis
    """
    try:
        content = json_path.read_text(encoding='utf-8', errors='ignore')
        data = json.loads(content)
    except:
        return None
    
    analysis = {
        'path': str(json_path),
        'size': json_path.stat().st_size,
        'content': content,  # Full JSON content
        'data': data,  # Parsed data
        'structure': type(data).__name__,
        'has_prompts': 'operativeEkphrasis' in content,
        'file_references': []
    }
    
    # If it's an array, count entries
    if isinstance(data, list):
        analysis['entry_count'] = len(data)
        analysis['sample'] = data[:3] if len(data) > 0 else []
        
        # Check for prompts in entries
        if len(data) > 0 and isinstance(data[0], dict):
            if 'operativeEkphrasis' in data[0]:
                analysis['prompts'] = [
                    item.get('operativeEkphrasis', '')[:100]
                    for item in data[:5]
                    if 'operativeEkphrasis' in item
                ]
    
    # Find file path references in JSON
    for match in re.finditer(r'["\']([^"\']+\.(mp4|png|jpg|wav|mp3|json))["\']', content, re.IGNORECASE):
        path = match.group(1)
        analysis['file_references'].append(path)
    
    return analysis

def build_dependency_graph(py_analyses, json_analyses, media_manifest):
    """
    Build complete dependency graph:
    - Which Python files reference which JSON files
    - Which Python files generate which media files
    - Which JSON files reference which media files
    """
    graph = {
        'nodes': [],
        'edges': []
    }
    
    # Add Python nodes
    for py in py_analyses:
        graph['nodes'].append({
            'id': py['path'],
            'type': 'python',
            'label': Path(py['path']).name,
            'lines': py['lines'],
            'generates': len(py['generates']) > 0,
            'reads': len(py['reads']) > 0
        })
    
    # Add JSON nodes
    for js in json_analyses:
        graph['nodes'].append({
            'id': js['path'],
            'type': 'json',
            'label': Path(js['path']).name,
            'size': js['size'],
            'has_prompts': js.get('has_prompts', False)
        })
    
    # Add media nodes (from manifest)
    if 'images' in media_manifest:
        for img in media_manifest['images'][:100]:  # Sample
            graph['nodes'].append({
                'id': img['path'],
                'type': 'image',
                'label': Path(img['path']).name
            })
    
    # Build edges (Python → JSON references)
    for py in py_analyses:
        for ref in py['file_references']:
            # Find matching JSON
            matching = [js for js in json_analyses if ref in js['path'] or Path(ref).name in js['path']]
            for match in matching:
                graph['edges'].append({
                    'source': py['path'],
                    'target': match['path'],
                    'type': 'references'
                })
    
    return graph

def run_deep_scan():
    """Run complete deep scan"""
    print("ARKADU Deep Scanner")
    print("=" * 60)
    
    # 1. Load original manifest
    print("\n[1/4] Loading original media manifest...")
    manifest = load_original_manifest()
    print(f"  Loaded manifest with {len(manifest.get('images', []))} images, "
          f"{len(manifest.get('videos', []))} videos")
    
    # 2. Deep scan all Python files
    print("\n[2/4] Deep scanning Python files...")
    py_files = list(Path('.').rglob('*.py'))
    py_files = [f for f in py_files if '.venv' not in str(f) and 'site-packages' not in str(f)]
    
    py_analyses = []
    for i, py_file in enumerate(py_files):
        if i % 50 == 0:
            print(f"  Scanned {i}/{len(py_files)} Python files...")
        analysis = deep_scan_python_file(py_file)
        if analysis:
            py_analyses.append(analysis)
    
    print(f"  ✓ Analyzed {len(py_analyses)} Python files")
    
    # 3. Deep scan all JSON files
    print("\n[3/4] Deep scanning JSON files...")
    json_files = list(Path('.').rglob('*.json'))
    json_files = [f for f in json_files if '.venv' not in str(f) and 'node_modules' not in str(f)]
    
    json_analyses = []
    for i, json_file in enumerate(json_files):
        if i % 50 == 0:
            print(f"  Scanned {i}/{len(json_files)} JSON files...")
        analysis = deep_scan_json_file(json_file)
        if analysis:
            json_analyses.append(analysis)
    
    print(f"  ✓ Analyzed {len(json_analyses)} JSON files")
    
    # 4. Build dependency graph
    print("\n[4/4] Building dependency graph...")
    graph = build_dependency_graph(py_analyses, json_analyses, manifest)
    print(f"  ✓ Graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
    
    # Save outputs
    print("\n" + "=" * 60)
    print("Saving outputs...")
    
    Path('ARKADU/deep').mkdir(parents=True, exist_ok=True)
    
    # Save Python analyses
    with open('ARKADU/deep/python_files.json', 'w') as f:
        json.dump(py_analyses, f, indent=2)
    print(f"  ✓ ARKADU/deep/python_files.json ({len(py_analyses)} files)")
    
    # Save JSON analyses  
    with open('ARKADU/deep/json_files.json', 'w') as f:
        json.dump(json_analyses, f, indent=2)
    print(f"  ✓ ARKADU/deep/json_files.json ({len(json_analyses)} files)")
    
    # Save dependency graph
    with open('ARKADU/deep/dependency_graph.json', 'w') as f:
        json.dump(graph, f, indent=2)
    print(f"  ✓ ARKADU/deep/dependency_graph.json")
    
    # Copy original manifest
    import shutil
    shutil.copy('media-manifest.json', 'ARKADU/deep/media_manifest.json')
    print(f"  ✓ ARKADU/deep/media_manifest.json (original preserved)")
    
    print("\n" + "=" * 60)
    print("✓ Deep scan complete")
    print("=" * 60)

if __name__ == '__main__':
    run_deep_scan()
