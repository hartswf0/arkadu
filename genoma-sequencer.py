#!/usr/bin/env python3
"""
GENOMA SEQUENCER - Extract genetic sequences from ARKADU primitive data

Sequences the genome of each media species (file type) by reading primitive.jsonl
and generating GENOMA-formatted JSON with codons for each file.

Theory: Files are genes (codons), species are genomes, the archive is the organism.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_primitive_data(jsonl_path):
    """Load all file records from primitive.jsonl"""
    files = []
    with open(jsonl_path, 'r') as f:
        for line in f:
            if line.strip():
                files.append(json.loads(line))
    return files

def get_codon_type(extension):
    """Map file extension to GENOMA codon type"""
    ext_map = {
        '.png': 'PNG',
        '.jpg': 'JPG', 
        '.jpeg': 'JPG',
        '.gif': 'GIF',
        '.mp4': 'MP4',
        '.mov': 'MOV',
        '.avi': 'AVI',
        '.mp3': 'MP3',
        '.wav': 'WAV',
        '.flac': 'FLAC',
        '.json': 'JSON',
        '.py': 'PY',
        '.js': 'JS',
        '.html': 'HTML',
        '.css': 'CSS',
        '.txt': 'TXT',
        '.md': 'MD',
        '.pdf': 'PDF'
    }
    return ext_map.get(extension.lower(), 'UNK')

def determine_origin(file_data):
    """Determine the origin/source of this file"""
    path = file_data.get('path', '')
    
    # Check for operative ekphrasis patterns
    if 'operativeEkphrasis' in str(file_data):
        return 'operative_ekphrasis'
    
    # Check for tool chain outputs
    if any(x in path for x in ['assembly', 'generated', 'output']):
        return 'tool_chain_output'
    
    # Check for metadata
    if file_data.get('ext') == '.json':
        return 'metadata'
    
    # Check for source material
    if any(x in path for x in ['source', 'raw', 'original']):
        return 'source_material'
    
    return 'excavated_artifact'

def is_intron(file_data):
    """Determine if this codon should be an intron (unexpressed)"""
    # Metadata files are introns (structural, not expressed)
    if file_data.get('ext') in ['.json', '.txt', '.md']:
        return True
    
    # Very small files might be metadata
    if file_data.get('size', 0) < 1024:  # < 1KB
        return True
    
    return False

def create_file_codon(file_data, repo_root):
    """Create a GENOMA codon from file data"""
    ext = file_data.get('ext', '')
    codon_type = get_codon_type(ext)
    
    # Build payload with relevant metadata
    relative_path = file_data.get('path', '')
    absolute_path = str(Path(repo_root).parent / relative_path)
    
    # Extract taxonomy from path if not in file_data
    kingdom = file_data.get('kingdom', '')
    phylum = file_data.get('phylum', '')
    class_name = file_data.get('class', '')
    
    # If empty, try to parse from path
    if not kingdom and relative_path:
        path_parts = Path(relative_path).parts
        if len(path_parts) > 0:
            kingdom = path_parts[0]
        if len(path_parts) > 1:
            phylum = path_parts[1]
        if len(path_parts) > 2:
            class_name = path_parts[2]
    
    payload = {
        'path_relative': relative_path,
        'path_absolute': absolute_path,
        'filename': Path(relative_path).name,
        'size_bytes': file_data.get('size', 0),
        'depth': file_data.get('depth', 0),
        'kingdom': kingdom,
        'phylum': phylum,
        'class': class_name
    }
    
    # Add type-specific metadata
    if codon_type in ['PNG', 'JPG', 'GIF']:
        payload['media_type'] = 'image'
    elif codon_type in ['MP4', 'MOV', 'AVI']:
        payload['media_type'] = 'video'
    elif codon_type in ['MP3', 'WAV', 'FLAC']:
        payload['media_type'] = 'audio'
    elif codon_type in ['JSON', 'PY', 'JS']:
        payload['media_type'] = 'code'
    
    # Add ekphrasis chain info if present
    if 'ekphrasis_chain' in file_data:
        payload['ekphrasis_chain'] = file_data['ekphrasis_chain']
    
    return {
        'type': codon_type,
        'payload': payload,
        'is_intron': is_intron(file_data),
        'origin': determine_origin(file_data)
    }

def sequence_species_genome(species_name, files, repo_root):
    """Create a complete genome sequence for a species (file type)"""
    
    # Calculate species statistics
    total_bytes = sum(f.get('size', 0) for f in files)
    total_instances = len(files)
    
    # Get color signature (from first file's dominant color if available)
    color_signature = '#6b8a96'  # default
    for f in files:
        if 'dominantColor' in f:
            color_signature = f['dominantColor']
            break
    
    # Create sequence of codons
    sequence = [create_file_codon(f, repo_root) for f in files]
    
    # Sort by depth then path for logical ordering
    sequence.sort(key=lambda c: (c['payload'].get('depth', 0), c['payload'].get('path', '')))
    
    genome = {
        'genome_id': f'species-{species_name.lower()}',
        'species_type': species_name,
        'total_instances': total_instances,
        'total_bytes': total_bytes,
        'color_signature': color_signature,
        'sequence': sequence
    }
    
    return genome

def create_ekphrasis_genomes(files):
    """Create genomes for ekphrasis chains (JSON -> PY -> Media)"""
    ekphrasis_genomes = []
    
    # Group files by potential chains
    chains = defaultdict(list)
    
    for f in files:
        if 'ekphrasis_chain' in f:
            chain_id = f['ekphrasis_chain']
            chains[chain_id].append(f)
    
    # Create genome for each chain
    for chain_id, chain_files in chains.items():
        sequence = [create_file_codon(f) for f in chain_files]
        
        ekphrasis_genomes.append({
            'genome_id': f'ekphrasis-chain-{chain_id}',
            'chain_type': 'operative_ekphrasis',
            'sequence': sequence
        })
    
    return ekphrasis_genomes

def main():
    # Paths
    primitive_path = Path('sys/primitive.jsonl')
    output_path = Path('sys/genoma-sequences.json')
    repo_root = Path.cwd()  # ARKADU directory
    
    if not primitive_path.exists():
        print(f"Error: {primitive_path} not found")
        sys.exit(1)
    
    print("🧬 GENOMA SEQUENCER - Extracting genetic sequences...")
    print(f"📂 Reading: {primitive_path}")
    print(f"📍 Repository root: {repo_root}")
    
    # Load all files
    files = load_primitive_data(primitive_path)
    print(f"📊 Loaded {len(files)} files")
    
    # Group files by species (extension)
    species_groups = defaultdict(list)
    for f in files:
        ext = f.get('ext', '.unk')
        species_groups[ext].append(f)
    
    print(f"🧬 Found {len(species_groups)} species")
    
    # Sequence each species genome
    species_genomes = []
    for ext, species_files in sorted(species_groups.items()):
        species_name = get_codon_type(ext)
        genome = sequence_species_genome(species_name, species_files, repo_root)
        species_genomes.append(genome)
        print(f"  ✓ {species_name}: {len(species_files)} instances, {genome['total_bytes'] / 1024 / 1024:.1f} MB")
    
    # Create ekphrasis chain genomes
    ekphrasis_genomes = create_ekphrasis_genomes(files)
    print(f"🔗 Found {len(ekphrasis_genomes)} ekphrasis chains")
    
    # Assemble complete GENOMA export
    genoma_export = {
        'arkadu_genomes': {
            'excavation_id': 'resurrecting-atlantis-2025',
            'timestamp': datetime.now().isoformat(),
            'repository_root': str(repo_root.parent),  # Parent of ARKADU
            'total_files': len(files),
            'total_bytes': sum(f.get('size', 0) for f in files),
            'total_species': len(species_groups),
            
            'species_genomes': species_genomes,
            'ekphrasis_genomes': ekphrasis_genomes,
            
            'metadata': {
                'sequencer_version': '1.0.0',
                'theory': 'Files are genes (codons), species are genomes, the archive is the organism',
                'format': 'GENOMA v1 - Digital Genetics for Media Archaeology',
                'path_format': 'Both relative (from repo root) and absolute paths included',
                'usage': 'Use path_absolute for direct file access, path_relative for portability'
            }
        }
    }
    
    # Write output
    with open(output_path, 'w') as f:
        json.dump(genoma_export, f, indent=2)
    
    print(f"\n✅ Genome sequences written to: {output_path}")
    print(f"📊 Total genome size: {len(json.dumps(genoma_export)) / 1024:.1f} KB")
    print("\n🧬 SEQUENCING COMPLETE")

if __name__ == '__main__':
    main()
