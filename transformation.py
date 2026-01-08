# -*- coding: utf-8 -*-
"""03_transformation.ipynb

# Data Refinement - Transformation et validation
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
df_clean = df.copy()

# Nettoyage (repris du module précédent)
df_clean['Rating'] = df_clean['Rating'].fillna(df_clean['Rating'].median())
df_clean['Revenue'] = df_clean['Revenue'].replace('Unknown / Non-Applicable', np.nan)
df_clean['Competitors'] = df_clean['Competitors'].replace('-1', np.nan)
df_clean = df_clean.drop_duplicates()
df_clean = df_clean.drop_duplicates(subset=['Job Title', 'Company Name', 'Location'], keep='first')

def separate_company_rating(company_str):
    if pd.isna(company_str) or '\n' not in str(company_str):
        return str(company_str), np.nan
    parts = str(company_str).split('\n')
    company = parts[0].strip()
    try:
        rating = float(parts[1]) if len(parts) > 1 else np.nan
    except:
        rating = np.nan
    return company, rating

company_data = df_clean['Company Name'].apply(separate_company_rating)
df_clean['Company_Clean'] = [x[0] for x in company_data]
df_clean['Company_Rating'] = [x[1] for x in company_data]

# Extraction salaires
def extract_salary(salary_str):
    if pd.isna(salary_str):
        return np.nan, np.nan, np.nan

    salary_clean = str(salary_str).replace('$', '').replace('K', '').replace(',', '')
    numbers = re.findall(r'\d+', salary_clean)

    if len(numbers) >= 2:
        sal_min = float(numbers[0])
        sal_max = float(numbers[1])
        sal_avg = (sal_min + sal_max) / 2
        return sal_min, sal_max, sal_avg

    return np.nan, np.nan, np.nan

salary_data = df_clean['Salary Estimate'].apply(extract_salary)
df_clean['Salary_Min_K'] = [x[0] for x in salary_data]
df_clean['Salary_Max_K'] = [x[1] for x in salary_data]
df_clean['Salary_Avg_K'] = [x[2] for x in salary_data]

# Géolocalisation
location_split = df_clean['Location'].str.extract(r'^(.*),\s*([A-Z]{2})$')
df_clean['City'] = location_split[0]
df_clean['State'] = location_split[1]

# Variables métier
def categorize_salary(salary):
    if pd.isna(salary):
        return np.nan
    if salary < 80:
        return 'Entry_Level'
    elif salary < 120:
        return 'Mid_Level'
    elif salary < 160:
        return 'Senior_Level'
    else:
        return 'Executive_Level'

df_clean['Salary_Segment'] = df_clean['Salary_Avg_K'].apply(categorize_salary)

def extract_seniority(job_title):
    if pd.isna(job_title):
        return 'Unknown'
    title = str(job_title).lower()
    if any(word in title for word in ['senior', 'sr.', 'lead', 'principal']):
        return 'Senior'
    elif any(word in title for word in ['manager', 'director', 'head']):
        return 'Management'
    elif any(word in title for word in ['junior', 'jr.', 'entry', 'associate']):
        return 'Junior'
    else:
        return 'Mid_Level'

df_clean['Seniority_Level'] = df_clean['Job Title'].apply(extract_seniority)

plt.figure(figsize=(10, 4))

# Distribution des salaires extraits
plt.subplot(1, 2, 1)
df_clean['Salary_Avg_K'].hist(bins=25, alpha=0.7, color='green')
plt.title('Distribution Salaires Extraits')
plt.xlabel('Salaire (K$)')

# Boxplot salaires par segment
plt.subplot(1, 2, 2)
salary_segments = df_clean.dropna(subset=['Salary_Segment', 'Salary_Avg_K'])
sns.boxplot(data=salary_segments, x='Salary_Segment', y='Salary_Avg_K')
plt.title('Validation Segments Salariaux')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Métriques de qualité finale
total_cells = df_clean.shape[0] * df_clean.shape[1]
missing_cells = df_clean.isnull().sum().sum()
completeness = ((total_cells - missing_cells) / total_cells) * 100
overall_quality = completeness

# Export final
df_clean.to_csv('refined_data/glassdoor_jobs_refined.csv', index=False)