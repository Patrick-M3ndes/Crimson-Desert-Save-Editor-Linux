# ⚔️ Crimson Desert - Item & Currency Save Editor (Terminal Linux)

Editor de save leve, rápido e de alta precisão desenvolvido em Python para o jogo **Crimson Desert** no **Linux**.

> 🟢 **Status**: Testado e **funcionando perfeitamente** na versão **2.01.00** do jogo!

---

## 📌 Visão Geral

Esta ferramenta foi desenvolvida para rodar diretamente via **terminal no Linux**, permitindo visualizar, alterar recursos, modificar quantidades de itens, trocar itens por qualquer outro do banco de dados e gerenciar backups dos seus saves do Crimson Desert de forma simples, rápida e segura (totalmente compatível com a versão **2.01.00**).

---

## ✨ Funcionalidades Principais

- **Detecta Automaticamente os Saves no Linux**: Identifica os arquivos de save localizados no diretório padrão do Steam/Proton (`~/.local/share/Steam/...`).
- **Identificação de Slots com Data e Horário**: Exibe a data e hora exatas da última modificação de cada slot (ex: `26/08/2026 às 14:59:02`).
- **💰 Edição de Moedas & Recursos do Acampamento**: Altere o saldo de moedas do jogador (`Copper`) e todos os fundos/recursos do acampamento (`Camp Funds`, `Food`, `Timber`, `Stone`, `Weapons`).
- **Banco de Dados Global com +6.200 Itens**: Tabela catalogada com mais de 6.200 itens para substituição e pesquisa.
- **Navegador e Pesquisa de Inventário**: Paginação interativa para navegar pelo inventário do seu personagem ou pesquisar itens específicos por nome.
- **Edição de Quantidade (Stack Count)**: Altere o tamanho da pilha de qualquer item consumível ou material.
- **Encantamento e Durabilidade**: Modifique nível de encanto (arma/armadura), durabilidade e nitidez.
- **Substituição / Troca de Itens**: Transforme qualquer item existente no seu inventário em qualquer outro item do jogo buscando por nome ou ID.
- **Proteção Anti-Corrupção (HMAC Recalculado)**: Recalcula automaticamente a assinatura de integridade do arquivo para que o jogo não aponte o save como corrompido.
- **Proteção Anti-Crash / Conflito Steam Cloud (`steam_autocloud.vdf`)**: Remove automaticamente os metadados antigos para evitar que o Steam Cloud sobrescreva suas edições ou trave o jogo no menu inicial.
- **Backup Automático com Restauração**: Cria cópias de segurança carimbadas (`.bak`) antes de gravar alterações e permite restaurar backups anteriores diretamente pelo menu.

---

## 🛡️ Mecanismos de Proteção e Sincronização com a Steam

### 1. Prevenção Contra Corrupção de Saves
O Crimson Desert valida os arquivos de save utilizando uma assinatura de integridade (HMAC/Checksum). Se o arquivo for editado sem recalcular essa chave, o jogo recusará o carregamento e indicará que o save está corrompido. Nosso editor **recalcula e re-assina a chave HMAC automaticamente** durante o salvamento, garantindo que o jogo reconheça o save como 100% legítimo.

### 2. Prevenção de Conflitos do Steam Cloud (Anti-Crash)
Ao salvar as modificações no editor, o arquivo de cache da nuvem local (`steam_autocloud.vdf`) é removido de forma automatizada. Isso previne que a Steam detecte uma dessincronização antes da execução e acabe sobrescrevendo seus dados editados ou fechando o jogo inesperadamente na tela de início.

### 3. Sincronização Automática com a Nuvem Steam
Após realizar qualquer alteração nos seus itens ou moedas através do editor:
1. Abra o jogo normalmente e carregue o seu save editado.
2. Assim que o jogo carregar com os itens novos, faça um **novo salvamento (manual ou rápido)** dentro do próprio Crimson Desert.
3. Ao salvar no jogo, a Steam gerará um novo arquivo `steam_autocloud.vdf` válido e **sincronizará suas alterações automaticamente com a nuvem Steam** de forma transparente.

---

## 🛠️ Requisitos do Sistema

- **Sistema Operacional**: Linux (Ubuntu, Debian, Fedora, Arch Linux, Pop!_OS, etc.)
- **Python**: Versão 3.8 ou superior (`python3 --version`)
- **Git**: (Opcional, para clonar o repositório)

---

## 🚀 Como Instalar e Rodar no Terminal (Linux)

Siga o passo a passo abaixo no seu terminal Linux:

### 1. Clonar ou Baixar o Repositório
```bash
git clone https://github.com/Patrick-M3ndes/CD_Save_Editor.git
cd CD_Save_Editor
```
*(Caso já tenha o repositório em sua máquina, basta abrir o terminal na pasta raiz do projeto).*

### 2. Criar e Ativar o Ambiente Virtual (Venv)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o Save Editor
```bash
python main.py
```

> 💡 **Nota**: Sempre que abrir uma nova janela de terminal para rodar o script, lembre-se de ativar o ambiente virtual executando `source .venv/bin/activate`.

---

## 🎮 Como Usar o Menu Interativo

Ao executar o `python main.py`, o editor exibirá um menu numérico no terminal:

```txt
==================================================
  CRIMSON DESERT - SAVE EDITOR (v2.01.00)
==================================================
 1. Escolher Slot de Save
 2. 💰 Alterar Dinheiro & Recursos do Acampamento
 3. Ver Inventário Completo
 4. Buscar Item no Inventário Atual
 5. Pesquisar Itens no Banco Global
 6. Salvar Alterações
 7. Restaurar Backup
 0. Sair
==================================================
```

### Passo a Passo Recomendado:

1. **Selecione o Slot (Opção `1`)**: Escolha qual slot de save deseja carregar (o editor mostra a data e hora exatas de modificação do save).
2. **Edite seus Dados**:
   - **Opção `2`**: Altere moedas do jogador e fundos do acampamento.
   - **Opção `3` ou `4`**: Navegue pelo inventário, selecione um item pelo número e altere sua quantidade, nível de encantamento ou troque-o por outro item do jogo.
3. **Salve as Alterações (Opção `6`)**: O script reciclará o HMAC, gerará um backup `.bak` automático e atualizará o arquivo com segurança.
4. **Abra o Jogo e Salve**: Abra o Crimson Desert, verifique suas alterações e faça um save pelo próprio menu do jogo para sincronizar com a nuvem Steam.

---

## 🛡️ Segurança e Backups

O editor gera um arquivo de segurança com carimbo de data/hora (`save.save.YYYYMMDD_HHMMSS.bak`) na pasta do save antes de aplicar qualquer alteração. Caso deseje desfazer modificações, basta utilizar a **Opção 7 (Restaurar Backup)** diretamente no menu do terminal.

---

## 📄 Licença

Este projeto é disponibilizado para fins educacionais e de entretenimento.
