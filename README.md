# Data Refinement - Analyse des emplois Data Science

## Description

Projet de refinement d'un dataset d'offres d'emploi Data Science collectées sur Glassdoor. Transformation de 672 enregistrements bruts en données exploitables pour analyses RH.

## Structure du Projet

```
Data_refine/
│
├── data/
│   └── Uncleaned_DS_jobs.csv          # Dataset brut original
│
├── refined_data/
│   └── glassdoor_jobs_refined.csv     # Dataset final nettoyé
│
├── exploration.py                     # Module 1: Exploration et diagnostic
├── cleaning.py                        # Module 2: Nettoyage des données  
├── transformation.py                  # Module 3: Transformations et validation
├── requirements.txt                   # Dépendances Python
├── LICENSE                           # Licence du projet
└── README.md                         # Documentation
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

Exécuter les modules dans l'ordre :

```bash
python exploration.py
python cleaning.py  
python transformation.py
```

Le dataset final sera généré dans `refined_data/glassdoor_jobs_refined.csv`.

## Résultats

- Dataset final : 493 enregistrements uniques
- 9 nouvelles variables créées
- Score qualité : 98,4%

## Auteur

**Jules** - DIA2 HETIC - Janvier 2026