import os
import glob
import tempfile
import shutil
from src.crypto import load_save_file, save_save_file
from src.scanner import (
    scan_items,
    search_items,
    set_item_stack,
    set_item_enchant,
    swap_item_key,
    load_item_database,
    search_database_items,
)
from src.backup import create_backup


def test_full_pipeline():
    saves = glob.glob("/home/patrik/.local/share/Steam/steamapps/compatdata/3321460/pfx/drive_c/users/steamuser/AppData/Local/Pearl Abyss/CD/save/1223366488/slot0/save.save")
    if not saves:
        saves = glob.glob("/home/patrik/SAVE DE TESTE ATOMIC/slot0/save.save")
    if not saves:
        saves = glob.glob("/home/patrik/Downloads/CrimsonDesertSaveEditor/backups/slot101/*.bak")
    if not saves:
        saves = glob.glob("/home/patrik/Games/save/**/save.save", recursive=True)

    assert saves, "No test save files found"
    test_save = saves[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_save_path = os.path.join(tmpdir, "save.save")
        shutil.copy2(test_save, temp_save_path)

        # 1. Test Load & Decrypt
        item_db = load_item_database()
        assert len(item_db) > 6000, f"Database items count: {len(item_db)}"
        print(f"Loaded {len(item_db)} items from database.")

        save_file = load_save_file(temp_save_path)
        assert save_file.version == 2
        assert save_file.hmac_valid is True

        # 2. Test Item Scanning
        items = scan_items(save_file.blob, item_db)
        assert len(items) > 0
        print(f"Scanned {len(items)} items in save.")

        # 3. Test Search Item
        artifacts = search_items(items, "Abyss Artifact")
        assert len(artifacts) > 0
        abyss_artifact = artifacts[0]
        print(f"Found target item: {abyss_artifact.name} with stack={abyss_artifact.stack_count}")

        # 4. Test Stack Edit
        target_quantity = 9999
        set_item_stack(save_file.blob, abyss_artifact, target_quantity)
        assert abyss_artifact.stack_count == target_quantity

        # 5. Test Enchant Level Edit on Equipment
        first_equip = next((it for it in items if it.is_equipment or it.slot_no == 0), items[0])
        set_item_enchant(save_file.blob, first_equip, 15)
        assert first_equip.enchant_level == 15
        print(f"Set enchant +15 on {first_equip.name}")

        # 6. Test Item Swap
        db_results = search_database_items("Wolf's Fang", item_db)
        if db_results:
            target_meta = db_results[0]
            swap_item_key(save_file.blob, items[5], target_meta["itemKey"], target_meta)
            assert items[5].item_key == target_meta["itemKey"]
            print(f"Swapped item to: {items[5].name}")

        # 7. Test Save & Re-encryption
        save_save_file(
            temp_save_path,
            save_file.blob,
            save_file.raw_header,
            save_file.version,
        )

        # 8. Reload and Verify
        reloaded = load_save_file(temp_save_path)
        assert reloaded.hmac_valid is True
        reloaded_items = scan_items(reloaded.blob, item_db)
        reloaded_artifacts = search_items(reloaded_items, "Abyss Artifact")
        assert reloaded_artifacts[0].stack_count == target_quantity
        print("ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_full_pipeline()
