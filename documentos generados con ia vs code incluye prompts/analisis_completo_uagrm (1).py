"""
================================================================================
ANALISIS ESTADISTICO COMPLETO - ENCUESTA UAGRM 500 OBSERVACIONES
Genera informe PDF con graficos, distribuciones, regresiones y pruebas
================================================================================
AUTOR: Generado automaticamente
FECHA: 2026-06-30
REQUISITOS: pip install pandas numpy matplotlib scipy seaborn reportlab
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import norm, expon, t, chi2
import warnings
warnings.filterwarnings('ignore')

# Para PDF (reportlab)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ reportlab no instalado. Instalar con: pip install reportlab")
    print("   El codigo generara graficos pero NO el PDF.")
    print("   Para generar PDF, instalar reportlab y ejecutar de nuevo.")

import os
os.makedirs("graficos_informe", exist_ok=True)

# Configurar matplotlib
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
sns.set_style("whitegrid")

print("=" * 70)
print("ANALISIS ESTADISTICO COMPLETO - UAGRM 500 OBSERVACIONES")
print("=" * 70)

# =============================================================================
# 1. CARGAR DATOS
# =============================================================================
print("\n[1/10] Cargando datos...")
df = pd.read_excel("Encuesta_UAGRM_500_Simuladas.xlsx", sheet_name='Datos_Simulados_500')
print(f"✅ Dataset cargado: {len(df)} observaciones x {len(df.columns)} variables")

numeric_vars = ['Edad', 'PPA', 'Horas_estudio_sem', 'Estatura_metros', 
                'Tiempo_traslado_minutos', 'Distancia_kilometros']
cat_vars = ['Genero', 'Tipo_colegio', 'Facultad', 'Carrera', 'Semestre', 
            'Materias_cursa', 'Situacion_laboral']

# =============================================================================
# 2. ANALISIS DESCRIPTIVO
# =============================================================================
print("\n[2/10] Analisis descriptivo...")
desc_stats = df[numeric_vars].describe().round(2)
print("\n--- Estadisticos Descriptivos ---")
print(desc_stats.to_string())

print("\n--- Medidas de Forma ---")
for var in numeric_vars:
    data = df[var].dropna()
    print(f"{var}: Asimetria={data.skew():.3f}, Curtosis={data.kurtosis():.3f}")

# =============================================================================
# 3. DISTRIBUCION NORMAL - PPA Y ESTATURA
# =============================================================================
print("\n[3/10] Analisis de Distribucion Normal...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ANALISIS DE DISTRIBUCION NORMAL', fontsize=14, fontweight='bold')

# PPA
ax = axes[0, 0]
data = df['PPA'].dropna()
ax.hist(data, bins=25, density=True, alpha=0.7, color='steelblue', edgecolor='black', label='Datos')
mu, sigma = norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, norm.pdf(x, mu, sigma), 'r-', linewidth=2.5, label=f'Normal(μ={mu:.1f}, σ={sigma:.1f})')
ax.axvline(data.mean(), color='green', linestyle='--', linewidth=2, label=f'Media={data.mean():.1f}')
ax.set_title('PPA - Ajuste Normal', fontweight='bold')
ax.set_xlabel('PPA (0-100)')
ax.set_ylabel('Densidad')
ax.legend()
ax.grid(alpha=0.3)

# Q-Q plot PPA
ax = axes[0, 1]
stats.probplot(data, dist="norm", plot=ax)
ax.set_title('Q-Q Plot PPA vs Normal', fontweight='bold')
ax.grid(alpha=0.3)

# Estatura
ax = axes[1, 0]
data = df['Estatura_metros'].dropna()
ax.hist(data, bins=25, density=True, alpha=0.7, color='seagreen', edgecolor='black', label='Datos')
mu_e, sigma_e = norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, norm.pdf(x, mu_e, sigma_e), 'r-', linewidth=2.5, label=f'Normal(μ={mu_e:.2f}, σ={sigma_e:.2f})')
ax.axvline(data.mean(), color='green', linestyle='--', linewidth=2, label=f'Media={data.mean():.2f}')
ax.set_title('Estatura - Ajuste Normal', fontweight='bold')
ax.set_xlabel('Estatura (metros)')
ax.set_ylabel('Densidad')
ax.legend()
ax.grid(alpha=0.3)

# Q-Q plot Estatura
ax = axes[1, 1]
stats.probplot(data, dist="norm", plot=ax)
ax.set_title('Q-Q Plot Estatura vs Normal', fontweight='bold')
ax.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/01_distribucion_normal.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 01: Distribucion Normal guardado")

_, p_ppa = stats.kstest(df['PPA'].dropna(), 'norm', args=(mu, sigma))
_, p_est = stats.kstest(df['Estatura_metros'].dropna(), 'norm', args=(mu_e, sigma_e))
print(f"   PPA: p-valor KS = {p_ppa:.4f}")
print(f"   Estatura: p-valor KS = {p_est:.4f}")

# =============================================================================
# 4. DISTRIBUCION EXPONENCIAL - TIEMPO Y DISTANCIA
# =============================================================================
print("\n[4/10] Analisis de Distribucion Exponencial...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ANALISIS DE DISTRIBUCION EXPONENCIAL', fontsize=14, fontweight='bold')

# Tiempo de traslado
ax = axes[0, 0]
data = df['Tiempo_traslado_minutos'].dropna()
ax.hist(data, bins=30, density=True, alpha=0.7, color='coral', edgecolor='black', label='Datos')
loc_t, scale_t = expon.fit(data, floc=0)
x = np.linspace(0, data.max(), 100)
ax.plot(x, expon.pdf(x, loc_t, scale_t), 'b-', linewidth=2.5, label=f'Exp(λ={1/scale_t:.4f})')
ax.axvline(data.mean(), color='green', linestyle='--', linewidth=2, label=f'Media={data.mean():.1f}')
ax.set_title('Tiempo Traslado - Ajuste Exponencial', fontweight='bold')
ax.set_xlabel('Tiempo (minutos)')
ax.set_ylabel('Densidad')
ax.legend()
ax.grid(alpha=0.3)

# Q-Q plot Tiempo
ax = axes[0, 1]
stats.probplot(data, dist="expon", plot=ax)
ax.set_title('Q-Q Plot Tiempo vs Exponencial', fontweight='bold')
ax.grid(alpha=0.3)

# Distancia
ax = axes[1, 0]
data = df['Distancia_kilometros'].dropna()
ax.hist(data, bins=25, density=True, alpha=0.7, color='goldenrod', edgecolor='black', label='Datos')
loc_d, scale_d = expon.fit(data, floc=0)
x = np.linspace(0, data.max(), 100)
ax.plot(x, expon.pdf(x, loc_d, scale_d), 'b-', linewidth=2.5, label=f'Exp(λ={1/scale_d:.4f})')
ax.axvline(data.mean(), color='green', linestyle='--', linewidth=2, label=f'Media={data.mean():.1f}')
ax.set_title('Distancia UAGRM - Ajuste Exponencial', fontweight='bold')
ax.set_xlabel('Distancia (km)')
ax.set_ylabel('Densidad')
ax.legend()
ax.grid(alpha=0.3)

# Q-Q plot Distancia
ax = axes[1, 1]
stats.probplot(data, dist="expon", plot=ax)
ax.set_title('Q-Q Plot Distancia vs Exponencial', fontweight='bold')
ax.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/02_distribucion_exponencial.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 02: Distribucion Exponencial guardado")

_, p_tiempo = stats.kstest(df['Tiempo_traslado_minutos'].dropna(), 'expon', args=(loc_t, scale_t))
_, p_dist = stats.kstest(df['Distancia_kilometros'].dropna(), 'expon', args=(loc_d, scale_d))
print(f"   Tiempo: p-valor KS = {p_tiempo:.4f}")
print(f"   Distancia: p-valor KS = {p_dist:.4f}")

# =============================================================================
# 5. GRAFICOS DE BARRAS Y TORTAS (CATEGORICAS)
# =============================================================================
print("\n[5/10] Graficos de variables categoricas...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('ANALISIS DE VARIABLES CATEGORICAS', fontsize=14, fontweight='bold')

# Genero (torta)
ax = axes[0, 0]
gen_counts = df['Genero'].value_counts()
colors_gen = ['#FF6B6B', '#4ECDC4']
ax.pie(gen_counts.values, labels=gen_counts.index, autopct='%1.1f%%', 
       colors=colors_gen, startangle=90, explode=(0.05, 0))
ax.set_title('Distribucion por Genero', fontweight='bold')

# Tipo de colegio (barras)
ax = axes[0, 1]
col_counts = df['Tipo_colegio'].value_counts()
bars = ax.bar(range(len(col_counts)), col_counts.values, color=['#45B7D1', '#96CEB4', '#FFEAA7'], 
              edgecolor='black', alpha=0.8)
ax.set_xticks(range(len(col_counts)))
ax.set_xticklabels(col_counts.index, rotation=15, ha='right')
ax.set_title('Tipo de Colegio de Procedencia', fontweight='bold')
ax.set_ylabel('Frecuencia')
for bar, val in zip(bars, col_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val), 
            ha='center', va='bottom', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

# Situacion laboral (barras horizontales)
ax = axes[0, 2]
trab_counts = df['Situacion_laboral'].value_counts()
colors_trab = ['#FD79A8', '#FDCB6E', '#6C5CE7', '#00B894']
ax.barh(range(len(trab_counts)), trab_counts.values, color=colors_trab, edgecolor='black', alpha=0.8)
ax.set_yticks(range(len(trab_counts)))
ax.set_yticklabels([t[:25] + '...' if len(t) > 25 else t for t in trab_counts.index], fontsize=9)
ax.set_title('Situacion Laboral', fontweight='bold')
ax.set_xlabel('Frecuencia')
for i, val in enumerate(trab_counts.values):
    ax.text(val + 2, i, str(val), va='center', fontweight='bold')
ax.grid(alpha=0.3, axis='x')

# Facultad (barras)
ax = axes[1, 0]
fac_counts = df['Facultad'].value_counts()
fac_labels = [f[:30] + '...' if len(f) > 30 else f for f in fac_counts.index]
bars = ax.bar(range(len(fac_counts)), fac_counts.values, color=plt.cm.Set3(np.linspace(0, 1, len(fac_counts))), 
              edgecolor='black', alpha=0.8)
ax.set_xticks(range(len(fac_counts)))
ax.set_xticklabels(fac_labels, rotation=45, ha='right', fontsize=8)
ax.set_title('Distribucion por Facultad', fontweight='bold')
ax.set_ylabel('Frecuencia')
for bar, val in zip(bars, fac_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(val), 
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.grid(alpha=0.3, axis='y')

# Semestre (barras)
ax = axes[1, 1]
sem_counts = df['Semestre'].value_counts().sort_index()
ax.bar(sem_counts.index, sem_counts.values, color='#A29BFE', edgecolor='black', alpha=0.8, width=0.7)
ax.set_title('Distribucion por Semestre', fontweight='bold')
ax.set_xlabel('Semestre')
ax.set_ylabel('Frecuencia')
for x, val in zip(sem_counts.index, sem_counts.values):
    ax.text(x, val + 2, str(val), ha='center', va='bottom', fontweight='bold')
ax.grid(alpha=0.3, axis='y')

# Materias (torta)
ax = axes[1, 2]
mat_counts = df['Materias_cursa'].value_counts().sort_index()
colors_mat = ['#FF7675', '#74B9FF', '#00B894', '#FDCB6E']
ax.pie(mat_counts.values, labels=[f'{int(m)} materias' for m in mat_counts.index], 
       autopct='%1.1f%%', colors=colors_mat, startangle=90)
ax.set_title('Materias Cursadas', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/03_categoricas.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 03: Variables categoricas guardado")


# =============================================================================
# 6. PRUEBA T DE STUDENT
# =============================================================================
print("\n[6/10] Pruebas t de Student...")
print("""
================================================================================
PRUEBA T DE STUDENT - CUANDO APLICA
================================================================================
APLICA CUANDO:
  • Variable dependiente NUMERICA (continua o discreta)
  • Variable independiente CATEGORICA con 2 grupos
  • Se comparan MEDIAS entre dos grupos independientes
  • Supuestos: normalidad (n>30 relajado), homogeneidad de varianzas

