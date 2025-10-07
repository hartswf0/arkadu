#!/usr/bin/env python3
"""
Provenance Network Analysis - Find key nodes in circulation networks
"""

import json
from collections import defaultdict
from pathlib import Path

def load_manifest(path='media-manifest.json'):
    with open(path, 'r') as f:
        return json.load(f)

def analyze_provenance_networks(manifest):
    """Analyze bidirectional provenance links"""
    
    all_artifacts = (manifest['artifacts']['images'] + 
                    manifest['artifacts']['videos'] + 
                    manifest['artifacts']['audio'])
    
    # Build network graph
    artifact_degree = defaultdict(int)  # how many HTML files use this
    html_degree = defaultdict(int)      # how many artifacts this HTML uses
    
    for artifact in all_artifacts:
        if artifact.get('used_by'):
            artifact_degree[artifact['path']] = len(artifact['used_by'])
            for html in artifact['used_by']:
                html_degree[html] += 1
    
    # Find hub artifacts (used by many HTML files)
    hubs = sorted(artifact_degree.items(), key=lambda x: x[1], reverse=True)
    
    # Find hub HTML files (use many artifacts)
    html_hubs = sorted(html_degree.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'artifact_hubs': hubs,
        'html_hubs': html_hubs,
        'total_edges': sum(artifact_degree.values())
    }

def find_shared_artifacts(manifest):
    """Find artifacts shared across multiple HTML files (candidates for Git)"""
    all_artifacts = (manifest['artifacts']['images'] + 
                    manifest['artifacts']['videos'] + 
                    manifest['artifacts']['audio'])
    
    shared = []
    for artifact in all_artifacts:
        if artifact.get('used_by') and len(artifact['used_by']) > 1:
            shared.append({
                'path': artifact['path'],
                'size': artifact['size'],
                'usage_count': len(artifact['used_by']),
                'used_by': artifact['used_by']
            })
    
    return sorted(shared, key=lambda x: x['usage_count'], reverse=True)

def find_critical_paths(manifest):
    """Find artifacts that are critical (only source for an HTML)"""
    circulation = manifest['circulation']
    
    # For each HTML, find its unique dependencies
    critical = []
    for html, artifacts in circulation.items():
        for artifact_path in artifacts:
            # Check if this artifact is used elsewhere
            all_artifacts = (manifest['artifacts']['images'] + 
                           manifest['artifacts']['videos'] + 
                           manifest['artifacts']['audio'])
            
            artifact_obj = next((a for a in all_artifacts if a['path'] == artifact_path), None)
            if artifact_obj and artifact_obj.get('used_by') and len(artifact_obj['used_by']) == 1:
                critical.append({
                    'artifact': artifact_path,
                    'html': html,
                    'size': artifact_obj['size'],
                    'type': artifact_obj['type']
                })
    
    return critical

def recommend_git_subset(manifest):
    """Recommend which files should stay in Git"""
    recommendations = {
        'must_keep': [],    # Shared across files
        'should_keep': [],  # Small and linked
        'can_external': [], # Large but used
        'can_archive': []   # Large and orphaned
    }
    
    all_artifacts = (manifest['artifacts']['images'] + 
                    manifest['artifacts']['videos'] + 
                    manifest['artifacts']['audio'])
    
    for artifact in all_artifacts:
        size = artifact['size']
        linked = bool(artifact.get('used_by'))
        usage_count = len(artifact.get('used_by', []))
        
        # Decision tree
        if usage_count > 1:
            recommendations['must_keep'].append(artifact)
        elif linked and size < 10_000_000:  # <10 MB
            recommendations['should_keep'].append(artifact)
        elif linked and size >= 10_000_000:
            recommendations['can_external'].append(artifact)
        else:  # Not linked
            if size > 50_000_000:  # >50 MB
                recommendations['can_archive'].append(artifact)
            # Small orphans can stay
    
    return recommendations

