"""
Group tracking and selection system for sequential Quran video publishing.
Ensures each group is published only once in order.
"""

import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


PUBLISHED_GROUPS_FILE = Path("published_groups.json")


def load_published_groups() -> Dict:
    """Load the published groups tracking file."""
    if not PUBLISHED_GROUPS_FILE.exists():
        return {
            "last_published": None,
            "published_groups": [],
            "queue": [],
            "statistics": {
                "total_published": 0,
                "last_run": None,
                "success_count": 0,
                "failure_count": 0
            }
        }
    
    try:
        with open(PUBLISHED_GROUPS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading published groups: {e}")
        return {
            "last_published": None,
            "published_groups": [],
            "queue": [],
            "statistics": {"total_published": 0, "last_run": None, "success_count": 0, "failure_count": 0}
        }


def save_published_groups(data: Dict):
    """Save the published groups tracking file."""
    try:
        with open(PUBLISHED_GROUPS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving published groups: {e}")


def get_all_groups() -> List[str]:
    """Get all available groups from reciter_1_AbdulBaset_AbdulSamad only."""
    all_groups = []
    quran_groups_dir = Path("quran_groups")
    
    # Only use reciter_1_AbdulBaset_AbdulSamad_groups.json
    reciter_1_file = quran_groups_dir / "reciter_1_AbdulBaset_AbdulSamad_groups.json"
    
    if not reciter_1_file.exists():
        print(f"Error: {reciter_1_file} not found!")
        return []
    
    try:
        with open(reciter_1_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            groups = data.get('groups', {})
            # Sort groups by surah and ayah (numerical order)
            sorted_groups = sorted(groups.keys(), key=lambda x: (
                int(x.split('_')[1][1:]),  # Surah number (s001 -> 1)
                int(x.split('_')[2].split('-')[0])  # Start ayah
            ))
            all_groups.extend(sorted_groups)
    except Exception as e:
        print(f"Error loading {reciter_1_file}: {e}")
    
    return all_groups


def get_next_group() -> Optional[str]:
    """
    Get the next group to publish in sequential order.
    Returns None if all groups have been published.
    """
    tracking = load_published_groups()
    all_groups = get_all_groups()
    
    if not all_groups:
        print("No groups found!")
        return None
    
    published = set(tracking.get('published_groups', []))
    
    # Find the first unpublished group
    for group in all_groups:
        if group not in published:
            print(f"Next group to publish: {group}")
            return group
    
    # All groups published - restart from beginning
    print("All groups published! Restarting from the beginning...")
    tracking['published_groups'] = []
    tracking['statistics']['total_published'] = 0
    save_published_groups(tracking)
    return all_groups[0] if all_groups else None


def mark_group_published(group_id: str, success: bool = True):
    """Mark a group as published and update statistics."""
    tracking = load_published_groups()
    
    if group_id not in tracking['published_groups']:
        tracking['published_groups'].append(group_id)
    
    tracking['last_published'] = group_id
    tracking['statistics']['last_run'] = datetime.now().isoformat()
    
    if success:
        tracking['statistics']['success_count'] += 1
        tracking['statistics']['total_published'] += 1
    else:
        tracking['statistics']['failure_count'] += 1
    
    save_published_groups(tracking)
    print(f"Marked {group_id} as published (Success: {success})")
    print(f"Total published: {tracking['statistics']['total_published']}")


def get_progress() -> Dict:
    """Get publishing progress statistics."""
    tracking = load_published_groups()
    all_groups = get_all_groups()
    published_count = len(tracking.get('published_groups', []))
    total_count = len(all_groups)
    
    return {
        'published': published_count,
        'total': total_count,
        'remaining': total_count - published_count,
        'percentage': (published_count / total_count * 100) if total_count > 0 else 0,
        'last_published': tracking.get('last_published'),
        'statistics': tracking.get('statistics', {})
    }


if __name__ == "__main__":
    # Test the tracking system
    print("=== Quran Video Publishing Tracker ===\n")
    
    progress = get_progress()
    print(f"Progress: {progress['published']}/{progress['total']} ({progress['percentage']:.1f}%)")
    print(f"Remaining: {progress['remaining']}")
    print(f"Last published: {progress['last_published']}")
    print(f"\nStatistics:")
    print(f"  Total published: {progress['statistics'].get('total_published', 0)}")
    print(f"  Success: {progress['statistics'].get('success_count', 0)}")
    print(f"  Failures: {progress['statistics'].get('failure_count', 0)}")
    print(f"  Last run: {progress['statistics'].get('last_run', 'Never')}")
    
    print(f"\n--- Next Group ---")
    next_group = get_next_group()
    if next_group:
        print(f"Ready to publish: {next_group}")
    else:
        print("No groups available")
