# -*- coding: utf-8 -*-
"""01_exploration.ipynb

# Data Refinement - Exploration des données

**Dataset :** Offres d'emploi Data Science sur Glassdoor  

Ce dataset contient 672 offres d'emploi Data Science collectées sur Glassdoor. L'objectif est de transformer ces données brutes en format exploitable pour des analyses RH fiables sur le marché de l'emploi tech américain.

**Variables cibles pour l'analyse :**
- Rémunérations par niveau de séniorité
- Répartition géographique des opportunités  
- Corrélation taille d'entreprise/salaires
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
warnings.filterwarnings('ignore')

plt.style.use('default')
sns.set_palette("husl")

# Chargement des données
df = pd.read_csv('data/Uncleaned_DS_jobs.csv')

print(f"Structure: {df.shape[0]} observations, {df.shape[1]} variables")

# Découverte des données
print(df.head())
print(df.info())

company_rating_mixed = df['Company Name'].str.contains('\n', na=False).sum()
missing_analysis = df.isnull().sum()
competitors_minus1 = (df['Competitors'] == '-1').sum()
unknown_revenue = df['Revenue'].str.contains('Unknown', na=False).sum()
business_dupes = df.duplicated(subset=['Job Title', 'Company Name', 'Location']).sum()

plt.figure(figsize=(12, 4))

# Distribution des ratings
plt.subplot(1, 3, 1)
df['Rating'].hist(bins=20, alpha=0.7, color='skyblue')
plt.title('Distribution des Ratings')
plt.xlabel('Rating (1-5)')

# Top 10 des états
plt.subplot(1, 3, 2)
location_states = df['Location'].str.extract(r', ([A-Z]{2})$')[0]
top_states = location_states.value_counts().head(10)
top_states.plot(kind='bar', color='coral')
plt.title('Répartition Géographique')
plt.xticks(rotation=45)

# Problèmes qualité détectés
plt.subplot(1, 3, 3)
problems = ['Company\n+Rating', 'Doublons\nmétier', 'Valeurs\n-1', 'Revenue\nUnknown']
counts = [company_rating_mixed, business_dupes, competitors_minus1, unknown_revenue]
plt.bar(problems, counts, color=['red', 'orange', 'yellow', 'pink'])
plt.title('Problèmes Qualité')

plt.tight_layout()
plt.show()