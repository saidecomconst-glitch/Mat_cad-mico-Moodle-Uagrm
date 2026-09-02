<?php
/**
 * Estructura de Tarea Sumativa y Rúbrica - Unidad 2: Probabilidades
 * Asignatura: Estadística II (MAT-260) - UAGRM
 * Docente: MSc. Anselmo Salguero Arano
 */

$unidad_02_practico = [
    'tarea_id' => 'PRACTICO_U02',
    'titulo' => 'Memoria de Cálculo: Modelación de Probabilidades en Auditoría y Negocios',
    'ponderacion_total' => 30.0,
    'casos' => [
        [
            'numero' => 1,
            'tema' => 'Auditoría Tributaria y Regla General de la Adición',
            'puntos' => 10.0,
            'descripcion' => 'Revisión fiscal de 400 empresas: IVA (45%), IUE (30%) e intersección (18%). Diagrama de Venn, unión, complemento y dictamen profesional.'
        ],
        [
            'numero' => 2,
            'tema' => 'Análisis Bivariado y Contingencia en Cartera de Créditos',
            'puntos' => 10.0,
            'descripcion' => 'Matriz 2x2 de 600 créditos (Microempresa vs Gran Empresa). Tasas de mora condicional y demostración analítica de dependencia estadística.'
        ],
        [
            'numero' => 3,
            'tema' => 'Auditoría Forense y Teorema de Bayes en 3 Sucursales',
            'puntos' => 10.0,
            'descripcion' => 'Facturación en Santa Cruz (50%, tasa 1%), La Paz (30%, tasa 3%) y Cochabamba (20%, tasa 6%). Árbol, probabilidad total y probabilidad a posteriori P(S3|E).'
        ]
    ],
    'rubrica' => [
        'criterio_1' => ['nombre' => 'Planteamiento y Notación Formal', 'peso' => 0.35, 'puntos' => 10.5],
        'criterio_2' => ['nombre' => 'Desarrollo Analítico y Precisión Matemática', 'peso' => 0.45, 'puntos' => 13.5],
        'criterio_3' => ['nombre' => 'Conclusión Profesional e Interpretación', 'peso' => 0.20, 'puntos' => 6.0]
    ]
];
