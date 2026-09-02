
# ============================================================
# ENVÍO AUTOMATIZADO POR WHATSAPP WEB - UAGRM ESTADÍSTICA
# ============================================================
# Requisitos: pip install selenium pandas
# Ejecuta: python envio_whatsapp.py

import pandas as pd
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================================================
# 1. CONFIGURACIÓN DEL MENSAJE
# ============================================================
LINK_ENCUESTA = "https://docs.google.com/forms/d/e/1FAIpQLSfwqWEnr-mllBAOxQ7iTP1u4lxXrNcIfMvUQrO9bTUvYLGyww/viewform"

MENSAJE_BASE = """Desde la Carrera de Contaduría Pública, Facultad de Ciencias Contables, Auditoría, Sistemas de Control de Gestión y Finanzas.

Te invito a participar en una encuesta estudiantil que estamos realizando como parte de las prácticas académicas de la asignatura Estadística 2 (unidad: Distribución de Probabilidad para Variables Aleatorias Continuas).

El objetivo es recopilar datos reales de estudiantes de las facultades de la UAGRM para el análisis de distribuciones de probabilidad.

1. TÍTULO DEL ESTUDIO: Recolección de datos para el análisis de distribuciones de probabilidad de variables aleatorias continuas de estudiantes de la UAGRM.

2. SITIO:
Universidad Autónoma Gabriel René Moreno (UAGRM), Santa Cruz de la Sierra, Bolivia. Facultades de la UAGRM

3. INVESTIGADORES RESPONSABLES
Docente: MSc. Anselmo Salguero Arano
Con participación de estudiantes del grupo de Estadística 2, cuarto semestre, Carrera de Contaduría Pública.

4. EL PROPÓSITO DEL ESTUDIO:
Recopilar datos de estudiantes de las facultades de la UAGRM para el análisis de distribuciones de probabilidad de variables aleatorias continuas (distribución normal y distribución exponencial), como parte de las prácticas académicas de la unidad correspondiente en la asignatura de Estadística 2.

📋 Tiempo estimado: 4 a 5 minutos
🔒 Anónima y voluntaria
🎓 Solo fines académicos

Te agradecería mucho si puedes completarla y compartirla con tus compañeros y amigos de la Universidad.

Link de la encuesta:
{link}"""

# Tiempos de espera (ajustables según tu conexión)
TIEMPO_ESPERA_CARGA = 12      # Segundos para cargar cada chat
TIEMPO_ENTRE_MENSAJES = 6     # Segundos entre envíos (evita bloqueos)
PAUSA_CADA_50 = 60            # Segundos de pausa cada 50 mensajes

# ============================================================
# 2. CARGAR CONTACTOS
# ============================================================
print("=" * 60)
print("CARGANDO CONTACTOS...")
print("=" * 60)

try:
    df = pd.read_csv('muestra_500_whatsapp.csv')
except FileNotFoundError:
    print("⚠ ERROR: No se encontró 'muestra_500_whatsapp.csv'")
    print("   Ejecuta primero 'limpieza_muestra_v4.py'")
    exit()

# Filtrar solo los pendientes
df_pendientes = df[df['estado_envio'] == 'pendiente'].copy()

print(f"✓ Total contactos en archivo: {len(df)}")
print(f"✓ Pendientes de envío: {len(df_pendientes)}")

if len(df_pendientes) == 0:
    print("\n⚠ No hay contactos pendientes. Todos los mensajes ya fueron enviados.")
    exit()

# ============================================================
# 3. CONFIGURAR NAVEGADOR (Chrome)
# ============================================================
print("\n" + "=" * 60)
print("INICIANDO WHATSAPP WEB...")
print("=" * 60)

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")  # No usar, necesitas ver el QR

try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"⚠ Error al iniciar Chrome: {e}")
    print("   Asegúrate de tener Chrome instalado y actualizado.")
    exit()

driver.get("https://web.whatsapp.com")

print("\n📱 POR FAVOR: Escanee el código QR con su celular")
print("   Esperando conexión...")

# Esperar a que cargue la interfaz principal
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]'))
    )
    print("✓ WhatsApp Web conectado correctamente")
except:
    print("⚠ Tiempo de espera agotado. Verifica que escaneaste el QR.")
    driver.quit()
    exit()

