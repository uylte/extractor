import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

"""
Dieses Skript verarbeitet und visualisiert die Evaluierungsergebnisse der LLM-Klassifikationen.

### Gruppierung der Ergebnisse:
1. Die JSON-Datei enthält die Klassifikationsergebnisse gruppiert nach Kontrollflussmuster (Pattern).
2. Innerhalb jedes Patterns sind die Ergebnisse weiter nach Modell und Prompting-Technik gruppiert.
3. Die Daten enthalten für jede Kombination aus Modell und Prompting:
   - Durchschnittliche Präzision (Precision)
   - Durchschnittlichen Recall
   - Durchschnittliche Latenzzeit (Latency)
4. Die Daten werden aus der JSON-Datei geladen, in ein Pandas DataFrame umgewandelt und nach 
   "Pattern", "Model" und "Prompting" gruppiert.
5. Die berechneten Metriken werden gespeichert und als Balkendiagramm für jedes Modell-Muster-Paar visualisiert.

"""

# Datei mit den evaluierten Metriken laden
file_path = "eval/eval_grouped_by_pattern_new_sysPrompt_all_traces.json"
with open(file_path, "r") as f:
    data = json.load(f)

# Umwandlung der JSON-Daten in ein Pandas DataFrame für einfache Analyse
records = []
for pattern, models in data.items():
    for model_prompt, metrics in models.items():
        model, prompting = model_prompt.split(" | ")

        # Erstellen einer Liste mit strukturierten Daten für die spätere Verarbeitung
        records.append({
            "Pattern": pattern,
            "Model": model,
            "Prompting": prompting,
            "Precision": metrics["average_precision"],
            "Recall": metrics["average_recall"],
            "Latency": metrics["average_latency"],
        })

# Konvertierung der Liste in ein Pandas DataFrame für weitere Analysen
df = pd.DataFrame(records)

# Durchschnittswerte pro Pattern, Modell und Prompting-Technik berechnen
df_avg = df.groupby(["Pattern", "Model", "Prompting"], as_index=False).mean()

# Speichern der berechneten Metriken als JSON für spätere Auswertung
df_avg.to_json("eval/eval_avg_metrics_per_pattern_new_sysPrompt_all_traces.json", orient="records", indent=4)

# Visualisierung der Ergebnisse: Precision und Recall für jede Prompting-Technik
for (pattern, model), group in df_avg.groupby(["Pattern", "Model"]):
    plt.figure(figsize=(12, 5))

    x_labels = group["Prompting"].tolist()
    x = np.arange(len(x_labels))
    
    precision = group["Precision"].values
    recall = group["Recall"].values

    width = 0.4  # Breite der Balken

    plt.bar(x - width/2, precision, width=width, color='blue', label='Precision')
    plt.bar(x + width/2, recall, width=width, color='orange', label='Recall')

    plt.xticks(ticks=x, labels=x_labels, rotation=45)
    plt.xlabel("Prompt Mode")
    plt.ylabel("Score")
    plt.ylim(0,1)
    plt.title(f"{model} - {pattern}: Precision and Recall by Prompting Technique")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()
