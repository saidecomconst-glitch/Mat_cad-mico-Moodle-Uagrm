"""
================================================================================
SCRIPT DE LIMPIEZA Y ANÁLISIS DE DISTRIBUCIONES
Encuesta UAGRM - Estudiantes de Contaduría y otras carreras
Basado en Excel con numeración (primera columna = Nro.)
================================================================================
Requisitos: pip install pandas numpy matplotlib seaborn scipy openpyxl
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
INPUT_FILE = "Encuesta_UAGRM_Limpia.xlsx"   # <-- Excel con numeración
OUTPUT_EXCEL = "Encuesta_UAGRM_Limpia_Final.xlsx"
OUTPUT_PNG = "distribuciones_practicas.png"

# =============================================================================
# 1. CARGAR EXCEL (ya viene con numeración y datos pre-limpios)
# =============================================================================
print("Cargando Excel...")
df = pd.read_excel(INPUT_FILE, sheet_name='Datos_Limpios')
print(f"Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"Columnas: {list(df.columns)}")

# =============================================================================
# 2. LIMPIEZA DE OUTLIERS Y DATOS PROBLEMÁTICOS
# =============================================================================
print("\nLimpiando outliers...")

# PPA: eliminar valores < 30 (errores de tipeo: ej. 5, 20)
# En Bolivia, PPA mínimo aprobatorio es 51. Valores < 30 son errores.
print(f"  PPA < 30 eliminados: {df['PPA'].lt(30).sum()}")
df.loc[df['PPA'] < 30, 'PPA'] = np.nan

# Estatura: eliminar > 2.2m (outlier físico imposible)
print(f"  Estatura > 2.2m eliminados: {df['Estatura_metros'].gt(2.2).sum()}")
df.loc[df['Estatura_metros'] > 2.2, 'Estatura_metros'] = np.nan

# Horas estudio: eliminar > 30 (excesivo, posible confusión con días)
print(f"  Horas estudio > 30 eliminados: {df['Horas_estudio_sem'].gt(30).sum()}")
df.loc[df['Horas_estudio_sem'] > 30, 'Horas_estudio_sem'] = np.nan

# Tiempo traslado: eliminar > 120 min (más de 2 horas es excesivo)
print(f"  Tiempo traslado > 120 min eliminados: {df['Tiempo_traslado_minutos'].gt(120).sum()}")
df.loc[df['Tiempo_traslado_minutos'] > 120, 'Tiempo_traslado_minutos'] = np.nan

# Edad: eliminar > 35 (outlier para estudiante universitario)
print(f"  Edad > 35 eliminados: {df['Edad'].gt(35).sum()}")
df.loc[df['Edad'] > 35, 'Edad'] = np.nan

# Genero: eliminar "Binario" (probable broma)
print(f"  Genero 'Binario' eliminados: {(df['Genero'] == 'Binario').sum()}")
df.loc[df['Genero'] == 'Binario', 'Genero'] = np.nan

# =============================================================================
# 3. RESUMEN DE DATOS FALTANTES
# =============================================================================
print("\n" + "="*60)
print("DATOS FALTANTES DESPUÉS DE LIMPIEZA")
print("="*60)
print(df.isnull().sum())

# =============================================================================
# 4. ESTADÍSTICAS DESCRIBITIVAS
# =============================================================================
print("\n" + "="*60)
print("ESTADÍSTICAS DESCRIBITIVAS")
print("="*60)
numeric_cols = ['Edad', 'PPA', 'Horas_estudio_sem', 'Estatura_metros', 
                'Tiempo_traslado_minutos', 'Distancia_kilometros', 'Materias_cursa']
print(df[numeric_cols].describe().round(2).to_string())

# =============================================================================
# 5. GUARDAR EXCEL LIMPIO
# =============================================================================
print("\nGuardando Excel...")
resumen = df[numeric_cols].describe().round(2)

dist_data = []
for var, title in zip(['PPA', 'Estatura_metros', 'Tiempo_traslado_minutos', 'Distancia_kilometros'],
                       ['PPA', 'Estatura', 'Tiempo_traslado', 'Distancia']):
    data = df[var].dropna()
    if len(data) == 0: continue
    mu, sigma = stats.norm.fit(data)
    loc, scale = stats.expon.fit(data, floc=0)
    dist_data.append({
        'Variable': title, 'N': len(data), 'Media': round(data.mean(), 3),
        'Desv_Std': round(data.std(), 3), 'Min': round(data.min(), 2), 'Max': round(data.max(), 2),
        'Normal_mu': round(mu, 3), 'Normal_sigma': round(sigma, 3),
        'Exp_lambda': round(1/scale, 4) if scale != 0 else np.nan, 'Exp_media': round(scale, 3)
    })
dist_df = pd.DataFrame(dist_data)

with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Datos_Limpios', index=False)
    resumen.to_excel(writer, sheet_name='Resumen_Estadistico')
    dist_df.to_excel(writer, sheet_name='Parametros_Distribuciones', index=False)

print(f"✅ Excel guardado: {OUTPUT_EXCEL}")

# =============================================================================
# 6. GRÁFICOS DE DISTRIBUCIONES
# =============================================================================
print("\nGenerando gráficos...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis de Distribuciones para Prácticas - UAGRM', fontsize=14, fontweight='bold')

# NORMAL: PPA
ax = axes[0, 0]
data = df['PPA'].dropna()
ax.hist(data, bins=15, density=True, alpha=0.6, color='steelblue', edgecolor='black', label='Datos')
mu, sigma = stats.norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label=f'N(μ={mu:.1f}, σ={sigma:.1f})')
ax.set_title('PPA → NORMAL', fontweight='bold')
ax.set_xlabel('PPA (0-100)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# NORMAL: ESTATURA
ax = axes[0, 1]
data = df['Estatura_metros'].dropna()
ax.hist(data, bins=15, density=True, alpha=0.6, color='seagreen', edgecolor='black', label='Datos')
mu, sigma = stats.norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label=f'N(μ={mu:.2f}, σ={sigma:.2f})')
ax.set_title('Estatura → NORMAL', fontweight='bold')
ax.set_xlabel('Estatura (m)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# EXPONENCIAL: TIEMPO TRASLADO
ax = axes[1, 0]
data = df['Tiempo_traslado_minutos'].dropna()
ax.hist(data, bins=20, density=True, alpha=0.6, color='coral', edgecolor='black', label='Datos')
loc, scale = stats.expon.fit(data, floc=0)
x = np.linspace(0, data.max(), 100)
ax.plot(x, stats.expon.pdf(x, loc, scale), 'b-', lw=2, label=f'Exp(λ={1/scale:.4f})')
ax.set_title('Tiempo traslado → EXPONENCIAL', fontweight='bold')
ax.set_xlabel('Tiempo (minutos)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# EXPONENCIAL: DISTANCIA
ax = axes[1, 1]
data = df['Distancia_kilometros'].dropna()
ax.hist(data, bins=15, density=True, alpha=0.6, color='goldenrod', edgecolor='black', label='Datos')
loc, scale = stats.expon.fit(data, floc=0)
x = np.linspace(0, data.max(), 100)
ax.plot(x, stats.expon.pdf(x, loc, scale), 'b-', lw=2, label=f'Exp(λ={1/scale:.4f})')
ax.set_title('Distancia UAGRM → EXPONENCIAL', fontweight='bold')
ax.set_xlabel('Distancia (km)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches='tight')
print(f"✅ Gráfico guardado: {OUTPUT_PNG}")

# =============================================================================
# 7. PRUEBAS DE AJUSTE (Kolmogorov-Smirnov)
# =============================================================================
print("\n" + "="*60)
print("RESULTADOS DE PRUEBAS KOLMOGOROV-SMIRNOV")
print("="*60)

variables_test = [
    ('PPA', 'PPA (Normal)'),
    ('Estatura_metros', 'Estatura (Normal)'),
    ('Tiempo_traslado_minutos', 'Tiempo traslado (Exponencial)'),
    ('Distancia_kilometros', 'Distancia (Exponencial)')
]

for var, label in variables_test:
    data = df[var].dropna()
    if 'Normal' in label:
        mu, sigma = stats.norm.fit(data)
        _, p = stats.kstest(data, 'norm', args=(mu, sigma))
        print(f"{label}: p-valor = {p:.4f} {'✅ Apto' if p > 0.05 else '⚠️ Revisar'}")
    else:
        loc, scale = stats.expon.fit(data, floc=0)
        _, p = stats.kstest(data, 'expon', args=(loc, scale))
        print(f"{label}: p-valor = {p:.4f} {'✅ Apto' if p > 0.05 else '⚠️ Revisar'}")

print("\n" + "="*60)
print("PROCESO COMPLETADO")
print("="*60)
print(f"Archivos generados:")
print(f"  1. {OUTPUT_EXCEL} - Datos limpios en Excel")
print(f"  2. {OUTPUT_PNG} - Gráficos de distribuciones")
