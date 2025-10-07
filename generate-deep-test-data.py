#!/usr/bin/env python3
"""
Generate deep test data for organic subdivision algorithms.
Extracts the deepest, densest path through ARKADU for thorough testing.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def load_primitive_data():
    """Load primitive.jsonl data"""
    primitive_path = Path('sys/primitive.jsonl')
    if not primitive_path.exists():
        print(f"❌ {primitive_path} not found!")
        sys.exit(1)
    
    items = []
    with open(primitive_path) as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    
    print(f"✅ Loaded {len(items)} items from primitive.jsonl")
    return items

def build_hierarchy(items):
    """Build hierarchical tree from flat file list"""
    hierarchy = defaultdict(lambda: {
        'name': '',
        'path': '',
        'depth': 0,
        'files': [],
        'children': defaultdict(lambda: None),
        'totalFiles': 0,
        'totalBytes': 0
    })
    
    for item in items:
        path_parts = item['path'].split('/')
        
        # Build path incrementally
        for i in range(len(path_parts)):
            node_path = '/'.join(path_parts[:i+1])
            node = hierarchy[node_path]
            
            if not node['name']:
                node['name'] = path_parts[i]
                node['path'] = node_path
                node['depth'] = i
            
            # If this is a file (last part), add to files
            if i == len(path_parts) - 1 and not item.get('is_dir', False):
                node['files'].append(item)
                node['totalFiles'] += 1
                node['totalBytes'] += item.get('size', 0)
            
            # Link parent to child
            if i > 0:
                parent_path = '/'.join(path_parts[:i])
                parent = hierarchy[parent_path]
                parent['children'][path_parts[i]] = node_path
    
    # Aggregate stats up the tree
    def aggregate_stats(node_path):
        node = hierarchy[node_path]
        total_files = len(node['files'])
        total_bytes = sum(f.get('size', 0) for f in node['files'])
        
        for child_path in node['children'].values():
            if child_path:
                cf, cb = aggregate_stats(child_path)
                total_files += cf
                total_bytes += cb
        
        node['totalFiles'] = total_files
        node['totalBytes'] = total_bytes
        return total_files, total_bytes
    
    # Find root nodes (depth 0)
    roots = [p for p, n in hierarchy.items() if n['depth'] == 0]
    for root in roots:
        aggregate_stats(root)
    
    return hierarchy, roots

def find_deepest_densest_path(hierarchy, roots):
    """Find the path with most depth AND density"""
    
    def score_path(node_path):
        """Score = depth × file_count × bytes"""
        node = hierarchy[node_path]
        return node['depth'] * node['totalFiles'] * (node['totalBytes'] / 1024 / 1024)
    
    def explore(node_path, current_path=[]):
        node = hierarchy[node_path]
        current_path = current_path + [node_path]
        
        # Base case: no children
        if not node['children'] or all(c is None for c in node['children'].values()):
            return [(current_path, score_path(node_path))]
        
        # Recursive case: explore all children
        paths = []
        for child_path in node['children'].values():
            if child_path:
                paths.extend(explore(child_path, current_path))
        
        # Also include this node as a potential endpoint
        paths.append((current_path, score_path(node_path)))
        return paths
    
    # Explore all roots
    all_paths = []
    for root in roots:
        all_paths.extend(explore(root))
    
    # Sort by score
    all_paths.sort(key=lambda x: x[1], reverse=True)
    
    # Return top path
    if all_paths:
        best_path, best_score = all_paths[0]
        return best_path
    return []

def extract_test_data(hierarchy, path, max_depth=12):
    """Extract hierarchical test data along path"""
    
    def build_node(node_path, current_depth=0):
        if current_depth > max_depth:
            return None
        
        node = hierarchy[node_path]
        
        # Convert to test data format
        result = {
            'name': node['name'],
            'path': node['path'],
            'depth': current_depth,
            'files': node['totalFiles'],
            'bytes': node['totalBytes'],
            'mb': round(node['totalBytes'] / 1024 / 1024, 1),
            'children': []
        }
        
        # Add children (sorted by size, limit to top 15 for reasonable visualization)
        child_items = []
        for child_name, child_path in node['children'].items():
            if child_path:
                child_node = hierarchy[child_path]
                child_items.append((child_path, child_node['totalFiles'], child_node['totalBytes']))
        
        # Sort by bytes, take top 15
        child_items.sort(key=lambda x: x[2], reverse=True)
        child_items = child_items[:15]
        
        for child_path, _, _ in child_items:
            child_data = build_node(child_path, current_depth + 1)
            if child_data:
                result['children'].append(child_data)
        
        return result
    
    # Build from root of path
    if not path:
        return None
    
    root_data = build_node(path[0])
    return root_data

def main():
    print("🌋 ARKADU Deep Test Data Generator\n")
    
    # Load data
    items = load_primitive_data()
    
    # Build hierarchy
    print("📊 Building hierarchy...")
    hierarchy, roots = build_hierarchy(items)
    print(f"✅ Built hierarchy with {len(hierarchy)} nodes, {len(roots)} roots\n")
    
    # Find deepest/densest path
    print("🔍 Finding deepest, densest path...")
    best_path = find_deepest_densest_path(hierarchy, roots)
    
    if not best_path:
        print("❌ No path found!")
        sys.exit(1)
    
    print(f"✅ Found path with {len(best_path)} levels:")
    for i, node_path in enumerate(best_path[:8]):  # Show first 8 levels
        node = hierarchy[node_path]
        print(f"  {'  ' * i}→ {node['name']} ({node['totalFiles']} files, {node['totalBytes']/1024/1024:.1f} MB)")
    if len(best_path) > 8:
        print(f"  ... and {len(best_path) - 8} more levels")
    print()
    
    # Extract test data
    print("📦 Extracting test data structure...")
    test_data = extract_test_data(hierarchy, best_path, max_depth=12)
    
    # Save to file
    output_path = Path('sys/deep-test-data.json')
    with open(output_path, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"✅ Saved to {output_path}")
    
    # Generate summary
    def count_nodes(node):
        if not node:
            return 0
        return 1 + sum(count_nodes(child) for child in node.get('children', []))
    
    total_nodes = count_nodes(test_data)
    print(f"\n📊 Test Data Summary:")
    print(f"  • Total nodes: {total_nodes}")
    print(f"  • Root: {test_data['name']}")
    print(f"  • Root files: {test_data['files']}")
    print(f"  • Root size: {test_data['mb']} MB")
    print(f"  • Max depth: {len(best_path)}")
    print(f"\n🚀 Ready to test! Load this data in your visualizations.")

if __name__ == '__main__':
    main()
