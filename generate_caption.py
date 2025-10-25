#!/usr/bin/env python3
"""
Generate Instagram caption with Arabic and English information.
Includes: Surah name, Ayah numbers, Reciter name (both languages)
"""

import json
import sys
import random
from pathlib import Path

# Configuration
HASHTAG_COUNT = 15  # Fixed number of hashtags to use per post


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


def get_hashtag_pool():
    """
    Return a large pool of relevant hashtags for Quran content.
    Mix of Islamic, spiritual, religious, and Quran-specific tags in English and Arabic.
    """
    return [
        # Core Quran hashtags (English)
        "#Quran", "#HolyQuran", "#QuranRecitation", "#QuranDaily", "#QuranVerse",
        "#QuranQuotes", "#QuranReading", "#QuranKareem", "#Tilawat", "#TilawatEQuran",
        "#QuranReels", "#QuranVideo", "#QuranAudio", "#QuranReciter", "#QuranicVerses",
        
        # Core Quran hashtags (Arabic)
        "#القرآن", "#القرآن_الكريم", "#تلاوة", "#تلاوة_القرآن", "#آيات_قرآنية",
        "#قرآن_كريم", "#تلاوات", "#القران", "#مصحف", "#تجويد",
        
        # Islamic faith hashtags (English)
        "#Islam", "#Islamic", "#Muslim", "#Allah", "#IslamicPost", "#IslamicContent",
        "#IslamicReminder", "#IslamicQuotes", "#MuslimLife", "#Ummah", "#Deen",
        "#Sunnah", "#IslamDaily", "#IslamicReels", "#MuslimReels",
        
        # Islamic faith hashtags (Arabic)
        "#الإسلام", "#إسلامي", "#مسلم", "#الله", "#دين", "#أمة_الإسلام",
        "#سنة", "#إسلاميات", "#ديني", "#مسلمون", "#أمة_محمد",
        
        # Spiritual and worship hashtags (English)
        "#Spirituality", "#Faith", "#Prayer", "#Dua", "#Worship", "#Blessed",
        "#SpiritualJourney", "#IslamicSpirituality", "#DivineWords", "#SacredText",
        "#HolyBook", "#ReligiousContent", "#Devotion", "#IslamicWisdom",
        
        # Spiritual and worship hashtags (Arabic)
        "#روحانيات", "#إيمان", "#صلاة", "#دعاء", "#عبادة", "#ذكر_الله",
        "#روحانية", "#مؤمنون", "#كتاب_الله", "#حكمة_إسلامية",
        
        # Recitation and learning hashtags (English)
        "#TajweedQuran", "#LearnQuran", "#QuranStudy", "#QuranTeaching", "#QuranLearning",
        "#QuranMemorization", "#Hifz", "#QuranSchool", "#QuranClass", "#QuranicStudies",
        "#ArabicRecitation", "#BeautifulRecitation", "#MelodiousQuran",
        
        # Recitation and learning hashtags (Arabic)
        "#تجويد_القرآن", "#تعلم_القرآن", "#حفظ_القرآن", "#حافظ", "#مقرئ",
        "#قراء", "#تعليم_القرآن", "#دراسة_قرآنية", "#حلقات_قرآنية",
        
        # Peace and reflection hashtags (English)
        "#Peace", "#InnerPeace", "#Reflection", "#Meditation", "#Contemplation",
        "#PeaceOfMind", "#Tranquility", "#Serenity", "#Calm", "#Mindfulness",
        "#SpiritualPeace", "#IslamicPeace",
        
        # Peace and reflection hashtags (Arabic)
        "#سلام", "#سكينة", "#طمأنينة", "#تأمل", "#راحة_البال",
        "#هدوء", "#سلام_القلب", "#تدبر", "#خشوع",
        
        # Community and sharing hashtags (English)
        "#ShareTheQuran", "#SpreadTheWord", "#IslamicCommunity", "#MuslimCommunity",
        "#MuslimWorld", "#IslamicWorld", "#BrotherhoodInIslam", "#UmmahUnity",
        
        # Community and sharing hashtags (Arabic)
        "#شارك_الخير", "#انشر_الخير", "#مجتمع_إسلامي", "#أخوة_الإسلام",
        "#أمة_واحدة", "#المسلمين", "#العالم_الإسلامي",
        
        # Arabic and language hashtags (English)
        "#Arabic", "#ArabicLanguage", "#ArabicCalligraphy", "#IslamicArt",
        "#ArabicQuran", "#ClassicalArabic",
        
        # Arabic and language hashtags (Arabic)
        "#عربي", "#لغة_عربية", "#خط_عربي", "#فن_إسلامي", "#قرآن_عربي",
        
        # Ramadan and special occasions (English)
        "#Ramadan", "#RamadanKareem", "#Jummah", "#JummahMubarak", "#IslamicReminders",
        "#DailyReminder", "#IslamicMotivation",
        
        # Ramadan and special occasions (Arabic)
        "#رمضان", "#رمضان_كريم", "#جمعة_مباركة", "#يوم_الجمعة",
        "#تذكير", "#تذكير_ديني", "#موعظة",
        
        # Blessings and gratitude hashtags (English)
        "#Alhamdulillah", "#SubhanAllah", "#MashaAllah", "#Barakah", "#Blessings",
        "#Grateful", "#Thankful", "#AllahuAkbar",
        
        # Blessings and gratitude hashtags (Arabic)
        "#الحمد_لله", "#الحمدلله", "#سبحان_الله", "#ماشاء_الله",
        "#بركة", "#شكر", "#الله_أكبر", "#نعمة",
        
        # Guidance and inspiration hashtags (English)
        "#Guidance", "#IslamicGuidance", "#DivineGuidance", "#Inspiration",
        "#IslamicInspiration", "#MotivationalQuotes", "#FaithInspiration",
        "#PathToParadise", "#Jannah",
        
        # Guidance and inspiration hashtags (Arabic)
        "#هداية", "#إرشاد", "#هدى", "#إلهام", "#طريق_الجنة",
        "#جنة", "#توجيه_ديني", "#نور", "#بصيرة",
        
        # Lifestyle and modern Muslim hashtags (English)
        "#ModernMuslim", "#MuslimLifestyle", "#IslamicLifestyle", "#MuslimMotivation",
        "#IslamInModernWorld", "#YoungMuslim", "#MuslimYouth",
        
        # Lifestyle and modern Muslim hashtags (Arabic)
        "#مسلم_عصري", "#حياة_إسلامية", "#أسلوب_حياة_إسلامي",
        "#شباب_مسلم", "#جيل_القرآن",
        
        # Reels and content format hashtags (English)
        "#Reels", "#InstagramReels", "#IslamicReels", "#MuslimReels", "#ViralReels",
        "#TrendingReels", "#ReelsOfInstagram", "#ExploreReels", "#ReelsViral",
        
        # Reels and content format hashtags (Arabic)
        "#ريلز", "#ريلز_إسلامي", "#فيديو_قصير", "#محتوى_إسلامي",
        "#ريلز_ديني", "#قصير",
        
        # Educational hashtags (English)
        "#IslamicEducation", "#LearnIslam", "#IslamicKnowledge", "#KnowledgeIsPower",
        "#SeekKnowledge", "#IslamicLearning", "#ReligiousEducation",
        
        # Educational hashtags (Arabic)
        "#تعليم_إسلامي", "#تعلم_الإسلام", "#علم_شرعي", "#معرفة",
        "#طلب_العلم", "#ثقافة_إسلامية", "#فقه",
        
        # Additional variations (English)
        "#AlQuran", "#AlQuranAlKareem", "#NobleQuran", "#GloriousQuran",
        "#BookOfAllah", "#WordOfGod", "#DivineSpeech", "#RevelationOfAllah",
        
        # Additional variations (Arabic)
        "#كلام_الله", "#وحي", "#آيات", "#سور", "#كتاب_الله",
        "#قول_الله", "#منزل_من_عند_الله", "#معجزة_القرآن"
    ]


