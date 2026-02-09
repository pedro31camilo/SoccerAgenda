# ⚽ Soccer Agenda

Um web scraper em Python que extrai automaticamente a agenda de times de futebol do site ESPN Brasil e exporta os dados em formato CSV, permitindo importar os compromissos em aplicativos de calendário.

## 📋 Funcionalidades

- **Extração automática de dados**: Coleta as agendas de todos os times presentes no ESPN Brasil
- **Múltiplas ligas**: Suporta scraping de diferentes ligas de futebol
- **Exportação em CSV**: Gera arquivos CSV para cada time, compatíveis com aplicativos de calendário
- **Processamento inteligente**: Extrai informações como:
  - Data do jogo
  - Times envolvidos
  - Horário de início e fim
  - Competição

## 🚀 Como Usar

### Pré-requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/pedro31camilo/SoccerAgenda.git
cd SoccerAgenda
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

### Executar o Script

```bash
python agendaScrape.py
```

O script irá:

1. Acessar o site ESPN Brasil
2. Extrair os dados das ligas e times
3. Coletar o calendário de cada time
4. Salvar os arquivos CSV na pasta `teamAgenda/`

### Importar no Calendário

Os arquivos CSV gerados podem ser importados em:

- **Google Calendar**: Import → Selecione o arquivo CSV
- **Outlook/Office 365**: Import → CSV File
- **Apple Calendar**: File → Import → CSV
- Qualquer outro aplicativo que suporte importação de CSV

## 📁 Estrutura de Saída

```
teamAgenda/
├── Team_Name_1.csv
├── Team_Name_2.csv
└── ...
```

Cada arquivo CSV contém as seguintes colunas:

- **Subject**: Nome do evento (Ex: "Team A vs Team B - Campeonato")
- **Start Date**: Data do jogo
- **End Date**: Data do jogo
- **Start Time**: Horário de início
- **End Time**: Horário de término (aproximadamente 2 horas após início)
- **All Day Event**: Indicador se é evento de dia inteiro

## 🛠️ Dependências

- [Playwright](https://playwright.dev/): Automação de navegador para web scraping
- [Rich](https://rich.readthedocs.io/): Formatação de output no terminal

## 📝 Exemplo de Saída

```csv
Subject,Start Date,End Date,Start Time,End Time,All Day Event
Flamengo vs Palmeiras - Campeonato Brasileiro,2026-02-15,2026-02-15,19:00,21:00,False
Santos vs Corinthians - Copa do Brasil,2026-02-20,2026-02-20,00:00,00:00,True
```

## ⚠️ Notas Importantes

- O script acessa o site ESPN Brasil em tempo real, então pode levar alguns minutos para executar
- Os compromisos com status "LIVE" são ignorados
- Para partidas sem horário definido, o horário é mantido como 00:00

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Aviso Legal**: Este projeto foi criado apenas para fins educacionais. Certifique-se de respeitar os termos de serviço do ESPN Brasil ao usar este scraper.
