# Skill: check-cib

Apply the Real-Time Manipulation Detection Framework to identify coordinated inauthentic behaviour
(CIB) or AI-generated manipulation in the current report's source material.

## Input

All source material and claim set for the current report.

## Action

Apply every signal from Intelligence Stack Section IX-D.
For each signal, record status as 🟢 Not detected, 🟡 Monitor, or 🔴 Active, with a one-line note.

| Signal | Status | Notes |
| ------ | ------ | ----- |
| Narrative velocity | | |
| Account age + posting frequency | | |
| Cross-platform simultaneity | | |
| Emotional valence | | |
| Source laundering chain | | |
| Synthetic image artifacts | | |
| LLM-style prose | | |
| Missing bylines | | |
| Geopolitical timing | | |

## Output

The completed signal table followed by a one-paragraph summary of active CIB risk level.
