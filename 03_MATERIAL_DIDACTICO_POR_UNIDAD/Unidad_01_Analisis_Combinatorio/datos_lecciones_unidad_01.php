<?php
/**
 * =========================================================================
 * DATOS DE CONFIGURACIÓN Y POBLADO DE LECCIONES INTERACTIVAS EN MOODLE
 * Unidad N° 1: Análisis Combinatorio y Métodos de Conteo
 * Materia: Estadística II (MAT-260) - UAGRM
 * Docente: MSc. Anselmo Salguero Arano
 * =========================================================================
 */

defined('MOODLE_INTERNAL') || die();

$unidad_01_lecciones = [
    'info' => [
        'unit_number' => 1,
        'unit_name' => 'Análisis Combinatorio y Métodos de Conteo',
        'course_code' => 'MAT260',
        'docente' => 'MSc. Anselmo Salguero Arano',
        'faculty' => 'Facultad de Ciencias Contables, Auditoría, Sistemas de Control de Gestión y Finanzas',
        'total_lessons' => 4,
        'lesson_pages_count' => 13
    ],
    'settings_template' => [
        'progressbar' => 1,
        'ongoing' => 0,
        'feedback' => 1,
        'maxattempts' => 3,
        'review' => 1,
        'nextpagedefault' => 0,
        'minquestions' => 10,
        'maxpages' => 0,
        'practice' => 1,
        'custom' => 1,
        'grade' => 0, // Formativo
        'completionendreached' => 1
    ],
    'lessons' => [
        [
            'lesson_id' => '1.1',
            'title' => 'Lección 1.1: Principios Fundamentales del Conteo y Factoriales',
            'shortname' => 'L1.1 Principios de Conteo',
            'summary' => 'Regla de la Multiplicación, Regla de la Adición y Álgebra de Factoriales.',
            'html_file' => 'Leccion_01_01_Principios_Conteo_Factoriales.html',
            'availability_prereq' => '00_Guia_Estudio_Unidad_01_Analisis_Combinatorio'
        ],
        [
            'lesson_id' => '1.2',
            'title' => 'Lección 1.2: Permutaciones Simples, Variaciones (nPr) y Circulares',
            'shortname' => 'L1.2 Permutaciones Simples y Circulares',
            'summary' => 'Ordenamientos lineales (n!), subgrupos ordenados (nPr) y mesas redondas (n-1)!.',
            'html_file' => 'Leccion_01_02_Permutaciones_Simples_Circulares.html',
            'availability_prereq' => 'Leccion_01_01_Principios_Conteo_Factoriales'
        ],
        [
            'lesson_id' => '1.3',
            'title' => 'Lección 1.3: Permutaciones con Repetición y Restricciones',
            'shortname' => 'L1.3 Permutaciones con Repetición',
            'summary' => 'Fórmulas de repetición, método de bloques indivisibles y método del complemento.',
            'html_file' => 'Leccion_01_03_Permutaciones_Repeticion.html',
            'availability_prereq' => 'Leccion_01_02_Permutaciones_Simples_Circulares'
        ],
        [
            'lesson_id' => '1.4',
            'title' => 'Lección 1.4: Combinaciones (nCr), Propiedades y Criterios de Decisión',
            'shortname' => 'L1.4 Combinaciones y Matriz de Decisión',
            'summary' => 'Muestreo no ordenado, simetría binomial, comités mixtos y matriz de decisión.',
            'html_file' => 'Leccion_01_04_Combinaciones_y_Diferenciacion.html',
            'availability_prereq' => 'Leccion_01_03_Permutaciones_Repeticion'
        ]
    ]
];
