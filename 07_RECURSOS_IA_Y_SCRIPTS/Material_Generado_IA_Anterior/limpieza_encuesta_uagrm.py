"""
================================================================================
SCRIPT DE LIMPIEZA Y ANÁLISIS DE DISTRIBUCIONES
Encuesta UAGRM - Estudiantes de Contaduría y otras carreras
Objetivo: Preparar datos para prácticas de Distribución Normal y Exponencial
================================================================================
Autor: Generado automáticamente
Fecha: 2026-06-29
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
# CONFIGURACIÓN - Modifica esta ruta según tu computadora
# =============================================================================
INPUT_FILE = "Formulario sin título.csv"   # <-- Cambia esto
OUTPUT_EXCEL = "Encuesta_UAGRM_Limpia.xlsx"
OUTPUT_PNG = "distribuciones_practicas.png"

# =============================================================================
# 1. CARGAR DATOS
# =============================================================================
print("Cargando datos...")
df = pd.read_csv(INPUT_FILE)
print(f"Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")

# =============================================================================
# 2. RENOMBRAR COLUMNAS
# =============================================================================
df.columns = [
    'Marca_temporal', 'Genero', 'Edad', 'Tipo_colegio', 'Facultad', 
    'Carrera', 'Semestre', 'Materias', 'PPA', 'Horas_estudio', 
    'Estatura', 'Trabajo', 'Distancia', 'Tiempo_traslado'
]

# =============================================================================
# 3. FUNCIONES DE LIMPIEZA
# =============================================================================

def clean_ppa(val):
    """Extrae solo números del PPA, filtra rango 0-100"""
    if pd.isna(val):
        return np.nan
    match = re.search(r'(\d+)(?:[.,](\d+))?', str(val))
    if match:
        num = float(match.group(0).replace(',', '.'))
        return num if 0 <= num <= 100 else np.nan
    return np.nan

def clean_estatura(val):
    """Normaliza estatura a metros"""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().lower().replace(',', '.').replace(' ', '')
    val_str = val_str.replace('cm', '').replace('metros', '').replace('m', '')
    match = re.search(r'(\d+\.?\d*)', val_str)
    if match:
        num = float(match.group(1))
        if num > 10:  # probablemente está en cm
            num = num / 100
        if 1.0 <= num <= 2.5:
            return round(num, 2)
    return np.nan

def clean_tiempo_traslado(val):
    """
    CORRECCIÓN IMPORTANTE: Valores 1, 2, 3, 4 probablemente son HORAS, no minutos.
    Se multiplican por 60. Valores >= 5 ya están en minutos.
    """
    if pd.isna(val):
        return np.nan
    val = float(val)
    if val <= 4:
        return round(val * 60, 0)
    if val <= 120:
        return val
    return np.nan

def extract_distancia(val):
    """
    Usa el límite inferior del rango para evitar decimales .5 confusos.
    Ej: 'Entre 10 y 15 km' -> 10 km
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).lower()
    rangos = {
        'menos de 1': 0, 'entre 2 y 5': 2, 'entre 5 y 10': 5,
        'entre 10 y 15': 10, 'entre 15 y 20': 15, 'entre 20 y 25': 20,
        'entre 25 y 30': 25, 'entre 30 y 35': 30, 'entre 40 y 45': 40,
        'entre 45 y 50': 45, 'más de 50': 50
    }
    for key, value in rangos.items():
        if key in val_str:
            return value
    match = re.search(r'(\d+)', val_str)
    return int(match.group(1)) if match else np.nan

