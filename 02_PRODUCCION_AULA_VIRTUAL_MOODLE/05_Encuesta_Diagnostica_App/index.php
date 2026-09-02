<?php
$dataFile = __DIR__ . '/encuesta_diagnostico.csv';
$excelFile = __DIR__ . '/encuesta_diagnostico.xlsx';

$saved = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $row = [
        date('Y-m-d H:i:s'),
        trim($_POST['registro'] ?? ''),
        trim($_POST['nombre'] ?? ''),
        trim($_POST['carrera'] ?? ''),
        trim($_POST['edad'] ?? ''),
        trim($_POST['sexo'] ?? ''),
        trim($_POST['ppa'] ?? ''),
        trim($_POST['horas_estudio'] ?? ''),
        trim($_POST['dispositivo'] ?? ''),
        trim($_POST['internet'] ?? ''),
        trim($_POST['nivel_excel'] ?? ''),
        trim($_POST['tablas_dinamicas'] ?? ''),
        trim($_POST['herramientas_software'] ?? ''),
        trim($_POST['uso_ia'] ?? ''),
        trim($_POST['geogebra_calculadoras'] ?? ''),
        trim($_POST['comentarios'] ?? '')
    ];

    $isNew = !file_exists($dataFile);
    $fp = fopen($dataFile, 'a');
    if ($isNew) {
        // UTF-8 BOM
        fputs($fp, "\xEF\xBB\xBF");
        fputcsv($fp, [
            'Fecha y Hora', 'Registro Universitario', 'Nombre Completo', 'Carrera', 'Edad', 'Sexo', 'PPA Estimado',
            'Horas de Estudio Semanal', 'Dispositivo Principal', 'Conexión a Internet', 'Nivel de Excel',
            'Tablas Dinámicas', 'Software Estadístico Previo', 'Uso de Herramientas IA', 'Uso de GeoGebra/Calculadoras', 'Comentarios y Expectativas'
        ]);
    }
    fputcsv($fp, $row);
    fclose($fp);
    $saved = true;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Encuesta Diagnóstica Inicial — Estadística II (MAT-260 EP)</title>
  <style>
    body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 20px; color: #2c3e50; }
    .container { width: 100%; max-width: 900px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 16px rgba(15,43,77,0.12); overflow: hidden; border: 1px solid #d0dbe5; }
    .header { background: linear-gradient(135deg, #0f2b4d 0%, #1a4a75 50%, #2980b9 100%); color: #ffffff; padding: 25px 30px; text-align: center; }
    .header h1 { margin: 0; font-size: 22px; }
    .header p { margin: 6px 0 0 0; font-size: 13px; color: #87ceeb; }
    .content { padding: 30px; }
    .group { margin-bottom: 22px; }
    label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 14px; color: #0f2b4d; }
    input[type="text"], input[type="number"], select, textarea { width: 100%; padding: 10px 12px; border: 1px solid #c9dbe9; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
    .btn { background: #27ae60; color: #ffffff; border: none; padding: 14px 28px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; transition: background 0.2s; }
    .btn:hover { background: #219653; }
    .alert-success { background: #d4edda; color: #155724; border-left: 5px solid #28a745; padding: 20px; border-radius: 6px; text-align: center; margin-bottom: 20px; }
  </style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📊 Encuesta Diagnóstica Inicial y Perfil Tecnológico</h1>
    <p>MSc. Anselmo Salguero Arano | Estadística II (MAT-260 EP) — UAGRM</p>
  </div>
  <div class="content">
    <?php if ($saved): ?>
      <div class="alert-success">
        <h2>✅ ¡Respuestas registradas exitosamente!</h2>
        <p>Sus datos han sido guardados directamente en el archivo <code>encuesta_diagnostico.csv</code> para la tabulación estadística del curso.</p>
        <p><a href="index.php" style="color: #155724; font-weight: bold;">Llenar otra respuesta</a> | <a href="encuesta_diagnostico.csv" style="color: #0f2b4d; font-weight: bold;">Descargar Datos Recolectados (CSV/Excel)</a></p>
      </div>
    <?php else: ?>
      <form method="POST">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
          <div class="group">
            <label>1. Número de Registro Universitario:</label>
            <input type="text" name="registro" required placeholder="Ej. 221045892">
          </div>
          <div class="group">
            <label>2. Nombre Completo:</label>
            <input type="text" name="nombre" required placeholder="Apellidos y Nombres">
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
          <div class="group">
            <label>3. Carrera:</label>
            <select name="carrera" required>
              <option value="Auditoría / Contaduría Pública">Auditoría / Contaduría Pública</option>
              <option value="Ingeniería Financiera">Ingeniería Financiera</option>
              <option value="Ingeniería Comercial">Ingeniería Comercial</option>
              <option value="Administración de Empresas">Administración de Empresas</option>
              <option value="Otra Carrera">Otra Carrera</option>
            </select>
          </div>
          <div class="group">
            <label>4. Edad:</label>
            <input type="number" name="edad" min="16" max="70" required placeholder="Años">
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
          <div class="group">
            <label>5. Sexo:</label>
            <select name="sexo" required>
              <option value="Femenino">Femenino</option>
              <option value="Masculino">Masculino</option>
            </select>
          </div>
          <div class="group">
            <label>6. Promedio Ponderado Acumulado (PPA estimado):</label>
            <input type="number" name="ppa" step="0.1" min="0" max="100" placeholder="Ej. 68.5">
          </div>
        </div>

        <div class="group">
          <label>7. Horas semanales estimadas para estudio autónomo de Estadística II:</label>
          <select name="horas_estudio" required>
            <option value="Menos de 3 horas">Menos de 3 horas semanales</option>
            <option value="Entre 3 y 6 horas">Entre 3 y 6 horas semanales</option>
            <option value="Entre 6 y 10 horas">Entre 6 y 10 horas semanales</option>
            <option value="Más de 10 horas">Más de 10 horas semanales</option>
          </select>
        </div>

        <div class="group">
          <label>8. Principal dispositivo con el que accederá a clases y aula virtual:</label>
          <select name="dispositivo" required>
            <option value="Laptop propia">Computadora portátil (Laptop) propia</option>
            <option value="PC escritorio">Computadora de escritorio (PC) en casa</option>
            <option value="Smartphone">Smartphone (Teléfono celular)</option>
            <option value="Tablet">Tablet</option>
            <option value="Sala de cómputo / Café internet">Sala de cómputo o café internet</option>
          </select>
        </div>

        <div class="group">
          <label>9. Calidad y estabilidad de su conexión a Internet:</label>
          <select name="internet" required>
            <option value="Excelente (Fibra óptica / WiFi estable)">Excelente y estable (Fibra óptica / WiFi sin cortes)</option>
            <option value="Buena (WiFi con desconexiones menores)">Buena (WiFi con desconexiones ocasionales)</option>
            <option value="Regular (Datos móviles / megas)">Regular (Uso principal de megas / datos móviles)</option>
            <option value="Inestable / Limitada">Limitada o muy inestable</option>
          </select>
        </div>

        <div class="group">
          <label>10. Nivel de dominio general en Microsoft Excel:</label>
          <select name="nivel_excel" required>
            <option value="Básico (Ingreso de datos y sumas)">Básico (Ingreso de datos, sumas simples, dar formato)</option>
            <option value="Intermedio (Funciones promedio, si, buscarv)">Intermedio (Funciones promedio, si, buscarv, gráficos)</option>
            <option value="Avanzado (Tablas dinámicas, fórmulas estadísticas)">Avanzado (Tablas dinámicas, gráficos dinámicos, funciones estadísticas)</option>
            <option value="Experto (Macros VBA, Power Query/Pivot)">Experto (Macros en VBA, Power Query, modelado financiero)</option>
          </select>
        </div>

        <div class="group">
          <label>11. Dominio específico con Tablas Dinámicas en Excel:</label>
          <select name="tablas_dinamicas" required>
            <option value="Nunca las he usado">No las he utilizado nunca</option>
            <option value="Concepto básico">Conozco el concepto pero me cuesta crearlas</option>
            <option value="Creación y segmentación autónoma">Sé crear tablas dinámicas y segmentaciones con soltura</option>
            <option value="Campos calculados y relaciones">Domino campos calculados y relaciones avanzadas</option>
          </select>
        </div>

        <div class="group">
          <label>12. Software estadístico que ha utilizado previamente:</label>
          <input type="text" name="herramientas_software" placeholder="Ej. SPSS, R, Python, JASP, Minitab, Ninguno">
        </div>

        <div class="group">
          <label>13. ¿Utiliza herramientas de Inteligencia Artificial (ChatGPT, Gemini, Claude) para estudiar?:</label>
          <select name="uso_ia" required>
            <option value="Frecuentemente como tutor de apoyo">Frecuentemente como tutor de apoyo y consultas</option>
            <option value="Ocasionalmente para dudas puntuales">Ocasionalmente para dudas puntuales</option>
            <option value="Raras veces">Raras veces</option>
            <option value="Nunca">Nunca he utilizado herramientas de IA</option>
          </select>
        </div>

        <div class="group">
          <label>14. Uso de GeoGebra o Calculadoras Científicas Avanzadas:</label>
          <select name="geogebra_calculadoras" required>
            <option value="Domino GeoGebra y Calculadora científica física">Domino GeoGebra y calculadora científica física</option>
            <option value="Solo calculadora científica física estándar">Solo calculadora científica física estándar</option>
            <option value="Solo calculadora del celular">Solo calculadora básica del celular</option>
            <option value="Ninguna">Ninguna</option>
          </select>
        </div>

        <div class="group">
          <label>15. Comentarios, necesidades particulares o expectativas para Estadística II:</label>
          <textarea name="comentarios" rows="4" placeholder="Escriba aquí sus comentarios o temas que desea profundizar..."></textarea>
        </div>

        <button type="submit" class="btn">💾 Enviar Respuestas y Guardar en Base de Datos / Excel</button>
      </form>
    <?php endif; ?>
  </div>
</div>
</body>
</html>