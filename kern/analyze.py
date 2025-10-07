#!/usr/bin/env python3
"""
ARKADU Analyzer
Generates insights from scanned data
"""

import json
from pathlib import Path
from collections import defaultdict

def load_jsonl(path):
    """Load JSONL file into list."""
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def analyze_chambers():
    """Analyze chamber distribution."""
    chambers = load_jsonl('ARKADU/sys/chambers.jsonl')
    
    # Group by rank
    by_rank = defaultdict(list)
    for c in chambers:
        by_rank[c['rank']].append(c)
    
    # Find largest chambers at each rank
    print("=" * 60)
    print("LARGEST CHAMBERS BY RANK")
    print("=" * 60)
    
    for rank in ['kingdom', 'phylum', 'class', 'order']:
        if rank in by_rank:
            print(f"\n{rank.upper()} (depth {['kingdom', 'phylum', 'class', 'order'].index(rank) + 1}):")
            top = sorted(by_rank[rank], key=lambda x: x['total_bytes'], reverse=True)[:5]
            for c in top:
                gb = c['total_bytes'] / 1024 / 1024 / 1024
                print(f"  {c['chamber']:45s} {c['file_count']:5d} files  {gb:6.2f} GB")

def analyze_species():
    """Analyze species (file types) distribution."""
    artifacts = load_jsonl('ARKADU/sys/taxonomy.jsonl')
    
    # Count by species
    species_count = defaultdict(int)
    species_bytes = defaultdict(int)
    
    for a in artifacts:
        species = a['species']
        species_count[species] += 1
        species_bytes[species] += a['size']
    
    print("\n" + "=" * 60)
    print("TOP SPECIES (File Types)")
    print("=" * 60)
    
    top_species = sorted(species_bytes.items(), key=lambda x: x[1], reverse=True)[:15]
    for species, total_bytes in top_species:
        count = species_count[species]
        gb = total_bytes / 1024 / 1024 / 1024
        avg_mb = (total_bytes / count) / 1024 / 1024
        print(f"{species:10s} {count:6d} files  {gb:8.2f} GB  (avg: {avg_mb:6.1f} MB/file)")

def analyze_ekphrasis():
    """Analyze operative ekphrasis chains."""
    chains = load_jsonl('ARKADU/sys/ekphrasis.jsonl')
    
    # Find chains with ffmpeg
    ffmpeg_chains = [c for c in chains if c.get('uses_ffmpeg')]
    drawtext_chains = [c for c in chains if c.get('uses_drawtext')]
    
    # Count unique prompts files
    unique_prompts = set(c['prompt_file'] for c in chains)
    unique_scripts = set(c['script'] for c in chains)
    
    print("\n" + "=" * 60)
    print("OPERATIVE EKPHRASIS ECOLOGY")
    print("=" * 60)
    print(f"\nTotal chains traced:        {len(chains)}")
    print(f"Unique prompt files:        {len(unique_prompts)}")
    print(f"Unique assembly scripts:    {len(unique_scripts)}")
    print(f"Chains using ffmpeg:        {len(ffmpeg_chains)}")
    print(f"Chains using drawtext:      {len(drawtext_chains)}")
    
    # Show top scripts by chain count
    script_count = defaultdict(int)
    for c in chains:
        script_name = Path(c['script']).name
        script_count[script_name] += 1
    
    print(f"\nTop assembly scripts:")
    top_scripts = sorted(script_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for script, count in top_scripts:
        print(f"  {script:40s} {count:3d} chains")

def analyze_patterns():
    """Analyze filename patterns."""
    artifacts = load_jsonl('ARKADU/sys/taxonomy.jsonl')
    
    # Count by pattern schema
    pattern_count = defaultdict(int)
    for a in artifacts:
        if 'pattern' in a:
            schema = a['pattern'].get('schema', 'unknown')
            pattern_count[schema] += 1
    
    print("\n" + "=" * 60)
    print("FILENAME PATTERNS")
    print("=" * 60)
    
    for schema, count in sorted(pattern_count.items(), key=lambda x: x[1], reverse=True):
        if count > 5:  # Only show significant patterns
            print(f"{schema:20s} {count:6d} files")

def generate_summary_stats():
    """Generate overall summary statistics."""
    artifacts = load_jsonl('ARKADU/sys/taxonomy.jsonl')
    chambers = load_jsonl('ARKADU/sys/chambers.jsonl')
    chains = load_jsonl('ARKADU/sys/ekphrasis.jsonl')
    
    total_bytes = sum(a['size'] for a in artifacts)
    total_gb = total_bytes / 1024 / 1024 / 1024
    
    # Count prompts
    prompt_count = 0
    for a in artifacts:
        if 'prompts' in a and a['prompts'].get('has_prompts'):
            prompt_count += 1
    
    print("\n" + "=" * 60)
    print("ARKADU OS - SYSTEM SUMMARY")
    print("=" * 60)
    print(f"""
Total artifacts:           {len(artifacts):,}
Total chambers:            {len(chambers):,}
Total storage:             {total_gb:.2f} GB
JSON files with prompts:   {prompt_count:,}
Ekphrasis chains traced:   {len(chains):,}

Deepest taxonomy depth:    {max(a['depth'] for a in artifacts)}
Unique species (types):    {len(set(a['species'] for a in artifacts))}
""")

# Run analysis
if __name__ == '__main__':
    print("\nARKADU Analyzer v1.0")
    print("=" * 60)
    
    generate_summary_stats()
    analyze_chambers()
    analyze_species()
    analyze_patterns()
    analyze_ekphrasis()
    
    print("\n" + "=" * 60)
    print("Analysis complete")
    print("=" * 60)
