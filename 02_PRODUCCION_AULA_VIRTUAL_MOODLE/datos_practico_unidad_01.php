<?php
/**
 * =========================================================================
 * DATOS DE CONFIGURACIÓN DEL PRÁCTICO EVALUATIVO Y RÚBRICA (GRADEBOOK 70/30)
 * Unidad N° 1: Análisis Combinatorio y Métodos de Conteo
 * Materia: Estadística II (MAT-260) - UAGRM
 * Docente: MSc. Anselmo Salguero Arano
 * =========================================================================
 */

defined('MOODLE_INTERNAL') || die();

$unidad_01_evaluacion = [
    'grade_category' => [
        'fullname' => 'Unidad 1 - Análisis Combinatorio',
        'aggregation' => 13, // SUM OF GRADES (Natural)
        'grademax' => 100.0,
        'grademin' => 0.0,
        'weight' => 0.20 // 20% del semestre
    ],
    'practico_online' => [
        'name' => 'Práctico Evaluativo N° 1: Análisis Combinatorio (70%)',
        'intro' => '<p>Evaluación cuantitativa oficial de la Unidad 1. Consta de preguntas aleatorias del banco sobre Principios de Conteo, Permutaciones y Combinaciones.</p>',
        'attempts' => 2,
        'grademethod' => 1, // Calificación más alta
        'grademax' => 70.0,
        'reviewoptions' => [
            'during' => 1,
            'immediately' => 1,
            'open' => 1,
            'closed' => 1
        ],
        'availability_prereq' => 'Leccion_01_04_Combinaciones_y_Diferenciacion'
    ],
    'memoria_pdf' => [
        'name' => 'Envío de Memoria de Cálculo Manuscrita en PDF: Unidad 1 (30%)',
        'intro' => '<p>Envío obligatorio de la memoria manuscrita escaneada en un único archivo PDF con el membrete institucional oficial.</p>',
        'grademax' => 30.0,
        'gradingmethod' => 'rubric',
        'filetypes' => '.pdf',
        'maxfiles' => 1,
        'maxbytes' => 20971520, // 20 MB
        'availability_prereq' => 'Práctico Evaluativo N° 1 (Al menos 1 intento)'
    ],
    'rubric_criteria' => [
        [
            'description' => 'Planteamiento Teórico y Modelo Analítico',
            'weight_pct' => 40,
            'levels' => [
                ['score' => 12.0, 'definition' => 'Identifica con precisión matemática el principio de conteo aplicable; define formalmente n y r; formula las ecuaciones algebraicas completas antes de reemplazar valores.'],
                ['score' => 9.5, 'definition' => 'Plantea correctamente los modelos de conteo; desarrollo algebraico claro con omisión de justificaciones menores en pasos intermedios.'],
                ['score' => 6.5, 'definition' => 'Planteamiento incompleto; confunde permutaciones con combinaciones en algunos casos; reemplaza valores sin fórmulas de respaldo.'],
                ['score' => 0.0, 'definition' => 'Sin justificación teórica ni lógica matemática demostrable; modelos totalmente erróneos.']
            ]
        ],
        [
            'description' => 'Precisión de Cálculos y Álgebra de Factoriales',
            'weight_pct' => 35,
            'levels' => [
                ['score' => 10.5, 'definition' => 'Desarrolla el álgebra de factoriales simplificando factores comunes; resultados numéricos 100% exactos destacados en recuadros con sus unidades contextuales.'],
                ['score' => 8.0, 'definition' => 'Cálculos correctos en su gran mayoría con errores aritméticos menores; respuestas identificadas.'],
                ['score' => 5.5, 'definition' => 'Errores en la simplificación de factoriales o en operaciones aritméticas; omite unidades contextuales.'],
                ['score' => 0.0, 'definition' => 'Cálculos totalmente erróneos o resultados numéricos aislados sin desarrollo procedimental.']
            ]
        ],
        [
            'description' => 'Formato Institucional, Membrete y PDF',
            'weight_pct' => 25,
            'levels' => [
                ['score' => 7.5, 'definition' => 'Membrete manuscrito oficial completo en la 1ra página; archivo único PDF nítido, vertical, iluminado y nombrado según la norma institucional.'],
                ['score' => 6.0, 'definition' => 'Membrete con datos completos; PDF único con buena legibilidad y orientación adecuada.'],
                ['score' => 4.0, 'definition' => 'Membrete incompleto; escaneo con sombras o páginas desorientadas; nombre de archivo no estándar.'],
                ['score' => 0.0, 'definition' => 'Sin membrete; documento ilegible o presentado en formatos no autorizados.']
            ]
        ]
    ]
];
