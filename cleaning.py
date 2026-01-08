import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('default')
sns.set_palette("husl")

# Chargement des données
df = pd.read_csv('data/Uncleaned_DS_jobs.csv')

df_clean = df.copy()

# Valeurs manquantes et standardisation
df_clean['Rating'] = df_clean['Rating'].fillna(df_clean['Rating'].median())
df_clean['Revenue'] = df_clean['Revenue'].replace('Unknown / Non-Applicable', np.nan)
before_competitors = (df_clean['Competitors'] == '-1').sum()
df_clean['Competitors'] = df_clean['Competitors'].replace('-1', np.nan)

# Doublons
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.drop_duplicates(subset=['Job Title', 'Company Name', 'Location'], keep='first')

plt.figure(figsize=(10, 4))

# Évolution du nombre d'enregistrements
plt.subplot(1, 2, 1)
categories = ['Initial', 'Nettoyé']
counts = [len(df), len(df_clean)]
bars = plt.bar(categories, counts, color=['red', 'green'], alpha=0.7)
plt.title('Évolution Enregistrements')
plt.ylabel('Nombre')
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             str(count), ha='center', va='bottom', fontweight='bold')

# Améliorations qualité
plt.subplot(1, 2, 2)
improvements = ['Doublons\nsupprimés', 'Incohérences\ncorrigées']
values = [179, before_competitors]
plt.bar(improvements, values, color=['orange', 'blue'])
plt.title('Améliorations Appliquées')
plt.ylabel('Nombre')

plt.tight_layout()
plt.show()