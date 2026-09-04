from __future__ import annotations
import os
import json
import struct
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Any

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
    average_price: int = 0
    
    # Offsets exatos calculados a partir da estrutura real do Save/ObjectBlock
    item_key_offset: Optional[int] = None
    stack_count_offset: Optional[int] = None
    slot_no_offset: Optional[int] = None
    enchant_level_offset: Optional[int] = None
    endurance_offset: Optional[int] = None
    sharpness_offset: Optional[int] = None
    average_price_offset: Optional[int] = None
    wrapper_offset: Optional[int] = None

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
    """Pesquisa itens em todo o banco de dados do jogo."""
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

def parse_save_schema(blob: bytes | bytearray) -> Tuple[Optional[Dict[int, dict]], Optional[int], int]:
    """
    Decodifica a tabela de Schema presente no início do save (offset 0x0E).
    Retorna (types_dict, item_save_data_type_index, schema_end_offset).
    """
    offset = 0x0E
    if len(blob) < offset + 6:
        return None, None, 0

    try:
        header_tag, header_zero, type_count = struct.unpack_from('<HHH', blob, offset)
        offset += 6
        if type_count == 0 or type_count > 2000:
            return None, None, 0

        root_len = struct.unpack_from('<I', blob, offset)[0]
        offset += 4
        if offset + root_len > len(blob):
            return None, None, 0

        root_name = blob[offset:offset+root_len].decode('ascii', errors='ignore')
        offset += root_len

        types: Dict[int, dict] = {}
        item_save_data_idx: Optional[int] = None
        current_name = root_name

        for t_idx in range(type_count):
            name = root_name if t_idx == 0 else current_name
            if name == 'ItemSaveData':
                item_save_data_idx = t_idx

            field_count = struct.unpack_from('<H', blob, offset)[0]
            offset += 2
            fields = []
            for f_idx in range(field_count):
                fname_len = struct.unpack_from('<I', blob, offset)[0]
                offset += 4
                fname = blob[offset:offset+fname_len].decode('ascii', errors='ignore')
                offset += fname_len

                tname_len = struct.unpack_from('<I', blob, offset)[0]
                offset += 4
                tname = blob[offset:offset+tname_len].decode('ascii', errors='ignore')
                offset += tname_len

                meta_kind, meta_size, meta_aux = struct.unpack_from('<HHI', blob, offset)
                offset += 8
                fields.append({
                    'index': f_idx,
                    'name': fname,
                    'type_name': tname,
                    'meta_kind': meta_kind,
                    'meta_size': meta_size,
                    'meta_aux': meta_aux,
                })
            types[t_idx] = {'index': t_idx, 'name': name, 'fields': fields}
            if t_idx < type_count - 1:
                next_len = struct.unpack_from('<I', blob, offset)[0]
                offset += 4
                current_name = blob[offset:offset+next_len].decode('ascii', errors='ignore')
                offset += next_len

        return types, item_save_data_idx, offset
    except Exception as e:
        return None, None, 0

def decode_item_save_data_payload(
    blob: bytes | bytearray,
    child_mask: bytes | bytearray,
    payload_start: int,
    item_schema: dict
) -> Optional[Tuple[Dict[str, Any], Dict[str, int]]]:
    """
    Decodifica o payload de uma instância de ItemSaveData com base na sua máscara de presença (child_mask).
    Retorna (field_values, field_offsets).
    """
    if payload_start + 4 > len(blob):
        return None

    cursor = payload_start + 4 # Pula reserved_u32
    field_values: Dict[str, Any] = {}
    field_offsets: Dict[str, int] = {}

    try:
        for f in item_schema['fields']:
            f_idx = f['index']
            byte_idx = f_idx // 8
            bit_idx = f_idx % 8
            is_present = bool(child_mask[byte_idx] & (1 << bit_idx)) if byte_idx < len(child_mask) else False
            if not is_present:
                continue

            mkind = f['meta_kind']
            msize = f['meta_size']
            fname = f['name']

            if mkind == 0: # Escalar Fixo
                val_offset = cursor
                field_offsets[fname] = val_offset
                if msize == 1:
                    val = blob[cursor]
                elif msize == 2:
                    val = struct.unpack_from('<H', blob, cursor)[0]
                elif msize == 4:
                    val = struct.unpack_from('<I', blob, cursor)[0]
                elif msize == 8:
                    val = struct.unpack_from('<Q', blob, cursor)[0]
                else:
                    val = bytes(blob[cursor:cursor+msize])
                field_values[fname] = val
                cursor += msize
            elif mkind in (4, 5): # Object Locator
                if cursor + 2 > len(blob):
                    return None
                mbc = struct.unpack_from('<H', blob, cursor)[0]
                if not (1 <= mbc <= 16):
                    return None
                wrapper_len = 2 + mbc + 2 + 1 + 4 + 4 + 4
                cursor += wrapper_len + 4
            elif mkind == 6: # ReflectObject list
                if cursor + 18 > len(blob):
                    return None
                prefix = blob[cursor]
                header_size = 19 if prefix == 1 else 18
                cursor += header_size

        return field_values, field_offsets
    except Exception:
        return None

