#!/usr/bin/env python3
"""
ARKADU SCALE - Measure Volume (count) and Mass (bytes) by Species

Reads primitive.jsonl and calculates:
- VOLUME: Number of files per species (media type)
- MASS: Total bytes per species
- At every level: ROOT → Kingdom → Phylum → Class → ... → File

Outputs verification data to compare against voronoi-depth-test.html
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

class TerritoryScale:
    """Measures volume and mass of file territories"""
    
    def __init__(self):
        self.measurements = {}
        self.total_files = 0
        self.total_bytes = 0
        self.species_totals = defaultdict(lambda: {'volume': 0, 'mass': 0})
        
    def measure_file(self, filepath: str, size: int) -> Tuple[str, int, int]:
        """Measure a single file - returns (species, volume=1, mass=bytes)"""
        ext = Path(filepath).suffix.lower().lstrip('.')
        if not ext:
            ext = 'unknown'
        
        self.total_files += 1
        self.total_bytes += size
        self.species_totals[ext]['volume'] += 1
        self.species_totals[ext]['mass'] += size
        
        return (ext, 1, size)
    
    def aggregate_territory(self, territory_path: str, files: List[Tuple[str, int, int]]) -> Dict:
        """Aggregate measurements for a territory (folder)"""
        species_data = defaultdict(lambda: {'volume': 0, 'mass': 0, 'files': []})
        
        for ext, volume, mass in files:
            species_data[ext]['volume'] += volume
            species_data[ext]['mass'] += mass
            species_data[ext]['files'].append({'volume': volume, 'mass': mass})
        
        # Calculate totals
        total_volume = sum(s['volume'] for s in species_data.values())
        total_mass = sum(s['mass'] for s in species_data.values())
        
        # Find dominant species (by combined metric)
        dominant = None
        max_weight = 0
        for ext, data in species_data.items():
            weight = data['volume'] * data['mass']
            if weight > max_weight:
                max_weight = weight
                dominant = ext
        
        result = {
            'path': territory_path,
            'total_volume': total_volume,
            'total_mass': total_mass,
            'species': dict(species_data),
            'dominant_species': dominant,
            'dominant_pct': (species_data[dominant]['volume'] / total_volume * 100) if dominant else 0
        }
        
        self.measurements[territory_path] = result
        return result

def parse_path_hierarchy(filepath: str) -> List[str]:
    """Parse file path into hierarchy levels"""
    path = Path(filepath)
    # Remove leading 'resurrecting atlantis/' if present
    parts = list(path.parts)
    if parts and 'resurrecting atlantis' in parts[0]:
        parts = parts[1:]
    
    return parts

def build_hierarchy_tree(primitives_data: List[Dict]) -> Dict:
    """Build hierarchical tree structure from flat primitive data"""
    tree = {}
    file_measurements = []
    
    for item in primitives_data:
        # All items in primitive.jsonl are files
        filepath = item.get('path', '')
        size = item.get('size', 0)
        
        if not filepath:
            continue
        
        # Get extension from item or filename
        ext = item.get('ext', '').lower().lstrip('.') or 'unknown'
        
        # Parse hierarchy
        parts = parse_path_hierarchy(filepath)
        if not parts:
            continue
        
        # Build nested dict
        current = tree
        for part in parts[:-1]:  # All but filename
            if part not in current:
                current[part] = {'_files': [], '_children': {}}
            current = current[part]['_children']
        
        # Add file to leaf
        filename = parts[-1]
        
        if filename not in current:
            current[filename] = {'_files': [], '_children': {}}
        
        current[filename]['_files'].append({
            'path': filepath,
            'size': size,
            'species': ext
        })
        
        file_measurements.append((filepath, size, ext))
    
    return tree, file_measurements

def measure_tree_recursive(node: Dict, path: str, scale: TerritoryScale, depth: int = 0) -> Dict:
    """Recursively measure all nodes in tree"""
    
    # Measure files at this level
    file_data = []
    for file_info in node.get('_files', []):
        ext = file_info['species']
        size = file_info['size']
        file_data.append((ext, 1, size))
    
    # Recursively measure children
    child_measurements = []
    for child_name, child_node in node.get('_children', {}).items():
        child_path = f"{path}/{child_name}" if path else child_name
        child_result = measure_tree_recursive(child_node, child_path, scale, depth + 1)
        child_measurements.append(child_result)
    
    # Aggregate all measurements (files + children)
    all_measurements = file_data.copy()
    for child in child_measurements:
        for ext, data in child['species'].items():
            all_measurements.append((ext, data['volume'], data['mass']))
    
    # Aggregate for this territory
    result = scale.aggregate_territory(path or 'ROOT', all_measurements)
    result['depth'] = depth
    result['direct_files'] = len(file_data)
    result['children'] = [c['path'] for c in child_measurements]
    
    return result

def format_bytes(bytes_val: int) -> str:
    """Format bytes as human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}TB"

