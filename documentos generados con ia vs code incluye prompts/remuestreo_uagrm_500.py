"""
================================================================================
SCRIPT DE REMUESTREO (BOOTSTRAP) - ENCUESTA UAGRM
Genera 500 observaciones simuladas a partir de 125 originales
Método: Bootstrap paramétrico con preservación de correlaciones (Cholesky)
================================================================================
Requisitos: pip install pandas numpy matplotlib scipy openpyxl
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm, expon
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
INPUT_FILE = "Encuesta_UAGRM_Limpia_Final.xlsx"  # Excel original con 125 obs
OUTPUT_EXCEL = "Encuesta_UAGRM_500_Simuladas.xlsx"
OUTPUT_PNG = "comparacion_original_simulado.png"
N_SIM = 500  # Número de observaciones simuladas
SEED = 123   # Semilla para reproducibilidad

np.random.seed(SEED)

# =============================================================================
# 1. CARGAR DATOS ORIGINALES
# =============================================================================
print("Cargando datos originales...")
df_orig = pd.read_excel(INPUT_FILE, sheet_name='Datos_Limpios')
print(f"Original: {len(df_orig)} observaciones")

# =============================================================================
# 2. EXTRAER PARÁMETROS DE DISTRIBUCIONES ORIGINALES
# =============================================================================
print("\nExtrayendo parámetros...")

numeric_vars = ['Edad', 'PPA', 'Horas_estudio_sem', 'Estatura_metros', 
                'Tiempo_traslado_minutos', 'Distancia_kilometros']

params = {}
for var in numeric_vars:
    data = df_orig[var].dropna()
    mu_n, sigma_n = norm.fit(data)
    loc_e, scale_e = expon.fit(data, floc=0)
    params[var] = {
        'mean': data.mean(), 'std': data.std(), 'median': data.median(),
        'min': data.min(), 'max': data.max(),
        'normal_mu': mu_n, 'normal_sigma': sigma_n,
        'exp_scale': scale_e
    }

# Probabilidades categóricas
cat_probs = {}
for col in ['Genero', 'Tipo_colegio', 'Facultad', 'Situacion_laboral']:
    cat_probs[col] = df_orig[col].value_counts(normalize=True, dropna=True).to_dict()

# Probabilidades condicionales
sem_probs = df_orig['Semestre'].value_counts(normalize=True, dropna=True).to_dict()
mat_probs = df_orig['Materias_cursa'].value_counts(normalize=True, dropna=True).to_dict()

# Mapeos
fac_carrera_map = {
    'Facultad de Ciencias Contables, Auditoría, Sistemas de Control de Gestión y Finanzas': 
        ['Contaduría Pública'],
    'Facultad de Ciencias Farmacéuticas y Bioquímicas': 
        ['Bioquímica', 'Farmacia'],
    'Facultad Politécnica': 
        ['Mecánica Industrial', 'Mecánica Automotriz', 'Mecánica General', 
         'Mecánica de Producción', 'Electrónica'],
    'Facultad de Ciencias Exactas y Tecnología': 
        ['Ingeniería de Alimentos', 'Ingeniería en Sistemas', 'Ingeniería en Redes y Telecomunicaciones'],
    'Facultad de Ciencias Económicas y Empresariales': 
        ['Ingeniería Comercial'],
    'Facultad de Ciencias de la Salud Humana': 
        ['Medicina'],
    'Facultad de Ingeniería en Ciencias de la Computación y Telecomunicaciones': 
        ['Ingeniería en Sistemas']
}

carrera_probs_raw = {
    'Contaduría Pública': 1.0,
    'Bioquímica': 0.689, 'Farmacia': 0.311,
    'Mecánica Industrial': 0.667, 'Mecánica Automotriz': 0.222, 
    'Mecánica General': 0.111, 'Mecánica de Producción': 0.056, 'Electrónica': 0.056,
    'Ingeniería de Alimentos': 0.5, 'Ingeniería en Sistemas': 0.25, 'Ingeniería en Redes y Telecomunicaciones': 0.25,
    'Ingeniería Comercial': 1.0,
    'Medicina': 1.0
}

sem_materias_map = {
    1: [5, 7], 2: [1, 5], 3: [3, 5, 7], 4: [1, 3, 5, 7],
    5: [3, 5, 7], 6: [3, 5], 7: [3, 5, 7], 8: [1, 3, 5, 7],
    9: [3, 5], 10: [1, 3, 5, 7]
}
sem_materias_probs = {
    1: [0.7, 0.3], 2: [0.6, 0.4], 3: [0.3, 0.5, 0.2], 4: [0.2, 0.2, 0.4, 0.2],
    5: [0.2, 0.5, 0.3], 6: [0.4, 0.6], 7: [0.2, 0.4, 0.4], 8: [0.2, 0.2, 0.3, 0.3],
    9: [0.5, 0.5], 10: [0.3, 0.2, 0.3, 0.2]
}

# =============================================================================
# 3. GENERAR VARIABLES CATEGÓRICAS
# =============================================================================
print("\nGenerando variables categóricas...")
df_sim = pd.DataFrame(index=range(N_SIM))

# Género (excluyendo Binario)
gen_options = ['Femenino', 'Masculino']
gen_probs = [0.718, 0.282]
df_sim['Genero'] = np.random.choice(gen_options, size=N_SIM, p=gen_probs)

# Tipo de colegio
col_options = list(cat_probs['Tipo_colegio'].keys())
col_probs = list(cat_probs['Tipo_colegio'].values())
df_sim['Tipo_colegio'] = np.random.choice(col_options, size=N_SIM, p=col_probs)

# Facultad
fac_options = list(cat_probs['Facultad'].keys())
fac_probs = list(cat_probs['Facultad'].values())
df_sim['Facultad'] = np.random.choice(fac_options, size=N_SIM, p=fac_probs)

# Carrera (dependiente de Facultad)
def assign_carrera(facultad):
    carreras = fac_carrera_map[facultad]
    probs = np.array([carrera_probs_raw.get(c, 1.0) for c in carreras])
    probs = probs / sum(probs)
    return np.random.choice(carreras, p=probs)

df_sim['Carrera'] = df_sim['Facultad'].apply(assign_carrera)

# Semestre
sem_options = list(sem_probs.keys())
sem_probs_list = list(sem_probs.values())
df_sim['Semestre'] = np.random.choice(sem_options, size=N_SIM, p=sem_probs_list)

# Materias (dependiente de Semestre)
def assign_materias(semestre):
    materias = sem_materias_map[semestre]
    probs = np.array(sem_materias_probs[semestre])
    probs = probs / sum(probs)
    return np.random.choice(materias, p=probs)

df_sim['Materias_cursa'] = df_sim['Semestre'].apply(assign_materias)

# Situación laboral
trab_options = list(cat_probs['Situacion_laboral'].keys())
trab_probs_list = list(cat_probs['Situacion_laboral'].values())
df_sim['Situacion_laboral'] = np.random.choice(trab_options, size=N_SIM, p=trab_probs_list)

print("✅ Categóricas generadas")

# =============================================================================
# 4. GENERAR VARIABLES NUMÉRICAS CON CORRELACIONES (Cholesky)
# =============================================================================
print("Generando variables numéricas con correlaciones preservadas...")

# Matriz de correlación original
corr_target = np.array([
    [1.000, -0.015, 0.003, 0.120, -0.121, -0.010],
    [-0.015, 1.000, 0.032, -0.165, 0.105, 0.132],
    [0.003, 0.032, 1.000, 0.077, -0.056, 0.094],
    [0.120, -0.165, 0.077, 1.000, -0.209, -0.284],
    [-0.121, 0.105, -0.056, -0.209, 1.000, 0.298],
    [-0.010, 0.132, 0.094, -0.284, 0.298, 1.000]
])

# Asegurar matriz definida positiva
eigenvalues, eigenvectors = np.linalg.eigh(corr_target)
eigenvalues = np.maximum(eigenvalues, 0.001)
corr_pd = eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
d = np.diag(corr_pd)
corr_pd = corr_pd / np.sqrt(np.outer(d, d))

# Cholesky
L = np.linalg.cholesky(corr_pd)

# Generar normales independientes y aplicar correlaciones
Z = np.random.randn(N_SIM, 6)
X_corr = Z @ L.T

# Transformar a distribuciones originales
var_names = ['Edad', 'PPA', 'Horas_estudio_sem', 'Estatura_metros', 
             'Tiempo_traslado_minutos', 'Distancia_kilometros']

for i, var in enumerate(var_names):
    z = X_corr[:, i]
    p = norm.cdf(z)

    if var == 'Edad':
        vals = norm.ppf(p, params[var]['normal_mu'], params[var]['normal_sigma'])
        vals = np.clip(np.round(vals), 17, 35).astype(int)
    elif var == 'PPA':
        vals = norm.ppf(p, params[var]['normal_mu'], params[var]['normal_sigma'])
        vals = np.clip(np.round(vals), 42, 100).astype(int)
    elif var == 'Horas_estudio_sem':
        vals = np.zeros(N_SIM)
        mask = p > 0.25
        vals[mask] = np.random.exponential(params[var]['exp_scale'], mask.sum())
        vals = np.clip(np.round(vals), 0, 30).astype(int)
    elif var == 'Estatura_metros':
        vals = np.zeros(N_SIM)
        for j in range(N_SIM):
            if df_sim.iloc[j]['Genero'] == 'Femenino':
                vals[j] = norm.ppf(p[j], 1.60, 0.06)
            else:
                vals[j] = norm.ppf(p[j], 1.72, 0.07)
        vals = np.clip(np.round(vals, 2), 1.50, 1.85)
    elif var == 'Distancia_kilometros':
        vals = expon.ppf(p, scale=params[var]['exp_scale'])
        vals = np.clip(np.round(vals), 0, 50).astype(int)
    elif var == 'Tiempo_traslado_minutos':
        # Depende de distancia (generada arriba)
        pass

    df_sim[var] = vals

# Tiempo de traslado: depende de distancia + correlación
z_time = X_corr[:, 4]
dist_vals = df_sim['Distancia_kilometros'].values
time_sim = 50.11 + 0.56 * dist_vals + z_time * 28
time_sim = np.clip(np.round(time_sim), 7, 120).astype(int)
df_sim['Tiempo_traslado_minutos'] = time_sim

# Añadir número
df_sim.insert(0, 'Nro.', range(1, N_SIM + 1))

print(f"✅ Dataset simulado: {len(df_sim)} observaciones")

# =============================================================================
# 5. GUARDAR EXCEL
# =============================================================================
print("\nGuardando Excel...")

resumen_sim = df_sim[numeric_vars].describe().round(2)

with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    df_sim.to_excel(writer, sheet_name='Datos_Simulados_500', index=False)
    resumen_sim.to_excel(writer, sheet_name='Resumen_Estadistico')

print(f"✅ Excel guardado: {OUTPUT_EXCEL}")

# =============================================================================
# 6. GRÁFICOS COMPARATIVOS
# =============================================================================
print("\nGenerando gráficos comparativos...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Comparación Original vs Simulado (Bootstrap)', fontsize=14, fontweight='bold')

for idx, var in enumerate(numeric_vars):
    ax = axes[idx // 3, idx % 3]
    orig_data = df_orig[var].dropna()
    sim_data = df_sim[var].dropna()

    ax.hist(orig_data, bins=20, density=True, alpha=0.5, color='blue', 
            label=f'Original (n={len(orig_data)})', edgecolor='black')
    ax.hist(sim_data, bins=20, density=True, alpha=0.5, color='red', 
            label=f'Simulado (n={len(sim_data)})', edgecolor='black')

    ax.set_title(var, fontweight='bold')
    ax.set_ylabel('Densidad')
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(OUTPUT_PNG, dpi=150, bbox_inches='tight')
print(f"✅ Gráfico guardado: {OUTPUT_PNG}")

print("\n" + "="*60)
print("PROCESO COMPLETADO")
print("="*60)
print(f"Archivos generados:")
print(f"  1. {OUTPUT_EXCEL} - 500 observaciones simuladas")
print(f"  2. {OUTPUT_PNG} - Gráficos comparativos")