def print_report(manifest):
    """Print comprehensive provenance analysis"""
    
    print("="*70)
    print("ARKADU PROVENANCE ANALYSIS")
    print("="*70)
    
    # Network analysis
    networks = analyze_provenance_networks(manifest)
    print(f"\n🔗 NETWORK TOPOLOGY")
    print(f"  Total provenance links: {networks['total_edges']}")
    print(f"  HTML hub nodes: {len(networks['html_hubs'])}")
    print(f"  Artifact hub nodes: {len(networks['artifact_hubs'])}")
    
    # Shared artifacts
    shared = find_shared_artifacts(manifest)
    print(f"\n🌟 SHARED ARTIFACTS (used by multiple HTML files)")
    if shared:
        print(f"  Found {len(shared)} shared artifacts")
        for i, item in enumerate(shared[:10], 1):
            size_mb = round(item['size'] / 1_000_000, 2)
            print(f"  {i}. {item['path']}")
            print(f"     Used by {item['usage_count']} files | {size_mb} MB")
    else:
        print("  None found - no artifacts are reused across HTML files")
    
    # HTML hubs
    print(f"\n📄 HTML HUBS (files that use many artifacts)")
    for i, (html, count) in enumerate(networks['html_hubs'][:10], 1):
        print(f"  {i}. {html} → uses {count} artifacts")
    
    # Recommendations
    recs = recommend_git_subset(manifest)
    print(f"\n🎯 GIT STORAGE RECOMMENDATIONS")
    
    must_keep_size = sum(a['size'] for a in recs['must_keep']) / 1_000_000
    should_keep_size = sum(a['size'] for a in recs['should_keep']) / 1_000_000
    can_external_size = sum(a['size'] for a in recs['can_external']) / 1_000_000
    can_archive_size = sum(a['size'] for a in recs['can_archive']) / 1_000_000
    
    print(f"\n  MUST KEEP (shared across files):")
    print(f"    Count: {len(recs['must_keep'])} files")
    print(f"    Size:  {must_keep_size:.2f} MB")
    print(f"    Why:   Used by multiple HTML files - critical to keep")
    
    print(f"\n  SHOULD KEEP (small & linked):")
    print(f"    Count: {len(recs['should_keep'])} files")
    print(f"    Size:  {should_keep_size:.2f} MB")
    print(f"    Why:   Small enough (<10 MB) and actively used")
    
    print(f"\n  CAN EXTERNALIZE (large & linked):")
    print(f"    Count: {len(recs['can_external'])} files")
    print(f"    Size:  {can_external_size:.2f} MB")
    print(f"    Why:   Used by HTML but too large for Git")
    
    print(f"\n  CAN ARCHIVE (large & orphaned):")
    print(f"    Count: {len(recs['can_archive'])} files")
    print(f"    Size:  {can_archive_size:.2f} MB")
    print(f"    Why:   Not referenced, likely working files")
    
    total_git_size = must_keep_size + should_keep_size
    print(f"\n  💾 TOTAL GIT SIZE: {total_git_size:.2f} MB")
    
    if total_git_size < 1000:
        print(f"     ✓ Under 1 GB - acceptable for GitHub")
    else:
        print(f"     ⚠️  Over 1 GB - consider Git LFS or further reduction")
    
    print("\n" + "="*70)

def export_recommendations(manifest, output_path='arkadu-recommendations.json'):
    """Export recommendations as JSON"""
    recs = recommend_git_subset(manifest)
    
    # Convert to simple format
    output = {
        'must_keep': [a['path'] for a in recs['must_keep']],
        'should_keep': [a['path'] for a in recs['should_keep']],
        'can_external': [a['path'] for a in recs['can_external']],
        'can_archive': [a['path'] for a in recs['can_archive']],
        'shared_artifacts': [s['path'] for s in find_shared_artifacts(manifest)]
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n💾 Recommendations exported to: {output_path}")

if __name__ == '__main__':
    manifest = load_manifest()
    print_report(manifest)
    export_recommendations(manifest)
