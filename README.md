# Extractor: Identifikation von Kontrollflussmustern

## Überblick

Der Extractor ist ein System zur automatisierten Identifikation von Kontrollflussmustern in textuellen Geschäftsprozessbeschreibungen. Dabei werden Large Language Models (LLMs) genutzt, um Prozessbeschreibungen zu analysieren und enthaltene Kontrollflussmuster zu extrahieren. Das System unterstützt verschiedene Prompting-Techniken (Zero-Shot, Few-Shot, Chain-of-Thought) und generiert strukturierte Ausgaben zur weiteren Verarbeitung.

## Funktionsweise

Das System arbeitet mit einer modularen Architektur und besteht aus den folgenden Hauptkomponenten:

- **PromptLoader**: Lädt und konfiguriert Prompts für die LLM-Anfragen aus einer YAML-Datei.
- **LLMClient**: Schnittstelle zur Kommunikation mit OpenAI- oder Groq-Modellen.
- **ExtractionPipeline**: Koordiniert den Extraktionsprozess von Kontrollflussmustern.
- **Datenverwaltung**: JSON-Dateien enthalten Definitionen und Beispielinstanzen der Muster.
- **Evaluationsmodule**: Berechnen Metriken wie Präzision und Recall zur Bewertung der Extraktionsergebnisse.

## Installation

### Voraussetzungen

- Python 3.8+
- Virtuelle Umgebung (empfohlen)
- Abhängigkeiten aus `requirements.txt`

### Einrichtung

1. **Repository klonen**
   ```bash
   git clone <repository-url>
   cd extractor
   ```
2. **Virtuelle Umgebung erstellen und aktivieren**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```
4. **API-Keys einrichten** (z. B. OpenAI/Groq)
   - `.env`-Datei erstellen mit folgendem Inhalt:
     ```ini
     OPENAI_API_KEY=your_openai_key
     GROQ_API_KEY=your_groq_key
     ```

## Nutzung

### 1. Extraktion von Kontrollflussmustern

Der Hauptprozess zur Musterextraktion kann über `main.py` gestartet werden:

```bash
python main.py
```

Dabei werden die in `patterns.json` definierten Muster mit verschiedenen Prompting-Techniken klassifiziert.

### 2. Evaluierung der Ergebnisse

Zur Berechnung von Präzision und Recall:

```bash
python eval_data.py
```

Die aggregierten Ergebnisse werden in `eval/results/` gespeichert.

### 3. Visualisierung

Ergebnisse können mit `detailed_resolution.py` visualisiert werden:

```bash
python detailed_resolution.py
```

Es werden Diagramme zu den verschiedenen LLMs und Prompt-Modi erstellt.

## Verzeichnisstruktur

```
extractor/
│── src/
│   ├── data/
│   │   ├── patterns.json  # Definierte Kontrollflussmuster
│   │   ├── prompts_config.yaml  # Prompt-Vorlagen
│   ├── model_architecture/
│   │   ├── llm_client.py  # Schnittstelle zu LLMs
│   │   ├── control_flow_patterns.py  # Datenstruktur für Klassifikationen
│   ├── pipeline/
│   │   ├── extraction_pipeline.py  # Workflow-Koordination
│── eval/
│   ├── raw_data/
│   ├── eval_data.py  # Evaluierungsskript
│   ├── detailed_resolution.py  # Visualisierungsskript
│── main.py  # Einstiegspunkt des Programms
│── requirements.txt  # Abhängigkeiten
```

## Anpassungen

- **Modellparameter** können in `models_config.yaml` geändert werden (z. B. Temperatur, Token-Limit).
- **Prompt-Templates** befinden sich in `prompts_config.yaml`.