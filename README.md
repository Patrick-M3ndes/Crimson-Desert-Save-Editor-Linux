# ⚔️ Crimson Desert - Item & Currency Save Editor (Enhanced Edition)

Save editor leve, rápido e funcional feito em Python para o jogo **Crimson Desert** (compatível com a atualização Enhanced / versão 2.00.00).

---

## ✨ Funcionalidades

- **Identificação de Slots com Data e Horário**: Exibe a data e hora exatas de cada slot de save (ex: `26/08/2026 às 14:59:02`) para você saber exatamente qual é o seu save de teste e qual é o de backup.
- **💰 Atalho Rápido de Dinheiro & Acampamento**: Altere diretamente suas moedas (`Copper` / Moedas do jogador) e todos os fundos do acampamento (`Camp Funds`, `Food`, `Timber`, `Stone`, `Weapons`).
- **Banco de Dados Global Completo**: Contém mais de **6.200 itens** catalogados (`item_names.json`).
- **Navegador Interativo de Inventário**: Lista todo o inventário do save carregado com paginação e permite selecionar qualquer item diretamente pelo número para editar.
- **Edição de Quantidade (Stack Count)**: Altera a quantidade de qualquer item, consumível ou material (ex: `Abyss Artifact`).
- **Definição de Nível de Encantamento**: Permite definir o nível de encanto de armas e armaduras (ex: `+0` até `+20`).
- **Substituição / Troca de Itens**: Permite transformar qualquer item do seu inventário em outro item buscando pelo nome ou ID no banco de dados de 6.200+ itens.
- **Proteção Anti-Crash (`steam_autocloud.vdf`)**: Ao salvar, o editor remove automaticamente o arquivo `steam_autocloud.vdf` para impedir que o jogo feche inesperadamente antes do menu inicial.
- **Backup Automático**: Cria cópias de segurança com carimbo de data/hora (`save.save.YYYYMMDD_HHMMSS.bak`) antes de gravar qualquer modificação.

---

## 🚀 Como Usar no VS Code

1. Abra a pasta `CD_Save_Editor` no seu VS Code (`/home/patrik/Projects/CD_Save_Editor`).
2. Pressione **`F5`** (ou vá em *Executar e Depurar* e clique em **Executar CD Save Editor**).
3. O menu interativo abrirá no terminal integrado:
   - **`1`**: Escolher Slot de Save (exibe todos os slots com suas datas e horários).
   - **`2`**: 💰 Alterar Dinheiro & Recursos do Acampamento.
   - **`3`**: Ver Inventário Completo (navegue pelas páginas e digite o número do item para editar).
   - **`4`**: Buscar Item no Inventário Atual (ex: `Abyss Artifact`).
   - **`5`**: Pesquisar Itens no Banco Global (para consultar nomes e IDs).
   - **`6`**: Salvar alterações (gera backup `.bak`, recalcula HMAC e limpa `steam_autocloud.vdf`).

---

## 💻 Como Rodar via Terminal

```bash
cd /home/patrik/Projects/CD_Save_Editor
source .venv/bin/activate
python main.py
```
