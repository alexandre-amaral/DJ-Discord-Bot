# Discord Music Bot 🎶

Um bot de música para Discord que permite adicionar músicas à fila, pausar, retomar, pular e parar músicas com comandos simples. Este guia fornece instruções detalhadas para Windows, macOS e Linux.

## Recursos

- **Adicionar músicas à fila** com consultas no YouTube
- **Reproduzir, pausar, retomar, pular e parar músicas**
- **Mostrar a fila de reprodução**, incluindo a música tocando agora e as próximas
- **Comando para limpar a fila**

## Pré-requisitos

1. **Python 3.8 ou superior**
2. **Dependências do bot**: `discord.py`, `yt-dlp`, `ffmpeg`
3. **Conta no Discord** para criar um bot e obter um token

## Configuração Inicial

### 1. Criar o Bot no Discord

1. Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications).
2. Clique em **New Application** e dê um nome ao seu bot.
3. Vá até a seção **Bot** no menu lateral e clique em **Add Bot**.
4. Em **Token**, clique em **Reset Token** e copie o token do bot. **Guarde o token com segurança**.
5. Em **OAuth2 > URL Generator**, selecione `bot` e `applications.commands` em **Scopes**. Em **Bot Permissions**, escolha `Send Messages`, `Connect`, `Speak` e `Read Message History`.
6. Copie o URL gerado, cole no navegador e adicione o bot ao seu servidor do Discord.

### 2. Configuração do Ambiente

1. Clone o repositório do bot.
2. No diretório do projeto, crie um arquivo `.env` e adicione o token do bot:
`DISCORD_TOKEN=SEU_TOKEN_AQUI`

### 3. Instalar o FFmpeg

O FFmpeg é necessário para processar o áudio. Siga as instruções abaixo de acordo com o seu sistema operacional.

#### Windows

1. Baixe o FFmpeg [aqui](https://ffmpeg.org/download.html).
2. Extraia o arquivo baixado e copie o caminho até a pasta `bin` (ex: `C:\ffmpeg\bin`).
3. Abra o **Painel de Controle** → **Sistema e Segurança** → **Sistema** → **Configurações avançadas do sistema**.
4. Clique em **Variáveis de ambiente** e, em **Path**, adicione o caminho até a pasta `bin` do FFmpeg.
5. Abra um novo prompt de comando e execute `ffmpeg -version` para verificar a instalação.

#### macOS

1. Instale o Homebrew, se ainda não tiver:
/bin/bash -c “$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”
2. Use o Homebrew para instalar o FFmpeg:
```brew install ffmpeg````

#### Linux

1. Atualize o sistema e instale o FFmpeg:
```sudo apt update && sudo apt install ffmpeg````

## Instalação das Dependências

No terminal, navegue até o diretório do projeto e execute o seguinte comando para instalar as dependências do bot:
```pip install -r requirements.txt````

> **Nota**: Certifique-se de que o arquivo `requirements.txt` contém:
> ```
> discord.py
> yt-dlp
> python-dotenv
> ```

## Executando o Bot

1. No terminal, navegue até o diretório do projeto e execute o bot com o comando:

```python bot.py````

2. Se tudo estiver correto, o bot estará online e pronto para uso no seu servidor do Discord!

## Comandos do Bot

- **`#play [link ou consulta]`**: Adiciona uma música à fila para tocar.
- **`#pause`**: Pausa a música atual.
- **`#resume`**: Retoma a música pausada.
- **`#skip`**: Pula para a próxima música na fila.
- **`#stop`**: Para a música atual e limpa a fila.
- **`#queue`**: Mostra a música que está tocando e a fila de próximas músicas.
- **`#clear`**: Limpa todas as músicas da fila sem interromper a música atual.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

