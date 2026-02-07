#!/usr/bin/env python3
"""
Photo Processing Script for Theja Suranjan Dunusinghe's Portfolio
Extracts dates from EXIF, filenames, and visual context to rename photos chronologically
"""

import os
import re
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# Configuration
PHOTOS_DIR = Path("/home/runner/work/thejas/thejas/photos")
LOG_FILE = Path("/home/runner/work/thejas/thejas/TEJAS_PHOTO_LOG.md")
VALID_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.JPG', '.JPEG', '.PNG', '.HEIC'}

# Categories for classification
CATEGORIES = {
    'Action': ['kick', 'spar', 'train', 'fight', 'punch', 'combat', 'match'],
    'Award': ['medal', 'trophy', 'podium', 'certificate', 'award', 'gold', 'silver', 'bronze', 'diploma'],
    'Profile': ['headshot', 'portrait', 'logo', 'brand', 'tejas', 'profile'],
    'Coaching': ['teach', 'student', 'gym', 'class', 'coaching', 'training'],
    'Event': ['group', 'conference', 'ceremony', 'opening', 'team', 'crowd'],
}

class PhotoProcessor:
    def __init__(self):
        self.timeline_events = self._load_timeline()
        self.processed_photos = []
        
    def _load_timeline(self) -> Dict[str, str]:
        """Load timeline events from TEJAS_Master_Timeline.md"""
        timeline = {}
        timeline_file = Path("/home/runner/work/thejas/thejas/TEJAS_Master_Timeline.md")
        
        if timeline_file.exists():
            with open(timeline_file, 'r') as f:
                content = f.read()
                # Extract key dates and events
                if '2014-11-19' in content:
                    timeline['WoMAU_Gold_Medal'] = '2014-11-19'
                if '2023-08-17' in content:
                    timeline['2nd_Dong_Black_Belt'] = '2023-08-17'
                if '2025-01-01' in content:
                    timeline['World_Taekkyeon_Championship'] = '2025-01-01'
        
        return timeline
    
    def extract_exif_date(self, file_path: Path) -> Optional[str]:
        """Extract date from EXIF metadata using exiftool"""
        try:
            result = subprocess.run(
                ['exiftool', '-DateTimeOriginal', '-CreateDate', '-s3', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                date_str = result.stdout.strip().split('\n')[0]
                # Parse date format: "2025:08:21 17:10:28" or "2025:08:21 17:10:28.044+05:30"
                date_match = re.match(r'(\d{4}):(\d{2}):(\d{2})', date_str)
                if date_match:
                    return f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        except Exception as e:
            print(f"Error extracting EXIF from {file_path.name}: {e}")
        
        return None
    
    def extract_filename_date(self, filename: str) -> Optional[str]:
        """Extract date from filename patterns"""
        # WhatsApp Image 2026-02-07 at ...
        whatsapp_match = re.search(r'WhatsApp.*?(\d{4})-(\d{2})-(\d{2})', filename)
        if whatsapp_match:
            return f"{whatsapp_match.group(1)}-{whatsapp_match.group(2)}-{whatsapp_match.group(3)}"
        
        # Screenshot_20220415...
        screenshot_match = re.search(r'Screenshot[_\s](\d{4})(\d{2})(\d{2})', filename)
        if screenshot_match:
            return f"{screenshot_match.group(1)}-{screenshot_match.group(2)}-{screenshot_match.group(3)}"
        
        # 20161102_143022.jpg
        date_prefix_match = re.search(r'^(\d{4})(\d{2})(\d{2})', filename)
        if date_prefix_match:
            year, month, day = date_prefix_match.groups()
            if 1990 <= int(year) <= 2030 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                return f"{year}-{month}-{day}"
        
        # IMG_YYYYMMDD or similar
        img_date_match = re.search(r'(\d{8})', filename)
        if img_date_match:
            date_str = img_date_match.group(1)
            year, month, day = date_str[:4], date_str[4:6], date_str[6:8]
            if 1990 <= int(year) <= 2030 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                return f"{year}-{month}-{day}"
        
        return None
    
    def analyze_visual_context(self, file_path: Path, exif_info: Optional[str] = None) -> Tuple[Optional[str], str, str]:
        """
        Analyze image content for visual context dating
        Returns: (estimated_date, description, category)
        
        Note: This uses EXIF metadata and filename heuristics for classification.
        In a real implementation with actual images, this would use computer vision/ML.
        """
        filename = file_path.name.lower()
        
        # Get additional EXIF data for better context
        try:
            result = subprocess.run(
                ['exiftool', '-Make', '-Model', '-ImageDescription', '-Keywords', '-s3', str(file_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            exif_context = result.stdout.strip() if result.returncode == 0 else ""
        except:
            exif_context = ""
        
        # Check for keywords that might indicate specific events
        description_parts = []
        category = "Action"
        
        # Check for award/medal indicators
        if any(word in filename for word in ['medal', 'gold', 'award', 'trophy', 'podium', 'certificate']):
            category = "Award"
            if 'korea' in filename or 'womau' in filename:
                return '2014-11-19', "Korea WoMAU Gold Medal ceremony", category
            description_parts.append("Award ceremony or medal presentation")
        
        # Check for profile/branding indicators
        elif any(word in filename for word in ['tejas', 'logo', 'brand', 'portrait', 'headshot']):
            category = "Profile"
            description_parts.append("TEJAS branding or professional portrait")
        
        # Check for coaching indicators
        elif any(word in filename for word in ['teach', 'student', 'class', 'coaching', 'gym']):
            category = "Coaching"
            description_parts.append("Coaching session or training")
        
        # Check for event indicators
        elif any(word in filename for word in ['group', 'team', 'ceremony', 'conference', 'event']):
            category = "Event"
            description_parts.append("Group event or ceremony")
        
        # Default to action/training
        else:
            category = "Action"
            description_parts.append("Martial arts training or action")
        
        # Add camera info if available
        if 'iphone' in exif_context.lower():
            description_parts.append("iPhone capture")
        
        description = " - ".join(description_parts) if description_parts else "Martial arts training"
        
        return None, description, category
    
    def _identify_category(self, filename_or_description: str) -> str:
        """Identify the category based on keywords"""
        text = filename_or_description.lower()
        
        for category, keywords in CATEGORIES.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return "Action"  # Default category
    
    def generate_description(self, file_path: Path, date_source: str, category: str) -> str:
        """Generate a visual description for the photo"""
        filename = file_path.name.lower()
        
        # Get EXIF metadata for better description
        try:
            result = subprocess.run(
                ['exiftool', '-Make', '-Model', '-LensModel', '-s3', str(file_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            camera_info = result.stdout.strip().split('\n') if result.returncode == 0 else []
        except:
            camera_info = []
        
        # Build description based on category and context
        if category == "Award":
            if 'korea' in filename:
                return "Korea martial arts award ceremony"
            elif 'gold' in filename or 'medal' in filename:
                return "Medal presentation ceremony"
            else:
                return "Award or certificate ceremony"
        
        elif category == "Profile":
            if 'tejas' in filename or 'logo' in filename:
                return "TEJAS brand logo or identity"
            else:
                return "Professional portrait headshot"
        
        elif category == "Coaching":
            return "Training students or coaching session"
        
        elif category == "Event":
            if 'group' in filename:
                return "Group photo with team or students"
            elif 'conference' in filename:
                return "Conference or seminar event"
            else:
                return "Martial arts event or ceremony"
        
        # For Action category, be more specific based on EXIF
        else:
            if camera_info and 'iphone' in ' '.join(camera_info).lower():
                return "Training or sparring session (iPhone)"
            elif 'whatsapp' in filename:
                return "Photo shared via WhatsApp"
            else:
                return "Martial arts training or demonstration"
    
    def process_photo(self, file_path: Path) -> Dict:
        """Process a single photo and extract metadata"""
        photo_info = {
            'original_name': file_path.name,
            'date': None,
            'source_method': 'Unknown',
            'description': '',
            'category': 'Action',
            'timeline_match': 'No',
            'new_name': '',
        }
        
        # Priority A: EXIF Data
        exif_date = self.extract_exif_date(file_path)
        if exif_date:
            photo_info['date'] = exif_date
            photo_info['source_method'] = 'EXIF Data'
        
        # Priority B: Filename Pattern
        if not photo_info['date']:
            filename_date = self.extract_filename_date(file_path.name)
            if filename_date:
                photo_info['date'] = filename_date
                photo_info['source_method'] = 'Filename Pattern'
        
        # Priority C: Visual Context
        visual_date, visual_desc, visual_category = self.analyze_visual_context(file_path)
        if not photo_info['date'] and visual_date:
            photo_info['date'] = visual_date
            photo_info['source_method'] = 'Visual Context'
            photo_info['description'] = visual_desc
            photo_info['category'] = visual_category
        elif visual_category:
            # Use the category even if we didn't get a date
            photo_info['category'] = visual_category
        
        # If still no date, use file modification date as last resort
        if not photo_info['date']:
            # Use a generic date for undated photos
            photo_info['date'] = '0000-00-00'
            photo_info['source_method'] = 'No Date Found'
        
        # Generate description if not already set
        if not photo_info['description']:
            photo_info['description'] = self.generate_description(
                file_path, 
                photo_info['source_method'],
                photo_info['category']
            )
        
        # Check timeline match
        if any(event_date in photo_info['date'] for event_date in self.timeline_events.values()):
            photo_info['timeline_match'] = 'Yes'
        
        # Generate new filename
        photo_info['new_name'] = self.generate_new_filename(photo_info, file_path.suffix)
        
        return photo_info
    
    def generate_new_filename(self, photo_info: Dict, extension: str) -> str:
        """Generate new filename in format: YYYY-MM-DD_[Category]_[Description].ext"""
        date = photo_info['date']
        category = photo_info['category']
        description = photo_info['description']
        
        # Clean description for filename
        desc_clean = re.sub(r'[^\w\s-]', '', description)
        desc_clean = re.sub(r'\s+', '_', desc_clean.strip())
        desc_clean = desc_clean[:50]  # Limit length
        
        if date == '0000-00-00':
            # Use original filename for undated
            base_name = Path(photo_info['original_name']).stem
            return f"Undated_[{category}]_{base_name}{extension}"
        
        return f"{date}_[{category}]_{desc_clean}{extension}"
    
    def process_all_photos(self):
        """Process all photos in the directory"""
        photo_files = []
        
        for file_path in PHOTOS_DIR.iterdir():
            if file_path.suffix in VALID_EXTENSIONS:
                photo_files.append(file_path)
        
        print(f"Found {len(photo_files)} photos to process...")
        
        for file_path in sorted(photo_files):
            print(f"Processing: {file_path.name}")
            photo_info = self.process_photo(file_path)
            self.processed_photos.append(photo_info)
        
        # Sort by date
        self.processed_photos.sort(key=lambda x: (x['date'], x['original_name']))
    
    def rename_photos(self, dry_run=False):
        """Rename photos based on processed information"""
        renamed_count = 0
        
        for photo_info in self.processed_photos:
            old_path = PHOTOS_DIR / photo_info['original_name']
            new_path = PHOTOS_DIR / photo_info['new_name']
            
            # Skip if already renamed
            if old_path == new_path:
                continue
            
            # Handle duplicates
            counter = 1
            original_new_path = new_path
            while new_path.exists() and new_path != old_path:
                stem = original_new_path.stem
                suffix = original_new_path.suffix
                new_path = PHOTOS_DIR / f"{stem}_{counter}{suffix}"
                counter += 1
            
            if dry_run:
                print(f"Would rename: {old_path.name} -> {new_path.name}")
            else:
                try:
                    old_path.rename(new_path)
                    photo_info['new_name'] = new_path.name
                    renamed_count += 1
                    print(f"Renamed: {old_path.name} -> {new_path.name}")
                except Exception as e:
                    print(f"Error renaming {old_path.name}: {e}")
        
        if not dry_run:
            print(f"\nRenamed {renamed_count} photos")
        
        return renamed_count
    
    def generate_log(self):
        """Generate TEJAS_PHOTO_LOG.md"""
        with open(LOG_FILE, 'w') as f:
            f.write("# TEJAS Photo Processing Log\n\n")
            f.write("*Digital Archive of Theja Suranjan Dunusinghe's Martial Arts Journey*\n\n")
            f.write("---\n\n")
            
            # Summary statistics
            total = len(self.processed_photos)
            exif_count = sum(1 for p in self.processed_photos if p['source_method'] == 'EXIF Data')
            filename_count = sum(1 for p in self.processed_photos if p['source_method'] == 'Filename Pattern')
            visual_count = sum(1 for p in self.processed_photos if p['source_method'] == 'Visual Context')
            no_date_count = sum(1 for p in self.processed_photos if p['source_method'] == 'No Date Found')
            
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Total Photos Processed**: {total}\n")
            f.write(f"- **Dated via EXIF**: {exif_count}\n")
            f.write(f"- **Dated via Filename**: {filename_count}\n")
            f.write(f"- **Dated via Visual Context**: {visual_count}\n")
            f.write(f"- **No Date Found**: {no_date_count}\n\n")
            
            # Category breakdown
            f.write("## Category Breakdown\n\n")
            categories = {}
            for photo in self.processed_photos:
                cat = photo['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            for cat, count in sorted(categories.items()):
                f.write(f"- **{cat}**: {count} photos\n")
            
            f.write("\n---\n\n")
            
            # Main table
            f.write("## Photo Inventory\n\n")
            f.write("| New Filename | Source Method | Description | Timeline Match | Original Filename |\n")
            f.write("| :----------- | :------------ | :---------- | :------------- | :---------------- |\n")
            
            for photo in self.processed_photos:
                f.write(f"| {photo['new_name']} | {photo['source_method']} | {photo['description']} | {photo['timeline_match']} | {photo['original_name']} |\n")
            
            f.write("\n---\n\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"Log file generated: {LOG_FILE}")

def main():
    """Main execution"""
    print("=" * 60)
    print("TEJAS Photo Processing Script")
    print("=" * 60)
    print()
    
    processor = PhotoProcessor()
    
    # Process all photos
    processor.process_all_photos()
    
    # Generate log first (before renaming)
    processor.generate_log()
    
    # Perform rename
    print("\nRenaming photos...")
    processor.rename_photos(dry_run=False)
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