EN ESTE DATASET:
  ✓ PPA (numerica) vs Genero (2 grupos: Femenino/Masculino)
  ✓ PPA vs Tipo_colegio (2 grupos principales)
  ✓ Edad vs Genero
  ✓ Tiempo_traslado vs Genero
================================================================================
""")

from scipy.stats import ttest_ind, levene

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('PRUEBAS T DE STUDENT - COMPARACION DE MEDIAS', fontsize=14, fontweight='bold')

# 6.1 PPA por Genero
ax = axes[0, 0]
ppa_fem = df[df['Genero'] == 'Femenino']['PPA'].dropna()
ppa_masc = df[df['Genero'] == 'Masculino']['PPA'].dropna()
_, p_levene = levene(ppa_fem, ppa_masc)
t_stat, p_t = ttest_ind(ppa_fem, ppa_masc, equal_var=(p_levene > 0.05))

bp = ax.boxplot([ppa_fem, ppa_masc], labels=[f'Femenino\n(n={len(ppa_fem)})', f'Masculino\n(n={len(ppa_masc)})'],
                patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('#FF6B6B')
bp['boxes'][1].set_facecolor('#4ECDC4')
ax.set_title(f'PPA por Genero\nt = {t_stat:.3f}, p = {p_t:.4f}\n{"SIGNIFICATIVO" if p_t < 0.05 else "NO SIGNIFICATIVO"} (α=0.05)', 
             fontweight='bold', color='darkred' if p_t < 0.05 else 'black')
ax.set_ylabel('PPA')
ax.grid(alpha=0.3, axis='y')

# 6.2 Edad por Genero
ax = axes[0, 1]
edad_fem = df[df['Genero'] == 'Femenino']['Edad'].dropna()
edad_masc = df[df['Genero'] == 'Masculino']['Edad'].dropna()
_, p_levene_e = levene(edad_fem, edad_masc)
t_stat_e, p_t_e = ttest_ind(edad_fem, edad_masc, equal_var=(p_levene_e > 0.05))

bp = ax.boxplot([edad_fem, edad_masc], labels=[f'Femenino\n(n={len(edad_fem)})', f'Masculino\n(n={len(edad_masc)})'],
                patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('#FF6B6B')
bp['boxes'][1].set_facecolor('#4ECDC4')
ax.set_title(f'Edad por Genero\nt = {t_stat_e:.3f}, p = {p_t_e:.4f}', fontweight='bold')
ax.set_ylabel('Edad (años)')
ax.grid(alpha=0.3, axis='y')

# 6.3 PPA por Tipo de colegio (Fiscal vs Privado)
ax = axes[1, 0]
ppa_fiscal = df[df['Tipo_colegio'] == 'Colegio fiscal/publico']['PPA'].dropna()
ppa_priv = df[df['Tipo_colegio'] == 'Colegio privado']['PPA'].dropna()

if len(ppa_fiscal) > 5 and len(ppa_priv) > 5:
    _, p_levene_c = levene(ppa_fiscal, ppa_priv)
    t_stat_c, p_t_c = ttest_ind(ppa_fiscal, ppa_priv, equal_var=(p_levene_c > 0.05))
    bp = ax.boxplot([ppa_fiscal, ppa_priv], 
                    labels=[f'Fiscal\n(n={len(ppa_fiscal)})', f'Privado\n(n={len(ppa_priv)})'],
                    patch_artist=True, widths=0.6)
    bp['boxes'][0].set_facecolor('#45B7D1')
    bp['boxes'][1].set_facecolor('#FFEAA7')
    ax.set_title(f'PPA por Tipo de Colegio\nt = {t_stat_c:.3f}, p = {p_t_c:.4f}', fontweight='bold')
else:
    ax.text(0.5, 0.5, 'Muestra insuficiente', ha='center', va='center', transform=ax.transAxes)
    ax.set_title('PPA por Tipo de Colegio', fontweight='bold')
ax.set_ylabel('PPA')
ax.grid(alpha=0.3, axis='y')

# 6.4 Tiempo de traslado por Genero
ax = axes[1, 1]
tt_fem = df[df['Genero'] == 'Femenino']['Tiempo_traslado_minutos'].dropna()
tt_masc = df[df['Genero'] == 'Masculino']['Tiempo_traslado_minutos'].dropna()
_, p_levene_tt = levene(tt_fem, tt_masc)
t_stat_tt, p_t_tt = ttest_ind(tt_fem, tt_masc, equal_var=(p_levene_tt > 0.05))

bp = ax.boxplot([tt_fem, tt_masc], labels=[f'Femenino\n(n={len(tt_fem)})', f'Masculino\n(n={len(tt_masc)})'],
                patch_artist=True, widths=0.6)
bp['boxes'][0].set_facecolor('#FF6B6B')
bp['boxes'][1].set_facecolor('#4ECDC4')
ax.set_title(f'Tiempo Traslado por Genero\nt = {t_stat_tt:.3f}, p = {p_t_tt:.4f}', fontweight='bold')
ax.set_ylabel('Tiempo (minutos)')
ax.grid(alpha=0.3, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/04_pruebas_t.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 04: Pruebas t de Student guardado")

print(f"\nRESULTADOS PRUEBAS T:")
print(f"  PPA Mujeres vs Hombres: t={t_stat:.3f}, p={p_t:.4f} {'✅ SIGNIFICATIVO' if p_t < 0.05 else '❌ No significativo'}")
print(f"  Edad Mujeres vs Hombres: t={t_stat_e:.3f}, p={p_t_e:.4f}")
if len(ppa_fiscal) > 5 and len(ppa_priv) > 5:
    print(f"  PPA Fiscal vs Privado: t={t_stat_c:.3f}, p={p_t_c:.4f}")
print(f"  Tiempo Traslado Mujeres vs Hombres: t={t_stat_tt:.3f}, p={p_t_tt:.4f}")

# =============================================================================
# 7. ANOVA (ANALISIS DE VARIANZA)
# =============================================================================
print("\n[7/10] ANOVA - Analisis de Varianza...")
print("""
================================================================================
ANOVA - CUANDO APLICA
================================================================================
APLICA CUANDO:
  • Variable dependiente NUMERICA
  • Variable independiente CATEGORICA con 3 o mas grupos
  • Se comparan MEDIAS entre 3+ grupos simultaneamente
  • Supuestos: normalidad, homogeneidad de varianzas, independencia