def print_territory_report(measurement: Dict, indent: int = 0):
    """Print formatted report for a territory"""
    prefix = "  " * indent
    path = measurement['path']
    vol = measurement['total_volume']
    mass = measurement['total_mass']
    dominant = measurement.get('dominant_species', 'none')
    dom_pct = measurement.get('dominant_pct', 0)
    
    print(f"{prefix}📦 {path}")
    print(f"{prefix}   Volume: {vol} files")
    print(f"{prefix}   Mass:   {format_bytes(mass)}")
    print(f"{prefix}   Dominant: .{dominant} ({dom_pct:.1f}%)")
    print(f"{prefix}   Species breakdown:")
    
    # Sort species by mass descending
    species_sorted = sorted(
        measurement['species'].items(),
        key=lambda x: x[1]['mass'],
        reverse=True
    )
    
    for ext, data in species_sorted[:5]:  # Top 5
        vol_pct = data['volume'] / vol * 100
        mass_pct = data['mass'] / mass * 100
        print(f"{prefix}     .{ext:8s} {data['volume']:6d} files ({vol_pct:5.1f}%)  {format_bytes(data['mass']):>10s} ({mass_pct:5.1f}%)")
    
    print()

def main():
    # Load primitive.jsonl
    primitive_path = Path(__file__).parent / 'sys' / 'primitive.jsonl'
    
    if not primitive_path.exists():
        print(f"❌ Error: {primitive_path} not found")
        print("Run arkadu-scan.py first to generate primitive.jsonl")
        return 1
    
    print("🔬 ARKADU SCALE - Volume & Mass Measurement")
    print("=" * 60)
    print()
    
    # Load data
    primitives = []
    with open(primitive_path, 'r') as f:
        for line in f:
            if line.strip():
                primitives.append(json.loads(line))
    
    print(f"✅ Loaded {len(primitives)} artifacts from primitive.jsonl")
    print()
    
    # Build hierarchy tree
    print("🌳 Building hierarchy tree...")
    tree, file_measurements = build_hierarchy_tree(primitives)
    print(f"✅ Built tree with {len(file_measurements)} files")
    print()
    
    # Measure everything
    print("⚖️  Measuring volumes and masses...")
    scale = TerritoryScale()
    
    # Measure each file
    for filepath, size, ext in file_measurements:
        scale.measure_file(filepath, size)
    
    # Measure tree recursively - need to iterate top-level keys
    # Each top-level key in tree is either a folder or a file
    root_children = []
    for key in tree.keys():
        child_result = measure_tree_recursive(tree[key], key, scale, depth=0)
        root_children.append(child_result)
    
    # Create synthetic ROOT measurement
    root_measurement = {
        'path': 'ROOT',
        'total_volume': scale.total_files,
        'total_mass': scale.total_bytes,
        'species': dict(scale.species_totals),
        'dominant_species': None,
        'dominant_pct': 0,
        'depth': -1,
        'direct_files': 0,
        'children': [c['path'] for c in root_children]
    }
    
    print(f"✅ Measured {scale.total_files} files, {format_bytes(scale.total_bytes)} total")
    print()
    
    # Print summary
    print("📊 GLOBAL SPECIES SUMMARY")
    print("-" * 60)
    species_sorted = sorted(
        scale.species_totals.items(),
        key=lambda x: x[1]['mass'],
        reverse=True
    )
    
    for ext, data in species_sorted:
        vol_pct = data['volume'] / scale.total_files * 100
        mass_pct = data['mass'] / scale.total_bytes * 100
        print(f"  .{ext:10s}  {data['volume']:6d} files ({vol_pct:5.1f}%)  {format_bytes(data['mass']):>10s} ({mass_pct:5.1f}%)")
    
    print()
    print()
    
    # Print territory measurements (top level only)
    print("🗺️  TOP-LEVEL TERRITORIES (KINGDOMS)")
    print("-" * 60)
    
    # Get top-level territories (kingdoms - direct children of root)
    top_territories = []
    for path, measurement in scale.measurements.items():
        # Top level = paths with no '/' separator (just kingdom name)
        if '/' not in path and path != 'ROOT' and path:
            top_territories.append(measurement)
    
    top_territories.sort(key=lambda x: x['total_mass'], reverse=True)
    
    if not top_territories:
        # Fallback: show all depth 1
        for path, measurement in scale.measurements.items():
            if measurement.get('depth', 99) == 1:
                top_territories.append(measurement)
        top_territories.sort(key=lambda x: x['total_mass'], reverse=True)
    
    for territory in top_territories:
        print_territory_report(territory, indent=0)
    
    # Export verification JSON
    export_path = Path(__file__).parent / 'sys' / 'scale-verification.json'
    export_data = {
        'total_files': scale.total_files,
        'total_bytes': scale.total_bytes,
        'global_species': dict(scale.species_totals),
        'territories': scale.measurements,
        'top_territories': [t['path'] for t in top_territories]
    }
    
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"💾 Verification data exported to: {export_path}")
    print()
    print("✅ Scale verification complete!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
