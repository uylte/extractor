from enum import Enum
from typing import List

from pydantic import BaseModel, Field

class PatternType(str, Enum):
    SEQUENCE = "Sequence"
    PARALLEL_SPLIT = "Parallel Split"
    SYNCHRONIZATION = "Synchronization"
    EXCLUSIVE_CHOICE = "Exclusive Choice"
    SIMPLE_MERGE = "Simple Merge"
    MULTI_CHOICE = "Multi-Choice"
    STRUCTURED_SYNCHRONIZING_MERGE = "Structured Synchronizing Merge"
    MULTI_MERGE = "Multi-Merge"
    STRUCTURED_DISCRIMINATOR = "Structured Discriminator"
    MILESTONE = "Milestone"
    CANCEL_TASK = "Cancel Task"
    CANCEL_CASE = "Cancel Case"
    CANCEL_REGION = "Cancel Region"
    CANCEL_MULTIPLE_INSTANCE_ACTIVITY = "Cancel Multiple Instance Activity"
    COMPLETE_MULTIPLE_INSTANCE_ACTIVITY = "Complete Multiple Instance Activity"
    ARBITRARY_CYCLES = "Arbitrary Cycles"
    STRUCTURED_LOOP = "Structured Loop"
    RECURSION = "Recursion"
    TRANSIENT_TRIGGER = "Transient Trigger"
    PERSISTENT_TRIGGER = "Persistent Trigger"
    BLOCKING_DISCRIMINATOR = "Blocking Discriminator"
    CANCELLING_DISCRIMINATOR = "Cancelling Discriminator"
    STRUCTURED_PARTIAL_JOIN = "Structured Partial Join"
    BLOCKING_PARTIAL_JOIN = "Blocking Partial Join"
    CANCELLING_PARTIAL_JOIN = "Cancelling Partial Join"
    GENERALIZED_AND_JOIN = "Generalized AND-Join"
    LOCAL_SYNCHRONIZING_MERGE = "Local Synchronizing Merge"
    GENERAL_SYNCHRONIZING_MERGE = "General Synchronizing Merge"
    THREAD_MERGE = "Thread Merge"
    THREAD_SPLIT = "Thread Split"
    EXPLICIT_TERMINATION = "Explicit Termination"
    IMPLICIT_TERMINATION = "Implicit Termination"
    MULTIPLE_INSTANCES_WITHOUT_SYNCHRONIZATION = "Multiple Instances Without Synchronization"
    MULTIPLE_INSTANCES_WITH_A_PRIORI_DESIGN_TIME_KNOWLEDGE = "Multiple Instances With a Priori Design-Time Knowledge"
    MULTIPLE_INSTANCES_WITH_A_PRIORI_RUN_TIME_KNOWLEDGE = "Multiple Instances With a Priori Run-Time Knowledge"
    MULTIPLE_INSTANCES_WITHOUT_A_PRIORI_RUN_TIME_KNOWLEDGE = "Multiple Instances Without a Priori Run-Time Knowledge"
    STATIC_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Static Partial Join for Multiple Instances"
    CANCELLING_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Cancelling Partial Join for Multiple Instances"
    DYNAMIC_PARTIAL_JOIN_FOR_MULTIPLE_INSTANCES = "Dynamic Partial Join for Multiple Instances"
    DEFERRED_CHOICE = "Deferred Choice"
    CRITICAL_SECTION = "Critical Section"
    INTERLEAVED_ROUTING = "Interleaved Routing"
    INTERLEAVED_PARALLEL_ROUTING = "Interleaved Parallel Routing"

class Difficulty(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    
"""
def describe_pattern(pattern):
    for item in data['patterns']:
        if item['name'] == pattern.value:
            return item['description']
    return "Description not found."
"""

class ControlFlowPattern(BaseModel):
    pattern: PatternType = Field(...,
        description="The identified Control flow pattern"    
        ) # Typ des Musters
    difficulty: Difficulty = Field(
        description="Difficulty of recognising the pattern"
        )
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence value between 0 and 1")
"""
    position: List[int] = Field(
        description="List of start and end index between the first and the last Action of the pattern in the process description",
        min_items=2, max_items=2)  # Genau 2 Elemente
    actions: List[str] = Field(
        description="All actions involved in the control flow pattern"
    )
"""    
"""
    relations: str = Field(
        description="Symbolic representations of the relationships between the actions in the pattern",
    )
"""
class ControlFlowClassification(BaseModel):
    patterns: List[ControlFlowPattern] = Field(...,
        description="Control flow patterns that are present in the process description"
        )