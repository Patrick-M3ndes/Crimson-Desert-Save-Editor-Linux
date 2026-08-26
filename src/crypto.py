from __future__ import annotations
import os
import struct
import hmac
import hashlib
from dataclasses import dataclass
from typing import Optional

import lz4.block
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

_SAVE_BASE_KEY: bytes = bytes.fromhex(
    "C41B8E730DF259A637CC04E9B12F9668DA107A853E61F9224DB80AD75C13EF90"
)[:31]

_VERSION_PREFIXES: dict[int, bytes] = {
    1: b"^Qgbrm/.#@`zsr]\\@rvfal#\"",
    2: b"^Pearl--#Abyss__@!!",
}

HEADER_SIZE: int = 128
MAGIC_OFFSET: int = 0
VERSION_OFFSET: int = 4
FLAGS_OFFSET: int = 6
UNCOMP_SIZE_OFFSET: int = 18
PAYLOAD_SIZE_OFFSET: int = 22
NONCE_OFFSET: int = 26
HMAC_OFFSET: int = 42
PAYLOAD_OFFSET: int = 128


@dataclass
class SaveFile:
    """Representa um arquivo de save carregado e descriptografado."""
    file_path: str
    version: int
    flags: int
    raw_header: bytearray
    blob: bytearray
    hmac_valid: bool


def generate_save_key(version: int) -> bytes:
    """Gera a chave ChaCha20/HMAC baseada na versão do formato do save."""
    prefix = _VERSION_PREFIXES.get(version)
    if prefix is None:
        raise ValueError(f"Versão de save não suportada: {version}")
    material = prefix + b"PRIVATE_HMAC_SECRET_CHECK"
    key_material = bytes(x ^ y for x, y in zip(_SAVE_BASE_KEY, material))
    return key_material + b"\x00"


def chacha20_crypt(data: bytes, nonce16: bytes, key: bytes) -> bytes:
    """Criptografa / Descriptografa dados usando ChaCha20."""
    cipher = Cipher(algorithms.ChaCha20(key, nonce16), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


def load_save_file(file_path: str) -> SaveFile:
    """
    Abre o arquivo save.save, valida o cabeçalho, descriptografa
    e descompacta o conteúdo com LZ4.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    with open(file_path, "rb") as f:
        file_data = f.read()

    if len(file_data) < HEADER_SIZE:
        raise ValueError(f"Arquivo corrompido ou menor que o cabeçalho ({len(file_data)} bytes)")

    magic = file_data[MAGIC_OFFSET:MAGIC_OFFSET + 4]
    if magic != b"SAVE":
        raise ValueError(f"Assinatura mágica inválida: {magic!r} (esperado b'SAVE')")

    version = struct.unpack_from("<H", file_data, VERSION_OFFSET)[0]
    flags = struct.unpack_from("<H", file_data, FLAGS_OFFSET)[0]
    uncomp_size = struct.unpack_from("<I", file_data, UNCOMP_SIZE_OFFSET)[0]
    payload_size = struct.unpack_from("<I", file_data, PAYLOAD_SIZE_OFFSET)[0]

    nonce = file_data[NONCE_OFFSET:NONCE_OFFSET + 16]
    stored_hmac = file_data[HMAC_OFFSET:HMAC_OFFSET + 32]

    if PAYLOAD_OFFSET + payload_size > len(file_data):
        raise ValueError("Tamanho do payload informado no cabeçalho excede o tamanho do arquivo.")

    ciphertext = file_data[PAYLOAD_OFFSET:PAYLOAD_OFFSET + payload_size]

    key = generate_save_key(version)
    compressed = chacha20_crypt(ciphertext, nonce, key)

    calculated_hmac = hmac.new(key, compressed, hashlib.sha256).digest()
    hmac_valid = hmac.compare_digest(stored_hmac, calculated_hmac)

    decompressed = lz4.block.decompress(compressed, uncompressed_size=uncomp_size)

    return SaveFile(
        file_path=file_path,
        version=version,
        flags=flags,
        raw_header=bytearray(file_data[:HEADER_SIZE]),
        blob=bytearray(decompressed),
        hmac_valid=hmac_valid,
    )


def save_save_file(
    file_path: str,
    blob: bytearray | bytes,
    original_header: Optional[bytes | bytearray] = None,
    version: int = 2,
) -> None:
    """
    Recompacta o blob em LZ4, calcula novo HMAC, criptografa com ChaCha20
    e salva o arquivo de volta no disco.
    """
    if original_header is not None and len(original_header) >= 6:
        version = struct.unpack_from("<H", original_header, VERSION_OFFSET)[0]

    key = generate_save_key(version)

    # Compressão LZ4 idêntica ao jogo original
    compressed = lz4.block.compress(
        bytes(blob),
        store_size=False,
        mode="high_compression",
        compression=9,
    )

    nonce = os.urandom(16)
    hmac_digest = hmac.new(key, compressed, hashlib.sha256).digest()
    encrypted = chacha20_crypt(compressed, nonce, key)

    header = bytearray(HEADER_SIZE)
    if original_header is not None and len(original_header) >= 18:
        header[:18] = original_header[:18]

    header[0:4] = b"SAVE"
    struct.pack_into("<H", header, VERSION_OFFSET, version)
    struct.pack_into("<H", header, FLAGS_OFFSET, 128)
    struct.pack_into("<I", header, UNCOMP_SIZE_OFFSET, len(blob))
    struct.pack_into("<I", header, PAYLOAD_SIZE_OFFSET, len(compressed))
    header[NONCE_OFFSET:NONCE_OFFSET + 16] = nonce
    header[HMAC_OFFSET:HMAC_OFFSET + 32] = hmac_digest

    with open(file_path, "wb") as f:
        f.write(header)
        f.write(encrypted)
