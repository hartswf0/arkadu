#!/usr/bin/env python3
"""
ARKADU Taxonomy Scanner
Maps Kingdom→Phylum→Class→Order→Family→Genus→Species hierarchy
Based on actual filesystem structure
"""

import json
from pathlib import Path
from collections import defaultdict

# Taxonomic rank names (Linnaean hierarchy)
RANKS = [
    'kingdom',   # depth 1: ANT, CAT, DOG, etc.
    'phylum',    # depth 2: CAT/WHISKER, CAT/PAW
    'class',     # depth 3: CAT/WHISKER/MEDIA
    'order',     # depth 4: CAT/WHISKER/MEDIA/MR07
    'family',    # depth 5: variant type (raw, export, etc.)
    'genus',     # depth 6: sequence position
    'species'    # file itself (extension)
]

def scan_taxonomy(root_path):
    """
    Walk filesystem and assign taxonomic ranks to each path.
    """
    root = Path(root_path)
    
    # Track chambers (directories) and their contents
    chambers = defaultdict(lambda: {
        'path': None,
        'rank': None,
        'depth': 0,
        'file_count': 0,
        'total_bytes': 0,
        'species': defaultdict(int),  # file types
        'children': set()
    })
    
    # Track all files
    artifacts = []
    
    for path in root.rglob('*'):
        # Skip venv/cache
        if any(skip in str(path) for skip in ['.venv', 'venv', '__pycache__', '.git', 'node_modules']):
            continue
        
        rel_path = path.relative_to(root)
        parts = rel_path.parts
        depth = len(parts)
        
        if path.is_file():
            # This is a species (individual file)
            species = path.suffix.lower() or 'no_ext'
            
            # Build taxonomic ID
            tax_components = list(parts[:-1])  # All but filename
            tax_id_parts = tax_components + [species]
            tax_id = '.'.join(tax_id_parts)
            
            # Determine ranks for each level
            taxonomy = {}
            for i, component in enumerate(parts[:-1]):
                if i < len(RANKS):
                    taxonomy[RANKS[i]] = component
            taxonomy['species'] = species
            
            artifact = {
                'taxonomic_id': tax_id,
                'path': str(rel_path),
                'taxonomy': taxonomy,
                'depth': depth,
                'size': path.stat().st_size,
                'species': species
            }
            artifacts.append(artifact)
            
            # Update parent chamber stats
            if len(parts) > 1:
                chamber_path = str(Path(*parts[:-1]))
                chambers[chamber_path]['file_count'] += 1
                chambers[chamber_path]['total_bytes'] += artifact['size']
                chambers[chamber_path]['species'][species] += 1
        
        elif path.is_dir():
            # This is a chamber (directory)
            chamber_path = str(rel_path)
            rank_idx = depth - 1
            rank = RANKS[rank_idx] if rank_idx < len(RANKS) else 'species'
            
            chambers[chamber_path]['path'] = chamber_path
            chambers[chamber_path]['rank'] = rank
            chambers[chamber_path]['depth'] = depth
            
            # Track parent-child relationships
            if depth > 1:
                parent_path = str(Path(*parts[:-1]))
                chambers[parent_path]['children'].add(chamber_path)
    
    # Convert sets to lists for JSON serialization
    for chamber in chambers.values():
        chamber['children'] = list(chamber['children'])
    
    return artifacts, dict(chambers)

def generate_chamber_summaries(chambers):
    """
    Generate per-chamber summaries with dominant species.
    """
    summaries = []
    
    for chamber_path, data in chambers.items():
        if data['file_count'] > 0:
            # Find dominant species (top 3 file types)
            top_species = sorted(
                data['species'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            summary = {
                'chamber': chamber_path,
                'rank': data['rank'],
                'depth': data['depth'],
                'file_count': data['file_count'],
                'total_bytes': data['total_bytes'],
                'total_mb': round(data['total_bytes'] / 1024 / 1024, 2),
                'dominant_species': [s[0] for s in top_species],
                'species_distribution': dict(data['species']),
                'child_count': len(data['children'])
            }
            summaries.append(summary)
    
    return sorted(summaries, key=lambda x: x['total_bytes'], reverse=True)

# Run scanner
if __name__ == '__main__':
    print("ARKADU Taxonomy Scanner v1.0")
    print("=" * 50)
    print("Scanning filesystem hierarchy...")
    
    artifacts, chambers = scan_taxonomy('.')
    
    print(f"\n✓ Scanned {len(artifacts)} artifacts")
    print(f"✓ Found {len(chambers)} chambers")
    
    # Generate summaries
    print("\nGenerating chamber summaries...")
    summaries = generate_chamber_summaries(chambers)
    
    # Create output directory
    Path('ARKADU/sys').mkdir(parents=True, exist_ok=True)
    
    # Write artifacts (taxonomic IDs for each file)
    with open('ARKADU/sys/taxonomy.jsonl', 'w') as f:
        for artifact in artifacts:
            f.write(json.dumps(artifact) + '\n')
    
    print(f"✓ Output: ARKADU/sys/taxonomy.jsonl ({len(artifacts)} entries)")
    
    # Write chamber summaries
    with open('ARKADU/sys/chambers.jsonl', 'w') as f:
        for summary in summaries:
            f.write(json.dumps(summary) + '\n')
    
    print(f"✓ Output: ARKADU/sys/chambers.jsonl ({len(summaries)} entries)")
    
    # Show top kingdoms (depth 1)
    print("\n" + "=" * 50)
    print("TOP KINGDOMS (Depth 1)")
    print("=" * 50)
    
    kingdoms = [s for s in summaries if s['depth'] == 1]
    for k in sorted(kingdoms, key=lambda x: x['total_bytes'], reverse=True)[:15]:
        mb = k['total_mb']
        bar = '█' * min(int(mb / 100), 40)
        print(f"{k['chamber']:15s} {k['file_count']:5d} files  {mb:8.1f} MB  {bar}")
    
    # Show sample taxonomic IDs
    print("\n" + "=" * 50)
    print("SAMPLE TAXONOMIC IDs")
    print("=" * 50)
    
    for artifact in artifacts[:5]:
        print(f"\n{artifact['path']}")
        print(f"  Tax ID: {artifact['taxonomic_id']}")
        print(f"  Taxonomy: {artifact['taxonomy']}")