def extract_materias(val):
    """
    Número entero representativo del rango.
    '1 a 2' -> 1, '3 a 4' -> 3, '5 a 6' -> 5, '7 o más' -> 7
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).lower()
    if '1 a 2' in val_str: return 1
    elif '3 a 4' in val_str: return 3
    elif '5 a 6' in val_str: return 5
    elif '7 o más' in val_str: return 7
    match = re.search(r'(\d+)', val_str)
    return int(match.group(1)) if match else np.nan

def extract_semestre(val):
    """Extrae número de semestre"""
    if pd.isna(val):
        return np.nan
    match = re.search(r'(\d+)', str(val))
    return int(match.group(1)) if match else np.nan

def uniformizar_carrera(val):
    """Uniformiza nombres de carreras"""
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip().lower()

    if any(x in val_str for x in ['contadur', 'contabilidad', 'auditor', 'ciencias contables', 
                                    'información y control', 'informacion y control']):
        return 'Contaduría Pública'
    elif 'bioq' in val_str:
        return 'Bioquímica'
    elif 'farma' in val_str:
        return 'Farmacia'
    elif 'mecánica' in val_str or 'mecanica' in val_str:
        if 'automotriz' in val_str:
            return 'Mecánica Automotriz'
        elif 'general' in val_str:
            return 'Mecánica General'
        elif 'produccion' in val_str or 'producción' in val_str:
            return 'Mecánica de Producción'
        else:
            return 'Mecánica Industrial'
    elif 'alimentos' in val_str:
        return 'Ingeniería de Alimentos'
    elif 'comercial' in val_str or 'economía' in val_str or 'economia' in val_str:
        return 'Ingeniería Comercial'
    elif 'electrónica' in val_str or 'electronica' in val_str:
        return 'Electrónica'
    elif 'electromecánica' in val_str or 'electromecanica' in val_str:
        return 'Ingeniería Electromecánica'
    elif 'redes' in val_str or 'telecomunicaciones' in val_str:
        return 'Ingeniería en Redes y Telecomunicaciones'
    elif 'sistemas' in val_str or 'sistemaa' in val_str:
        return 'Ingeniería en Sistemas'
    elif 'medicina' in val_str:
        return 'Medicina'
    else:
        return val.strip()

# =============================================================================
# 4. APLICAR LIMPIEZA
# =============================================================================
print("Limpiando datos...")

df['PPA_numerico'] = df['PPA'].apply(clean_ppa)
df['Estatura_m'] = df['Estatura'].apply(clean_estatura)
df['Edad_clean'] = df['Edad'].apply(lambda x: x if 17 <= x <= 45 else np.nan)
df['Horas_estudio_clean'] = df['Horas_estudio'].apply(lambda x: x if x <= 70 else np.nan)
df['Tiempo_traslado_clean'] = df['Tiempo_traslado'].apply(clean_tiempo_traslado)
df['Semestre_num'] = df['Semestre'].apply(extract_semestre)
df['Materias_num'] = df['Materias'].apply(extract_materias)
df['Distancia_km'] = df['Distancia'].apply(extract_distancia)

# Facultad: nombres completos (ya vienen completos en el CSV)
df['Facultad_clean'] = df['Facultad'].str.strip()

# Carrera: uniformizar
df['Carrera_clean'] = df['Carrera'].apply(uniformizar_carrera)

# Normalizar categóricas
df['Genero_clean'] = df['Genero'].str.strip().str.title()
df['Tipo_colegio_clean'] = df['Tipo_colegio'].str.strip()
df['Trabajo_clean'] = df['Trabajo'].str.strip()

# =============================================================================
# 5. PREPARAR DATAFRAME FINAL
# =============================================================================
columnas_finales = [
    'Marca_temporal', 'Genero_clean', 'Edad_clean', 'Tipo_colegio_clean', 
    'Facultad_clean', 'Carrera_clean', 'Semestre_num', 'Materias_num',
    'PPA_numerico', 'Horas_estudio_clean', 'Estatura_m', 
    'Trabajo_clean', 'Distancia_km', 'Tiempo_traslado_clean'
]

nombres_amigables = {
    'Marca_temporal': 'Fecha_respuesta',
    'Genero_clean': 'Genero',
    'Edad_clean': 'Edad',
    'Tipo_colegio_clean': 'Tipo_colegio',
    'Facultad_clean': 'Facultad',
    'Carrera_clean': 'Carrera',
    'Semestre_num': 'Semestre',
    'Materias_num': 'Materias_cursa',
    'PPA_numerico': 'PPA',
    'Horas_estudio_clean': 'Horas_estudio_sem',
    'Estatura_m': 'Estatura_metros',
    'Trabajo_clean': 'Situacion_laboral',
    'Distancia_km': 'Distancia_kilometros',
    'Tiempo_traslado_clean': 'Tiempo_traslado_minutos'
}

df_final = df[columnas_finales].rename(columns=nombres_amigables)

# =============================================================================
# 6. GUARDAR EXCEL
# =============================================================================
print("Guardando Excel...")
resumen = df_final[['Edad', 'PPA', 'Horas_estudio_sem', 'Estatura_metros', 
                    'Tiempo_traslado_minutos', 'Distancia_kilometros', 'Materias_cursa']].describe().round(2)

with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    df_final.to_excel(writer, sheet_name='Datos_Limpios', index=False)
    resumen.to_excel(writer, sheet_name='Resumen_Estadistico')

print(f"✅ Excel guardado: {OUTPUT_EXCEL}")

# =============================================================================
# 7. GRÁFICOS DE DISTRIBUCIONES
# =============================================================================
print("Generando gráficos...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Análisis de Distribuciones para Prácticas - UAGRM', fontsize=14, fontweight='bold')

# NORMAL: PPA
ax = axes[0, 0]
data = df_final['PPA'].dropna()
ax.hist(data, bins=15, density=True, alpha=0.6, color='steelblue', edgecolor='black', label='Datos')
mu, sigma = stats.norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label=f'N(μ={mu:.1f}, σ={sigma:.1f})')
ax.set_title('PPA → NORMAL', fontweight='bold')
ax.set_xlabel('PPA (0-100)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# NORMAL: ESTATURA
ax = axes[0, 1]
data = df_final['Estatura_metros'].dropna()
ax.hist(data, bins=15, density=True, alpha=0.6, color='seagreen', edgecolor='black', label='Datos')
mu, sigma = stats.norm.fit(data)
x = np.linspace(data.min(), data.max(), 100)
ax.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', lw=2, label=f'N(μ={mu:.2f}, σ={sigma:.2f})')
ax.set_title('Estatura → NORMAL', fontweight='bold')
ax.set_xlabel('Estatura (m)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# EXPONENCIAL: TIEMPO TRASLADO
ax = axes[1, 0]
data = df_final['Tiempo_traslado_minutos'].dropna()
ax.hist(data, bins=20, density=True, alpha=0.6, color='coral', edgecolor='black', label='Datos')
loc, scale = stats.expon.fit(data, floc=0)
x = np.linspace(0, data.max(), 100)
ax.plot(x, stats.expon.pdf(x, loc, scale), 'b-', lw=2, label=f'Exp(λ={1/scale:.4f})')
ax.set_title('Tiempo traslado → EXPONENCIAL', fontweight='bold')
ax.set_xlabel('Tiempo (minutos)'); ax.set_ylabel('Densidad')
ax.legend(); ax.grid(alpha=0.3)

# EXPONENCIAL: DISTANCIA
ax = axes[1, 1]
data = df_final['Distancia_kilometros'].dropna()
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
# 8. PRUEBAS DE AJUSTE (Kolmogorov-Smirnov)
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
    data = df_final[var].dropna()
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
