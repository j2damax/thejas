#!/usr/bin/env python3
"""
Example: Using the Manual Categorization Helper
This demonstrates how to use the helper programmatically
"""

from manual_categorization_helper import ManualCategorizationHelper

def demonstrate_manual_categorization():
    """
    Example of how to programmatically add manual categorizations
    for the 19 undated photos
    """
    
    helper = ManualCategorizationHelper()
    
    # Example manual categorizations based on common patterns
    # These are EXAMPLES - actual dates would need visual inspection
    
    example_mappings = {
        # UUID-named files - likely from social media or cloud storage
        # These would need visual inspection to date properly
        'Undated_[Action]_72fb59f9-86c2-4f22-b491-e5a0560a8365.jpg': {
            'date': '2020-01-01',  # Example: estimated year
            'category': 'Action',
            'description': 'Martial arts training session'
        },
        'Undated_[Action]_7fd6b534-4d44-4fe4-8981-40e2e0ffd129.jpg': {
            'date': '2020-01-01',  # Example: estimated year
            'category': 'Action',
            'description': 'Sparring practice'
        },
        'Undated_[Action]_c158df3a-160a-4d37-a2a1-b88f51e96b89.jpg': {
            'date': '2020-01-01',  # Example: estimated year
            'category': 'Action',
            'description': 'Training demonstration'
        },
        
        # IMG_*.JPG files - camera photos without EXIF
        # Sequential numbering suggests they're from same time period
        # These would need visual inspection for actual dates
        'Undated_[Action]_IMG_0121.JPG': {
            'date': '2015-01-01',  # Example
            'category': 'Event',
            'description': 'Group photo or event'
        },
        # More IMG files could be categorized similarly...
    }
    
    print("=" * 70)
    print("Manual Categorization Helper - Example Usage")
    print("=" * 70)
    print()
    print("This script demonstrates how to manually categorize undated photos.")
    print("The example entries below are NOT actual dates - they require")
    print("visual inspection of each photo to determine the correct date.")
    print()
    print("-" * 70)
    print()
    
    # Display example entries without actually adding them
    print("Example Manual Categorizations:")
    print()
    for filename, data in example_mappings.items():
        print(f"Filename: {filename}")
        print(f"  → Date: {data['date']}")
        print(f"  → Category: {data['category']}")
        print(f"  → Description: {data['description']}")
        print()
    
    print("-" * 70)
    print()
    print("To actually add these categorizations:")
    print("1. Visually inspect each photo to determine the actual date")
    print("2. Use helper.add_manual_entry(filename, date, category, description)")
    print("3. Run helper._save_mappings() to save")
    print("4. Run helper.export_for_renaming() to create rename script")
    print()
    
    # Show current undated photos
    undated = helper.list_undated_photos()
    print(f"Total undated photos: {len(undated)}")
    print()
    print("Files requiring manual review:")
    for i, photo in enumerate(undated, 1):
        print(f"  {i}. {photo.name}")
    
    print()
    print("=" * 70)
    print("To use interactively:")
    print("  python3 manual_categorization_helper.py --interactive")
    print("=" * 70)

if __name__ == "__main__":
    demonstrate_manual_categorization()
