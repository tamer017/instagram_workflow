#!/usr/bin/env python3
"""Test Arabic font rendering with detailed diagnostics."""

from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# Test text (Bismillah)
text = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"

print("="*70)
print("ARABIC FONT RENDERING TEST")
print("="*70)

print(f"\n1. Original text: {text}")
print(f"   Length: {len(text)} characters")

# Step 1: Reshape
reshaped = arabic_reshaper.reshape(text)
print(f"\n2. After reshaping: {reshaped}")
print(f"   Length: {len(reshaped)} characters")

# Step 2: Bidi
bidi_text = get_display(reshaped)
print(f"\n3. After bidi: {bidi_text}")
print(f"   Length: {len(bidi_text)} characters")

# Step 3: Load font
font_path = 'fonts/ScheherazadeNew-Regular.ttf'
print(f"\n4. Loading font: {font_path}")

try:
    font = ImageFont.truetype(font_path, 120)
    print(f"   ✓ Font loaded successfully")
except Exception as e:
    print(f"   ✗ Font loading failed: {e}")
    exit(1)

# Step 4: Create test image
print("\n5. Creating test image...")
img = Image.new('RGB', (1080, 400), (20, 20, 40))
draw = ImageDraw.Draw(img)

# Get text dimensions
try:
    bbox = draw.textbbox((0, 0), bidi_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    print(f"   Text dimensions: {text_width}x{text_height} pixels")
except Exception as e:
    print(f"   ✗ textbbox failed: {e}")
    text_width = 800
    text_height = 100

# Center the text
x = (1080 - text_width) // 2
y = (400 - text_height) // 2

print(f"   Position: ({x}, {y})")

# Draw shadow
try:
    draw.text((x+4, y+4), bidi_text, font=font, fill=(0, 0, 0))
    print("   ✓ Shadow drawn")
except Exception as e:
    print(f"   ✗ Shadow failed: {e}")

# Draw main text
try:
    draw.text((x, y), bidi_text, font=font, fill=(255, 215, 0))
    print("   ✓ Main text drawn")
except Exception as e:
    print(f"   ✗ Main text failed: {e}")

# Save image
output_file = 'test_arabic_detailed.png'
img.save(output_file)
print(f"\n6. ✓ Image saved: {output_file}")

# Verify image content
print("\n7. Verifying image content...")
img_verify = Image.open(output_file)
center_pixel = img_verify.getpixel((540, 200))
print(f"   Center pixel: {center_pixel}")

# Check if any gold pixels exist
gold_found = False
for y_check in range(100, 300):
    for x_check in range(200, 880):
        pixel = img_verify.getpixel((x_check, y_check))
        if pixel[0] > 200 and pixel[1] > 180:  # Looking for gold color
            gold_found = True
            print(f"   ✓ Gold text pixels found at ({x_check}, {y_check}): {pixel}")
            break
    if gold_found:
        break

if not gold_found:
    print("   ✗ NO GOLD TEXT PIXELS FOUND - TEXT NOT RENDERED!")
    print("\n   This means the font doesn't support these Arabic characters")
    print("   or PIL failed to render them.")
else:
    print("\n✅ SUCCESS! Arabic text rendered correctly.")

print("="*70)
