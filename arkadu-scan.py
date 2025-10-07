#!/usr/bin/env python3
"""
ARKADU - Media Archaeology Engine Scanner
Noah's Ark ⊗ Xanadu for Resurrecting Atlantis

Excavates media artifacts, documents provenance, maps circulation networks.
"""

import os
import json
import mimetypes
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

class MediaArchaeologist:
    """
    A Media Archaeologist [investigates] <media> <artifacts> across <time>
    """
    
    def __init__(self, root_path):
        self.root = Path(root_path)
        self.artifacts = {
            'images': [],
            'videos': [],
            'audio': []
        }
        self.provenance = defaultdict(list)  # file -> used_by mapping
        self.strata = defaultdict(list)  # animal -> artifacts
        self.circulation = defaultdict(list)  # html -> media mapping
        
    def excavate(self):
        """[excavate] all <technocultural strata>"""
        print("🔍 EXCAVATING MEDIA STRATA...")
        
        # Find all media files
        media_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
            'videos': ['.mp4', '.mov', '.avi', '.webm', '.mkv'],
            'audio': ['.mp3', '.wav', '.ogg', '.m4a']
        }
        
        for artifact_type, extensions in media_extensions.items():
            for ext in extensions:
                files = self.root.rglob(f'*{ext}')
                for file_path in files:
                    self.catalog_artifact(file_path, artifact_type)
        
        # Find all HTML files and scan for references
        html_files = self.root.rglob('*.html')
        for html_file in html_files:
            self.map_circulation(html_file)
        
        print(f"✓ Discovered {len(self.artifacts['images'])} images")
        print(f"✓ Discovered {len(self.artifacts['videos'])} videos")
        print(f"✓ Discovered {len(self.artifacts['audio'])} audio files")
        print(f"✓ Mapped {len(self.circulation)} HTML circulation nodes")
        
    def catalog_artifact(self, file_path, artifact_type):
        """[document] <artifact> with <metadata>"""
        rel_path = file_path.relative_to(self.root)
        stat = file_path.stat()
        
        artifact = {
            'path': str(rel_path),
            'absolute_path': str(file_path),
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'type': file_path.suffix.upper().strip('.'),
            'animal': self.infer_animal(rel_path),
            'stratum': self.infer_stratum(rel_path),
            'used_by': []
        }
        
        self.artifacts[artifact_type].append(artifact)
        self.strata[artifact['animal']].append(artifact)
        
    def infer_animal(self, path):
        """Infer which animal kingdom this artifact belongs to"""
        parts = path.parts
        animals = ['CAT', 'DOG', 'HORSE', 'ELEPHANT', 'ANT', 'BOY', 'TIGER', 
                   'WHALE', 'SPIDER', 'MANTA', 'LIZARD', 'IMPALA', 'JELLYFISH',
                   'KOALA', 'IBEX', 'HONEYBADGER', 'SHARK']
        
        for part in parts:
            if part in animals:
                return part
        return 'UNKNOWN'
    
    def infer_stratum(self, path):
        """Infer technocultural stratum"""
        path_str = str(path).upper()
        
        strata_markers = {
            'WHISKER': 'WHISKER_LAYER',
            'TRUNK': 'TRUNK_LAYER',
            'SLIDESHOWS': 'SLIDESHOW_COMPILATION',
            'HEADER_PROMPT': 'HEADER_PROMPT_LAYER',
            'CLAPPER': 'CLAPPER_CARD_LAYER',
            'TIMAEUS': 'TIMAEUS_PORTAL',
            'MYTH': 'MYTH_TIME',
            'FAL': 'FAL_SHEET'
        }
        
        for marker, stratum in strata_markers.items():
            if marker in path_str:
                return stratum
        
        return 'ROOT_STRATUM'
    
    def map_circulation(self, html_path):
        """[document] <circulation> through <networks>"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            rel_html_path = html_path.relative_to(self.root)
            
            # Find all media references (src, href with media extensions)
            media_pattern = r'(?:src|href)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg|mp4|mov|avi|webm|mp3|wav))["\']'
            matches = re.findall(media_pattern, content, re.IGNORECASE)
            
            for media_ref in matches:
                # Normalize path
                media_path = self.normalize_media_path(media_ref, html_path)
                if media_path:
                    self.circulation[str(rel_html_path)].append(media_path)
                    self.provenance[media_path].append(str(rel_html_path))
            
        except Exception as e:
            print(f"⚠️  Could not scan {html_path}: {e}")
    
    def normalize_media_path(self, ref, from_html):
        """Convert relative references to project-relative paths"""
        # Handle absolute paths, URLs, etc.
        if ref.startswith('http') or ref.startswith('//'):
            return None
        
        if ref.startswith('/'):
            ref = ref.lstrip('/')
        
        # Resolve relative to HTML file location
        html_dir = from_html.parent
        try:
            media_path = (html_dir / ref).resolve().relative_to(self.root)
            return str(media_path)
        except:
            return ref
    
    def link_provenance(self):
        """Link provenance data back to artifacts"""
        all_artifacts = (self.artifacts['images'] + 
                        self.artifacts['videos'] + 
                        self.artifacts['audio'])
        
        for artifact in all_artifacts:
            path = artifact['path']
            if path in self.provenance:
                artifact['used_by'] = self.provenance[path]
    
    def analyze_github_strategy(self):
        """Analyze size constraints and recommend GitHub strategy"""
        all_artifacts = (self.artifacts['images'] + 
                        self.artifacts['videos'] + 
                        self.artifacts['audio'])
        
        total_size = sum(a['size'] for a in all_artifacts)
        video_size = sum(a['size'] for a in self.artifacts['videos'])
        large_files = [a for a in all_artifacts if a['size'] > 100_000_000]
        very_large_files = [a for a in all_artifacts if a['size'] > 50_000_000]
        
        analysis = {
            'total_size': total_size,
            'total_size_mb': round(total_size / 1_000_000, 2),
            'video_size_mb': round(video_size / 1_000_000, 2),
            'total_files': len(all_artifacts),
            'large_files_over_100mb': len(large_files),
            'large_files_over_50mb': len(very_large_files),
            'github_limit_exceeded': len(large_files) > 0,
            'recommendation': self.generate_recommendation(total_size, large_files, very_large_files)
        }
        
        return analysis
    
    def generate_recommendation(self, total_size, large_files, very_large_files):
        """Generate storage strategy recommendation"""
        if total_size < 100_000_000:  # < 100 MB
            return "PROJECT_SMALL: Safe to push all media to GitHub"
        elif total_size < 1_000_000_000 and not large_files:  # < 1 GB, no huge files
            return "USE_GIT_LFS: Use Git LFS for videos, keep images in repo"
        elif len(large_files) > 0:
            return "EXTERNAL_REQUIRED: Files >100MB detected. Must use external hosting or split files"
        else:
            return "HYBRID_APPROACH: Keep selective media in Git, host full collection externally"
    
    def export_manifest(self, output_path='media-manifest.json'):
        """Export complete manifest as JSON"""
        self.link_provenance()
        
        manifest = {
            'generated': datetime.now().isoformat(),
            'project': 'Resurrecting Atlantis - ARKADU Scan',
            'artifacts': self.artifacts,
            'strata': {k: len(v) for k, v in self.strata.items()},
            'circulation': dict(self.circulation),
            'provenance': dict(self.provenance),
            'github_analysis': self.analyze_github_strategy(),
            'stats': {
                'total_images': len(self.artifacts['images']),
                'total_videos': len(self.artifacts['videos']),
                'total_audio': len(self.artifacts['audio']),
                'html_files': len(self.circulation),
                'orphaned_artifacts': len([a for artifacts in self.artifacts.values() 
                                          for a in artifacts if not a.get('used_by')])
            }
        }
        
        output_file = self.root / output_path
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n💾 Manifest exported to: {output_file}")
        return manifest
    
    def print_report(self):
        """Print excavation report to console"""
        self.link_provenance()
        analysis = self.analyze_github_strategy()
        
        print("\n" + "="*70)
        print("ARKADU EXCAVATION REPORT")
        print("="*70)
        
        print(f"\n📊 STATISTICS")
        print(f"  Images:       {len(self.artifacts['images'])}")
        print(f"  Videos:       {len(self.artifacts['videos'])}")
        print(f"  Audio:        {len(self.artifacts['audio'])}")
        print(f"  Total Size:   {analysis['total_size_mb']} MB")
        print(f"  HTML Files:   {len(self.circulation)}")
        
        print(f"\n🦁 ANIMAL KINGDOMS (Strata)")
        for animal, artifacts in sorted(self.strata.items(), key=lambda x: len(x[1]), reverse=True):
            if artifacts:
                print(f"  {animal:15} → {len(artifacts)} artifacts")
        
        print(f"\n🔗 PROVENANCE")
        linked = len([a for artifacts in self.artifacts.values() 
                     for a in artifacts if a.get('used_by')])
        orphaned = len([a for artifacts in self.artifacts.values() 
                       for a in artifacts if not a.get('used_by')])
        print(f"  Linked artifacts:    {linked}")
        print(f"  Orphaned artifacts:  {orphaned}")
        
        print(f"\n⚠️  GITHUB ANALYSIS")
        print(f"  Total size:          {analysis['total_size_mb']} MB")
        print(f"  Video size:          {analysis['video_size_mb']} MB")
        print(f"  Files over 50MB:     {analysis['large_files_over_50mb']}")
        print(f"  Files over 100MB:    {analysis['large_files_over_100mb']}")
        print(f"  Recommendation:      {analysis['recommendation']}")
        
        print("\n" + "="*70)


if __name__ == '__main__':
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print("🏛️  ARKADU — Media Archaeology Engine")
    print("    Noah's Ark ⊗ Xanadu\n")
    
    archaeologist = MediaArchaeologist(root_dir)
    archaeologist.excavate()
    archaeologist.print_report()
    archaeologist.export_manifest()
    
    print("\n✓ Excavation complete. Review media-manifest.json for full details.")
