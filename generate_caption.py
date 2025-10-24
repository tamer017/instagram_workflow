#!/usr/bin/env python3
"""
Generate Instagram caption with Arabic and English information.
Includes: Surah name, Ayah numbers, Reciter name (both languages)
"""

import json
import sys
from pathlib import Path


def load_json(file_path):
    """Load JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}


def get_surah_info(surah_num):
    """Get surah name in Arabic and English."""
    surah_names = load_json('surah_names.json')
    surahs = surah_names.get('surahs', {})
    surah_key = str(surah_num)
    
    if surah_key in surahs:
        return {
            'arabic': surahs[surah_key].get('arabic', ''),
            'english': surahs[surah_key].get('english', ''),
        }
    return {'arabic': '', 'english': f'Surah {surah_num}'}


def get_reciter_info(reciter_id):
    """Get reciter name in Arabic and English."""
    reciter_names = load_json('reciter_names.json')
    reciters = reciter_names.get('reciters', {})
    
    # Map reciter ID to name (based on available_reciters.json)
    reciter_map = {
        '1': 'abdulbaset abdulsamad',
        '2': 'abdulbaset abdulsamad',
        '3': 'abdur-rahman as-sudais',
        '4': 'abu bakr al-shatri',
        '5': 'hani ar-rifai',
        '6': 'mahmoud khalil al-husary',
        '7': 'mishari rashid al-afasy',
        '8': 'mohamed siddiq al-minshawi',
        '9': 'mohamed siddiq al-minshawi',
        '10': 'sa`ud ash-shuraym',
        '11': 'mohamed al-tablawi',
        '12': 'mahmoud khalil al-husary'
    }
    
    reciter_key = reciter_map.get(reciter_id, '').lower()
    
    if reciter_key in reciters:
        return {
            'arabic': reciters[reciter_key].get('arabic', ''),
            'english': reciters[reciter_key].get('english', '')
        }
    return {'arabic': '', 'english': f'Reciter {reciter_id}'}


def parse_group_id(group_id):
    """
    Parse group ID to extract components.
    Example: reciter1_s001_001-007
    Returns: (reciter_id, surah_num, start_ayah, end_ayah)
    """
    parts = group_id.split('_')
    
    # Extract reciter ID (e.g., "reciter1" -> "1")
    reciter_id = parts[0].replace('reciter', '')
    
    # Extract surah number (e.g., "s001" -> 1)
    surah_num = int(parts[1][1:])
    
    # Extract ayah range (e.g., "001-007" -> 1, 7)
    ayah_range = parts[2].split('-')
    start_ayah = int(ayah_range[0])
    end_ayah = int(ayah_range[1])
    
    return reciter_id, surah_num, start_ayah, end_ayah


def generate_caption(group_id):
    """
    Generate Instagram caption with Arabic and English information.
    
    Format:
    🕌 [Arabic Surah Name] | [English Surah Name]
    📖 Ayah [start] - [end]
    
    🎙️ [Arabic Reciter Name]
    🎙️ [English Reciter Name]
    
    #Quran #QuranRecitation #Islam
    """
    try:
        reciter_id, surah_num, start_ayah, end_ayah = parse_group_id(group_id)
        
        surah_info = get_surah_info(surah_num)
        reciter_info = get_reciter_info(reciter_id)
        
        # Build caption
        caption_parts = []
        
        # Surah name (Arabic and English)
        if surah_info['arabic'] and surah_info['english']:
            caption_parts.append(f"🕌 {surah_info['arabic']} | {surah_info['english']}")
        elif surah_info['english']:
            caption_parts.append(f"🕌 {surah_info['english']}")
        
        # Ayah range
        if start_ayah == end_ayah:
            caption_parts.append(f"📖 Ayah {start_ayah}")
        else:
            caption_parts.append(f"📖 Ayah {start_ayah} - {end_ayah}")
        
        caption_parts.append("")  # Empty line
        
        # Reciter name (Arabic)
        if reciter_info['arabic']:
            caption_parts.append(f"🎙️ {reciter_info['arabic']}")
        
        # Reciter name (English)
        if reciter_info['english']:
            caption_parts.append(f"🎙️ {reciter_info['english']}")
        
        caption_parts.append("")  # Empty line
        
        # Hashtags
        hashtags = [
            "#Quran",
            "#QuranRecitation",
            "#Islam",
            "#Islamic",
            "#Muslim",
            "#Allah",
            "#HolyQuran",
            "#Tilawat"
        ]
        
        if surah_info.get('english'):
            # Add surah-specific hashtag
            surah_tag = surah_info['english'].replace(' ', '').replace('-', '')
            hashtags.append(f"#{surah_tag}")
        
        caption_parts.append(" ".join(hashtags))
        
        return "\n".join(caption_parts)
        
    except Exception as e:
        print(f"Error generating caption: {e}")
        # Fallback caption
        return f"Quran Recitation - {group_id}\n\n#Quran #Islam #QuranRecitation"


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_caption.py <group_id>")
        print("Example: python generate_caption.py reciter1_s001_001-007")
        sys.exit(1)
    
    group_id = sys.argv[1]
    caption = generate_caption(group_id)
    
    print(caption)
    
    # Also save to file for GitHub Actions
    with open('caption.txt', 'w', encoding='utf-8') as f:
        f.write(caption)


if __name__ == '__main__':
    main()
