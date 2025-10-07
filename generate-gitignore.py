#!/usr/bin/env python3
"""
Generate intelligent .gitignore based on ARKADU manifest analysis
"""

import json
from pathlib import Path

def load_manifest(path='media-manifest.json'):
    with open(path, 'r') as f:
        return json.load(f)

def generate_gitignore(manifest):
    """Generate .gitignore based on artifact analysis"""
    
    all_artifacts = (manifest['artifacts']['images'] + 
                    manifest['artifacts']['videos'] + 
                    manifest['artifacts']['audio'])
    
    # Find files to keep (linked or small)
    keep_files = set()
    keep_patterns = set()
    
    for artifact in all_artifacts:
        # Keep if used by HTML files
        if artifact.get('used_by'):
            keep_files.add(artifact['path'])
        
        # Keep small header prompts
        if 'header_prompt' in artifact['path'] and artifact['size'] < 20_000_000:
            keep_patterns.add('*_header_prompt.mp4')
        
        # Keep clapper cards
        if 'clapper' in artifact['path'].lower():
            keep_patterns.add('*clapper*.png')
    
    # Generate ignore rules
    rules = []
    rules.append("# ARKADU-generated .gitignore")
    rules.append("# Media Archaeology Strategy: Selective Archival")
    rules.append("")
    
    rules.append("# Exclude large video formats")
    rules.append("*.mp4")
    rules.append("*.mov")
    rules.append("*.avi")
    rules.append("*.webm")
    rules.append("*.mkv")
    rules.append("")
    
    rules.append("# Exclude large audio formats")
    rules.append("*.wav")
    rules.append("!*.mp3  # MP3s are usually small enough")
    rules.append("")
    
    rules.append("# But keep critical video artifacts")
    for pattern in sorted(keep_patterns):
        rules.append(f"!{pattern}")
    rules.append("")
    
    rules.append("# Exclude animal working directories")
    animal_dirs = set()
    for artifact in all_artifacts:
        if '/MEDIA/' in artifact['path'] or '/TRUNK/' in artifact['path']:
            parts = Path(artifact['path']).parts
            if len(parts) > 2:
                animal_dirs.add(f"{parts[0]}/{parts[1]}/")
    
    for animal_dir in sorted(animal_dirs):
        rules.append(f"{animal_dir}")
    rules.append("")
    
    rules.append("# Exclude large compilations")
    for artifact in all_artifacts:
        if artifact['size'] > 100_000_000:  # >100 MB
            rules.append(f"{artifact['path']}")
    rules.append("")
    
    rules.append("# Keep archaeology tools and manifests")
    rules.append("!ARKADU/")
    rules.append("!media-manifest.json")
    rules.append("!*.html")
    rules.append("!*.py")
    rules.append("!*.md")
    rules.append("")
    
    rules.append("# Standard exclusions")
    rules.append(".DS_Store")
    rules.append("__pycache__/")
    rules.append("*.pyc")
    rules.append(".venv/")
    rules.append("venv/")
    
    return '\n'.join(rules)

def analyze_savings(manifest):
    """Calculate how much space we'd save"""
    all_artifacts = (manifest['artifacts']['images'] + 
                    manifest['artifacts']['videos'] + 
                    manifest['artifacts']['audio'])
    
    excluded_size = 0
    kept_size = 0
    
    for artifact in all_artifacts:
        is_video = artifact['path'].endswith(('.mp4', '.mov', '.avi', '.webm', '.mkv'))
        is_large = artifact['size'] > 100_000_000
        is_media_dir = '/MEDIA/' in artifact['path'] or '/TRUNK/' in artifact['path']
        has_keep_pattern = ('header_prompt' in artifact['path'] or 
                           'clapper' in artifact['path'].lower())
        is_linked = bool(artifact.get('used_by'))
        
        should_exclude = (is_video or is_large or is_media_dir) and not (has_keep_pattern or is_linked)
        
        if should_exclude:
            excluded_size += artifact['size']
        else:
            kept_size += artifact['size']
    
    return {
        'excluded_mb': round(excluded_size / 1_000_000, 2),
        'kept_mb': round(kept_size / 1_000_000, 2),
        'savings_percent': round((excluded_size / (excluded_size + kept_size)) * 100, 1)
    }

if __name__ == '__main__':
    manifest = load_manifest()
    
    # Generate .gitignore
    gitignore_content = generate_gitignore(manifest)
    
    # Write to file
    output_path = Path('.gitignore.arkadu')
    with open(output_path, 'w') as f:
        f.write(gitignore_content)
    
    print("✓ Generated .gitignore.arkadu")
    print(f"  Review and rename to .gitignore to use")
    print()
    
    # Show savings analysis
    savings = analyze_savings(manifest)
    print("📊 Storage Analysis:")
    print(f"  Would exclude: {savings['excluded_mb']} MB")
    print(f"  Would keep:    {savings['kept_mb']} MB")
    print(f"  Space savings: {savings['savings_percent']}%")
    print()
    print("⚠️  Review .gitignore.arkadu before using!")
    print("   Make sure critical files aren't excluded.")