def generate_caption(group_id):
    """
    Generate Instagram caption with Arabic and English information.
    
    Format:
    🕌 [Arabic Surah Name] | [English Surah Name]
    📖 Ayah [start] - [end]
    
    🎙️ [Arabic Reciter Name]
    🎙️ [English Reciter Name]
    
    [Random selection of hashtags from pool]
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
        
        # Get hashtag pool and select random hashtags
        hashtag_pool = get_hashtag_pool()
        
        # Always include core hashtags
        core_hashtags = ["#Quran", "#Islam", "#QuranRecitation"]
        
        # Add surah-specific hashtag if available
        if surah_info.get('english'):
            surah_tag = surah_info['english'].replace(' ', '').replace('-', '')
            core_hashtags.append(f"#{surah_tag}")
        
        # Remove core hashtags from pool to avoid duplicates
        available_hashtags = [tag for tag in hashtag_pool if tag not in core_hashtags]
        
        # Calculate how many random hashtags to add
        num_random = HASHTAG_COUNT - len(core_hashtags)
        
        # Select random hashtags from available pool
        if num_random > 0 and available_hashtags:
            random_hashtags = random.sample(available_hashtags, min(num_random, len(available_hashtags)))
        else:
            random_hashtags = []
        
        # Combine core and random hashtags
        all_hashtags = core_hashtags + random_hashtags
        
        # Add hashtags to caption
        caption_parts.append(" ".join(all_hashtags))
        
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
