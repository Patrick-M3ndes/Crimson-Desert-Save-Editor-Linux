from __future__ import annotations
import os
import json
import struct
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple


@dataclass
class Item:
    """Representa um item localizado no inventário / save."""
    offset: int
    item_no: int
    item_key: int
    name: str
    category: str
    slot_no: int
    stack_count: int
    internal_name: str = ""
    max_stack: int = 1
    enchant_level: int = 0
    endurance: int = 0
    sharpness: int = 0
    is_equipment: bool = False

    def __str__(self) -> str:
        cat_str = f"[{self.category}]" if self.category else ""
        enchant_str = f" (+{self.enchant_level})" if self.enchant_level > 0 else ""
        return (
            f"Slot {self.slot_no:3} | {self.name}{enchant_str} (ID: {self.item_key}) "
            f"x{self.stack_count:,} {cat_str}"
        )


def get_default_db_path() -> str:
    """Retorna o caminho padrão do arquivo item_names.json."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "item_names.json")


def load_item_database(db_path: Optional[str] = None) -> Dict[int, dict]:
    """Carrega o banco de dados completo de itens do jogo."""
    if db_path is None:
        db_path = get_default_db_path()

    item_db: Dict[int, dict] = {}
    if not os.path.exists(db_path):
        return item_db

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items_list = data.get("items", [])
            for item in items_list:
                key = item.get("itemKey")
                if key is not None:
                    item_db[key] = item
    except Exception as e:
        print(f"[Aviso] Não foi possível carregar o banco de itens: {e}")

    return item_db


def search_database_items(query: str, item_db: Optional[Dict[int, dict]] = None, limit: int = 30) -> List[dict]:
    """Pesquisa itens em todo o banco de dados de 6.200+ itens do jogo."""
    if item_db is None:
        item_db = load_item_database()

    q = query.strip().lower()
    if not q:
        return []

    results: List[dict] = []
    if q.isdigit():
        target_key = int(q)
        if target_key in item_db:
            return [item_db[target_key]]

    for item in item_db.values():
        name = item.get("name", "").lower()
        internal = item.get("internalName", "").lower()
        cat = item.get("category", "").lower()
        if q in name or q in internal or q in cat:
            results.append(item)
            if len(results) >= limit:
                break

    return results


def scan_items(
    blob: bytearray | bytes,
    item_db: Optional[Dict[int, dict]] = None,
) -> List[Item]:
    """
    Percorre o blob descompactado e localiza todos os registros de itens válidos.
    """
    if item_db is None:
        item_db = load_item_database()

    items: List[Item] = []
    length = len(blob)

    for off in range(16, length - 40):
        # Marcador uint32 == 1
        if struct.unpack_from("<I", blob, off)[0] != 1:
            continue

        # Sentinela int64 == -1
        if struct.unpack_from("<q", blob, off - 16)[0] != -1:
            continue

        item_no = struct.unpack_from("<q", blob, off + 4)[0]
        if not (1 <= item_no <= 999999):
            continue

        item_key = struct.unpack_from("<I", blob, off + 12)[0]
        if not (1 <= item_key <= 2147483647):
            continue

        slot_no = struct.unpack_from("<H", blob, off + 16)[0]
        stack_count = struct.unpack_from("<q", blob, off + 18)[0]
        if not (1 <= stack_count <= 9000000000000000000):
            continue

        enchant_raw = struct.unpack_from("<H", blob, off + 26)[0] if off + 28 <= length else 0
        endurance_raw = struct.unpack_from("<H", blob, off + 30)[0] if off + 32 <= length else 0
        sharpness_raw = struct.unpack_from("<H", blob, off + 32)[0] if off + 34 <= length else 0

        has_enchant = (enchant_raw != 65535 and enchant_raw > 0 and enchant_raw < 1000)

        item_meta = item_db.get(item_key, {})
        name = item_meta.get("name", f"Item Desconhecido ({item_key})")
        category = item_meta.get("category", "Geral")
        internal_name = item_meta.get("internalName", "")
        max_stack = item_meta.get("maxStack", 1)

        is_equip = has_enchant or (category in ["Equipment", "Misc"] and max_stack == 1)

        items.append(
            Item(
                offset=off,
                item_no=item_no,
                item_key=item_key,
                name=name,
                category=category,
                slot_no=slot_no,
                stack_count=stack_count,
                internal_name=internal_name,
                max_stack=max_stack,
                enchant_level=enchant_raw if has_enchant else 0,
                endurance=endurance_raw,
                sharpness=sharpness_raw,
                is_equipment=is_equip,
            )
        )

    return items


def set_item_stack(blob: bytearray, item: Item, new_quantity: int) -> int:
    """Modifica a quantidade (stack count) de um item no blob em memória."""
    if new_quantity < 1:
        raise ValueError("A quantidade deve ser pelo menos 1.")

    old_quantity = item.stack_count
    struct.pack_into("<q", blob, item.offset + 18, new_quantity)
    item.stack_count = new_quantity
    return old_quantity


def set_item_enchant(blob: bytearray, item: Item, new_enchant: int) -> int:
    """Modifica o nível de encantamento de um equipamento no blob em memória."""
    if new_enchant < 0 or new_enchant > 65534:
        raise ValueError("Nível de encantamento inválido (deve ser entre 0 e 65534).")

    old_enchant = item.enchant_level
    struct.pack_into("<H", blob, item.offset + 26, new_enchant)
    item.enchant_level = new_enchant
    item.is_equipment = True
    return old_enchant


def set_item_endurance(blob: bytearray, item: Item, new_val: int) -> int:
    """Modifica a durabilidade (endurance) de um equipamento."""
    old_val = item.endurance
    struct.pack_into("<H", blob, item.offset + 30, new_val)
    item.endurance = new_val
    return old_val


def set_item_sharpness(blob: bytearray, item: Item, new_val: int) -> int:
    """Modifica a afiação (sharpness) de um equipamento."""
    old_val = item.sharpness
    struct.pack_into("<H", blob, item.offset + 32, new_val)
    item.sharpness = new_val
    return old_val


def repair_item(blob: bytearray, item: Item, max_endurance: int = 1000, max_sharpness: int = 1280) -> Tuple[int, int]:
    """Restaura a durabilidade e a afiação máximas de um equipamento."""
    set_item_endurance(blob, item, max_endurance)
    set_item_sharpness(blob, item, max_sharpness)
    return max_endurance, max_sharpness


def swap_item_key(blob: bytearray, item: Item, new_key: int, new_meta: dict) -> int:
    """
    Substitui o ID do item atual por outro item da base de dados.
    Atualiza todas as referências diretas no registro binário.
    """
    old_key = item.item_key
    old_key_bytes = struct.pack("<I", old_key)
    new_key_bytes = struct.pack("<I", new_key)

    # 1. Atualiza no offset principal
    struct.pack_into("<I", blob, item.offset + 12, new_key)

    # 2. Atualiza referências locais do item no bloco (até 300 bytes à frente)
    scan_end = min(len(blob) - 4, item.offset + 300)
    for pos in range(item.offset + 16, scan_end):
        if blob[pos:pos + 4] == old_key_bytes:
            blob[pos:pos + 4] = new_key_bytes

    # Atualiza o objeto item
    item.item_key = new_key
    item.name = new_meta.get("name", f"Item ({new_key})")
    item.category = new_meta.get("category", "Geral")
    item.internal_name = new_meta.get("internalName", "")
    item.max_stack = new_meta.get("maxStack", 1)

    return old_key


def search_items(items: List[Item], query: str) -> List[Item]:
    """Busca itens carregados no inventário atual."""
    q = query.strip().lower()
    if not q:
        return []

    if q.isdigit():
        target_num = int(q)
        return [it for it in items if it.item_key == target_num or it.slot_no == target_num]

    return [
        it for it in items
        if q in it.name.lower() or q in it.internal_name.lower() or q in it.category.lower()
    ]