def scan_items_schema(
    blob: bytes | bytearray,
    item_db: Optional[Dict[int, dict]] = None,
) -> List[Item]:
    """
    Realiza o parsing estrutural baseado em Schema, TOC e ObjectBlock.
    Enumera todas as instâncias de ItemSaveData sem varredura heurística cega.
    """
    if item_db is None:
        item_db = load_item_database()

    types, item_save_data_idx, schema_end = parse_save_schema(blob)
    if item_save_data_idx is None or types is None:
        return []

    item_schema = types[item_save_data_idx]
    items: List[Item] = []

    # Procura por ObjectLocatorWrappers apontando para child_type_index == item_save_data_idx
    target_child_type = item_save_data_idx
    search_start = max(0x7F51, schema_end)
    blob_len = len(blob)

    for pos in range(search_start, blob_len - 30):
        mbc = struct.unpack_from('<H', blob, pos)[0]
        if 1 <= mbc <= 16:
            if pos + 2 + mbc + 2 > blob_len:
                continue
            child_type_index = struct.unpack_from('<H', blob, pos + 2 + mbc)[0]
            if child_type_index == target_child_type:
                child_mask = blob[pos + 2 : pos + 2 + mbc]
                payload_start = pos + 2 + mbc + 2 + 1 + 4 + 4 + 4
                res = decode_item_save_data_payload(blob, child_mask, payload_start, item_schema)
                if res is not None:
                    fvals, foffs = res
                    item_key = fvals.get('_itemKey')
                    # Validação de sanidade do ID do item
                    if item_key is not None and 1 <= item_key <= 2000000:
                        item_no = fvals.get('_itemNo', 0)
                        slot_no = fvals.get('_slotNo', 0)
                        stack_count = fvals.get('_stackCount', 1)
                        average_price = fvals.get('_averagePrice', 0)
                        enchant_raw = fvals.get('_enchantLevel', 0)
                        endurance_raw = fvals.get('_endurance', 0)
                        sharpness_raw = fvals.get('_sharpness', 0)

                        item_meta = item_db.get(item_key, {})
                        name = item_meta.get("name", f"Unknown Item ({item_key})")
                        category = item_meta.get("category", "Geral")
                        internal_name = item_meta.get("internalName", "")
                        max_stack = item_meta.get("maxStack", 1)

                        has_enchant = (enchant_raw != 65535 and enchant_raw > 0 and enchant_raw < 1000)
                        is_equip = has_enchant or (category in ["Equipment", "Misc"] and max_stack == 1)

                        items.append(
                            Item(
                                offset=payload_start,
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
                                average_price=average_price,
                                item_key_offset=foffs.get('_itemKey'),
                                stack_count_offset=foffs.get('_stackCount'),
                                slot_no_offset=foffs.get('_slotNo'),
                                enchant_level_offset=foffs.get('_enchantLevel'),
                                endurance_offset=foffs.get('_endurance'),
                                sharpness_offset=foffs.get('_sharpness'),
                                average_price_offset=foffs.get('_averagePrice'),
                                wrapper_offset=pos,
                            )
                        )

    return items

