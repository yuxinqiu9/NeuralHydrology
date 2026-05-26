# Seminar_neuralhydrology

**SoSe 2026 — Interdisciplinary Seminar: Climate Change Statistics: Applications and Methods**  
**Topic #6: Neural Hydrology (Python Library)** · Master · Supervisor: Henri Funk  
**Discussion Leader for:** Hydrology under Climate Change

---

## What This Repository Is

This is the personal seminar folder following the format of
[Seminar_ClimateNStatistics2425](https://github.com/henrifnk/Seminar_ClimateNStatistics2425).

All files in this folder are new; **no existing files in the parent repository were modified**.

---

## Folder Structure

```
Seminar_neuralhydrology/
│
├── README.md                          ← This file
├── _bookdown.yml                      ← BookDown GitBook config
├── _output.yml                        ← Output format config
├── index.Rmd                          ← GitBook preface
│
├── 06-NeuralHydrology.Rmd             ← Main chapter (~2500 words)
├── book.bib                           ← BibTeX bibliography (14 entries)
│
├── presentation.qmd                   ← Quarto revealjs slides (24 slides, 30 min)
├── presentation_script.md             ← Full spoken script (~3500 words)
│
└── work/
    └── 06-NeuralHydrology/
        ├── code/
        │   ├── showcase.py            ← Python demo (NeuralHydrology library)
        │   ├── 1_basin_demo.yml       ← EA-LSTM config for basin 01013500
        │   └── 1_basin.txt            ← Basin ID list
        ├── data/
        │   └── README.md              ← CAMELS-US download instructions
        ├── figures/
        │   └── README.md              ← Figure generation instructions
        └── results/
            └── README.md              ← Results loading (R + Python)
```

---

## Topic Requirements

From the S26 course PDF:

> **Neural Hydrology (Python Library)**  
> – Overview of current methods and model architectures to model streamflow  
> – Possible extensions towards physically consistent model architectures  
> – How to do transfer learning in a changing climate?

---

## Key Files

| File | Purpose | Target length |
|------|---------|---------------|
| `06-NeuralHydrology.Rmd` | GitBook chapter submitted to Seminar repo | 1000–3000 words |
| `presentation.qmd` | Slides submitted 24h before presentation | 30 minutes |
| `presentation_script.md` | Spoken text for each slide | ~3500 words |
| `book.bib` | Shared bibliography | 14 entries |

---

## Schedule

| Event | Date |
|-------|------|
| Kick Off | 15.04.2026 |
| Interim Meeting | 09.06.2026 |
| **Final Presentation** | **14.–15.07.2026** |
| Report Deadline | 11.08.2026 |

---

## R + Python Integration

The seminar requires R/RMarkdown. NeuralHydrology runs in Python.
Recommended workflow:

1. **Train model** in Python: `python code/showcase.py`
2. **Pass results to R** via `reticulate` or CSV export
3. **Visualise and analyse** in R with `ggplot2`

Quarto (`.qmd`) natively supports both `{r}` and `{python}` code chunks in the
same document — no extra configuration needed.

---

## GitBook Submission Instructions (from S26 slides)

1. Clone the teacher's repo: `git clone https://github.com/henrifnk/Seminar_ClimateNStatistics2425.git`
2. Create your own branch
3. Copy `06-NeuralHydrology.Rmd`, `book.bib`, and `work/06-NeuralHydrology/` into the repo
4. Commit and push to your branch
5. Open a pull request, assign Henri as reviewer
6. Do NOT merge — wait for review
