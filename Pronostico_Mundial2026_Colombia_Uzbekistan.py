# %%
# =============================================================================
# 🏆 PRONÓSTICO ESTADÍSTICO AVANZADO - MUNDIAL 2026
# Uzbekistan vs Colombia | Grupo K | 17/06/2026 20:00
# Autor: Anselmo Salguero | Maestria en Estadistica Aplicada
# Metodologia: Dataset historico (49,398 partidos) + Modelo Poisson + Monte Carlo
# Fuentes: API worldcup26.ir | GitHub martj42/international_results
# =============================================================================

# %%
# =============================================================================
# CELDA 1: IMPORTACION DE LIBRERIAS
# =============================================================================
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson
import warnings
warnings.filterwarnings('ignore')

# Configuracion visual - Paleta Pastel Profesional
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

COLORES = {
    'celeste': '#A8D8EA', 'naranja': '#FFD3B6', 'amarillo': '#FFF9C4',
    'verde': '#C8E6C9', 'rosa': '#F8BBD0', 'lavanda': '#E1BEE7',
    'gris': '#F5F5F5', 'colombia': '#FCD116', 'colombia_azul': '#003893',
    'uzbekistan': '#1EB53A', 'uzbekistan_azul': '#0099B5'
}

print("Librerias importadas correctamente")
print("pandas:", pd.__version__)
print("numpy:", np.__version__)
print("matplotlib:", plt.matplotlib.__version__)

# %%
# =============================================================================
# CELDA 2: DESCARGA DATASET HISTORICO
# Dataset: GitHub martj42/international_results (49,398 partidos desde 1872)
# =============================================================================
URL_HISTORICO = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

print("Descargando dataset historico...")
df_hist = pd.read_csv(URL_HISTORICO)

print("Dataset cargado:", len(df_hist), "partidos")
print("Rango de fechas:", df_hist['date'].min(), "a", df_hist['date'].max())
print("\nPrimeras filas:")
print(df_hist.head())
print("\nColumnas:", list(df_hist.columns))

