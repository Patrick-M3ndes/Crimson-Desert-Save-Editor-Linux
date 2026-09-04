# ⚔️ Crimson Desert - Item & Currency Save Editor (Linux & Windows)

[🇧🇷 Versão em Português](README.md) | [🇺🇸 English Version](README_EN.md)

Editor de save leve, rápido e de alta precisão desenvolvido em Python para o jogo **Crimson Desert** no **Linux e Windows**.

> 🟢 **Status**: Testado e **funcionando perfeitamente** na versão **2.01.00** do jogo!

---

## ⚡ Como Abrir e Executar o Editor (Modo Rápido / 1 Clique)

Para facilitar ao máximo a execução sem precisar digitar comandos no terminal:

### 🐧 No Linux:
- Abra o terminal na pasta do projeto e execute:
  ```bash
  ./run.sh
  ```
  *(Ou dê 2 cliques no arquivo `run.sh` no seu gerenciador de arquivos e selecione "Executar no Terminal").*

### 🪟 No Windows:
- Dê **2 cliques** no arquivo **`run.bat`** dentro da pasta do projeto. Ele fará tudo automaticamente e abrirá a tela do editor!

---

## 💻 Guia Completo por Terminal (Linux & Windows)

Se preferir rodar manualmente digitando os comandos no seu terminal favorito:

### 🐧 Linux (Variações de Terminal & Shell)

#### 1. Bash / Zsh (Ubuntu, Debian, Fedora, Arch Linux, Pop!_OS, etc.)
```bash
# Entrar na pasta do projeto
cd Crimson-Desert-Save-Editor-Linux-Windows

# Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências e executar
pip install -r requirements.txt
python3 main.py
```

#### 2. Fish Shell
```fish
# Criar e ativar o ambiente virtual no Fish
python3 -m venv .venv
source .venv/bin/activate.fish

# Instalar dependências e executar
pip install -r requirements.txt
python3 main.py
```

---

### 🪟 Windows (Variações de Terminal)

#### 1. PowerShell
```powershell
# Entrar na pasta do projeto
cd Crimson-Desert-Save-Editor-Linux-Windows

# Criar e ativar o ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Instalar dependências e executar
pip install -r requirements.txt
python main.py
```
> 💡 *Dica*: Se o PowerShell exibir erro de execução de scripts, rode antes o comando: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

#### 2. Prompt de Comando (`cmd.exe`)
```cmd
# Entrar na pasta do projeto
cd Crimson-Desert-Save-Editor-Linux-Windows

# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate.bat

# Instalar dependências e executar
pip install -r requirements.txt
python main.py
```

#### 3. Git Bash no Windows
```bash
# Criar e ativar o ambiente virtual no Git Bash
python -m venv .venv
source .venv/Scripts/activate

# Instalar dependências e executar
pip install -r requirements.txt
python main.py
```

---

## 🎮 Como Usar o Menu Interativo Passo a Passo

Assim que você executar o script (`python main.py` ou via `run.sh` / `run.bat`), o menu interativo abrirá no seu terminal:

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

### Guia Simples de Uso:

1. **Digite `1` e aperte Enter**: O programa buscará automaticamente todos os saves no seu computador (Windows ou Linux) e mostrará os slots com data e hora. Selecione o número do slot que você deseja editar.
2. **Digite `2` e aperte Enter**: Altere o valor de ouro/moedas do seu personagem e recursos do acampamento.
3. **Digite `3` ou `4` e aperte Enter**: Navegue pelo seu inventário, escolha o item pelo número e altere sua quantidade (stack), nível de encantamento (`+0` a `+20`) ou troque-o por qualquer outro item do jogo.
4. **Digite `6` e aperte Enter**: Salva todas as alterações no arquivo com segurança, recalculando o HMAC e removendo conflitos da nuvem.
5. **Abra o Crimson Desert**: Carregue seu save editado no jogo e faça um novo salvamento in-game para que a Steam sincronize com a nuvem automaticamente.

---

## ✨ Funcionalidades Principais

- **Detecta Automaticamente os Saves (Multiplataforma)**: Identifica os arquivos de save localizados no diretório padrão do **Linux** (`~/.local/share/Steam/...`) e do **Windows** (`%LOCALAPPDATA%\Pearl Abyss\CD\save`).
- **Identificação de Slots com Data e Horário**: Exibe a data e hora exatas da última modificação de cada slot (ex: `26/08/2026 às 14:59:02`).
- **💰 Edição de Moedas & Recursos do Acampamento**: Altere o saldo de moedas do jogador (`Copper`) e todos os fundos/recursos do acampamento (`Camp Funds`, `Food`, `Timber`, `Stone`, `Weapons`).
- **Banco de Dados Global com +6.200 Itens**: Tabela catalogada com mais de 6.200 itens para substituição e pesquisa.
- **Navegador e Pesquisa de Inventário**: Paginação interativa para navegar pelo inventário do seu personagem ou pesquisar itens específicos por nome.
- **Edição de Quantidade (Stack Count)**: Altere o tamanho da pilha de qualquer item consumível ou material.
- **Encantamento e Durabilidade**: Modifique nível de encanto (arma/armadura de `+0` a `+20`), durabilidade e nitidez.
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

## 📄 Licença

Este projeto é disponibilizado sob a Licença MIT para fins educacionais e de entretenimento.
