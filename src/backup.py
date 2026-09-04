from __future__ import annotations
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any


def create_backup(save_file_path: str, backup_dir: str | None = None) -> str:
    """
    Cria uma cópia de segurança com carimbo de data/hora do arquivo save.
    Retorna o caminho do arquivo de backup criado.
    """
    if not os.path.exists(save_file_path):
        raise FileNotFoundError(f"Arquivo de save para backup não existe: {save_file_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(save_file_path)

    if backup_dir is None:
        save_dir = os.path.dirname(save_file_path)
        backup_dir = os.path.join(save_dir, "backups")

    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"{base_name}.{timestamp}.bak")

    shutil.copy2(save_file_path, backup_path)
    return backup_path


def list_backups(save_file_path: str, backup_dir: str | None = None) -> List[Dict[str, Any]]:
    """
    Lista todos os backups disponíveis para o save especificado, ordenados do mais recente ao mais antigo.
    """
    save_dir = os.path.dirname(os.path.abspath(save_file_path))
    if backup_dir is None:
        backup_dir = os.path.join(save_dir, "backups")

    if not os.path.exists(backup_dir):
        return []

    backups = []
    for entry in os.listdir(backup_dir):
        if entry.endswith(".bak"):
            full_path = os.path.join(backup_dir, entry)
            if os.path.isfile(full_path):
                mtime = os.path.getmtime(full_path)
                mtime_str = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y às %H:%M:%S")
                size = os.path.getsize(full_path)
                backups.append({
                    "filename": entry,
                    "path": full_path,
                    "mtime": mtime,
                    "mtime_str": mtime_str,
                    "size_bytes": size,
                })

    backups.sort(key=lambda b: b["mtime"], reverse=True)
    return backups


def restore_backup(backup_path: str, target_save_path: str) -> bool:
    """
    Restaura o arquivo de backup selecionado sobre o save de destino.
    """
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Arquivo de backup não existe: {backup_path}")

    shutil.copy2(backup_path, target_save_path)
    return True