def scan_items_legacy(
    blob: bytearray | bytes,
    item_db: Optional[Dict[int, dict]] = None,
) -> List[Item]:
    """Scanner de fallback (legado) baseado em sentinela -1 para compatibilidade."""
    if item_db is None:
        item_db = load_item_database()

    items: List[Item] = []
    length = len(blob)

    for off in range(0, length - 60):
        if struct.unpack_from("<q", blob, off)[0] != -1:
            continue

        item_no = struct.unpack_from("<q", blob, off + 8)[0]
        if not (1 <= item_no <= 999999):
            continue

        item_key = struct.unpack_from("<I", blob, off + 20)[0]
        if not (1 <= item_key <= 2147483647):
            continue

        item_meta = item_db.get(item_key, {})
        name = item_meta.get("name", f"Unknown Item ({item_key})")

        slot_no = struct.unpack_from("<H", blob, off + 24)[0]
        stack_count = struct.unpack_from("<q", blob, off + 26)[0]
        if not (1 <= stack_count <= 9000000000000000000):
            continue

        average_price = struct.unpack_from("<q", blob, off + 34)[0]
        enchant_raw = struct.unpack_from("<H", blob, off + 42)[0] if off + 44 <= length else 0
        endurance_raw = struct.unpack_from("<H", blob, off + 44)[0] if off + 46 <= length else 0
        sharpness_raw = struct.unpack_from("<H", blob, off + 46)[0] if off + 48 <= length else 0

        has_enchant = (enchant_raw != 65535 and enchant_raw > 0 and enchant_raw < 1000)
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
                average_price=average_price
            )
        )

    return items

def scan_items(
    blob: bytearray | bytes,
    item_db: Optional[Dict[int, dict]] = None,
) -> List[Item]:
    """
    Função principal de busca. Tenta o parser estrutural baseado no Schema/ObjectBlock.
    Se nenhum item for encontrado, faz o fallback gracioso para o scanner legado.
    """
    if item_db is None:
        item_db = load_item_database()

    items = scan_items_schema(blob, item_db)
    if items:
        return items

    return scan_items_legacy(blob, item_db)

def set_item_stack(blob: bytearray, item: Item, new_quantity: int) -> int:
    """Modifica a quantidade (stack count) de um item no blob em memória."""
    if new_quantity < 1:
        raise ValueError("A quantidade deve ser pelo menos 1.")

    old_quantity = item.stack_count
    target_off = item.stack_count_offset if item.stack_count_offset is not None else item.offset + 26
    struct.pack_into("<Q", blob, target_off, new_quantity)
    item.stack_count = new_quantity
    return old_quantity

def set_item_enchant(blob: bytearray, item: Item, new_enchant: int) -> int:
    """Modifica o nível de encantamento de um equipamento no blob em memória."""
    if new_enchant < 0 or new_enchant > 65534:
        raise ValueError("Nível de encantamento inválido (deve ser entre 0 e 65534).")

    old_enchant = item.enchant_level
    target_off = item.enchant_level_offset if item.enchant_level_offset is not None else item.offset + 42
    struct.pack_into("<H", blob, target_off, new_enchant)
    item.enchant_level = new_enchant
    item.is_equipment = True
    return old_enchant

def set_item_endurance(blob: bytearray, item: Item, new_val: int) -> int:
    """Modifica a durabilidade (endurance) de um equipamento."""
    old_val = item.endurance
    target_off = item.endurance_offset if item.endurance_offset is not None else item.offset + 44
    struct.pack_into("<H", blob, target_off, new_val)
    item.endurance = new_val
    return old_val

def set_item_sharpness(blob: bytearray, item: Item, new_val: int) -> int:
    """Modifica a afiação (sharpness) de um equipamento."""
    old_val = item.sharpness
    target_off = item.sharpness_offset if item.sharpness_offset is not None else item.offset + 46
    struct.pack_into("<H", blob, target_off, new_val)
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
    Atualiza as referências no registro binário.
    """
    old_key = item.item_key
    target_off = item.item_key_offset if item.item_key_offset is not None else item.offset + 20
    struct.pack_into("<I", blob, target_off, new_key)

    # Atualiza o objeto item
    item.item_key = new_key
    item.name = new_meta.get("name", f"Unknown Item ({new_key})")
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