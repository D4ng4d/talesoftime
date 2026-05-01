"""
seed.py - Populates all reference / lookup tables with initial data.
Run once: python database/seed.py
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.models import get_db, init_db

LOOKUP_SEED_DATA = {
    "CharacterClass": [
        {"ClassName": "Warrior",  "Description": "A powerful melee fighter."},
        {"ClassName": "Wizard",  "Description": "An educated practitioner of magic."},
        {"ClassName": "Sorcerer",  "Description": "A sinister dabbler in the dark arts"},
        {"ClassName": "Hunter",  "Description": "A skilled bowman and tracker"},
        {"ClassName": "Druid",  "Description": "Can shapeshift into various animals"},
        {"ClassName": "Engineer",  "Description": "Tinkerer of technology"},
        {"ClassName": "Rogue",  "Description": "A skilled thief and assassin"},
    ],
    "Species": [
        {"SpeciesName": "Human"},
        {"SpeciesName": "Dwarf"},
        {"SpeciesName": "Orc"},
        {"SpeciesName": "Elf"},
        {"SpeciesName": "Dark Elf"},
        {"SpeciesName": "Halfling"},
    ],
    "Alignment": [
        {"AlignmentName": "Philanthropist"},
        {"AlignmentName": "Heretic"},
        {"AlignmentName": "Draconist"},
        {"AlignmentName": "Divergent"},
        {"AlignmentName": "Anarchist"},
        {"AlignmentName": "Extremist"},
        {"AlignmentName": "Conservationist"},
    ],
    "ItemType": [
        {"TypeName": "Weapon"},
        {"TypeName": "Armour"},
        {"TypeName": "Potion"},
        {"TypeName": "Reagent"},
        {"TypeName": "Poison"},
        {"TypeName": "Jewellery"},
    ],
    "Rarity": [
        {"RarityName": "Common"},
        {"RarityName": "Uncommon"},
        {"RarityName": "Rare"},
        {"RarityName": "Epic"},
        {"RarityName": "Legendary"},
        {"RarityName": "Artifact"},
    ],
    "Region": [
        {"RegionName": "The Badlands"},
        {"RegionName": "Hierland"},
        {"RegionName": "Alderland"},
        {"RegionName": "The Dead City"},
        {"RegionName": "Gaia's Wood"},
        {"RegionName": "Silversale"},

    ],
    "Difficulty": [
        {"DifficultyName": "Novice"},
        {"DifficultyName": "Amateur"},
        {"DifficultyName": "Superior"},
        {"DifficultyName": "Professional"},
        {"DifficultyName": "Tread Lightly....."},
        {"DifficultyName": "Deathwish"},
    ],
}


def table_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) AS Total FROM {table_name}")
    return cursor.fetchone()["Total"]


def fetch_lookup_map(cursor, table_name, key_field):
    cursor.execute(f"SELECT * FROM {table_name}")
    return {row[key_field]: dict(row) for row in cursor.fetchall()}


def seed_lookup_tables(cursor):
    for table_name, rows in LOOKUP_SEED_DATA.items():
        if table_count(cursor, table_name) == 0:
            for row in rows:
                columns      = ", ".join(row.keys())
                placeholders = ", ".join(["?"] * len(row))
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                    tuple(row.values())
                )
            print(f"  ✔ Seeded {table_name}")
        else:
            print(f"  – Skipped {table_name} (already has data)")


def seed_core_data(cursor):
    if table_count(cursor, "Character") > 0:
        print("  – Skipped Character / Item / Quest / Inventory / CharacterQuest (already has data)")
        return

    classes    = fetch_lookup_map(cursor, "CharacterClass", "ClassName")
    species    = fetch_lookup_map(cursor, "Species",        "SpeciesName")
    alignments = fetch_lookup_map(cursor, "Alignment",      "AlignmentName")
    item_types = fetch_lookup_map(cursor, "ItemType",       "TypeName")
    rarities   = fetch_lookup_map(cursor, "Rarity",         "RarityName")
    regions    = fetch_lookup_map(cursor, "Region",         "RegionName")
    difficulties = fetch_lookup_map(cursor, "Difficulty",   "DifficultyName")

    # ── Characters ────────────────────────────────────────────────────────────
    character_rows = [
        {"CharacterName": "Thorin Ironblade",    "ClassID": classes["Warrior"]["ClassID"],  "SpeciesID": species["Dwarf"]["SpeciesID"],  "AlignmentID": alignments["Draconist"]["AlignmentID"],     "Level": 32},
        {"CharacterName": "Corvana",    "ClassID": classes["Wizard"]["ClassID"],  "SpeciesID": species["Elf"]["SpeciesID"],  "AlignmentID": alignments["Conservationist"]["AlignmentID"],     "Level": 45},
        {"CharacterName": "Jinra",    "ClassID": classes["Hunter"]["ClassID"],  "SpeciesID": species["Dark Elf"]["SpeciesID"],  "AlignmentID": alignments["Heretic"]["AlignmentID"],     "Level": 30},
        {"CharacterName": "Gnablar",    "ClassID": classes["Sorcerer"]["ClassID"],  "SpeciesID": species["Halfling"]["SpeciesID"],  "AlignmentID": alignments["Conservationist"]["AlignmentID"],     "Level": 49},
        {"CharacterName": "Woodlyn",    "ClassID": classes["Druid"]["ClassID"],  "SpeciesID": species["Human"]["SpeciesID"],  "AlignmentID": alignments["Divergent"]["AlignmentID"],     "Level": 38},
        {"CharacterName": "Ghazkull",    "ClassID": classes["Warrior"]["ClassID"],  "SpeciesID": species["Orc"]["SpeciesID"],  "AlignmentID": alignments["Extremist"]["AlignmentID"],     "Level": 45},
        {"CharacterName": "Darryn",    "ClassID": classes["Rogue"]["ClassID"],  "SpeciesID": species["Human"]["SpeciesID"],  "AlignmentID": alignments["Draconist"]["AlignmentID"],     "Level": 40},
        {"CharacterName": "Bizkit",    "ClassID": classes["Engineer"]["ClassID"],  "SpeciesID": species["Orc"]["SpeciesID"],  "AlignmentID": alignments["Philanthropist"]["AlignmentID"],     "Level": 53},
    ]

    for row in character_rows:
        cursor.execute("""
            INSERT INTO Character (CharacterName, ClassID, SpeciesID, AlignmentID, Level)
            VALUES (?, ?, ?, ?, ?)
        """, (row["CharacterName"], row["ClassID"], row["SpeciesID"], row["AlignmentID"], row["Level"]))

    print("  ✔ Seeded Character")
    character_map = fetch_lookup_map(cursor, "Character", "CharacterName")

    # ── Items ─────────────────────────────────────────────────────────────────
    item_rows = [
        {"ItemName": "Iron Sword",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Common"]["RarityID"]},
        {"ItemName": "Staff of Power",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Rare"]["RarityID"]},
        {"ItemName": "Jade Amulet",          "ItemTypeID": item_types["Jewellery"]["ItemTypeID"],  "RarityID": rarities["Epic"]["RarityID"]},
        {"ItemName": "Great Bow",          "ItemTypeID": item_types["Weapon"]["ItemTypeID"],  "RarityID": rarities["Common"]["RarityID"]},
        {"ItemName": "Fortified Shield",          "ItemTypeID": item_types["Armour"]["ItemTypeID"],  "RarityID": rarities["Uncommon"]["RarityID"]},
        {"ItemName": "Blood Gem",          "ItemTypeID": item_types["Reagent"]["ItemTypeID"],  "RarityID": rarities["Epic"]["RarityID"]},
        {"ItemName": "Kings Crown",          "ItemTypeID": item_types["Armour"]["ItemTypeID"],  "RarityID": rarities["Legendary"]["RarityID"]},
        {"ItemName": "Mana Vial",          "ItemTypeID": item_types["Potion"]["ItemTypeID"],  "RarityID": rarities["Common"]["RarityID"]},
        {"ItemName": "Nightshade",          "ItemTypeID": item_types["Poison"]["ItemTypeID"],  "RarityID": rarities["Rare"]["RarityID"]},
        ]

    for row in item_rows:
        cursor.execute("""
            INSERT INTO Item (ItemName, ItemTypeID, RarityID)
            VALUES (?, ?, ?)
        """, (row["ItemName"], row["ItemTypeID"], row["RarityID"]))

    print("  ✔ Seeded Item")
    item_map = fetch_lookup_map(cursor, "Item", "ItemName")

    # ── Quests ────────────────────────────────────────────────────────────────
    quest_rows = [
        {"QuestName": "Peasant's Revolt!",       "RegionID": regions["The Badlands"]["RegionID"],        "DifficultyID": difficulties["Amateur"]["DifficultyID"]},
        {"QuestName": "Dragon's Awakening",       "RegionID": regions["The Dead City"]["RegionID"],        "DifficultyID": difficulties["Deathwish"]["DifficultyID"]},
        {"QuestName": "Granny's Lost Cat",       "RegionID": regions["Alderland"]["RegionID"],        "DifficultyID": difficulties["Novice"]["DifficultyID"]},
        {"QuestName": "Death to the King!",       "RegionID": regions["Hierland"]["RegionID"],        "DifficultyID": difficulties["Tread Lightly....."]["DifficultyID"]},
        {"QuestName": "Poison the Well",       "RegionID": regions["Silversale"]["RegionID"],        "DifficultyID": difficulties["Professional"]["DifficultyID"]},
    ]

    for row in quest_rows:
        cursor.execute("""
            INSERT INTO Quest (QuestName, RegionID, DifficultyID)
            VALUES (?, ?, ?)
        """, (row["QuestName"], row["RegionID"], row["DifficultyID"]))

    print("  ✔ Seeded Quest")
    quest_map = fetch_lookup_map(cursor, "Quest", "QuestName")

    # ── Inventory ─────────────────────────────────────────────────────────────
    inventory_rows = [
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "ItemID": item_map["Iron Sword"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "ItemID": item_map["Fortified Shield"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Darryn"]["CharacterID"],    "ItemID": item_map["Nightshade"]["ItemID"],           "Quantity": 5},
        {"CharacterID": character_map["Woodlyn"]["CharacterID"],    "ItemID": item_map["Great Bow"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Ghazkull"]["CharacterID"],    "ItemID": item_map["Kings Crown"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Gnablar"]["CharacterID"],    "ItemID": item_map["Staff of Power"]["ItemID"],           "Quantity": 1},
        {"CharacterID": character_map["Bizkit"]["CharacterID"],    "ItemID": item_map["Blood Gem"]["ItemID"],           "Quantity": 10},
        {"CharacterID": character_map["Jinra"]["CharacterID"],    "ItemID": item_map["Great Bow"]["ItemID"],           "Quantity": 2},
        {"CharacterID": character_map["Corvana"]["CharacterID"],    "ItemID": item_map["Mana Vial"]["ItemID"],           "Quantity": 3},
        {"CharacterID": character_map["Jinra"]["CharacterID"],    "ItemID": item_map["Jade Amulet"]["ItemID"],           "Quantity": 1},
    ]

    for row in inventory_rows:
        cursor.execute("""
            INSERT INTO Inventory (CharacterID, ItemID, Quantity)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["ItemID"], row["Quantity"]))

    print("  ✔ Seeded Inventory")

    # ── CharacterQuest ────────────────────────────────────────────────────────
    character_quest_rows = [
        {"CharacterID": character_map["Thorin Ironblade"]["CharacterID"],    "QuestID": quest_map["Peasant's Revolt!"]["QuestID"],       "CompletionDate": datetime(2025, 1, 10, 15, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Darryn"]["CharacterID"],    "QuestID": quest_map["Peasant's Revolt!"]["QuestID"],       "CompletionDate": datetime(2026, 12, 4, 11, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Woodlyn"]["CharacterID"],    "QuestID": quest_map["Dragon's Awakening"]["QuestID"],       "CompletionDate": datetime(2026, 4, 5, 10, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Gnablar"]["CharacterID"],    "QuestID": quest_map["Death to the King!"]["QuestID"],       "CompletionDate": datetime(2025, 8, 12, 2, 59).isoformat(sep=" ")},
        {"CharacterID": character_map["Jinra"]["CharacterID"],    "QuestID": quest_map["Peasant's Revolt!"]["QuestID"],       "CompletionDate": datetime(2026, 6, 12, 1, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Corvana"]["CharacterID"],    "QuestID": quest_map["Poison the Well"]["QuestID"],       "CompletionDate": datetime(2026, 10, 12, 1, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Bizkit"]["CharacterID"],    "QuestID": quest_map["Granny's Lost Cat"]["QuestID"],       "CompletionDate": datetime(2025, 7, 19, 8, 30).isoformat(sep=" ")},
        {"CharacterID": character_map["Ghazkull"]["CharacterID"],    "QuestID": quest_map["Peasant's Revolt!"]["QuestID"],       "CompletionDate": datetime(2026, 2, 2, 5, 30).isoformat(sep=" ")},
    ]

    for row in character_quest_rows:
        cursor.execute("""
            INSERT INTO CharacterQuest (CharacterID, QuestID, CompletionDate)
            VALUES (?, ?, ?)
        """, (row["CharacterID"], row["QuestID"], row["CompletionDate"]))

    print("  ✔ Seeded CharacterQuest")


def seed():
    init_db()
    conn = get_db()          # was: get_connection() - does not exist
    cursor = conn.cursor()

    try:
        seed_lookup_tables(cursor)
        seed_core_data(cursor)
        conn.commit()
        print("\nSeed complete.")
    except Exception as e:
        conn.rollback()
        print(f"\nSeed failed: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    seed()
