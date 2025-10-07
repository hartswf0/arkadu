#!/usr/bin/env python3
"""
ARKADU Primitive Scanner
Most basic scan - no assumptions, just facts:
- path, size, extension, depth, modified time
- detect known filename patterns
- identify JSON files with prompts
"""

import json
import re
from pathlib import Path
from datetime import datetime

def scan_primitive(root_path):
    """
    Most basic scan - captures raw file metadata.
    """
    root = Path(root_path)
    
    for path in root.rglob('*'):
        # Skip venv/cache
        if any(skip in str(path) for skip in ['.venv', 'venv', '__pycache__', '.git', 'node_modules']):
            continue
            
        if path.is_file():
            yield {
                'path': str(path.relative_to(root)),
                'size': path.stat().st_size,
                'ext': path.suffix.lower(),
                'depth': len(path.relative_to(root).parts),
                'mtime': datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                'name': path.name
            }

def detect_pattern(filename):
    """
    Detect known filename patterns.
    """
    # CAT/WHISKER pattern: WGY058_RI__Memory_Storage_Retrieval__POET_and_MOTHE_uuid_0.png
    wgy_match = re.match(r'WGY(\d+)_(\w+)__([^_]+)__(.+)_([a-f0-9-]{36})_(\d+)', filename)
    if wgy_match:
        return {
            'schema': 'CAT_WHISKER',
            'shot_num': wgy_match.group(1),
            'operator': wgy_match.group(2),
            'operation': wgy_match.group(3),
            'uuid': wgy_match.group(5),
            'variant': wgy_match.group(6)
        }
    
    # HORSE pattern: 01_SH_OutOfLife_000000_header_prompt.mp4
    horse_match = re.match(r'(\d+)_(\w+)_(.+?)_(\d+)_header_prompt', filename)
    if horse_match:
        return {
            'schema': 'HORSE_HEADER',
            'track_num': horse_match.group(1),
            'track_code': horse_match.group(2),
            'title': horse_match.group(3),
            'timestamp': horse_match.group(4)
        }
    
    return {'schema': 'unknown'}

def check_for_prompts(path_obj, artifact):
    """
    If JSON, check if it contains operativeEkphrasis prompts.
    """
    if artifact['ext'] == '.json':
        try:
            content = path_obj.read_text(encoding='utf-8', errors='ignore')
            if 'operativeEkphrasis' in content:
                # Sample first operativeEkphrasis
                data = json.loads(content)
                if isinstance(data, list) and len(data) > 0:
                    first_item = data[0]
                    if 'operativeEkphrasis' in first_item:
                        return {
                            'has_prompts': True,
                            'sample_prompt': first_item.get('operativeEkphrasis', '')[:100],
                            'entry_count': len(data)
                        }
        except:
            pass
    return {'has_prompts': False}

# Run scan
if __name__ == '__main__':
    print("ARKADU Primitive Scanner v1.0")
    print("=" * 50)
    print("Scanning...")
    
    root = Path('.')
    count = 0
    prompt_files = []
    
    # Create output directory
    (root / 'ARKADU' / 'sys').mkdir(parents=True, exist_ok=True)
    
    with open('ARKADU/sys/primitive.jsonl', 'w') as f:
        for artifact in scan_primitive('.'):
            path_obj = Path(artifact['path'])
            
            # Add pattern detection
            artifact['pattern'] = detect_pattern(artifact['name'])
            
            # Check for prompts
            artifact['prompts'] = check_for_prompts(path_obj, artifact)
            
            if artifact['prompts']['has_prompts']:
                prompt_files.append(artifact['path'])
            
            f.write(json.dumps(artifact) + '\n')
            count += 1
            
            if count % 1000 == 0:
                print(f"  {count} files...")
    
    print("=" * 50)
    print(f"✓ Scanned {count} files")
    print(f"✓ Found {len(prompt_files)} JSON files with prompts")
    print(f"✓ Output: ARKADU/sys/primitive.jsonl")
    
    if prompt_files:
        print(f"\nSample prompt files:")
        for pf in prompt_files[:5]:
            print(f"  - {pf}")