# ============================================================
# 4. ENVIAR MENSAJES
# ============================================================
print("\n" + "=" * 60)
print("INICIANDO ENVÍO DE MENSAJES...")
print("=" * 60)
print(f"   Enviando a {len(df_pendientes)} contactos...")
print(f"   Pausa entre mensajes: {TIEMPO_ENTRE_MENSAJES} segundos")
print(f"   Pausa cada 50 mensajes: {PAUSA_CADA_50} segundos")
print("=" * 60)

enviados = 0
errores = 0
numeros_invalidos = 0

for idx, row in df_pendientes.iterrows():
    telefono = row['telefono']
    nombre = row['nombre']

    print(f"\n[{enviados + errores + numeros_invalidos + 1}/{len(df_pendientes)}] {nombre}")
    print(f"    Tel: {telefono}")

    try:
        # Preparar mensaje
        mensaje = MENSAJE_BASE.format(link=LINK_ENCUESTA)
        mensaje_codificado = urllib.parse.quote(mensaje)

        # Abrir chat directo
        url = f"https://web.whatsapp.com/send?phone={telefono}&text={mensaje_codificado}"
        driver.get(url)

        # Esperar a que cargue el chat
        time.sleep(TIEMPO_ESPERA_CARGA)

        # Verificar si el número es inválido (WhatsApp muestra alerta)
        try:
            alerta_invalido = driver.find_element(By.XPATH, 
                '//div[contains(text(), "número de teléfono") and contains(text(), "inválido")]')
            if alerta_invalido:
                print(f"    ⚠ Número inválido o no tiene WhatsApp")
                df.loc[idx, 'estado_envio'] = 'numero_invalido'
                numeros_invalidos += 1
                continue
        except:
            pass  # No hay alerta, continuar

        # Verificar si hay popup de "No se encontró una cuenta"
        try:
            popup = driver.find_element(By.XPATH, 
                '//div[contains(text(), "No se encontró una cuenta")]')
            if popup:
                print(f"    ⚠ Número no registrado en WhatsApp")
                df.loc[idx, 'estado_envio'] = 'no_registrado'
                numeros_invalidos += 1
                continue
        except:
            pass

        # Encontrar caja de texto y enviar
        try:
            caja_texto = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, 
                    '//div[@contenteditable="true"][@data-tab="1"]'))
            )

            # Enviar mensaje (presionar ENTER)
            caja_texto.send_keys(Keys.ENTER)

            # Marcar como enviado
            df.loc[idx, 'estado_envio'] = 'enviado'
            enviados += 1

            print(f"    ✓ Enviado correctamente")

        except Exception as e:
            print(f"    ✗ Error al enviar: {str(e)[:60]}")
            df.loc[idx, 'estado_envio'] = 'error_envio'
            errores += 1
            continue

        # Pausa entre mensajes (IMPORTANTE para evitar bloqueos)
        time.sleep(TIEMPO_ENTRE_MENSAJES)

        # Cada 50 mensajes, pausa más larga
        if enviados % 50 == 0 and enviados > 0:
            print(f"\n⏱ Pausa de {PAUSA_CADA_50} segundos después de {enviados} envíos...")
            time.sleep(PAUSA_CADA_50)

    except Exception as e:
        print(f"    ✗ Error general: {str(e)[:60]}")
        df.loc[idx, 'estado_envio'] = f'error: {str(e)[:50]}'
        errores += 1
        time.sleep(5)
        continue

# ============================================================
# 5. GUARDAR RESULTADOS
# ============================================================
print("\n" + "=" * 60)
print("GUARDANDO RESULTADOS...")
print("=" * 60)

# Guardar CSV actualizado
df.to_csv('muestra_500_whatsapp.csv', index=False, encoding='utf-8-sig')

# Generar resumen
resumen = df['estado_envio'].value_counts()
print(f"\n✓ Archivo actualizado: 'muestra_500_whatsapp.csv'")
print(f"\n--- RESUMEN DE ENVÍOS ---")
print(resumen.to_string())
print(f"\nTotal procesados: {enviados + errores + numeros_invalidos}")
print(f"  ✓ Enviados: {enviados}")
print(f"  ⚠ Números inválidos: {numeros_invalidos}")
print(f"  ✗ Errores: {errores}")

# ============================================================
# 6. CERRAR NAVEGADOR
# ============================================================
print("\n" + "=" * 60)
input("Presiona ENTER para cerrar el navegador...")
driver.quit()
print("✓ Navegador cerrado. ¡Proceso completado!")
print("=" * 60)
