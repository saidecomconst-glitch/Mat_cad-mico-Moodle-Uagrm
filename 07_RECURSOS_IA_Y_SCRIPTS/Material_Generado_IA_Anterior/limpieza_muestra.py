# ============================================================
# LIMPIEZA Y MUESTREO DE CONTACTOS - UAGRM ESTADÍSTICA
# V4: Corregido error de NaN en filas
# ============================================================

import pandas as pd

# ============================================================
# 1. LEER ARCHIVO SIN ENCABEZADOS
# ============================================================
print("=" * 60)
print("LEYENDO ARCHIVO (modo raw)...")
print("=" * 60)

df_raw = pd.read_excel("Estudiantescont.xlsx", header=None)
print(f"✓ Filas totales leídas: {len(df_raw)}")

# ============================================================
# 2. DETECTAR Y FILTRAR FILAS INSTITUCIONALES
# ============================================================
print("\n" + "=" * 60)
print("FILTRANDO ENCABEZADOS INSTITUCIONALES REPETIDOS...")
print("=" * 60)

def es_fila_institucional(fila):
    """Detecta filas con texto institucional de la UAGRM"""
    # CORRECCIÓN: Convertir cada valor a string individualmente
    fila_str = ' '.join(str(x) for x in fila).upper()
    palabras = ['U.A.G', 'R.M.', 'PERSONALES DE ALUMNOS', 'POR CARR', 
                'PAG:', 'SANTA CRUZ', 'CONTADU', 'GESTION', 'UAGRM',
                'DATOS PERSONALES']
    return any(pal in fila_str for pal in palabras)

def es_fila_encabezado_tabla(fila):
    """Detecta fila con nombres de columnas (NRO, NOMBRE, CELULAR)"""
    fila_str = ' '.join(str(x) for x in fila).upper()
    return 'NRO' in fila_str and 'NOMBRE' in fila_str and 'CELULAR' in fila_str

def es_fila_datos(fila):
    """Detecta si la primera columna es un número (NRO de registro)"""
    primero = str(fila.iloc[0]).strip()
    try:
        int(primero)
        return True
    except:
        return False

# Filtrar filas
filas_datos = []
filas_institucionales = 0
filas_encabezado_tabla = 0

for idx, fila in df_raw.iterrows():
    if es_fila_institucional(fila):
        filas_institucionales += 1
        continue
    if es_fila_encabezado_tabla(fila):
        filas_encabezado_tabla += 1
        continue
    if es_fila_datos(fila):
        filas_datos.append(fila.values)

print(f"✓ Filas institucionales eliminadas: {filas_institucionales}")
print(f"✓ Filas de encabezado de tabla eliminadas: {filas_encabezado_tabla}")
print(f"✓ Filas de datos detectadas: {len(filas_datos)}")

# ============================================================
# 3. CREAR DATAFRAME CON COLUMNAS CORRECTAS
# ============================================================
print("\n" + "=" * 60)
print("CREANDO DATAFRAME LIMPIO...")
print("=" * 60)

columnas = ['NRO', 'REGISTRO', 'NOMBRE', 'DOCTO_ID', 'TEL_FIJO', 'CELULAR', 'CORREO']
n_cols = len(df_raw.columns)
if n_cols > len(columnas):
    columnas = columnas + [f'COL_{i}' for i in range(len(columnas), n_cols)]
elif n_cols < len(columnas):
    columnas = columnas[:n_cols]

df = pd.DataFrame(filas_datos, columns=columnas)
print(f"✓ DataFrame creado: {len(df)} filas x {len(df.columns)} columnas")

# ============================================================
# 4. LIMPIEZA DE CELULARES
# ============================================================
print("\n" + "=" * 60)
print("LIMPIEZA DE TELÉFONOS")
print("=" * 60)

df_limpio = df.copy()
df_limpio['celular_str'] = df_limpio['CELULAR'].astype(str)
df_limpio['celular_limpio'] = df_limpio['celular_str'].str.replace(r'[^\d]', '', regex=True)

# Filtrar válidos
df_limpio = df_limpio[
    (df_limpio['celular_limpio'].notna()) & 
    (df_limpio['celular_limpio'] != '') & 
    (df_limpio['celular_limpio'] != '0') &
    (df_limpio['celular_limpio'] != 'nan') &
    (df_limpio['celular_limpio'].str.len() >= 7)
].copy()

print(f"✓ Con celular válido: {len(df_limpio)}")

# Agregar código de país 591
def formatear_numero(numero):
    if numero.startswith('591'):
        return numero
    return f"591{numero}"

df_limpio['telefono_final'] = df_limpio['celular_limpio'].apply(formatear_numero)
df_limpio = df_limpio[df_limpio['telefono_final'].str.len() >= 10].copy()

print(f"✓ Con formato válido: {len(df_limpio)}")

# ============================================================
# 5. MUESTREO ALEATORIO DE 500
# ============================================================
print("\n" + "=" * 60)
print("MUESTREO ALEATORIO")
print("=" * 60)

N_MUESTRA = 500
if len(df_limpio) >= N_MUESTRA:
    df_muestra = df_limpio.sample(n=N_MUESTRA, random_state=42)
    print(f"✓ Muestra de {N_MUESTRA} contactos")
else:
    df_muestra = df_limpio.copy()
    print(f"⚠ Solo {len(df_limpio)} disponibles")

# ============================================================
# 6. EXPORTAR
# ============================================================
df_envio = df_muestra[['NOMBRE', 'telefono_final']].copy()
df_envio['correo'] = df_muestra['CORREO'] if 'CORREO' in df_muestra.columns else ''
df_envio.columns = ['nombre', 'telefono', 'correo']
df_envio['estado_envio'] = 'pendiente'
df_envio.reset_index(drop=True, inplace=True)

df_envio.to_csv('muestra_500_whatsapp.csv', index=False, encoding='utf-8-sig')

# ============================================================
# 7. RESUMEN
# ============================================================
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)
print(f"Filas originales:        {len(df_raw)}")
print(f"Institucionales eliminadas: {filas_institucionales}")
print(f"Encabezados eliminados:  {filas_encabezado_tabla}")
print(f"Datos reales:            {len(df)}")
print(f"Con celular válido:      {len(df_limpio)}")
print(f"Muestra seleccionada:    {len(df_muestra)}")
print(f"Archivo: muestra_500_whatsapp.csv")

print("\n--- Primeros 10 contactos ---")
print(df_envio.head(10).to_string())

print("\n" + "=" * 60)
print("¡LISTO!")
print("=" * 60)