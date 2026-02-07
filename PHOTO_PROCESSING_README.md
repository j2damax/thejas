# Photo Processing Documentation

## Overview

This document describes the automated photo processing system for Theja Suranjan Dunusinghe's portfolio website. The system extracts dates from photos, renames them chronologically, and generates a comprehensive reference log.

## Processing Results

- **Total Photos Processed**: 70
- **Successfully Dated**: 51 photos (73%)
  - Via EXIF Data: 39 photos
  - Via Filename Pattern: 12 photos
- **Undated Photos**: 19 photos (27%)

## File Naming Convention

All photos are renamed using the ISO 8601 standard format:

```
YYYY-MM-DD_[Category]_[Description].ext
```

### Examples:
- `2024-11-05_[Action]_Camera_photo.HEIC`
- `2026-02-07_[Action]_Photo_from_WhatsApp.jpeg`
- `Undated_[Action]_IMG_0121.JPG`

### Categories:
1. **[Action]**: Training, sparring, kicking, martial arts demonstrations
2. **[Award]**: Medal ceremonies, podium moments, certificate presentations
3. **[Profile]**: Headshots, portraits, branding photos
4. **[Coaching]**: Teaching students, gym sessions, coaching activities
5. **[Event]**: Group photos, conferences, opening ceremonies, team events

## Date Extraction Logic

The script follows a three-tier priority system:

### Priority A: EXIF Metadata
- Extracts `DateTimeOriginal` or `CreateDate` from image metadata
- Most reliable source for camera photos (iPhone HEIC files)
- Success rate: 56% (39/70 photos)

### Priority B: Filename Patterns
- **WhatsApp Images**: `WhatsApp Image 2026-02-07 at...` → `2026-02-07`
- **Screenshots**: `Screenshot_20220415...` → `2022-04-15`
- **Date-prefixed**: `20161102_143022.jpg` → `2016-11-02`
- Success rate: 17% (12/70 photos)

### Priority C: Visual Context
- Currently uses filename heuristics and keywords
- Future enhancement: Computer vision analysis for content-based dating
- Placeholder for manual categorization

## Timeline Integration

The system cross-references photos with the `TEJAS_Master_Timeline.md` to identify photos matching documented events:

- **2014-11-19**: WoMAU Gold Medal (Korea)
- **2023-08-17**: 2nd Dong Black Belt
- **2025-01-01**: World Taekkyeon Championship

## Generated Files

### 1. TEJAS_PHOTO_LOG.md
A comprehensive markdown table containing:
- New filenames (chronologically sorted)
- Source method (EXIF, Filename, Visual Context)
- Visual descriptions
- Timeline matches
- Original filenames for reference

### 2. Renamed Photos
All photos in `/photos` directory have been renamed according to the convention above.

## Manual Refinement Guide

### Undated Photos (19 files)
The following photos require manual dating and categorization:

```
Undated_[Action]_72fb59f9-86c2-4f22-b491-e5a0560a8365.jpg
Undated_[Action]_7fd6b534-4d44-4fe4-8981-40e2e0ffd129.jpg
Undated_[Action]_IMG_0121.JPG (and 16 other IMG_*.JPG files)
Undated_[Action]_c158df3a-160a-4d37-a2a1-b88f51e96b89.jpg
```

### Recommended Manual Review Process:

1. **View Each Undated Photo**: Examine the image content
2. **Identify Visual Clues**:
   - Recognizable locations or events
   - Age of people in photos (to estimate year)
   - Visible medals/awards (cross-reference with timeline)
   - Equipment or uniforms that may indicate time period
   
3. **Cross-Reference with Timeline**:
   - Check `TEJAS_Master_Timeline.md` for documented events
   - Match visual elements with known dates
   
4. **Update Category if Needed**:
   - Change from generic `[Action]` to more specific category
   - Award photos showing medals or podiums
   - Profile photos for branding/headshots
   - Coaching photos showing students
   - Event photos with groups or ceremonies

5. **Manual Rename**: Use the helper script (see below)

## Helper Scripts

### process_photos.py
The main processing script that:
- Extracts EXIF data using `exiftool`
- Parses filename patterns
- Renames files chronologically
- Generates the photo log

**Usage:**
```bash
python3 process_photos.py
```

### Future Enhancement: Manual Categorization Tool
A future helper script could provide:
- Interactive photo viewer
- Manual date input
- Category selection
- Bulk rename operations

## Technical Details

### Dependencies
- **Python 3.12+**
- **exiftool** (libimage-exiftool-perl)
- **Pillow** (Python imaging library)
- **piexif** (EXIF manipulation)
- **python-dateutil** (Date parsing)

### Supported Formats
- `.jpg`, `.jpeg` - JPEG images
- `.png` - PNG images
- `.heic`, `.HEIC` - Apple HEIC format (iPhone photos)

### Installation
```bash
# Install system dependencies
sudo apt-get install libimage-exiftool-perl

# Install Python dependencies
pip install pillow piexif python-dateutil pillow-heif
```

## Next Steps

1. **Manual Review**: Examine undated photos and assign appropriate dates/categories
2. **Enhanced Descriptions**: Add more detailed visual descriptions to dated photos
3. **Timeline Correlation**: Manually match photos to specific timeline events
4. **Category Refinement**: Reclassify photos with more accurate categories
5. **Visual Analysis**: Future integration of computer vision for automated content analysis

## Notes

- All original filenames are preserved in `TEJAS_PHOTO_LOG.md`
- File renames are actual filesystem operations (not copies)
- The log is regenerated each time the script runs
- Chronological sorting helps identify gaps in the photo timeline
- WhatsApp images have dates from the upload date, not necessarily the capture date

## Contact

For questions or to request specific categorizations, contact the repository maintainer.

---

*Last Updated: 2026-02-07*
