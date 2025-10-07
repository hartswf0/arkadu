#!/usr/bin/env python3
"""
ARKADU Ekphrasis Tracer
Maps operative ekphrasis chains:
  JSON (prompts) → Python (assembly scripts) → Media (generated output)
"""

import json
import re
import ast
from pathlib import Path
from collections import defaultdict

def find_json_with_prompts():
    """
    Find all JSON files containing operativeEkphrasis.
    """
    prompt_files = []
    root = Path('.')
    
    for json_file in root.rglob('*.json'):
        # Skip venv/cache
        if any(skip in str(json_file) for skip in ['.venv', 'node_modules', '__pycache__']):
            continue
        
        try:
            content = json_file.read_text(encoding='utf-8', errors='ignore')
            if 'operativeEkphrasis' in content:
                data = json.loads(content)
                if isinstance(data, list):
                    prompt_files.append({
                        'path': str(json_file),
                        'entry_count': len(data),
                        'sample_prompts': [
                            item.get('operativeEkphrasis', '')[:80]
                            for item in data[:3]
                            if 'operativeEkphrasis' in item
                        ]
                    })
        except:
            pass
    
    return prompt_files

def find_python_scripts():
    """
    Find all Python scripts (exclude venv).
    """
    scripts = []
    root = Path('.')
    
    for py_file in root.rglob('*.py'):
        # Skip venv/cache
        if any(skip in str(py_file) for skip in ['.venv', 'venv', 'node_modules', '__pycache__', 'site-packages']):
            continue
        
        scripts.append(py_file)
    
    return scripts

def trace_json_usage_in_script(script_path):
    """
    Find JSON files referenced in Python script.
    """
    try:
        content = script_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return []
    
    # Find JSON file references
    json_refs = []
    
    # Pattern 1: direct file paths
    for match in re.finditer(r'["\']([^"\']+\.json)["\']', content):
        json_path = match.group(1)
        json_refs.append(json_path)
    
    # Pattern 2: variable assignments
    for match in re.finditer(r'(\w+)\s*=\s*["\']([^"\']+\.json)["\']', content):
        var_name = match.group(1)
        json_path = match.group(2)
        json_refs.append(json_path)
    
    return list(set(json_refs))

def trace_ffmpeg_usage_in_script(script_path):
    """
    Find ffmpeg/subprocess calls in Python script.
    """
    try:
        content = script_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return []
    
    ffmpeg_calls = []
    
    # Check for ffmpeg usage
    if 'ffmpeg' in content or 'subprocess' in content:
        # Extract docstring (intent)
        try:
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
        except:
            docstring = None
        
        # Check for drawtext (text overlay)
        has_drawtext = 'drawtext' in content
        
        # Check for overlay operations
        has_overlay = any(term in content for term in ['overlay', 'vf', 'filter'])
        
        ffmpeg_calls.append({
            'script': str(script_path),
            'intent': docstring[:200] if docstring else None,
            'uses_drawtext': has_drawtext,
            'uses_overlay': has_overlay,
            'likely_generates_video': '.mp4' in content or '.mov' in content
        })
    
    return ffmpeg_calls

def build_ekphrasis_chains():
    """
    Connect JSON prompts → Python scripts → Video outputs.
    """
    print("Finding JSON files with prompts...")
    prompt_files = find_json_with_prompts()
    print(f"  Found {len(prompt_files)} JSON files with prompts")
    
    print("\nFinding Python scripts...")
    scripts = find_python_scripts()
    print(f"  Found {len(scripts)} Python scripts")
    
    print("\nTracing connections...")
    chains = []
    script_to_json = defaultdict(list)
    script_to_ffmpeg = {}
    
    for script in scripts:
        # Find JSON references
        json_refs = trace_json_usage_in_script(script)
        if json_refs:
            script_to_json[str(script)] = json_refs
        
        # Find ffmpeg usage
        ffmpeg_usage = trace_ffmpeg_usage_in_script(script)
        if ffmpeg_usage:
            script_to_ffmpeg[str(script)] = ffmpeg_usage[0]
    
    # Build chains
    for script_path, json_refs in script_to_json.items():
        # Check if this script uses ffmpeg
        ffmpeg_info = script_to_ffmpeg.get(script_path)
        
        # Match JSON refs to actual prompt files
        for json_ref in json_refs:
            # Find matching prompt file
            matching_prompts = [
                pf for pf in prompt_files
                if json_ref in pf['path'] or Path(json_ref).name in pf['path']
            ]
            
            if matching_prompts:
                for prompt_file in matching_prompts:
                    chain = {
                        'type': 'operative_ekphrasis_chain',
                        'prompt_file': prompt_file['path'],
                        'script': script_path,
                        'sample_prompts': prompt_file['sample_prompts'],
                        'uses_ffmpeg': ffmpeg_info is not None if ffmpeg_info else False,
                        'uses_drawtext': ffmpeg_info['uses_drawtext'] if ffmpeg_info else False,
                        'intent': ffmpeg_info['intent'] if ffmpeg_info else None
                    }
                    chains.append(chain)
    
    return chains

# Run tracer
if __name__ == '__main__':
    print("ARKADU Ekphrasis Tracer v1.0")
    print("=" * 50)
    
    chains = build_ekphrasis_chains()
    
    print(f"\n✓ Found {len(chains)} ekphrasis chains")
    
    # Create output directory
    Path('ARKADU/sys').mkdir(parents=True, exist_ok=True)
    
    # Write output
    with open('ARKADU/sys/ekphrasis.jsonl', 'w') as f:
        for chain in chains:
            f.write(json.dumps(chain) + '\n')
    
    print(f"✓ Output: ARKADU/sys/ekphrasis.jsonl")
    
    # Show samples
    if chains:
        print(f"\nSample chains:")
        for chain in chains[:3]:
            print(f"\n  {Path(chain['prompt_file']).name}")
            print(f"    → {Path(chain['script']).name}")
            if chain['sample_prompts']:
                print(f"    Prompt: {chain['sample_prompts'][0][:60]}...")
            if chain['uses_drawtext']:
                print(f"    Uses drawtext overlay ✓")