# Partidos por decada
df_hist['year'] = pd.to_datetime(df_hist['date']).dt.year
decadas = (df_hist['year'] // 10 * 10).value_counts().sort_index()
print("\nPartidos por decada (ultimas):")
print(decadas.tail(10))

# %%
# =============================================================================
# CELDA 3: FILTRAR PARTIDOS POR EQUIPO
# =============================================================================
# Partidos de Colombia
colombia_home = df_hist[df_hist['home_team'] == 'Colombia'].copy()
colombia_away = df_hist[df_hist['away_team'] == 'Colombia'].copy()
colombia_all = pd.concat([colombia_home, colombia_away]).sort_values('date')

# Partidos de Uzbekistan
uzbekistan_home = df_hist[df_hist['home_team'] == 'Uzbekistan'].copy()
uzbekistan_away = df_hist[df_hist['away_team'] == 'Uzbekistan'].copy()
uzbekistan_all = pd.concat([uzbekistan_home, uzbekistan_away]).sort_values('date')

# Enfrentamientos directos
directos = df_hist[
    ((df_hist['home_team'] == 'Colombia') & (df_hist['away_team'] == 'Uzbekistan')) |
    ((df_hist['home_team'] == 'Uzbekistan') & (df_hist['away_team'] == 'Colombia'))
].copy()

print("=" * 70)
print("COLOMBIA - HISTORIAL INTERNACIONAL")
print("=" * 70)
print("Total partidos:", len(colombia_all))
print("Como local:", len(colombia_home))
print("Como visitante:", len(colombia_away))
print("Primero:", colombia_all['date'].min())
print("Ultimo:", colombia_all['date'].max())

print("\n" + "=" * 70)
print("UZBEKISTAN - HISTORIAL INTERNACIONAL")
print("=" * 70)
print("Total partidos:", len(uzbekistan_all))
print("Como local:", len(uzbekistan_home))
print("Como visitante:", len(uzbekistan_away))
print("Primero:", uzbekistan_all['date'].min())
print("Ultimo:", uzbekistan_all['date'].max())

print("\n" + "=" * 70)
print("ENFRENTAMIENTOS DIRECTOS")
print("=" * 70)
print("Total partidos:", len(directos))
if len(directos) > 0:
    print(directos[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament']].to_string(index=False))
else:
    print("No hay enfrentamientos directos historicos registrados")

# %%
# =============================================================================
# CELDA 4: ESTADISTICAS HISTORICAS DETALLADAS
# =============================================================================

def calcular_stats_equipo(df_home, df_away, nombre_equipo):
    """Calcula estadisticas completas de un equipo."""
    # Como local
    goles_favor_local = df_home['home_score'].sum()
    goles_contra_local = df_home['away_score'].sum()
    victorias_local = len(df_home[df_home['home_score'] > df_home['away_score']])
    empates_local = len(df_home[df_home['home_score'] == df_home['away_score']])
    derrotas_local = len(df_home[df_home['home_score'] < df_home['away_score']])
    pj_local = len(df_home)

    # Como visitante
    goles_favor_away = df_away['away_score'].sum()
    goles_contra_away = df_away['home_score'].sum()
    victorias_away = len(df_away[df_away['away_score'] > df_away['home_score']])
    empates_away = len(df_away[df_away['away_score'] == df_away['home_score']])
    derrotas_away = len(df_away[df_away['away_score'] < df_away['home_score']])
    pj_away = len(df_away)

    # Totales
    pj_total = pj_local + pj_away
    gf_total = goles_favor_local + goles_favor_away
    gc_total = goles_contra_local + goles_contra_away

    stats = {
        'equipo': nombre_equipo,
        'pj_total': pj_total, 'pj_local': pj_local, 'pj_visitante': pj_away,
        'gf_total': gf_total, 'gc_total': gc_total,
        'gf_local': goles_favor_local, 'gc_local': goles_contra_local,
        'gf_visitante': goles_favor_away, 'gc_visitante': goles_contra_away,
        'prom_gf_total': gf_total / pj_total if pj_total > 0 else 0,
        'prom_gc_total': gc_total / pj_total if pj_total > 0 else 0,
        'prom_gf_local': goles_favor_local / pj_local if pj_local > 0 else 0,
        'prom_gc_local': goles_contra_local / pj_local if pj_local > 0 else 0,
        'prom_gf_visitante': goles_favor_away / pj_away if pj_away > 0 else 0,
        'prom_gc_visitante': goles_contra_away / pj_away if pj_away > 0 else 0,
        'victorias_local': victorias_local, 'empates_local': empates_local, 'derrotas_local': derrotas_local,
        'victorias_visitante': victorias_away, 'empates_visitante': empates_away, 'derrotas_visitante': derrotas_away,
        'pct_v_local': victorias_local / pj_local * 100 if pj_local > 0 else 0,
        'pct_e_local': empates_local / pj_local * 100 if pj_local > 0 else 0,
        'pct_d_local': derrotas_local / pj_local * 100 if pj_local > 0 else 0,
        'pct_v_visitante': victorias_away / pj_away * 100 if pj_away > 0 else 0,
        'pct_e_visitante': empates_away / pj_away * 100 if pj_away > 0 else 0,
        'pct_d_visitante': derrotas_away / pj_away * 100 if pj_away > 0 else 0,
    }
    return stats

# Calcular para ambos equipos
stats_col = calcular_stats_equipo(colombia_home, colombia_away, 'Colombia')
stats_uzb = calcular_stats_equipo(uzbekistan_home, uzbekistan_away, 'Uzbekistan')

# Mostrar comparativa
print("=" * 70)
print("COMPARATIVA ESTADISTICA HISTORICA")
print("=" * 70)
print("\n{:<35} {:>15} {:>15}".format('Indicador', 'Colombia', 'Uzbekistan'))
print("-" * 70)
print("{:<35} {:>15,} {:>15,}".format('Partidos jugados (total)', stats_col['pj_total'], stats_uzb['pj_total']))
print("{:<35} {:>15,} {:>15,}".format('Partidos como local', stats_col['pj_local'], stats_uzb['pj_local']))
print("{:<35} {:>15,} {:>15,}".format('Partidos como visitante', stats_col['pj_visitante'], stats_uzb['pj_visitante']))
print("{:<35} {:>15,} {:>15,}".format('Goles a favor (total)', stats_col['gf_total'], stats_uzb['gf_total']))
print("{:<35} {:>15,} {:>15,}".format('Goles en contra (total)', stats_col['gc_total'], stats_uzb['gc_total']))
print("{:<35} {:>15.2f} {:>15.2f}".format('Prom. goles a favor (local)', stats_col['prom_gf_local'], stats_uzb['prom_gf_local']))
print("{:<35} {:>15.2f} {:>15.2f}".format('Prom. goles en contra (local)', stats_col['prom_gc_local'], stats_uzb['prom_gc_local']))
print("{:<35} {:>15.2f} {:>15.2f}".format('Prom. goles a favor (visitante)', stats_col['prom_gf_visitante'], stats_uzb['prom_gf_visitante']))
print("{:<35} {:>15.2f} {:>15.2f}".format('Prom. goles en contra (visitante)', stats_col['prom_gc_visitante'], stats_uzb['prom_gc_visitante']))
print("{:<35} {:>14.1f}% {:>14.1f}%".format('% Victoria como local', stats_col['pct_v_local'], stats_uzb['pct_v_local']))
print("{:<35} {:>14.1f}% {:>14.1f}%".format('% Victoria como visitante', stats_col['pct_v_visitante'], stats_uzb['pct_v_visitante']))
print("{:<35} {:>14.1f}% {:>14.1f}%".format('% Empate como local', stats_col['pct_e_local'], stats_uzb['pct_e_local']))
print("{:<35} {:>14.1f}% {:>14.1f}%".format('% Empate como visitante', stats_col['pct_e_visitante'], stats_uzb['pct_e_visitante']))

# %%
# =============================================================================
# CELDA 5: API MUNDIAL 2026 - DATOS EN TIEMPO REAL
# =============================================================================
BASE_URL = "http://worldcup26.ir"

print("Conectando con API Mundial 2026...")
games_resp = requests.get(f"{BASE_URL}/get/games", timeout=30)
games_data = games_resp.json()['games']
df_games = pd.DataFrame(games_data)

teams_resp = requests.get(f"{BASE_URL}/get/teams", timeout=30)
df_teams = pd.DataFrame(teams_resp.json()['teams'])

# Buscar partido especifico
partido = df_games[
    ((df_games['home_team_name_en'].str.contains('Uzbekistan', case=False, na=False)) & 
     (df_games['away_team_name_en'].str.contains('Colombia', case=False, na=False)))
].iloc[0]

team_local = partido['home_team_name_en']
team_visitante = partido['away_team_name_en']

print("\nPARTIDO ENCONTRADO:")
print("  ", team_local, "vs", team_visitante)
print("  Grupo:", partido['group'])
print("  Fecha:", partido['local_date'])
print("  Estado:", partido['time_elapsed'])
print("  Estadio ID:", partido['stadium_id'])

# Estadisticas del torneo actual
finished = df_games[df_games['finished'] == 'TRUE'].copy()
finished['home_score_num'] = pd.to_numeric(finished['home_score'], errors='coerce')
finished['away_score_num'] = pd.to_numeric(finished['away_score'], errors='coerce')

stats_torneo = {
    'total_partidos': len(finished),
    'promedio_goles_total': (finished['home_score_num'].sum() + finished['away_score_num'].sum()) / len(finished) if len(finished) > 0 else 3.0,
    'promedio_goles_local': finished['home_score_num'].mean() if len(finished) > 0 else 2.0,
    'promedio_goles_visitante': finished['away_score_num'].mean() if len(finished) > 0 else 1.0,
}

print("\nEstadisticas del torneo actual (", stats_torneo['total_partidos'], "partidos finalizados):")
print("  Promedio goles/partido:", round(stats_torneo['promedio_goles_total'], 2))
print("  Local:", round(stats_torneo['promedio_goles_local'], 2))
print("  Visitante:", round(stats_torneo['promedio_goles_visitante'], 2))

# %%
# =============================================================================
# CELDA 6: MODELO POISSON CON DATOS HISTORICOS + TORNEO ACTUAL
# =============================================================================

# FACTORES DE FUERZA basados en datos historicos
if stats_col['pj_visitante'] > 20:
    factor_ofensivo_col = stats_col['prom_gf_visitante'] / max(stats_torneo['promedio_goles_visitante'], 0.5)
    factor_defensivo_col = stats_col['prom_gc_visitante'] / max(stats_torneo['promedio_goles_local'], 0.5)
else:
    factor_ofensivo_col = 1.0
    factor_defensivo_col = 1.0

if stats_uzb['pj_local'] > 20:
    factor_ofensivo_uzb = stats_uzb['prom_gf_local'] / max(stats_torneo['promedio_goles_local'], 0.5)
    factor_defensivo_uzb = stats_uzb['prom_gc_local'] / max(stats_torneo['promedio_goles_visitante'], 0.5)
else:
    factor_ofensivo_uzb = 1.0
    factor_defensivo_uzb = 1.0

# Factor de localia conservador
factor_localia = 1.20

# Calcular lambdas
lambda_local = stats_torneo['promedio_goles_local'] * factor_localia * factor_ofensivo_uzb * (1 / max(factor_defensivo_col, 0.5))
lambda_visitante = stats_torneo['promedio_goles_visitante'] / factor_localia * factor_ofensivo_col * (1 / max(factor_defensivo_uzb, 0.5))

# Ajustar valores extremos
lambda_local = max(min(lambda_local, 4.0), 0.5)
lambda_visitante = max(min(lambda_visitante, 3.0), 0.5)

print("=" * 70)
print("PARAMETROS DEL MODELO POISSON AJUSTADO")
print("=" * 70)
print("\nFactores de ajuste:")
print("  Factor localia:", factor_localia)
print("  Factor ofensivo", team_local, "(historico):", round(factor_ofensivo_uzb, 3))
print("  Factor defensivo", team_local, "(historico):", round(factor_defensivo_uzb, 3))
print("  Factor ofensivo", team_visitante, "(historico):", round(factor_ofensivo_col, 3))
print("  Factor defensivo", team_visitante, "(historico):", round(factor_defensivo_col, 3))
print("\nParametros lambda (goles esperados):")
print("  lambda(" + team_local + ") =", round(lambda_local, 3))
print("  lambda(" + team_visitante + ") =", round(lambda_visitante, 3))
print("\nTotal goles esperados:", round(lambda_local + lambda_visitante, 2))

# %%
# =============================================================================
# CELDA 7: MATRIZ DE PROBABILIDADES Y 1X2
# =============================================================================
max_goles = 7
matriz = np.zeros((max_goles + 1, max_goles + 1))

for i in range(max_goles + 1):
    for j in range(max_goles + 1):
        matriz[i, j] = poisson.pmf(i, lambda_local) * poisson.pmf(j, lambda_visitante)

# Probabilidades 1X2
prob_local = sum(matriz[i, j] for i in range(max_goles+1) for j in range(max_goles+1) if i > j)
prob_empate = sum(matriz[i, j] for i in range(max_goles+1) for j in range(max_goles+1) if i == j)
prob_visitante = sum(matriz[i, j] for i in range(max_goles+1) for j in range(max_goles+1) if i < j)

prob_1x2 = {'1': prob_local, 'X': prob_empate, '2': prob_visitante}

print("=" * 70)
print("PROBABILIDADES 1X2 (Modelo Poisson)")
print("=" * 70)
print("\n  1 (" + team_local + "):", round(prob_1x2['1']*100, 2), "%")
print("  X (Empate):    ", round(prob_1x2['X']*100, 2), "%")
print("  2 (" + team_visitante + "):", round(prob_1x2['2']*100, 2), "%")

# Tabla de resultados mas probables
print("\n" + "=" * 70)
print("TOP 15 RESULTADOS MAS PROBABLES")
print("=" * 70)
resultados_tabla = []
for i in range(max_goles + 1):
    for j in range(max_goles + 1):
        prob = matriz[i, j] * 100
        if prob > 0.1:
            resultados_tabla.append({
                'Marcador': str(i) + "-" + str(j),
                'Resultado': '1' if i > j else ('X' if i == j else '2'),
                'Probabilidad': round(prob, 2)
            })

df_resultados = pd.DataFrame(resultados_tabla)
df_resultados = df_resultados.sort_values('Probabilidad', ascending=False)
print(df_resultados.head(15).to_string(index=False))

# %%
# =============================================================================
# CELDA 8: SIMULACION MONTE CARLO (10,000 ITERACIONES)
# =============================================================================
np.random.seed(42)
n_sim = 10000

goles_l = np.random.poisson(lambda_local, n_sim)
goles_v = np.random.poisson(lambda_visitante, n_sim)

mc = pd.DataFrame({
    'goles_local': goles_l,
    'goles_visitante': goles_v
})
mc['resultado'] = mc.apply(
    lambda r: '1' if r['goles_local'] > r['goles_visitante'] else 
              ('X' if r['goles_local'] == r['goles_visitante'] else '2'), axis=1)
mc['total_goles'] = mc['goles_local'] + mc['goles_visitante']
mc['diferencia'] = mc['goles_local'] - mc['goles_visitante']

probs_mc = mc['resultado'].value_counts(normalize=True)

print("=" * 70)
print("MONTE CARLO -", n_sim, "SIMULACIONES")
print("=" * 70)
for res, prob in probs_mc.items():
    nombre = team_local if res == '1' else (team_visitante if res == '2' else 'Empate')
    print("  ", res, "(" + nombre + "):", round(prob*100, 2), "%")

# Marcador mas probable
top_marcador = mc.groupby(['goles_local', 'goles_visitante']).size().sort_values(ascending=False).head(1)
marcador_prob = (top_marcador.values[0] / n_sim) * 100
gl, gv = top_marcador.index[0]

print("\nMarcador mas probable:", gl, "-", gv, "(", round(marcador_prob, 1), "%)")
print("\nEstadisticas adicionales:")
print("  Media goles", team_local, ":", round(mc['goles_local'].mean(), 2))
print("  Media goles", team_visitante, ":", round(mc['goles_visitante'].mean(), 2))
print("  Media total goles:", round(mc['total_goles'].mean(), 2))
print("  Over 2.5:", round((mc['total_goles'] > 2.5).mean()*100, 1), "%")
print("  Under 2.5:", round((mc['total_goles'] <= 2.5).mean()*100, 1), "%")
print("  Ambos anotan:", round(((mc['goles_local'] > 0) & (mc['goles_visitante'] > 0)).mean()*100, 1), "%")
print("  Solo local anota:", round(((mc['goles_local'] > 0) & (mc['goles_visitante'] == 0)).mean()*100, 1), "%")
print("  Solo visitante anota:", round(((mc['goles_local'] == 0) & (mc['goles_visitante'] > 0)).mean()*100, 1), "%")

# %%
# =============================================================================
# CELDA 9: GRAFICO 1 - MATRIZ DE PROBABILIDADES (HEATMAP)
# =============================================================================
fig, ax = plt.subplots(figsize=(12, 10))

annot = np.empty_like(matriz, dtype=object)
for i in range(matriz.shape[0]):
    for j in range(matriz.shape[1]):
        annot[i, j] = str(round(matriz[i, j]*100, 1)) + "%"

sns.heatmap(matriz, annot=annot, fmt='', cmap='YlOrRd', 
            cbar_kws={'label': 'Probabilidad'},
            linewidths=1, linecolor='white',
            ax=ax, vmin=0, vmax=matriz.max())

ax.set_xlabel('Goles ' + team_visitante + ' (Visitante)', fontsize=13, fontweight='bold')
ax.set_ylabel('Goles ' + team_local + ' (Local)', fontsize=13, fontweight='bold')
ax.set_title(
    'MATRIZ DE PROBABILIDADES - RESULTADOS POSIBLES\n' +
    team_local + ' vs ' + team_visitante + ' | Mundial 2026 | Grupo K\n' +
    'lambda(' + team_local + ') = ' + str(round(lambda_local, 2)) + ' | lambda(' + team_visitante + ') = ' + str(round(lambda_visitante, 2)),
    fontsize=14, fontweight='bold', pad=20
)

# Resaltar diagonal (empates)
for i in range(min(matriz.shape)):
    ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False, edgecolor='#003893', lw=3))

plt.tight_layout()
plt.show()

# %%
# =============================================================================
# CELDA 10: GRAFICO 2 - DISTRIBUCION DE GOLES (POISSON)
# =============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

goles_range = range(0, 8)

# Local
probs_local = [poisson.pmf(k, lambda_local) * 100 for k in goles_range]
bars1 = ax1.bar(goles_range, probs_local, color=COLORES['verde'], 
                edgecolor='white', linewidth=2, width=0.7)
ax1.set_xlabel('Goles', fontsize=12, fontweight='bold')
ax1.set_ylabel('Probabilidad (%)', fontsize=12, fontweight='bold')
ax1.set_title(team_local + ' (Local)\nlambda = ' + str(round(lambda_local, 2)) + ' goles esperados', 
              fontsize=13, fontweight='bold')
ax1.set_xticks(list(goles_range))
ax1.set_ylim(0, max(probs_local) * 1.25)
ax1.grid(axis='y', alpha=0.3)

for bar, prob in zip(bars1, probs_local):
    height = bar.get_height()
    ax1.annotate(str(round(prob, 1)) + '%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Visitante
probs_visitante = [poisson.pmf(k, lambda_visitante) * 100 for k in goles_range]
bars2 = ax2.bar(goles_range, probs_visitante, color=COLORES['amarillo'], 
                edgecolor='white', linewidth=2, width=0.7)
ax2.set_xlabel('Goles', fontsize=12, fontweight='bold')
ax2.set_ylabel('Probabilidad (%)', fontsize=12, fontweight='bold')
ax2.set_title(team_visitante + ' (Visitante)\nlambda = ' + str(round(lambda_visitante, 2)) + ' goles esperados', 
              fontsize=13, fontweight='bold')
ax2.set_xticks(list(goles_range))
ax2.set_ylim(0, max(probs_visitante) * 1.25)
ax2.grid(axis='y', alpha=0.3)

for bar, prob in zip(bars2, probs_visitante):
    height = bar.get_height()
    ax2.annotate(str(round(prob, 1)) + '%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.suptitle('DISTRIBUCION DE POISSON - GOLES ESPERADOS', 
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# %%
# =============================================================================
# CELDA 11: GRAFICO 3 - MONTE CARLO (4 PANELES)
# =============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Pie 1X2
ax1 = axes[0, 0]
probs = mc['resultado'].value_counts(normalize=True) * 100
colores_pie = [COLORES['verde'], COLORES['amarillo'], COLORES['naranja']]
labels_pie = [
    '1 (' + team_local + '): ' + str(round(probs.get('1', 0), 1)) + '%',
    'X (Empate): ' + str(round(probs.get('X', 0), 1)) + '%',
    '2 (' + team_visitante + '): ' + str(round(probs.get('2', 0), 1)) + '%'
]
wedges, texts = ax1.pie(probs.values, labels=labels_pie, startangle=90, 
                         colors=colores_pie, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax1.set_title('PROBABILIDADES 1X2\n(Monte Carlo)', fontsize=13, fontweight='bold')

# 2. Total goles
ax2 = axes[0, 1]
total_goles = mc['total_goles']
ax2.hist(total_goles, bins=range(0, total_goles.max()+2), color=COLORES['celeste'], 
         edgecolor='white', linewidth=2, alpha=0.8, density=True)
ax2.set_xlabel('Total de Goles', fontsize=12, fontweight='bold')
ax2.set_ylabel('Densidad', fontsize=12, fontweight='bold')
ax2.set_title('DISTRIBUCION TOTAL DE GOLES', fontsize=13, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
ax2.axvline(total_goles.mean(), color='#CE1126', linestyle='--', linewidth=2, 
            label='Media: ' + str(round(total_goles.mean(), 2)))
ax2.legend(fontsize=11)

# 3. Top 10 resultados
ax3 = axes[1, 0]
top_resultados = mc.groupby(['goles_local', 'goles_visitante']).size().sort_values(ascending=False).head(10)
top_resultados_pct = (top_resultados / n_sim) * 100
etiquetas = [str(g[0]) + "-" + str(g[1]) for g in top_resultados.index]
colores_barras = [COLORES['verde'] if g[0] > g[1] else 
                  (COLORES['amarillo'] if g[0] == g[1] else COLORES['naranja']) 
                  for g in top_resultados.index]

bars = ax3.barh(range(len(etiquetas)), top_resultados_pct.values, color=colores_barras,
                edgecolor='white', linewidth=2)
ax3.set_yticks(range(len(etiquetas)))
ax3.set_yticklabels(etiquetas)
ax3.set_xlabel('Probabilidad (%)', fontsize=12, fontweight='bold')
ax3.set_title('TOP 10 RESULTADOS MAS PROBABLES', fontsize=13, fontweight='bold')
ax3.invert_yaxis()
ax3.grid(axis='x', alpha=0.3)

for i, (bar, pct) in enumerate(zip(bars, top_resultados_pct.values)):
    width = bar.get_width()
    ax3.annotate(str(round(pct, 1)) + '%', xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center', fontsize=10, fontweight='bold')

# 4. Diferencia goles
ax4 = axes[1, 1]
diff_goles = mc['diferencia']
ax4.hist(diff_goles, bins=range(diff_goles.min(), diff_goles.max()+2), 
         color=COLORES['lavanda'], edgecolor='white', linewidth=2, alpha=0.8)
ax4.set_xlabel('Diferencia (Local - Visitante)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
ax4.set_title('DISTRIBUCION DIFERENCIA DE GOLES', fontsize=13, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
ax4.axvline(0, color='#CE1126', linestyle='--', linewidth=2, label='Empate (0)')
ax4.legend(fontsize=11)

plt.suptitle('SIMULACION MONTE CARLO - ' + str(n_sim) + ' ITERACIONES\n' + team_local + ' vs ' + team_visitante, 
             fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# %%
# =============================================================================
# CELDA 12: GRAFICO 4 - RESUMEN EJECUTIVO
# =============================================================================
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)

# Titulo
fig.suptitle(
    'PRONOSTICO ESTADISTICO AVANZADO - MUNDIAL 2026\n' +
    team_local + ' vs ' + team_visitante + ' | Grupo K | 17/06/2026 20:00\n' +
    'Modelo: Poisson + Monte Carlo + Datos Historicos',
    fontsize=16, fontweight='bold', y=0.98
)

# Panel 1: 1X2 barras
ax1 = fig.add_subplot(gs[0, :2])
resultados_labels = ['1 (Local)', 'X (Empate)', '2 (Visitante)']
probabilidades = [prob_1x2['1']*100, prob_1x2['X']*100, prob_1x2['2']*100]
colores = [COLORES['verde'], COLORES['amarillo'], COLORES['naranja']]

bars = ax1.bar(resultados_labels, probabilidades, color=colores, edgecolor='white', linewidth=3, width=0.6)
ax1.set_ylabel('Probabilidad (%)', fontsize=12, fontweight='bold')
ax1.set_title('PROBABILIDADES DE RESULTADO FINAL', fontsize=14, fontweight='bold')
ax1.set_ylim(0, max(probabilidades) * 1.3)
ax1.grid(axis='y', alpha=0.3)

for bar, prob in zip(bars, probabilidades):
    height = bar.get_height()
    ax1.annotate(str(round(prob, 1)) + '%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=14, fontweight='bold')

# Panel 2: Goles esperados
ax2 = fig.add_subplot(gs[0, 2])
equipos = [team_local, team_visitante]
lambdas = [lambda_local, lambda_visitante]
colores_goles = [COLORES['verde'], COLORES['amarillo']]

bars2 = ax2.bar(equipos, lambdas, color=colores_goles, edgecolor='white', linewidth=2, width=0.5)
ax2.set_ylabel('Goles Esperados (lambda)', fontsize=11, fontweight='bold')
ax2.set_title('GOLES ESPERADOS', fontsize=13, fontweight='bold')
ax2.set_ylim(0, max(lambdas) * 1.5)

for bar, lam in zip(bars2, lambdas):
    height = bar.get_height()
    ax2.annotate(str(round(lam, 2)), xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=12, fontweight='bold')

# Panel 3: Estadisticas
ax3 = fig.add_subplot(gs[1, :])
stats_text = (
    "BASE ESTADISTICA DEL MODELO\n" +
    "   Dataset historico: " + str(len(df_hist)) + " partidos (1872-2024)\n" +
    "   Partidos torneo actual: " + str(stats_torneo['total_partidos']) + " finalizados\n" +
    "   Promedio goles/partido (torneo): " + str(round(stats_torneo['promedio_goles_total'], 2)) + "\n" +
    "   Promedio goles local (torneo): " + str(round(stats_torneo['promedio_goles_local'], 2)) + "\n" +
    "   Promedio goles visitante (torneo): " + str(round(stats_torneo['promedio_goles_visitante'], 2)) + "\n" +
    "\n" +
    "PRONOSTICO PRINCIPAL\n" +
    "   Resultado mas probable: " + resultados_labels[np.argmax(probabilidades)] + " (" + str(round(max(probabilidades), 1)) + "%)\n" +
    "   Marcador mas probable: " + str(gl) + "-" + str(gv) + " (" + str(round(marcador_prob, 1)) + "%)\n" +
    "   Total goles esperados: " + str(round(lambda_local + lambda_visitante, 2)) + "\n" +
    "   Over 2.5: " + str(round((mc['total_goles'] > 2.5).mean()*100, 1)) + "% | Ambos anotan: " + str(round(((mc['goles_local'] > 0) & (mc['goles_visitante'] > 0)).mean()*100, 1)) + "%"
)
ax3.text(0.05, 0.95, stats_text, transform=ax3.transAxes, fontsize=11,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor=COLORES['gris'], alpha=0.8, edgecolor='gray'))
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# Panel 4: Intervalos confianza
ax4 = fig.add_subplot(gs[2, :])
ax4.text(0.5, 0.5, 
         'INTERVALOS DE CONFIANZA AL 95% (Distribucion Poisson)\n\n' +
         '• Goles ' + team_local + ': [' + str(round(max(0, lambda_local - 1.96*np.sqrt(lambda_local)), 1)) + ', ' + str(round(lambda_local + 1.96*np.sqrt(lambda_local), 1)) + ']\n' +
         '• Goles ' + team_visitante + ': [' + str(round(max(0, lambda_visitante - 1.96*np.sqrt(lambda_visitante)), 1)) + ', ' + str(round(lambda_visitante + 1.96*np.sqrt(lambda_visitante), 1)) + ']\n' +
         '• Total goles: [' + str(round(max(0, (lambda_local + lambda_visitante) - 1.96*np.sqrt(lambda_local + lambda_visitante)), 1)) + ', ' +
         str(round((lambda_local + lambda_visitante) + 1.96*np.sqrt(lambda_local + lambda_visitante), 1)) + ']\n' +
         '\nNota: El modelo se actualiza automaticamente con datos del torneo. ' +
         'Reejecutar esta celda despues de cada jornada mejora la precision.',
         transform=ax4.transAxes, fontsize=12, verticalalignment='center', horizontalalignment='center',
         bbox=dict(boxstyle='round', facecolor=COLORES['amarillo'], alpha=0.6, edgecolor='orange'))
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')

plt.show()

# %%
# =============================================================================
# CELDA 13: COMPARATIVA DE PLANTILLAS Y VALOR DE MERCADO
# =============================================================================
# Datos de plantillas (fuente: ESPN / Transfermarkt, Junio 2026)
plantilla_data = {
    'Indicador': [
        'Valor total plantilla (EUR M)',
        'Jugador mas valioso (EUR M)',
        'Jugadores top 5 ligas',
        'Experiencia Mundial',
        'Edad promedio',
        'Entrenador',
        'Ranking FIFA aprox.',
        'Factor localia',
        'Debutante Mundial'
    ],
    'Colombia': [
        '302.35', 'Luis Diaz 70.0', '8+', '6 participaciones', '~28', 'Nestor Lorenzo', '15-20', 'No (visitante)', 'No'
    ],
    'Uzbekistan': [
        '85.33', 'Khusanov 15.0', '2-3', '0 (debutante)', '~27', 'Fabio Cannavaro', '70-80', 'Si (local)', 'Si'
    ]
}

df_plantilla = pd.DataFrame(plantilla_data)
print("=" * 70)
print("COMPARATIVA DE PLANTILLAS - MUNDIAL 2026")
print("=" * 70)
print(df_plantilla.to_string(index=False))

# Grafico comparativo de valor de mercado
fig, ax = plt.subplots(figsize=(10, 6))

equipos_comp = ['Colombia', 'Uzbekistan']
valores = [302.35, 85.33]
colores_comp = [COLORES['amarillo'], COLORES['verde']]

bars = ax.bar(equipos_comp, valores, color=colores_comp, edgecolor='white', linewidth=3, width=0.5)
ax.set_ylabel('Valor de Mercado (Millones EUR)', fontsize=12, fontweight='bold')
ax.set_title('VALOR DE PLANTILLA - COMPARATIVA\n(Fuente: Transfermarkt, Junio 2026)', 
             fontsize=14, fontweight='bold')
ax.set_ylim(0, max(valores) * 1.3)
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, valores):
    height = bar.get_height()
    ax.annotate('EUR ' + str(round(val, 2)) + 'M', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.show()

# %%
# =============================================================================
# CELDA 14: EXPORTAR RESULTADOS A CSV
# =============================================================================
output_file = 'pronostico_colombia_uzbekistan_2026.csv'
df_resultados.to_csv(output_file, index=False)
print("Resultados exportados a:", output_file)
print("\nResumen final del pronostico:")
print("  Equipos:", team_local, "vs", team_visitante)
print("  Fecha: 17/06/2026 20:00")
print("  Modelo: Poisson + Monte Carlo + Historico")
print("  1:", round(prob_1x2['1']*100, 1), "% | X:", round(prob_1x2['X']*100, 1), "% | 2:", round(prob_1x2['2']*100, 1), "%")
print("\nPara actualizar el modelo: reejecutar desde la Celda 5 despues de cada jornada")