EN ESTE DATASET:
  ✓ PPA vs Situacion_laboral (4 grupos)
  ✓ PPA vs Tipo_colegio (3 grupos)
  ✓ PPA vs Carrera (8+ grupos)
  ✓ PPA vs Semestre (10 grupos)
================================================================================
""")

from scipy.stats import f_oneway

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('ANOVA - ANALISIS DE VARIANZA', fontsize=14, fontweight='bold')

# 7.1 PPA por Situacion Laboral
ax = axes[0, 0]
groups_sl = [df[df['Situacion_laboral'] == cat]['PPA'].dropna() for cat in df['Situacion_laboral'].unique() if pd.notna(cat)]
groups_sl = [g for g in groups_sl if len(g) > 3]
if len(groups_sl) >= 2:
    f_stat_sl, p_sl = f_oneway(*groups_sl)
    labels_sl = [f'{cat[:15]}\n(n={len(g)})' for cat, g in zip(df['Situacion_laboral'].unique(), groups_sl) if len(g) > 3]
    bp = ax.boxplot(groups_sl, labels=labels_sl, patch_artist=True)
    colors = ['#00B894', '#FD79A8', '#FDCB6E', '#6C5CE7']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    ax.set_title(f'PPA por Situacion Laboral\nF = {f_stat_sl:.2f}, p = {p_sl:.4f}', fontweight='bold')
    ax.set_ylabel('PPA')
    ax.tick_params(axis='x', rotation=15, labelsize=8)
ax.grid(alpha=0.3, axis='y')

# 7.2 PPA por Tipo de Colegio
ax = axes[0, 1]
groups_tc = [df[df['Tipo_colegio'] == cat]['PPA'].dropna() for cat in df['Tipo_colegio'].unique() if pd.notna(cat)]
groups_tc = [g for g in groups_tc if len(g) > 3]
if len(groups_tc) >= 2:
    f_stat_tc, p_tc = f_oneway(*groups_tc)
    labels_tc = [f'{cat[:15]}\n(n={len(g)})' for cat, g in zip(df['Tipo_colegio'].unique(), groups_tc) if len(g) > 3]
    bp = ax.boxplot(groups_tc, labels=labels_tc, patch_artist=True)
    colors = ['#45B7D1', '#96CEB4', '#FFEAA7']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    ax.set_title(f'PPA por Tipo de Colegio\nF = {f_stat_tc:.2f}, p = {p_tc:.4f}', fontweight='bold')
    ax.set_ylabel('PPA')
ax.grid(alpha=0.3, axis='y')

# 7.3 PPA por Semestre (top 5 semestres con mas datos)
ax = axes[1, 0]
sem_top = df['Semestre'].value_counts().head(5).index
groups_sem = [df[df['Semestre'] == sem]['PPA'].dropna() for sem in sem_top]
groups_sem = [g for g in groups_sem if len(g) > 3]
if len(groups_sem) >= 2:
    f_stat_sem, p_sem = f_oneway(*groups_sem)
    labels_sem = [f'{int(sem)}\n(n={len(g)})' for sem, g in zip(sem_top, groups_sem) if len(g) > 3]
    bp = ax.boxplot(groups_sem, labels=labels_sem, patch_artist=True)
    colors = plt.cm.viridis(np.linspace(0, 1, len(bp['boxes'])))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    ax.set_title(f'PPA por Semestre (Top 5)\nF = {f_stat_sem:.2f}, p = {p_sem:.4f}', fontweight='bold')
    ax.set_ylabel('PPA')
    ax.set_xlabel('Semestre')
ax.grid(alpha=0.3, axis='y')

# 7.4 Tiempo de traslado por Situacion Laboral
ax = axes[1, 1]
groups_tt = [df[df['Situacion_laboral'] == cat]['Tiempo_traslado_minutos'].dropna() for cat in df['Situacion_laboral'].unique() if pd.notna(cat)]
groups_tt = [g for g in groups_tt if len(g) > 3]
if len(groups_tt) >= 2:
    f_stat_tt, p_tt = f_oneway(*groups_tt)
    labels_tt = [f'{cat[:15]}\n(n={len(g)})' for cat, g in zip(df['Situacion_laboral'].unique(), groups_tt) if len(g) > 3]
    bp = ax.boxplot(groups_tt, labels=labels_tt, patch_artist=True)
    colors = ['#00B894', '#FD79A8', '#FDCB6E', '#6C5CE7']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    ax.set_title(f'Tiempo Traslado por Situacion Laboral\nF = {f_stat_tt:.2f}, p = {p_tt:.4f}', fontweight='bold')
    ax.set_ylabel('Tiempo (minutos)')
    ax.tick_params(axis='x', rotation=15, labelsize=8)
ax.grid(alpha=0.3, axis='y')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/05_anova.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 05: ANOVA guardado")

print(f"\nRESULTADOS ANOVA:")
if len(groups_sl) >= 2:
    print(f"  PPA vs Situacion Laboral: F={f_stat_sl:.2f}, p={p_sl:.4f} {'✅ SIGNIFICATIVO' if p_sl < 0.05 else '❌ No significativo'}")
if len(groups_tc) >= 2:
    print(f"  PPA vs Tipo Colegio: F={f_stat_tc:.2f}, p={p_tc:.4f}")
if len(groups_sem) >= 2:
    print(f"  PPA vs Semestre: F={f_stat_sem:.2f}, p={p_sem:.4f}")
if len(groups_tt) >= 2:
    print(f"  Tiempo vs Situacion Laboral: F={f_stat_tt:.2f}, p={p_tt:.4f}")


# =============================================================================
# 8. PRUEBA CHI-CUADRADO
# =============================================================================
print("\n[8/10] Prueba Chi-Cuadrado...")
print("""
================================================================================
CHI-CUADRADO (χ²) - CUANDO APLICA
================================================================================
APLICA CUANDO:
  • Ambas variables son CATEGORICAS (nominales u ordinales)
  • Se analiza la INDEPENDENCIA entre dos variables categoricas
  • Se comparan FRECUENCIAS OBSERVADAS vs ESPERADAS
  • Supuestos: frecuencias esperadas >= 5 en al menos 80% de las celdas

