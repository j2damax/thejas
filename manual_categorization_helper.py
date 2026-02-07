#!/usr/bin/env python3
"""
Manual Photo Categorization Helper
Allows manual review and recategorization of photos
"""

import os
import json
from pathlib import Path
from typing import Dict, List

PHOTOS_DIR = Path("/home/runner/work/thejas/thejas/photos")
MAPPING_FILE = Path("/home/runner/work/thejas/thejas/photo_manual_mapping.json")

CATEGORIES = ["Action", "Award", "Profile", "Coaching", "Event"]

class ManualCategorizationHelper:
    def __init__(self):
        self.mappings = self._load_mappings()
        
    def _load_mappings(self) -> Dict:
        """Load existing manual mappings"""
        if MAPPING_FILE.exists():
            with open(MAPPING_FILE, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_mappings(self):
        """Save manual mappings"""
        with open(MAPPING_FILE, 'w') as f:
            json.dump(self.mappings, f, indent=2, sort_keys=True)
    
    def list_undated_photos(self) -> List[Path]:
        """Get list of undated photos"""
        undated = []
        for photo in sorted(PHOTOS_DIR.glob("Undated_*")):
            undated.append(photo)
        return undated
    
    def add_manual_entry(self, filename: str, date: str, category: str, description: str):
        """Add a manual categorization entry"""
        self.mappings[filename] = {
            'date': date,
            'category': category,
            'description': description,
            'source': 'manual'
        }
        self._save_mappings()
        print(f"Added mapping for {filename}")
    
    def show_manual_entries(self):
        """Display all manual entries"""
        if not self.mappings:
            print("No manual entries yet.")
            return
        
        print("\n=== Manual Photo Mappings ===\n")
        for filename, data in sorted(self.mappings.items()):
            print(f"File: {filename}")
            print(f"  Date: {data['date']}")
            print(f"  Category: {data['category']}")
            print(f"  Description: {data['description']}")
            print()
    
    def export_for_renaming(self, output_file: str = "rename_commands.sh"):
        """Export shell commands to rename files based on manual mappings"""
        if not self.mappings:
            print("No manual entries to export.")
            return
        
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Auto-generated rename commands\n")
            f.write(f"cd {PHOTOS_DIR}\n\n")
            
            for old_name, data in self.mappings.items():
                date = data['date']
                category = data['category']
                desc = data['description'].replace(' ', '_').replace('/', '_')
                
                # Get file extension
                old_path = PHOTOS_DIR / old_name
                if old_path.exists():
                    ext = old_path.suffix
                    new_name = f"{date}_[{category}]_{desc}{ext}"
                    f.write(f'mv "{old_name}" "{new_name}"\n')
        
        print(f"Rename commands exported to {output_path}")
        print(f"Run: bash {output_path}")

def interactive_mode():
    """Interactive mode for manual categorization"""
    helper = ManualCategorizationHelper()
    undated = helper.list_undated_photos()
    
    print("=" * 60)
    print("Manual Photo Categorization Helper")
    print("=" * 60)
    print()
    print(f"Found {len(undated)} undated photos")
    print()
    
    while True:
        print("\nOptions:")
        print("1. List undated photos")
        print("2. Add manual categorization")
        print("3. Show manual entries")
        print("4. Export rename commands")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            print("\nUndated Photos:")
            for i, photo in enumerate(undated, 1):
                print(f"{i}. {photo.name}")
        
        elif choice == '2':
            print("\nAdd Manual Categorization")
            filename = input("Filename: ").strip()
            date = input("Date (YYYY-MM-DD or YYYY-MM or YYYY): ").strip()
            
            print(f"\nCategories: {', '.join(CATEGORIES)}")
            category = input("Category: ").strip()
            
            description = input("Description (brief): ").strip()
            
            helper.add_manual_entry(filename, date, category, description)
        
        elif choice == '3':
            helper.show_manual_entries()
        
        elif choice == '4':
            output_file = input("Output file name [rename_commands.sh]: ").strip()
            if not output_file:
                output_file = "rename_commands.sh"
            helper.export_for_renaming(output_file)
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

def example_usage():
    """Show example of how to use the helper programmatically"""
    helper = ManualCategorizationHelper()
    
    # Example: Add manual entries for photos
    examples = [
        {
            'filename': 'Undated_[Action]_IMG_0121.JPG',
            'date': '2014-11-19',
            'category': 'Award',
            'description': 'Korea WoMAU Gold Medal ceremony'
        },
        # Add more examples as needed
    ]
    
    print("Example entries (not added, just showing format):\n")
    for example in examples:
        print(f"Filename: {example['filename']}")
        print(f"Date: {example['date']}")
        print(f"Category: {example['category']}")
        print(f"Description: {example['description']}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        example_usage()
    elif len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_mode()
    else:
        print("Usage:")
        print("  python3 manual_categorization_helper.py --interactive")
        print("  python3 manual_categorization_helper.py --example")
        print()
        print("Or import and use programmatically:")
        print("  from manual_categorization_helper import ManualCategorizationHelper")
