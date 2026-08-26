from __future__ import annotations
import os
import shutil
from datetime import datetime


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
