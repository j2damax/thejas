#!/bin/bash
# Verification script to validate photo processing

echo "=== Photo Processing Verification ==="
echo ""

# Check if all required files exist
echo "Checking required files..."
for file in process_photos.py manual_categorization_helper.py TEJAS_PHOTO_LOG.md PHOTO_PROCESSING_README.md PHOTO_PROCESSING_SUMMARY.md; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file missing"
    fi
done

echo ""
echo "Photo Statistics:"
cd photos
TOTAL=$(ls -1 | wc -l)
DATED=$(ls -1 | grep -E "^20[0-9]{2}-" | wc -l)
UNDATED=$(ls -1 | grep "^Undated" | wc -l)

echo "  Total photos: $TOTAL"
echo "  Dated photos: $DATED ($(awk "BEGIN {printf \"%.1f\", ($DATED/$TOTAL)*100}")%)"
echo "  Undated photos: $UNDATED ($(awk "BEGIN {printf \"%.1f\", ($UNDATED/$TOTAL)*100}")%)"

echo ""
echo "Date Range:"
EARLIEST=$(ls -1 | grep -E "^20[0-9]{2}-" | head -1 | cut -d'_' -f1)
LATEST=$(ls -1 | grep -E "^20[0-9]{2}-" | tail -1 | cut -d'_' -f1)
echo "  Earliest: $EARLIEST"
echo "  Latest: $LATEST"

echo ""
echo "Category Distribution:"
for category in Action Award Profile Coaching Event; do
    COUNT=$(ls -1 | grep -c "\[$category\]" || echo "0")
    echo "  [$category]: $COUNT photos"
done

echo ""
echo "=== Verification Complete ==="
