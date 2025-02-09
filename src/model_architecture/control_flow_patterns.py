from enum import Enum # Importiert die Enum-Klasse zur Definition von Aufzählungstypen
from typing import List, Optional # Wird für die Typannotationen verwendet
from pydantic import BaseModel, Field # Importiert Pydantic für die Modellvalidierung

class PatternType(str, Enum):
    SEQUENCE = "Sequence"   # Einfacher sequentieller Ablauf
    PARALLEL_SPLIT = "Parallel Split"   # Parallele Verzweigung
    SYNCHRONIZATION = "Synchronization"     # Synchronisation mehrerer Abläufe
    EXCLUSIVE_CHOICE = "Exclusive Choice"   # Exklusive Entscheidung
    SIMPLE_MERGE = "Simple Merge"   # Zusammenführung ohne Synchronisation
    MULTI_CHOICE = "Multi-Choice"   # Mehrfachauswahl mit parallelen Pfaden
    STRUCTURED_SYNCHRONIZING_MERGE = "Structured Synchronizing Merge"   # Strukturierte Synchronisation
    MULTI_MERGE = "Multi-Merge"     # Mehrfachzusammenführung ohne Synchronisation
    STRUCTURED_DISCRIMINATOR = "Structured Discriminator"   # Strukturierte diskriminierende Entscheidung
    MILESTONE = "Milestone"     # Ein festgelegter Kontrollpunkt im Prozess
    CANCEL_TASK = "Cancel Task"     # Abbruch einer einzelnen Aufgabe
    CANCEL_CASE = "Cancel Case"     # Abbruch eines gesamten Falles
    CANCEL_REGION = "Cancel Region"     # Abbruch eines bestimmten Bereichs
    CANCEL_MULTIPLE_INSTANCE_ACTIVITY = "Cancel Multiple Instance Activity"     # Abbruch mehrerer Instanzen einer Aktivität
    COMPLETE_MULTIPLE_INSTANCE_ACTIVITY = "Complete Multiple Instance Activity"     # Abschließen mehrerer Instanzen einer Aktivität
    ARBITRARY_CYCLES = "Arbitrary Cycles"   # Beliebige zyklische Strukturen
    STRUCTURED_LOOP = "Structured Loop"     # Strukturierte Schleife mit festgelegten Regeln
    RECURSION = "Recursion"     # Rekursive Prozesse
    TRANSIENT_TRIGGER = "Transient Trigger"     # Kurzlebiger Auslöser
    PERSISTENT_TRIGGER = "Persistent Trigger"   # Dauerhafter Auslöser
    BLOCKING_DISCRIMINATOR = "Blocking Discriminator"   # Blockierende diskriminierende Entscheidung
    CANCELLING_DISCRIMINATOR = "Cancelling Discriminator"    # Abbrechende diskriminierende Entscheidung
    STRUCTURED_PARTIAL_JOIN = "Structured Partial Join"     # Strukturierte partielle Zusammenführung
    BLOCKING_PARTIAL_JOIN = "Blocking Partial Join"     # Blockierende partielle Zusammenführung
    CANCELLING_PARTIAL_JOIN = "Cancelling Partial Join"     # Abbrechende partielle Zusammenführung
    GENERALIZED_AND_JOIN = "Generalized AND-Join"   # Verallgemeinerte UND-Zusammenführung
    LOCAL_SYNCHRONIZING_MERGE = "Local Synchronizing Merge"     # Lokale synchronisierte Zusammenführung
    GENERAL_SYNCHRONIZING_MERGE = "General Synchronizing Merge"     # Allgemeine synchronisierte Zusammenführung
    THREAD_MERGE = "Thread Merge"   # Zusammenführung von Threads
    THREAD_SPLIT = "Thread Split"   # Aufteilung in mehrere Threads
    EXPLICIT_TERMINATION = "Explicit Termination"   # Explizites Beenden eines Prozesses
    IMPLICIT_TERMINATION = "Implicit Termination"   # Implizites Beenden eines Prozesses
    MULTIPLE_INSTANCES_WITHOUT_SYNCHRONIZATION = "Multiple Instances Without Synchronization"   # Mehrere Instanzen ohne Synchronisation
    MULTIPLE_INSTANCES_WITH_A_PRIORI_DESIGN_TIME_KNOWLEDGE = "Multiple Instances With a Priori Design-Time Knowledge"   # Instanzen mit vorab bekanntem Design-Wissen
    MULTIPLE_INSTANCES_WITH_A_PRIORI_RUN_TIME_KNOWLEDGE = "Multiple Instances With a Priori Run-Time Knowledge"     # Instanzen mit bekanntem Laufzeitwissen
    MULTIPLE_INSTANCES_WITHOUT_A_PRIORI_RUN_TIME_KNOWLEDGE = "Multiple Instances Without a Priori Run-Time Knowledge"   # Instanzen ohne vorheriges Laufzeitwissen
    STATIC_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Static Partial Join for Multiple Instances"   # Statische partielle Zusammenführung für mehrere Instanzen
    CANCELLING_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Cancelling Partial Join for Multiple Instances"   # Abbrechende partielle Zusammenführung für mehrere Instanzen
    DYNAMIC_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Dynamic Partial Join for Multiple Instances"     # Dynamische partielle Zusammenführung für mehrere Instanzen
    DEFERRED_CHOICE = "Deferred Choice"     # Verzögerte Wahl
    CRITICAL_SECTION = "Critical Section"   # Kritischer Abschnitt in einem Prozess
    INTERLEAVED_ROUTING = "Interleaved Routing"     # Verschachtelte Prozessabläufe
    INTERLEAVED_PARALLEL_ROUTING = "Interleaved Parallel Routing"   # Verschachtelte parallele Prozessausführung

# Definiert die Schwierigkeitsstufe eines Kontrollflussmusters
class Difficulty(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
# Modell zur Darstellung einzelner Erklärungsschritte bei der Mustererkennung
class Reasoning_Step(BaseModel):
    explanation: str = Field(..., description="The reasoning or explanation behind this step.")
    output: str = Field(..., description="The result or output generated at this step.")

# Modell zur Darstellung eines erkannten Kontrollflussmusters
class ControlFlowPattern(BaseModel):
    pattern: PatternType = Field(...,
        description="The identified Control flow pattern"    
        )
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence value between 0 and 1")
    reasoning_steps: list[Reasoning_Step] = Field(
        description="Reasoning steps leading to the identification of this specific pattern."
    )
    
# Modell zur Zusammenfassung aller erkannten Kontrollflussmuster in einer Geschäftsprozessbeschreibung    
class ControlFlowClassification(BaseModel):
    patterns: list[ControlFlowPattern] = Field(...,
        description="Control flow patterns that are present in the process description"
        )