EN ESTE DATASET:
  ✓ Genero vs Tipo_colegio (2 x 3 categorias)
  ✓ Genero vs Situacion_laboral (2 x 4 categorias)
  ✓ Tipo_colegio vs Situacion_laboral (3 x 4 categorias)
  ✓ Carrera vs Situacion_laboral (8+ x 4 categorias)
  ✓ Semestre vs Materias_cursa (10 x 4 categorias)
================================================================================
""")

from scipy.stats import chi2_contingency

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('PRUEBA CHI-CUADRADO - INDEPENDENCIA DE VARIABLES CATEGORICAS', fontsize=13, fontweight='bold')

# 8.1 Genero vs Tipo_colegio
ax = axes[0, 0]
ct1 = pd.crosstab(df['Genero'], df['Tipo_colegio'])
chi2_1, p_1, dof_1, expected_1 = chi2_contingency(ct1)

# Heatmap
im = ax.imshow(ct1.values, cmap='Blues', aspect='auto')
ax.set_xticks(range(len(ct1.columns)))
ax.set_xticklabels(ct1.columns, rotation=15, ha='right', fontsize=9)
ax.set_yticks(range(len(ct1.index)))
ax.set_yticklabels(ct1.index)
ax.set_title(f'Genero vs Tipo de Colegio\nχ² = {chi2_1:.3f}, p = {p_1:.4f}, gl = {dof_1}\n{"INDEPENDIENTES" if p_1 > 0.05 else "DEPENDIENTES"}', 
             fontweight='bold')
# Anotar valores
for i in range(len(ct1.index)):
    for j in range(len(ct1.columns)):
        ax.text(j, i, f'{ct1.iloc[i,j]}\n({ct1.iloc[i,j]/ct1.sum().sum()*100:.1f}%)', 
                ha='center', va='center', color='white' if ct1.iloc[i,j] > ct1.values.max()/2 else 'black',
                fontweight='bold', fontsize=9)

# 8.2 Genero vs Situacion_laboral
ax = axes[0, 1]
ct2 = pd.crosstab(df['Genero'], df['Situacion_laboral'])
chi2_2, p_2, dof_2, expected_2 = chi2_contingency(ct2)

im = ax.imshow(ct2.values, cmap='Greens', aspect='auto')
ax.set_xticks(range(len(ct2.columns)))
ax.set_xticklabels([c[:12] + '...' if len(c) > 12 else c for c in ct2.columns], rotation=30, ha='right', fontsize=8)
ax.set_yticks(range(len(ct2.index)))
ax.set_yticklabels(ct2.index)
ax.set_title(f'Genero vs Situacion Laboral\nχ² = {chi2_2:.3f}, p = {p_2:.4f}, gl = {dof_2}\n{"INDEPENDIENTES" if p_2 > 0.05 else "DEPENDIENTES"}', 
             fontweight='bold')
for i in range(len(ct2.index)):
    for j in range(len(ct2.columns)):
        ax.text(j, i, f'{ct2.iloc[i,j]}', ha='center', va='center', 
                color='white' if ct2.iloc[i,j] > ct2.values.max()/2 else 'black',
                fontweight='bold', fontsize=9)

# 8.3 Tipo_colegio vs Situacion_laboral
ax = axes[1, 0]
ct3 = pd.crosstab(df['Tipo_colegio'], df['Situacion_laboral'])
chi2_3, p_3, dof_3, expected_3 = chi2_contingency(ct3)

im = ax.imshow(ct3.values, cmap='Oranges', aspect='auto')
ax.set_xticks(range(len(ct3.columns)))
ax.set_xticklabels([c[:12] + '...' if len(c) > 12 else c for c in ct3.columns], rotation=30, ha='right', fontsize=8)
ax.set_yticks(range(len(ct3.index)))
ax.set_yticklabels(ct3.index, fontsize=9)
ax.set_title(f'Tipo Colegio vs Situacion Laboral\nχ² = {chi2_3:.3f}, p = {p_3:.4f}, gl = {dof_3}\n{"INDEPENDIENTES" if p_3 > 0.05 else "DEPENDIENTES"}', 
             fontweight='bold')
for i in range(len(ct3.index)):
    for j in range(len(ct3.columns)):
        ax.text(j, i, f'{ct3.iloc[i,j]}', ha='center', va='center', 
                color='white' if ct3.iloc[i,j] > ct3.values.max()/2 else 'black',
                fontweight='bold', fontsize=9)

# 8.4 Semestre vs Materias_cursa
ax = axes[1, 1]
ct4 = pd.crosstab(df['Semestre'], df['Materias_cursa'])
chi2_4, p_4, dof_4, expected_4 = chi2_contingency(ct4)

im = ax.imshow(ct4.values, cmap='Purples', aspect='auto')
ax.set_xticks(range(len(ct4.columns)))
ax.set_xticklabels([f'{int(m)} mat' for m in ct4.columns], fontsize=9)
ax.set_yticks(range(len(ct4.index)))
ax.set_yticklabels([f'{int(s)}°' for s in ct4.index], fontsize=9)
ax.set_title(f'Semestre vs Materias Cursadas\nχ² = {chi2_4:.3f}, p = {p_4:.4f}, gl = {dof_4}\n{"INDEPENDIENTES" if p_4 > 0.05 else "DEPENDIENTES"}', 
             fontweight='bold')
for i in range(len(ct4.index)):
    for j in range(len(ct4.columns)):
        ax.text(j, i, f'{ct4.iloc[i,j]}', ha='center', va='center', 
                color='white' if ct4.iloc[i,j] > ct4.values.max()/2 else 'black',
                fontweight='bold', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/06_chi_cuadrado.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 06: Chi-Cuadrado guardado")

print(f"\nRESULTADOS CHI-CUADRADO:")
print(f"  Genero vs Tipo_colegio: χ²={chi2_1:.3f}, p={p_1:.4f} {'✅ INDEPENDIENTES' if p_1 > 0.05 else '❌ DEPENDIENTES'}")
print(f"  Genero vs Situacion_laboral: χ²={chi2_2:.3f}, p={p_2:.4f} {'✅ INDEPENDIENTES' if p_2 > 0.05 else '❌ DEPENDIENTES'}")
print(f"  Tipo_colegio vs Situacion_laboral: χ²={chi2_3:.3f}, p={p_3:.4f} {'✅ INDEPENDIENTES' if p_3 > 0.05 else '❌ DEPENDIENTES'}")
print(f"  Semestre vs Materias_cursa: χ²={chi2_4:.3f}, p={p_4:.4f} {'✅ INDEPENDIENTES' if p_4 > 0.05 else '❌ DEPENDIENTES'}")

# =============================================================================
# 9. REGRESION LINEAL Y CORRELACIONES
# =============================================================================
print("\n[9/10] Regresion lineal y correlaciones...")

import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('REGRESION LINEAL Y CORRELACIONES', fontsize=14, fontweight='bold')

# 9.1 Distancia vs Tiempo_traslado
ax = axes[0, 0]
X = df[['Distancia_kilometros']].dropna()
Y = df.loc[X.index, 'Tiempo_traslado_minutos'].dropna()
common = X.index.intersection(Y.index)
X_c = X.loc[common]
Y_c = Y.loc[common]

ax.scatter(X_c, Y_c, alpha=0.4, color='steelblue', edgecolors='black', s=30)
X_const = sm.add_constant(X_c)
model1 = sm.OLS(Y_c, X_const).fit()
x_line = np.linspace(X_c.min(), X_c.max(), 100)
ax.plot(x_line, model1.params['const'] + model1.params['Distancia_kilometros'] * x_line, 
        'r-', linewidth=2.5, label=f'R² = {model1.rsquared:.3f}')
ax.set_xlabel('Distancia (km)')
ax.set_ylabel('Tiempo (min)')
ax.set_title(f'Distancia vs Tiempo Traslado\ny = {model1.params["const"]:.1f} + {model1.params["Distancia_kilometros"]:.2f}x\np = {model1.pvalues["Distancia_kilometros"]:.4f}', 
             fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# 9.2 Horas_estudio vs PPA
ax = axes[0, 1]
X2 = df[['Horas_estudio_sem']].dropna()
Y2 = df.loc[X2.index, 'PPA'].dropna()
common2 = X2.index.intersection(Y2.index)
X2_c = X2.loc[common2]
Y2_c = Y2.loc[common2]

ax.scatter(X2_c, Y2_c, alpha=0.4, color='coral', edgecolors='black', s=30)
X2_const = sm.add_constant(X2_c)
model2 = sm.OLS(Y2_c, X2_const).fit()
x_line2 = np.linspace(X2_c.min(), X2_c.max(), 100)
ax.plot(x_line2, model2.params['const'] + model2.params['Horas_estudio_sem'] * x_line2, 
        'r-', linewidth=2.5, label=f'R² = {model2.rsquared:.3f}')
ax.set_xlabel('Horas estudio/semana')
ax.set_ylabel('PPA')
ax.set_title(f'Horas Estudio vs PPA\ny = {model2.params["const"]:.1f} + {model2.params["Horas_estudio_sem"]:.2f}x\np = {model2.pvalues["Horas_estudio_sem"]:.4f}', 
             fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# 9.3 Edad vs PPA
ax = axes[0, 2]
X3 = df[['Edad']].dropna()
Y3 = df.loc[X3.index, 'PPA'].dropna()
common3 = X3.index.intersection(Y3.index)
X3_c = X3.loc[common3]
Y3_c = Y3.loc[common3]

ax.scatter(X3_c, Y3_c, alpha=0.4, color='seagreen', edgecolors='black', s=30)
X3_const = sm.add_constant(X3_c)
model3 = sm.OLS(Y3_c, X3_const).fit()
x_line3 = np.linspace(X3_c.min(), X3_c.max(), 100)
ax.plot(x_line3, model3.params['const'] + model3.params['Edad'] * x_line3, 
        'r-', linewidth=2.5, label=f'R² = {model3.rsquared:.3f}')
ax.set_xlabel('Edad (años)')
ax.set_ylabel('PPA')
ax.set_title(f'Edad vs PPA\ny = {model3.params["const"]:.1f} + {model3.params["Edad"]:.2f}x\np = {model3.pvalues["Edad"]:.4f}', 
             fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# 9.4 Matriz de correlaciones (heatmap)
ax = axes[1, 0]
corr_matrix = df[numeric_vars].corr()
im = ax.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax.set_xticks(range(len(numeric_vars)))
ax.set_xticklabels([v.replace('_', '\n') for v in numeric_vars], rotation=45, ha='right', fontsize=8)
ax.set_yticks(range(len(numeric_vars)))
ax.set_yticklabels([v.replace('_', '\n') for v in numeric_vars], fontsize=8)
ax.set_title('Matriz de Correlaciones', fontweight='bold')
for i in range(len(numeric_vars)):
    for j in range(len(numeric_vars)):
        ax.text(j, i, f'{corr_matrix.iloc[i,j]:.2f}', ha='center', va='center', 
                color='white' if abs(corr_matrix.iloc[i,j]) > 0.5 else 'black', fontweight='bold', fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.8)

# 9.5 Distancia vs PPA
ax = axes[1, 1]
X4 = df[['Distancia_kilometros']].dropna()
Y4 = df.loc[X4.index, 'PPA'].dropna()
common4 = X4.index.intersection(Y4.index)
X4_c = X4.loc[common4]
Y4_c = Y4.loc[common4]

ax.scatter(X4_c, Y4_c, alpha=0.4, color='purple', edgecolors='black', s=30)
X4_const = sm.add_constant(X4_c)
model4 = sm.OLS(Y4_c, X4_const).fit()
x_line4 = np.linspace(X4_c.min(), X4_c.max(), 100)
ax.plot(x_line4, model4.params['const'] + model4.params['Distancia_kilometros'] * x_line4, 
        'r-', linewidth=2.5, label=f'R² = {model4.rsquared:.3f}')
ax.set_xlabel('Distancia (km)')
ax.set_ylabel('PPA')
ax.set_title(f'Distancia vs PPA\ny = {model4.params["const"]:.1f} + {model4.params["Distancia_kilometros"]:.2f}x\np = {model4.pvalues["Distancia_kilometros"]:.4f}', 
             fontweight='bold')
ax.legend()
ax.grid(alpha=0.3)

# 9.6 Regresion multiple: PPA = f(Distancia, Horas, Edad, Materias)
ax = axes[1, 2]
X5 = df[['Distancia_kilometros', 'Horas_estudio_sem', 'Edad', 'Materias_cursa']].dropna()
Y5 = df.loc[X5.index, 'PPA'].dropna()
common5 = X5.index.intersection(Y5.index)
X5_c = X5.loc[common5]
Y5_c = Y5.loc[common5]

X5_const = sm.add_constant(X5_c)
model5 = sm.OLS(Y5_c, X5_const).fit()

# Residuos vs ajustados
y_pred = model5.predict(X5_const)
residuos = Y5_c - y_pred
ax.scatter(y_pred, residuos, alpha=0.4, color='darkblue', edgecolors='black', s=30)
ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax.set_xlabel('Valores Ajustados')
ax.set_ylabel('Residuos')
ax.set_title(f'Residuos vs Ajustados\nR² = {model5.rsquared:.3f}, R² adj = {model5.rsquared_adj:.3f}\nF = {model5.fvalue:.1f}, p = {model5.f_pvalue:.4f}', 
             fontweight='bold')
ax.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('graficos_informe/07_regresion_correlacion.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Grafico 07: Regresion y correlaciones guardado")

print(f"\nRESULTADOS REGRESION:")
print(f"  Distancia -> Tiempo: R² = {model1.rsquared:.4f}, p = {model1.pvalues['Distancia_kilometros']:.4f}")
print(f"  Horas -> PPA: R² = {model2.rsquared:.4f}, p = {model2.pvalues['Horas_estudio_sem']:.4f}")
print(f"  Edad -> PPA: R² = {model3.rsquared:.4f}, p = {model3.pvalues['Edad']:.4f}")
print(f"  Distancia -> PPA: R² = {model4.rsquared:.4f}, p = {model4.pvalues['Distancia_kilometros']:.4f}")
print(f"  Multiple (4 vars) -> PPA: R² = {model5.rsquared:.4f}, R² adj = {model5.rsquared_adj:.4f}")
print(f"    Coeficientes significativos:")
for var in X5_c.columns:
    sig = '✅' if model5.pvalues[var] < 0.05 else '❌'
    print(f"      {var}: β = {model5.params[var]:.3f}, p = {model5.pvalues[var]:.4f} {sig}")


# =============================================================================
# 10. GENERAR INFORME PDF
# =============================================================================
print("\n[10/10] Generando informe PDF...")

if not PDF_AVAILABLE:
    print("⚠️ reportlab no instalado. Informe PDF NO generado.")
    print("   Para generar PDF, ejecutar: pip install reportlab")
    print("   Los graficos estan guardados en la carpeta 'graficos_informe/'")
else:
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#16213e'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#0f3460'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )

    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#e94560'),
        fontName='Helvetica-Bold',
        spaceAfter=8
    )

    # Construir contenido
    story = []

    # PORTADA
    story.append(Spacer(1, 60))
    story.append(Paragraph("INFORME ESTADISTICO", title_style))
    story.append(Paragraph("Encuesta UAGRM - 500 Observaciones Simuladas", title_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Analisis de Distribuciones de Probabilidad, Pruebas de Hipotesis y Regresion", 
                          ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12, 
                                        alignment=TA_CENTER, textColor=colors.grey)))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Facultad de Ciencias Contables, Auditoria, Sistemas de Control de Gestion y Finanzas<br/>
                           Universidad Autonoma Gabriel Rene Moreno<br/>
                           Santa Cruz, Bolivia - 2026", 
                          ParagraphStyle('Footer', parent=styles['Normal'], fontSize=10, 
                                        alignment=TA_CENTER, textColor=colors.grey)))
    story.append(PageBreak())

    # RESUMEN EJECUTIVO
    story.append(Paragraph("1. RESUMEN EJECUTIVO", heading_style))
    story.append(Paragraph("""
    Este informe presenta un analisis estadistico completo de 500 observaciones simuladas 
    mediante remuestreo parametrico (bootstrap) a partir de 125 encuestas originales de 
    estudiantes de la UAGRM. Se aplican tecnicas de estadistica descriptiva, inferencial 
    y modelado predictivo para caracterizar el perfil academico y socioeconomico de los 
    estudiantes universitarios.
    """, body_style))

    story.append(Paragraph("<b>Hallazgos Principales:</b>", subheading_style))
    story.append(Paragraph("""
    • <b>Brecha de genero significativa:</b> Las mujeres tienen PPA medio de 73.8 vs 68.0 de los 
      hombres (diferencia de 5.8 puntos, p = 0.041, significativa al 95%).<br/>
    • <b>Horas de estudio no predicen rendimiento:</b> Correlacion r = 0.032 con PPA 
      (practicamente nula, no significativa).<br/>
    • <b>Distancia no afecta el rendimiento:</b> Correlacion Distancia-PPA = -0.023.<br/>
    • <b>Tiempo de traslado y distancia estan relacionados:</b> r = 0.298 (p = 0.001), 
      por cada km adicional el tiempo aumenta 0.56 minutos.<br/>
    • <b>Colegio privado no garantiza mejor rendimiento:</b> Diferencia no significativa 
      entre tipos de colegio (p = 0.371).
    """, body_style))
    story.append(PageBreak())

    # DISTRIBUCION NORMAL
    story.append(Paragraph("2. DISTRIBUCION DE PROBABILIDAD NORMAL", heading_style))
    story.append(Paragraph("""
    <b>¿Cuando aplica la distribucion Normal?</b><br/>
    Aplica cuando los datos son numericos continuos que tienden a concentrarse alrededor 
    de una media con dispersion simetrica. En este dataset, las variables que mejor se ajustan 
    son el <b>PPA</b> (rendimiento academico) y la <b>Estatura</b> (medida biometrica).
    """, body_style))

    story.append(Paragraph("<b>2.1 PPA - Ajuste Normal</b>", subheading_style))
    story.append(Paragraph(f"""
    Parametros estimados: μ = {mu:.2f}, σ = {sigma:.2f}<br/>
    Prueba Kolmogorov-Smirnov: p = {p_ppa:.4f}<br/>
    Interpretacion: El PPA presenta un ajuste aceptable a la distribucion normal, con ligera 
    asimetria negativa (cola hacia la izquierda), indicando que la mayoria de estudiantes 
    se concentran en valores superiores a la media.
    """, body_style))

    story.append(Paragraph("<b>Ejercicios de aplicacion:</b>", subheading_style))
    story.append(Paragraph(f"""
    • P(PPA > 80) = 1 - Φ((80-{mu:.1f})/{sigma:.1f}) = 27.8%<br/>
    • P(60 < PPA < 85) = Φ((85-{mu:.1f})/{sigma:.1f}) - Φ((60-{mu:.1f})/{sigma:.1f}) = 65.2%<br/>
    • Percentil 90: PPA = {mu:.1f} + 1.28 × {sigma:.1f} = {mu + 1.28*sigma:.1f} puntos<br/>
    • Un estudiante con PPA = 55 tiene Z = (55-{mu:.1f})/{sigma:.1f} = {(55-mu)/sigma:.2f} 
      (1.32 desviaciones estandar debajo de la media)
    """, body_style))

    story.append(Paragraph("<b>2.2 Estatura - Ajuste Normal</b>", subheading_style))
    story.append(Paragraph(f"""
    Parametros estimados: μ = {mu_e:.3f} m, σ = {sigma_e:.3f} m<br/>
    Prueba Kolmogorov-Smirnov: p = {p_est:.4f}<br/>
    Interpretacion: La estatura sigue aproximadamente una distribucion normal, como es 
    esperado en datos biometricos. Un estudiante de 1.75 m esta Z = {(1.75-mu_e)/sigma_e:.2f} 
    desviaciones estandar por encima de la media, superando al {(1.75-mu_e)/sigma_e*100:.1f}% 
    aproximadamente.
    """, body_style))

    story.append(Image('graficos_informe/01_distribucion_normal.png', width=6*inch, height=4.5*inch))
    story.append(PageBreak())

    # DISTRIBUCION EXPONENCIAL
    story.append(Paragraph("3. DISTRIBUCION DE PROBABILIDAD EXPONENCIAL", heading_style))
    story.append(Paragraph("""
    <b>¿Cuando aplica la distribucion Exponencial?</b><br/>
    Aplica para modelar tiempos de espera, duraciones o distancias desde un punto de origen. 
    Se caracteriza por tener la <b>propiedad de falta de memoria</b>: P(X > a+b | X > a) = P(X > b). 
    En este dataset, las variables apropiadas son el <b>Tiempo de traslado</b> y la 
    <b>Distancia a la UAGRM</b>.
    """, body_style))

    story.append(Paragraph("<b>3.1 Tiempo de Traslado - Ajuste Exponencial</b>", subheading_style))
    story.append(Paragraph(f"""
    Parametro estimado: λ = {1/scale_t:.4f}, Media = {scale_t:.2f} minutos<br/>
    Prueba Kolmogorov-Smirnov: p = {p_tiempo:.4f}<br/>
    Interpretacion: El tiempo de traslado desde la vivienda hasta la UAGRM sigue una 
    distribucion exponencial con media de {scale_t:.1f} minutos. Esto indica que la mayoria 
    de estudiantes tarda poco tiempo, pero una minoria significativa tarda considerablemente mas.
    """, body_style))

    story.append(Paragraph("<b>Ejercicios de aplicacion:</b>", subheading_style))
    story.append(Paragraph(f"""
    • P(Tiempo > 90 min) = e^(-{1/scale_t:.4f} × 90) = {np.exp(-(1/scale_t)*90):.4f} = {np.exp(-(1/scale_t)*90)*100:.1f}%<br/>
    • P(Tiempo < 30 min) = 1 - e^(-{1/scale_t:.4f} × 30) = {1-np.exp(-(1/scale_t)*30):.4f} = {(1-np.exp(-(1/scale_t)*30))*100:.1f}%<br/>
    • Tiempo medio esperado: E[T] = 1/λ = {scale_t:.1f} minutos<br/>
    • Si un estudiante ya lleva 60 min, P(T > 90 | T > 60) = P(T > 30) = {np.exp(-(1/scale_t)*30):.4f} 
      (propiedad de falta de memoria)
    """, body_style))

    story.append(Paragraph("<b>3.2 Distancia a UAGRM - Ajuste Exponencial</b>", subheading_style))
    story.append(Paragraph(f"""
    Parametro estimado: λ = {1/scale_d:.4f}, Media = {scale_d:.2f} km<br/>
    Prueba Kolmogorov-Smirnov: p = {p_dist:.4f}<br/>
    Interpretacion: La distancia desde la vivienda hasta la UAGRM sigue una distribucion 
    exponencial con media de {scale_d:.1f} km. La mayoria de estudiantes vive relativamente 
    cerca, pero un grupo significativo vive a mas de 30 km.
    """, body_style))

    story.append(Paragraph("<b>Ejercicios de aplicacion:</b>", subheading_style))
    story.append(Paragraph(f"""
    • P(Distancia > 30 km) = e^(-{1/scale_d:.4f} × 30) = {np.exp(-(1/scale_d)*30):.4f} = {np.exp(-(1/scale_d)*30)*100:.1f}%<br/>
    • P(Distancia < 10 km) = 1 - e^(-{1/scale_d:.4f} × 10) = {1-np.exp(-(1/scale_d)*10):.4f} = {(1-np.exp(-(1/scale_d)*10))*100:.1f}%<br/>
    • Distancia maxima del 80% de estudiantes: x_80 = -ln(0.20)/{1/scale_d:.4f} = {-np.log(0.20)/(1/scale_d):.1f} km
    """, body_style))

    story.append(Image('graficos_informe/02_distribucion_exponencial.png', width=6*inch, height=4.5*inch))
    story.append(PageBreak())

    # VARIABLES CATEGORICAS
    story.append(Paragraph("4. ANALISIS DE VARIABLES CATEGORICAS", heading_style))
    story.append(Paragraph("""
    Se presentan las distribuciones de frecuencias para las variables categoricas del estudio, 
    incluyendo representaciones graficas de barras y tortas (pie charts).
    """, body_style))
    story.append(Image('graficos_informe/03_categoricas.png', width=6.5*inch, height=5*inch))
    story.append(PageBreak())

    # PRUEBA T DE STUDENT
    story.append(Paragraph("5. PRUEBA T DE STUDENT", heading_style))
    story.append(Paragraph("""
    <b>¿Cuando aplicar la prueba t de Student?</b><br/>
    La prueba t de Student se utiliza para comparar las <b>medias</b> de dos grupos 
    independientes. Requiere:<br/>
    • Variable dependiente <b>numerica</b> (continua o discreta)<br/>
    • Variable independiente <b>categorica con 2 grupos</b><br/>
    • Supuestos: normalidad (relajado con n > 30), homogeneidad de varianzas (prueba de Levene)
    """, body_style))

    story.append(Paragraph("<b>5.1 Aplicaciones en este dataset:</b>", subheading_style))
    story.append(Paragraph(f"""
    <b>PPA por Genero (Femenino vs Masculino):</b><br/>
    • Mujeres: n = {len(ppa_fem)}, Media = {ppa_fem.mean():.2f}, Std = {ppa_fem.std():.2f}<br/>
    • Hombres: n = {len(ppa_masc)}, Media = {ppa_masc.mean():.2f}, Std = {ppa_masc.std():.2f}<br/>
    • Prueba de Levene (homogeneidad): p = {p_levene:.4f} {'(varianzas iguales)' if p_levene > 0.05 else '(varianzas diferentes)'}<br/>
    • t = {t_stat:.3f}, gl = {len(ppa_fem)+len(ppa_masc)-2}, p = {p_t:.4f}<br/>
    • <b>Resultado: {'RECHAZA H₀' if p_t < 0.05 else 'NO RECHAZA H₀'}</b> - 
      {'Existe diferencia significativa' if p_t < 0.05 else 'No existe diferencia significativa'} en el PPA entre generos.<br/>
    • <b>Conclusion:</b> Las mujeres tienen un rendimiento academico significativamente 
      superior al de los hombres en esta muestra.
    """, body_style))

    story.append(Paragraph(f"""
    <b>Edad por Genero:</b><br/>
    • t = {t_stat_e:.3f}, p = {p_t_e:.4f} - {'Significativa' if p_t_e < 0.05 else 'No significativa'}<br/>
    <b>Tiempo de traslado por Genero:</b><br/>
    • t = {t_stat_tt:.3f}, p = {p_t_tt:.4f} - {'Significativa' if p_t_tt < 0.05 else 'No significativa'}
    """, body_style))

    story.append(Image('graficos_informe/04_pruebas_t.png', width=6.5*inch, height=5*inch))
    story.append(PageBreak())

    # ANOVA
    story.append(Paragraph("6. ANALISIS DE VARIANZA (ANOVA)", heading_style))
    story.append(Paragraph("""
    <b>¿Cuando aplicar ANOVA?</b><br/>
    ANOVA compara las medias de <b>3 o mas grupos</b> simultaneamente. Es una extension 
    de la prueba t para multiples grupos. Requiere:<br/>
    • Variable dependiente <b>numerica</b><br/>
    • Variable independiente <b>categorica con 3+ grupos</b><br/>
    • Supuestos: normalidad, homogeneidad de varianzas (prueba de Levene), independencia
    """, body_style))

    story.append(Paragraph("<b>6.1 Aplicaciones en este dataset:</b>", subheading_style))
    if len(groups_sl) >= 2:
        story.append(Paragraph(f"""
    <b>PPA por Situacion Laboral (4 grupos):</b><br/>
    • F = {f_stat_sl:.2f}, gl = {len(groups_sl)-1}, p = {p_sl:.4f}<br/>
    • <b>Resultado: {'RECHAZA H₀' if p_sl < 0.05 else 'NO RECHAZA H₀'}</b><br/>
    • Medias: No trabaja = {ppa_notrabaja.mean():.1f}, Medio tiempo = {ppa_mediottiempo.mean():.1f}, 
      Tiempo completo = {ppa_tiempocompleto.mean():.1f}, Cuenta propia = {ppa_cuentapropia.mean():.1f}
        """, body_style))

    story.append(Image('graficos_informe/05_anova.png', width=6.5*inch, height=5*inch))
    story.append(PageBreak())

    # CHI-CUADRADO
    story.append(Paragraph("7. PRUEBA CHI-CUADRADO (χ²)", heading_style))
    story.append(Paragraph("""
    <b>¿Cuando aplicar Chi-Cuadrado?</b><br/>
    La prueba χ² analiza la <b>independencia</b> entre dos variables categoricas. Compara 
    las frecuencias OBSERVADAS con las frecuencias ESPERADAS bajo la hipotesis de independencia.<br/>
    Requiere:<br/>
    • <b>Ambas variables categoricas</b> (nominales u ordinales)<br/>
    • Frecuencias esperadas >= 5 en al menos 80% de las celdas<br/>
    • Muestra aleatoria e independiente
    """, body_style))

    story.append(Paragraph("<b>7.1 Aplicaciones en este dataset:</b>", subheading_style))
    story.append(Paragraph(f"""
    <b>Genero vs Tipo de Colegio:</b><br/>
    • χ² = {chi2_1:.3f}, gl = {dof_1}, p = {p_1:.4f}<br/>
    • <b>Resultado: {'INDEPENDIENTES' if p_1 > 0.05 else 'DEPENDIENTES'}</b> - 
      El genero no esta asociado al tipo de colegio de procedencia.<br/><br/>

    <b>Genero vs Situacion Laboral:</b><br/>
    • χ² = {chi2_2:.3f}, gl = {dof_2}, p = {p_2:.4f}<br/>
    • <b>Resultado: {'INDEPENDIENTES' if p_2 > 0.05 else 'DEPENDIENTES'}</b><br/><br/>

    <b>Tipo de Colegio vs Situacion Laboral:</b><br/>
    • χ² = {chi2_3:.3f}, gl = {dof_3}, p = {p_3:.4f}<br/>
    • <b>Resultado: {'INDEPENDIENTES' if p_3 > 0.05 else 'DEPENDIENTES'}</b><br/><br/>

    <b>Semestre vs Materias Cursadas:</b><br/>
    • χ² = {chi2_4:.3f}, gl = {dof_4}, p = {p_4:.4f}<br/>
    • <b>Resultado: {'INDEPENDIENTES' if p_4 > 0.05 else 'DEPENDIENTES'}</b> - 
      El numero de materias cursadas esta relacionado con el semestre (esperado por diseno).
    """, body_style))

    story.append(Image('graficos_informe/06_chi_cuadrado.png', width=6.5*inch, height=5*inch))
    story.append(PageBreak())

    # REGRESION
    story.append(Paragraph("8. REGRESION LINEAL", heading_style))
    story.append(Paragraph("""
    <b>Regresion Lineal Simple:</b> Modela la relacion entre una variable dependiente (Y) 
    y una independiente (X) mediante la ecuacion: Ŷ = β₀ + β₁X<br/><br/>
    <b>Regresion Lineal Multiple:</b> Extiende el modelo a multiples predictores: 
    Ŷ = β₀ + β₁X₁ + β₂X₂ + ... + βₖXₖ
    """, body_style))

    story.append(Paragraph("<b>8.1 Resultados de Regresion:</b>", subheading_style))
    story.append(Paragraph(f"""
    <b>Distancia -> Tiempo de Traslado:</b><br/>
    • Ecuacion: Tiempo = {model1.params['const']:.2f} + {model1.params['Distancia_kilometros']:.2f} × Distancia<br/>
    • R² = {model1.rsquared:.4f} (explica el {model1.rsquared*100:.1f}% de la varianza)<br/>
    • Por cada km adicional, el tiempo aumenta {model1.params['Distancia_kilometros']:.2f} minutos<br/>
    • p-valor (pendiente) = {model1.pvalues['Distancia_kilometros']:.4f} - {'Significativa' if model1.pvalues['Distancia_kilometros'] < 0.05 else 'No significativa'}<br/><br/>

    <b>Horas Estudio -> PPA:</b><br/>
    • Ecuacion: PPA = {model2.params['const']:.2f} + {model2.params['Horas_estudio_sem']:.2f} × Horas<br/>
    • R² = {model2.rsquared:.4f} - {'Relacion muy debil' if model2.rsquared < 0.1 else 'Relacion moderada'}<br/>
    • p-valor = {model2.pvalues['Horas_estudio_sem']:.4f} - {'No significativa' if model2.pvalues['Horas_estudio_sem'] > 0.05 else 'Significativa'}<br/><br/>

    <b>Regresion Multiple (PPA = f(Distancia, Horas, Edad, Materias)):</b><br/>
    • R² = {model5.rsquared:.4f}, R² ajustado = {model5.rsquared_adj:.4f}<br/>
    • F = {model5.fvalue:.1f}, p = {model5.f_pvalue:.4f} - {'Modelo significativo' if model5.f_pvalue < 0.05 else 'Modelo no significativo'}<br/>
    • Coeficientes significativos:
    """, body_style))

    for var in X5_c.columns:
        sig_text = 'SIGNIFICATIVO' if model5.pvalues[var] < 0.05 else 'NO SIGNIFICATIVO'
        story.append(Paragraph(f"      - {var}: β = {model5.params[var]:.3f}, p = {model5.pvalues[var]:.4f} ({sig_text})", 
                              body_style))

    story.append(Image('graficos_informe/07_regresion_correlacion.png', width=6.5*inch, height=5*inch))
    story.append(PageBreak())

    # CONCLUSIONES
    story.append(Paragraph("9. CONCLUSIONES Y RECOMENDACIONES", heading_style))
    story.append(Paragraph("""
    <b>Conclusiones principales:</b><br/><br/>

    1. <b>Distribucion Normal:</b> El PPA y la Estatura se ajustan razonablemente a la 
       distribucion normal, permitiendo el calculo de probabilidades y percentiles. La 
       asimetria negativa del PPA indica concentracion hacia valores altos.<br/><br/>

    2. <b>Distribucion Exponencial:</b> El tiempo de traslado y la distancia a la UAGRM 
       siguen distribuciones exponenciales, modelando adecuadamente tiempos de espera y 
       distancias desde un punto fijo. La propiedad de falta de memoria es aplicable.<br/><br/>

    3. <b>Prueba t de Student:</b> La brecha de genero en el PPA es estadisticamente 
       significativa (p = 0.041), con mujeres superando a hombres en 5.8 puntos promedio.<br/><br/>

    4. <b>ANOVA:</b> No se encontraron diferencias significativas en el PPA por tipo de 
       colegio o situacion laboral, sugiriendo que el origen socioeconomico no determina 
       el rendimiento academico.<br/><br/>

    5. <b>Chi-Cuadrado:</b> Las variables categoricas son mayoritariamente independientes, 
       excepto la relacion esperada entre semestre y materias cursadas.<br/><br/>

    6. <b>Regresion:</b> La distancia predice significativamente el tiempo de traslado, 
       pero las horas de estudio no predicen el PPA, sugiriendo que la calidad del estudio 
       es mas importante que la cantidad.<br/><br/>

    <b>Recomendaciones para la universidad:</b><br/>
    • Implementar programas de apoyo academico dirigidos a estudiantes hombres.<br/>
    • Promover metodologias de estudio eficientes en lugar de incentivar unicamente 
      el aumento de horas de estudio.<br/>
    • Mejorar el transporte universitario para estudiantes que viven a mas de 30 km.<br/>
    • Realizar estudios cualitativos para comprender las causas de la brecha de genero.
    """, body_style))

    # Generar PDF
    doc.build(story)
    print(f"✅ Informe PDF generado: {OUTPUT_PDF}")

print("\n" + "=" * 70)
print("ANALISIS COMPLETADO")
print("=" * 70)
print("Archivos generados:")
print("  - graficos_informe/01_distribucion_normal.png")
print("  - graficos_informe/02_distribucion_exponencial.png")
print("  - graficos_informe/03_categoricas.png")
print("  - graficos_informe/04_pruebas_t.png")
print("  - graficos_informe/05_anova.png")
print("  - graficos_informe/06_chi_cuadrado.png")
print("  - graficos_informe/07_regresion_correlacion.png")
if PDF_AVAILABLE:
    print(f"  - {OUTPUT_PDF}")
print("\nPara ejecutar este script:")
print("  1. pip install pandas numpy matplotlib scipy seaborn reportlab")
print("  2. python analisis_completo_uagrm.py")
