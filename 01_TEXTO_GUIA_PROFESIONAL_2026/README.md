# PROYECTO: NUEVO TEXTO GUÍA PROFESIONAL DE ESTADÍSTICA II (2026)
**Asignatura:** Estadística II (MAT-260)  
**Autor:** MSc. Ing. Anselmo Salguero Arano  
**Destinatarios:** Estudiantes de la Carrera de Contaduría Pública — UAGRM  

---

## 🔍 1. Diagnóstico y Revisión del Texto Guía Actual (rev2025)

El texto base que se ha venido utilizando cuenta con un contenido temático sólido y directo, enfocado en resolver problemas típicos de la materia. Tras revisarlo a fondo, se identifican las siguientes oportunidades de mejora para convertirlo en una **obra de nivel universitario y editorial profesional**:

### Puntos Fuertes Actuales:
1. **Secuencia lógica:** Va desde el análisis combinatorio básico hasta distribuciones continuas y muestreo.
2. **Ejemplos prácticos y directos:** Ejercicios clásicos resueltos paso a paso con fórmulas explícitas.
3. **Adaptado al programa oficial de Contaduría Pública de la UAGRM.**

### Áreas de Mejora para la Nueva Versión Profesional:
1. **Tipografía y Maquetación Editorial:**
   - Migrar del formato Word estándar a un diseño profesional (usando LaTeX / Bookdown / Typst o plantilla avanzada de Word con estilos unificados).
   - Ecuaciones matemáticas formateadas con precisión tipográfica (notación estándar de probabilidades, operadores matemáticos limpios).
2. **Gráficos y Diagramas Vectoriales de Alta Calidad:**
   - Sustituir diagramas pegados o de baja resolución por gráficos vectoriales modernos generados con Python (Matplotlib / Seaborn) o TikZ en LaTeX:
     - Curvas normales con áreas bajo la curva y zonas críticas sombreadas.
     - Diagramas de árbol de probabilidades bien delineados.
     - Histogramas y funciones de masa de probabilidad discretas (Binomial, Poisson).
3. **Contexto Aplicado a Contaduría, Finanzas y Auditoría:**
   - Enriquecer los ejemplos teóricos con casos reales de negocios, auditoría financiera, control de inventarios, pronósticos de ventas y muestreo de facturas/transacciones.
4. **Estructura Pedagógica por Capítulo:**
   - **Objetivos de aprendizaje** al inicio de cada capítulo.
   - **Mapas conceptuales / esquemas resúmenes**.
   - **Ejemplos resueltos explicados paso a paso** (Planteamiento $\to$ Modelo $\to$ Desarrollo $\to$ Interpretación para la toma de decisiones).
   - **Ejercicios propuestos graduados** (Nivel Básico, Intermedio, Avanzado / Casos Reales).
   - **Resumen de fórmulas** al final de cada unidad.
   - **Autoevaluación tipo Moodle / Examen** para que el estudiante mida su avance.
5. **Apéndice Completo de Tablas Estadísticas:**
   - Tablas de distribución Normal Estándar $Z$ ($P(0 < Z < z)$ y $P(Z \le z)$).
   - Tabla de la distribución $t$ de Student.
   - Tabla de la distribución Binomial y Poisson.

---

## 📚 2. Estructura Propuesta para el Nuevo Libro

| Cap. | Título | Temas Clave | Aplicación Contable / Financiera |
| :---: | :--- | :--- | :--- |
| **1** | **Análisis Combinatorio** | Principio de conteo, Ley de multiplicación, Ley de adición, Permutaciones, Combinaciones. | Combinatoria de códigos de cuentas, combinaciones de muestras de auditoría, permutaciones de puestos de trabajo. |
| **2** | **Teoría de Probabilidades** | Conceptos básicos, Espacio muestral, Reglas de adición y multiplicación, Probabilidad condicional, Teorema de Bayes, Tablas de contingencia. | Probabilidad de impago de clientes, análisis bayesiano en detección de fraudes o errores contables. |
| **3** | **Distribuciones de Probabilidad Discreta** | Variable aleatoria discreta, Función de probabilidad y acumulada, Esperanza y Varianza, Distribución Binomial, Hipergeométrica, Poisson, Aproximación de Poisson a Binomial. | Auditoría de cheques devueltos, control de calidad en auditoría de documentos, llegada de clientes a cajas bancarias. |
| **4** | **Distribuciones de Probabilidad Continua** | Variable aleatoria continua, Función de densidad, Distribución Normal, Estandarización $Z$, Percentiles, Distribución Exponencial, Distribución $t$ de Student, Teorema del Límite Central. | Rendimientos financieros, tiempos de atención en sucursales, salarios del personal, límites de tolerancia contable. |
| **5** | **Distribuciones Muestrales e Intervalos de Confianza** | Muestreo probabilístico, Distribución muestral de la media, Intervalos de confianza para $\mu$ (con $\sigma$ conocida y desconocida), Tamaño de muestra necesario. | Estimación del saldo promedio de cuentas por cobrar, auditoría por muestreo estadístico, control de costos. |

---

## 🛠️ 3. Carpetas de Trabajo del Proyecto

- `00_Fuentes_Originales_Word/`: Archivos `.doc` históricos preservados como referencia.
- `01_Estructura_y_Capitulos/`: Contenido en texto/markdown/Word por cada unidad para redacción y pulido.
- `02_Latex_Book_Project/`: Código fuente del libro completo estructurado en LaTeX.
- `03_Graficos_y_Diagramas/`: Scripts y figuras vectoriales generadas.
- `04_Tablas_Estadisticas/`: Tablas de referencia matemática y estadística en alta definición.
- `05_Compilados_PDF_Finales/`: Versiones finales listas para publicar y compartir con los alumnos.
