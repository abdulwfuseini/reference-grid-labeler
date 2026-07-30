# -*- coding: utf-8 -*-
"""
Lightweight text lookup covering the six official UN languages (Arabic,
Chinese, English, French, Russian, Spanish) plus German. Language follows
QGIS's own UI locale setting automatically; anything not in this list
falls back to English.
"""
from qgis.PyQt.QtCore import QSettings

SUPPORTED_LANGUAGES = ("ar", "de", "en", "es", "fr", "ru", "zh")


def current_language():
    locale = str(QSettings().value("locale/userLocale", "en")).lower()
    lang = locale.replace("-", "_").split("_")[0]
    return lang if lang in SUPPORTED_LANGUAGES else "en"


STRINGS = {
    "alg_display_name": {
        "en": "Reference Grid Labeler",
        "de": "Kartenraster-Beschriftung",
        "es": "Etiquetador de cuadrícula de referencia",
        "fr": "Étiqueteur de grille de référence",
        "ru": "Подписи координатной сетки",
        "zh": "参考网格标注器",
        "ar": "أداة تسمية الشبكة المرجعية",
    },
    "alg_group": {
        "en": "Cartography",
        "de": "Kartografie",
        "es": "Cartografía",
        "fr": "Cartographie",
        "ru": "Картография",
        "zh": "制图",
        "ar": "رسم الخرائط",
    },
    "provider_name": {
        "en": "Reference Grid Labeler",
        "de": "Kartenraster-Beschriftung",
        "es": "Etiquetador de cuadrícula de referencia",
        "fr": "Étiqueteur de grille de référence",
        "ru": "Подписи координатной сетки",
        "zh": "参考网格标注器",
        "ar": "أداة تسمية الشبكة المرجعية",
    },
    "alg_short_help": {
        "en": (
            "Atlas-style reference grid over the canvas or a layer's extent. "
            "Columns and rows can each be letters or numbers, with their own "
            "range, direction, and a customizable cell reference format "
            "(default '{col}{row}'). Outputs a grid-cell layer and a border-"
            "label layer; border sides and center labels are optional."
        ),
        "de": (
            "Kartenraster im Atlas-Stil über die Karten- oder Layerausdehnung. "
            "Spalten und Zeilen können jeweils Buchstaben oder Zahlen sein, mit "
            "eigenem Bereich, eigener Richtung und anpassbarem Zellreferenz-"
            "Format (Standard '{col}{row}'). Erzeugt eine Raster- und eine "
            "Beschriftungs-Ebene; Randseiten und Zellmitten-Beschriftung sind "
            "optional."
        ),
        "es": (
            "Cuadrícula de referencia al estilo atlas sobre el lienzo o la "
            "extensión de una capa. Columnas y filas pueden ser letras o "
            "números, cada una con su propio rango, dirección y un formato de "
            "referencia de celda personalizable (por defecto '{col}{row}'). "
            "Genera una capa de cuadrícula y una de etiquetas; los lados del "
            "borde y las etiquetas centrales son opcionales."
        ),
        "fr": (
            "Grille de référence de style atlas sur le canevas ou l'emprise "
            "d'une couche. Colonnes et lignes peuvent être des lettres ou des "
            "nombres, chacune avec sa propre plage, direction et un format de "
            "référence de cellule personnalisable (par défaut '{col}{row}'). "
            "Produit une couche de grille et une couche d'étiquettes ; les "
            "côtés de bordure et les étiquettes centrales sont facultatifs."
        ),
        "ru": (
            "Координатная сетка в стиле атласа поверх охвата карты или слоя. "
            "Столбцы и строки могут быть буквами или числами, каждый со своим "
            "диапазоном, направлением и настраиваемым форматом ссылки на "
            "ячейку (по умолчанию '{col}{row}'). Создаёт слой сетки и слой "
            "подписей; стороны границы и подписи в центре ячеек необязательны."
        ),
        "zh": (
            "在画布或图层范围上创建图集风格的参考网格。列和行可各自使用字母或"
            "数字,各有独立的范围、方向,以及可自定义的单元格参考格式(默认 "
            "'{col}{row}')。生成网格图层和标注图层;边界各侧标注与单元格中心"
            "标注均为可选项。"
        ),
        "ar": (
            "شبكة مرجعية على طراز الأطالس فوق نطاق لوحة الخريطة أو طبقة. يمكن "
            "أن تكون الأعمدة والصفوف أحرفًا أو أرقامًا، ولكل منها نطاقه "
            "واتجاهه الخاص، وتنسيق مرجع خلية قابل للتخصيص (الافتراضي "
            "'{col}{row}'). ينتج طبقة شبكة وطبقة تسميات؛ جوانب الحدود "
            "والتسميات المركزية اختيارية."
        ),
    },
    "param_extent_label": {
        "en": "Grid extent (use canvas extent, or calculate from a layer)",
        "de": "Rasterausdehnung (Kartenausdehnung verwenden oder aus einem Layer berechnen)",
        "es": "Extensión de la cuadrícula (usar la extensión del lienzo o calcularla a partir de una capa)",
        "fr": "Emprise de la grille (utiliser l'emprise du canevas, ou la calculer à partir d'une couche)",
        "ru": "Охват сетки (использовать охват карты или вычислить из слоя)",
        "zh": "网格范围(使用画布范围,或根据图层计算)",
        "ar": "نطاق الشبكة (استخدام نطاق لوحة الخريطة، أو حسابه من طبقة)",
    },
    "param_grid_extent_label": {
        "en": "Grid extent",
        "de": "Rasterausdehnung",
        "es": "Extensión de la cuadrícula",
        "fr": "Emprise de la grille",
        "ru": "Охват сетки",
        "zh": "网格范围",
        "ar": "نطاق الشبكة",
    },
    "extent_resolved_label": {
        "en": "Using: {name} ({width} x {height})",
        "de": "Verwendet: {name} ({width} x {height})",
        "es": "Usando: {name} ({width} x {height})",
        "fr": "Utilisation : {name} ({width} x {height})",
        "ru": "Используется: {name} ({width} x {height})",
        "zh": "使用:{name}({width} x {height})",
        "ar": "المستخدم: {name} ({width} × {height})",
    },
    "extent_source_canvas": {
        "en": "Canvas",
        "de": "Kartenansicht",
        "es": "Lienzo",
        "fr": "Canevas",
        "ru": "Карта",
        "zh": "画布",
        "ar": "لوحة الخريطة",
    },
    "extent_source_custom": {
        "en": "Custom extent",
        "de": "Eigene Ausdehnung",
        "es": "Extensión personalizada",
        "fr": "Emprise personnalisée",
        "ru": "Свой охват",
        "zh": "自定义范围",
        "ar": "نطاق مخصص",
    },
    "extent_source_drawn": {
        "en": "Drawn on canvas",
        "de": "Auf der Karte gezeichnet",
        "es": "Dibujado en el lienzo",
        "fr": "Dessinée sur le canevas",
        "ru": "Нарисовано на карте",
        "zh": "在画布上绘制",
        "ar": "مرسوم على لوحة الخريطة",
    },
    "param_crs_label": {
        "en": "Working CRS (also determines the units offered for cell size/margin below)",
        "de": "Arbeits-Koordinatenreferenzsystem (bestimmt auch die verfügbaren Einheiten für Zellgröße/Randabstand unten)",
        "es": "SRC de trabajo (también determina las unidades ofrecidas para el tamaño de celda/margen de abajo)",
        "fr": "SCR de travail (détermine aussi les unités proposées pour la taille de cellule/marge ci-dessous)",
        "ru": "Рабочая система координат (также определяет единицы измерения для размера ячейки/отступа ниже)",
        "zh": "工作坐标参考系统(同时决定下方单元格大小/边距可选用的单位)",
        "ar": "نظام الإحداثيات المرجعي العامل (يحدد أيضًا الوحدات المعروضة لحجم الخلية/الهامش أدناه)",
    },
    "param_extent_buffer_label": {
        "en": "Margin around extent (expand the extent outward by this much before building the grid; blank/0 = none)",
        "de": "Randabstand um die Ausdehnung (Ausdehnung um diesen Betrag nach außen erweitern, bevor das Raster erstellt wird; leer/0 = kein Puffer)",
        "es": "Margen alrededor de la extensión (ampliar la extensión hacia afuera esta distancia antes de crear la cuadrícula; en blanco/0 = ninguno)",
        "fr": "Marge autour de l'emprise (agrandir l'emprise vers l'extérieur de cette valeur avant de créer la grille ; vide/0 = aucune)",
        "ru": "Отступ вокруг охвата (расширить охват наружу на эту величину перед созданием сетки; пусто/0 = без отступа)",
        "zh": "范围周围的边距(在创建网格之前将范围向外扩展此距离;留空/0 表示不扩展)",
        "ar": "هامش حول النطاق (توسيع النطاق للخارج بهذا المقدار قبل إنشاء الشبكة؛ فارغ/0 = بلا هامش)",
    },
    "param_use_custom_cell_size_label": {
        "en": "Use a custom cell size instead (set width/height below)",
        "de": "Stattdessen eigene Zellgröße verwenden (Breite/Höhe unten festlegen)",
        "es": "Usar un tamaño de celda personalizado (establecer ancho/alto abajo)",
        "fr": "Utiliser plutôt une taille de cellule personnalisée (définir largeur/hauteur ci-dessous)",
        "ru": "Использовать свой размер ячейки (задать ширину/высоту ниже)",
        "zh": "改用自定义单元格大小(在下方设置宽度/高度)",
        "ar": "استخدام حجم خلية مخصص بدلاً من ذلك (تحديد العرض/الارتفاع أدناه)",
    },
    "param_cell_width_label": {
        "en": "Cell width (pick a unit in the field; only used with custom cell size)",
        "de": "Zellbreite (Einheit im Feld wählbar; nur bei eigener Zellgröße)",
        "es": "Ancho de celda (elija una unidad en el campo; solo se usa con tamaño de celda personalizado)",
        "fr": "Largeur de cellule (choisir une unité dans le champ ; utilisé seulement avec une taille de cellule personnalisée)",
        "ru": "Ширина ячейки (выберите единицу измерения в поле; используется только со своим размером ячейки)",
        "zh": "单元格宽度(在字段中选择单位;仅在使用自定义单元格大小时生效)",
        "ar": "عرض الخلية (اختر وحدة في الحقل؛ يُستخدم فقط مع حجم الخلية المخصص)",
    },
    "param_cell_height_label": {
        "en": "Cell height (pick a unit in the field; only used with custom cell size)",
        "de": "Zellhöhe (Einheit im Feld wählbar; nur bei eigener Zellgröße)",
        "es": "Alto de celda (elija una unidad en el campo; solo se usa con tamaño de celda personalizado)",
        "fr": "Hauteur de cellule (choisir une unité dans le champ ; utilisé seulement avec une taille de cellule personnalisée)",
        "ru": "Высота ячейки (выберите единицу измерения в поле; используется только со своим размером ячейки)",
        "zh": "单元格高度(在字段中选择单位;仅在使用自定义单元格大小时生效)",
        "ar": "ارتفاع الخلية (اختر وحدة في الحقل؛ يُستخدم فقط مع حجم الخلية المخصص)",
    },
    "param_exclude_i_label": {
        "en": "Exclude the letter 'I' from letter sequences (avoids confusion with 1 / l)",
        "de": "Buchstabe 'I' aus Buchstabenfolgen ausschließen (vermeidet Verwechslung mit 1 / l)",
        "es": "Excluir la letra 'I' de las secuencias de letras (evita confusión con 1 / l)",
        "fr": "Exclure la lettre « I » des séquences de lettres (évite la confusion avec 1 / l)",
        "ru": "Исключить букву 'I' из буквенных последовательностей (избегает путаницы с 1 / l)",
        "zh": "在字母序列中排除字母 'I'(避免与 1 / l 混淆)",
        "ar": "استبعاد الحرف 'I' من تسلسلات الأحرف (لتجنب الخلط مع 1 / l)",
    },
    "param_column_label_type_label": {
        "en": "Column labels",
        "de": "Spaltenbeschriftung",
        "es": "Etiquetas de columna",
        "fr": "Étiquettes de colonne",
        "ru": "Подписи столбцов",
        "zh": "列标注类型",
        "ar": "تسميات الأعمدة",
    },
    "param_row_label_type_label": {
        "en": "Row labels",
        "de": "Zeilenbeschriftung",
        "es": "Etiquetas de fila",
        "fr": "Étiquettes de ligne",
        "ru": "Подписи строк",
        "zh": "行标注类型",
        "ar": "تسميات الصفوف",
    },
    "opt_letters": {
        "en": "Letters",
        "de": "Buchstaben",
        "es": "Letras",
        "fr": "Lettres",
        "ru": "Буквы",
        "zh": "字母",
        "ar": "أحرف",
    },
    "opt_numbers": {
        "en": "Numbers",
        "de": "Zahlen",
        "es": "Números",
        "fr": "Nombres",
        "ru": "Числа",
        "zh": "数字",
        "ar": "أرقام",
    },
    "param_column_range_label": {
        "en": "Column range (From / To)",
        "de": "Spaltenbereich (Von / Bis)",
        "es": "Rango de columnas (Desde / Hasta)",
        "fr": "Plage de colonnes (De / À)",
        "ru": "Диапазон столбцов (От / До)",
        "zh": "列范围(从/到)",
        "ar": "نطاق الأعمدة (من / إلى)",
    },
    "param_column_range_from_label": {
        "en": "Column range - From",
        "de": "Spaltenbereich - Von",
        "es": "Rango de columnas - Desde",
        "fr": "Plage de colonnes - De",
        "ru": "Диапазон столбцов - От",
        "zh": "列范围 - 从",
        "ar": "نطاق الأعمدة - من",
    },
    "param_column_range_to_label": {
        "en": "Column range - To",
        "de": "Spaltenbereich - Bis",
        "es": "Rango de columnas - Hasta",
        "fr": "Plage de colonnes - À",
        "ru": "Диапазон столбцов - До",
        "zh": "列范围 - 到",
        "ar": "نطاق الأعمدة - إلى",
    },
    "param_row_range_from_label": {
        "en": "Row range - From",
        "de": "Zeilenbereich - Von",
        "es": "Rango de filas - Desde",
        "fr": "Plage de lignes - De",
        "ru": "Диапазон строк - От",
        "zh": "行范围 - 从",
        "ar": "نطاق الصفوف - من",
    },
    "param_row_range_to_label": {
        "en": "Row range - To",
        "de": "Zeilenbereich - Bis",
        "es": "Rango de filas - Hasta",
        "fr": "Plage de lignes - À",
        "ru": "Диапазон строк - До",
        "zh": "行范围 - 到",
        "ar": "نطاق الصفوف - إلى",
    },
    "hint_range_value": {
        "en": "Enter a single letter (e.g. A) or number (e.g. 5), matching the Letters/Numbers choice above.",
        "de": "Einen einzelnen Buchstaben (z. B. A) oder eine Zahl (z. B. 5) eingeben, passend zur Auswahl Buchstaben/Zahlen oben.",
        "es": "Introduzca una sola letra (p. ej. A) o número (p. ej. 5), según la opción Letras/Números anterior.",
        "fr": "Saisissez une seule lettre (ex. A) ou un nombre (ex. 5), selon le choix Lettres/Nombres ci-dessus.",
        "ru": "Введите одну букву (например, A) или число (например, 5) в соответствии с выбором Буквы/Числа выше.",
        "zh": "输入单个字母(例如 A)或数字(例如 5),需与上方的字母/数字选择一致。",
        "ar": "أدخل حرفًا واحدًا (مثل A) أو رقمًا (مثل 5)، بما يتوافق مع اختيار الأحرف/الأرقام أعلاه.",
    },
    "range_label": {
        "en": "Range",
        "de": "Bereich",
        "es": "Rango",
        "fr": "Plage",
        "ru": "Диапазон",
        "zh": "范围",
        "ar": "النطاق",
    },
    "hint_range_numbers": {
        "en": "Number ranges list up to 30 - type a larger value directly if you need more.",
        "de": "Zahlenbereiche listen bis 30 - für größere Werte einfach direkt eingeben.",
        "es": "Los rangos numéricos listan hasta 30 - escriba un valor mayor directamente si lo necesita.",
        "fr": "Les plages numériques vont jusqu'à 30 - saisissez directement une valeur plus grande si besoin.",
        "ru": "Числовые диапазоны показаны до 30 - введите большее значение вручную при необходимости.",
        "zh": "数字范围列表最多到 30 - 如需更大的值请直接输入。",
        "ar": "تُدرج النطاقات الرقمية حتى 30 - اكتب قيمة أكبر مباشرة إذا احتجت ذلك.",
    },
    "hint_label_margin": {
        "en": "Move individual labels afterward via Label toolbar -> 'Move Label'.",
        "de": "Einzelne Beschriftungen lassen sich danach über die Beschriftungs-Werkzeugleiste -> 'Beschriftung verschieben' verschieben.",
        "es": "Las etiquetas individuales se pueden mover después con la barra de herramientas de etiquetas -> 'Mover etiqueta'.",
        "fr": "Déplacez ensuite les étiquettes individuelles via la barre d'outils Étiquettes -> « Déplacer l'étiquette ».",
        "ru": "Отдельные подписи можно переместить позже через панель подписей -> «Переместить подпись».",
        "zh": "之后可通过标注工具栏 -> \"移动标注\" 移动单个标注。",
        "ar": "يمكن نقل التسميات الفردية لاحقًا عبر شريط أدوات التسميات -> 'نقل التسمية'.",
    },
    "range_from_label": {
        "en": "From:",
        "de": "Von:",
        "es": "Desde:",
        "fr": "De :",
        "ru": "От:",
        "zh": "从:",
        "ar": "من:",
    },
    "range_to_label": {
        "en": "To:",
        "de": "Bis:",
        "es": "Hasta:",
        "fr": "À :",
        "ru": "До:",
        "zh": "到:",
        "ar": "إلى:",
    },
    "param_column_direction_label": {
        "en": "Column direction",
        "de": "Spaltenrichtung",
        "es": "Dirección de columnas",
        "fr": "Direction des colonnes",
        "ru": "Направление столбцов",
        "zh": "列方向",
        "ar": "اتجاه الأعمدة",
    },
    "param_row_range_label": {
        "en": "Row range (From / To)",
        "de": "Zeilenbereich (Von / Bis)",
        "es": "Rango de filas (Desde / Hasta)",
        "fr": "Plage de lignes (De / À)",
        "ru": "Диапазон строк (От / До)",
        "zh": "行范围(从/到)",
        "ar": "نطاق الصفوف (من / إلى)",
    },
    "param_row_direction_label": {
        "en": "Row direction",
        "de": "Zeilenrichtung",
        "es": "Dirección de filas",
        "fr": "Direction des lignes",
        "ru": "Направление строк",
        "zh": "行方向",
        "ar": "اتجاه الصفوف",
    },
    "opt_left_to_right": {
        "en": "Left to right",
        "de": "Links nach rechts",
        "es": "Izquierda a derecha",
        "fr": "De gauche à droite",
        "ru": "Слева направо",
        "zh": "从左到右",
        "ar": "من اليسار إلى اليمين",
    },
    "opt_right_to_left": {
        "en": "Right to left",
        "de": "Rechts nach links",
        "es": "Derecha a izquierda",
        "fr": "De droite à gauche",
        "ru": "Справа налево",
        "zh": "从右到左",
        "ar": "من اليمين إلى اليسار",
    },
    "opt_top_to_bottom": {
        "en": "Top to bottom",
        "de": "Oben nach unten",
        "es": "Arriba a abajo",
        "fr": "De haut en bas",
        "ru": "Сверху вниз",
        "zh": "从上到下",
        "ar": "من الأعلى إلى الأسفل",
    },
    "opt_bottom_to_top": {
        "en": "Bottom to top",
        "de": "Unten nach oben",
        "es": "Abajo a arriba",
        "fr": "De bas en haut",
        "ru": "Снизу вверх",
        "zh": "从下到上",
        "ar": "من الأسفل إلى الأعلى",
    },
    "param_cell_label_format_label": {
        "en": "Cell label format (placeholders: {col}, {row})",
        "de": "Format der Zellbeschriftung (Platzhalter: {col}, {row})",
        "es": "Formato de la etiqueta de celda (marcadores: {col}, {row})",
        "fr": "Format de l'étiquette de cellule (paramètres : {col}, {row})",
        "ru": "Формат подписи ячейки (плейсхолдеры: {col}, {row})",
        "zh": "单元格标注格式(占位符:{col}、{row})",
        "ar": "تنسيق تسمية الخلية (العناصر النائبة: {col}، {row})",
    },
    "param_label_margin_label": {
        "en": "Inset from grid edge (pick a unit in the field; blank = automatic)",
        "de": "Randabstand vom Rasterrand (Einheit im Feld wählbar; leer = automatisch)",
        "es": "Margen desde el borde de la cuadrícula (elija una unidad en el campo; en blanco = automático)",
        "fr": "Retrait par rapport au bord de la grille (choisir une unité dans le champ ; vide = automatique)",
        "ru": "Отступ от края сетки (выберите единицу измерения в поле; пусто = автоматически)",
        "zh": "与网格边缘的内缩距离(在字段中选择单位;留空 = 自动)",
        "ar": "الإزاحة عن حافة الشبكة (اختر وحدة في الحقل؛ فارغ = تلقائي)",
    },
    "param_border_sides_label": {
        "en": "Border index labels on",
        "de": "Randbeschriftung auf",
        "es": "Etiquetas de índice en el borde",
        "fr": "Étiquettes d'index en bordure",
        "ru": "Подписи на границе",
        "zh": "边界索引标注位置",
        "ar": "تسميات الفهرس الحدودية على",
    },
    "opt_side_top": {
        "en": "Top",
        "de": "Oben",
        "es": "Arriba",
        "fr": "Haut",
        "ru": "Сверху",
        "zh": "顶部",
        "ar": "أعلى",
    },
    "opt_side_bottom": {
        "en": "Bottom",
        "de": "Unten",
        "es": "Abajo",
        "fr": "Bas",
        "ru": "Снизу",
        "zh": "底部",
        "ar": "أسفل",
    },
    "opt_side_left": {
        "en": "Left",
        "de": "Links",
        "es": "Izquierda",
        "fr": "Gauche",
        "ru": "Слева",
        "zh": "左侧",
        "ar": "يسار",
    },
    "opt_side_right": {
        "en": "Right",
        "de": "Rechts",
        "es": "Derecha",
        "fr": "Droite",
        "ru": "Справа",
        "zh": "右侧",
        "ar": "يمين",
    },
    "param_center_labels_label": {
        "en": "Label every grid cell (interior label, fixed to the cell)",
        "de": "Jede Rasterzelle beschriften (Innenbeschriftung, an der Zelle fixiert)",
        "es": "Etiquetar cada celda de la cuadrícula (etiqueta interior, fija a la celda)",
        "fr": "Étiqueter chaque cellule de la grille (étiquette intérieure, fixée à la cellule)",
        "ru": "Подписывать каждую ячейку сетки (внутренняя подпись, закреплённая за ячейкой)",
        "zh": "标注每个网格单元(内部标注,固定于该单元格)",
        "ar": "تسمية كل خلية في الشبكة (تسمية داخلية، مثبتة على الخلية)",
    },
    "param_output_grid_label": {
        "en": "Grid layer",
        "de": "Raster-Ebene",
        "es": "Capa de la cuadrícula",
        "fr": "Couche de la grille",
        "ru": "Слой сетки",
        "zh": "网格图层",
        "ar": "طبقة الشبكة",
    },
    "param_output_labels_label": {
        "en": "Grid labels",
        "de": "Rasterbeschriftung",
        "es": "Etiquetas de la cuadrícula",
        "fr": "Étiquettes de la grille",
        "ru": "Подписи сетки",
        "zh": "网格标注",
        "ar": "تسميات الشبكة",
    },
    "param_output_lines_label": {
        "en": "Grid lines",
        "de": "Rasterlinien",
        "es": "Líneas de la cuadrícula",
        "fr": "Lignes de la grille",
        "ru": "Линии сетки",
        "zh": "网格线",
        "ar": "خطوط الشبكة",
    },
    "param_grid_line_borders_label": {
        "en": "Close grid border on (unselected sides are left open)",
        "de": "Rasteraußenrand schließen bei (nicht ausgewählte Seiten bleiben offen)",
        "es": "Cerrar el borde de la cuadrícula en (los lados no seleccionados quedan abiertos)",
        "fr": "Fermer le bord de la grille sur (les côtés non sélectionnés restent ouverts)",
        "ru": "Замкнуть границу сетки на (невыбранные стороны остаются открытыми)",
        "zh": "在以下位置闭合网格边界(未选中的一侧将保持开放)",
        "ar": "إغلاق حد الشبكة عند (الجوانب غير المحددة تبقى مفتوحة)",
    },
    "hint_grid_line_borders": {
        "en": "Only affects the optional grid-lines output. Interior divider lines between cells are always included; this just controls the four outer edges.",
        "de": "Betrifft nur die optionale Rasterlinien-Ausgabe. Innere Trennlinien zwischen den Zellen werden immer erzeugt; dies steuert nur die vier Außenkanten.",
        "es": "Solo afecta a la salida opcional de líneas de la cuadrícula. Las líneas divisorias internas entre celdas siempre se incluyen; esto solo controla los cuatro bordes exteriores.",
        "fr": "N'affecte que la sortie facultative des lignes de la grille. Les lignes de séparation internes entre les cellules sont toujours incluses ; ceci ne contrôle que les quatre bords extérieurs.",
        "ru": "Влияет только на необязательный вывод линий сетки. Внутренние разделительные линии между ячейками добавляются всегда; это управляет только четырьмя внешними краями.",
        "zh": "仅影响可选的网格线输出。单元格之间的内部分隔线始终会生成;此选项仅控制四条外边。",
        "ar": "يؤثر فقط على مخرجات خطوط الشبكة الاختيارية. يتم دائمًا تضمين خطوط الفصل الداخلية بين الخلايا؛ يتحكم هذا فقط في الحواف الخارجية الأربع.",
    },
    "err_invalid_extent": {
        "en": "The grid extent is empty or invalid.",
        "de": "Die Rasterausdehnung ist leer oder ungültig.",
        "es": "La extensión de la cuadrícula está vacía o no es válida.",
        "fr": "L'emprise de la grille est vide ou invalide.",
        "ru": "Охват сетки пуст или недействителен.",
        "zh": "网格范围为空或无效。",
        "ar": "نطاق الشبكة فارغ أو غير صالح.",
    },
    "err_cell_size_required": {
        "en": "Cell width and height must both be greater than 0 when 'use a custom cell size' is checked.",
        "de": "Zellbreite und -höhe müssen größer als 0 sein, wenn 'eigene Zellgröße verwenden' aktiviert ist.",
        "es": "El ancho y el alto de celda deben ser mayores que 0 cuando 'usar un tamaño de celda personalizado' está marcado.",
        "fr": "La largeur et la hauteur de cellule doivent toutes deux être supérieures à 0 lorsque « utiliser une taille de cellule personnalisée » est coché.",
        "ru": "Ширина и высота ячейки должны быть больше 0, если отмечено «использовать свой размер ячейки».",
        "zh": "勾选「使用自定义单元格大小」时,单元格宽度和高度都必须大于 0。",
        "ar": "يجب أن يكون عرض وارتفاع الخلية أكبر من 0 كلاهما عند تفعيل 'استخدام حجم خلية مخصص'.",
    },
    "err_count_required": {
        "en": "Number of columns and rows must both be at least 1.",
        "de": "Spalten- und Zeilenanzahl müssen mindestens 1 betragen.",
        "es": "El número de columnas y filas debe ser al menos 1 en ambos casos.",
        "fr": "Le nombre de colonnes et de lignes doit être d'au moins 1 dans les deux cas.",
        "ru": "Количество столбцов и строк должно быть не менее 1 в обоих случаях.",
        "zh": "列数和行数都必须至少为 1。",
        "ar": "يجب أن يكون عدد الأعمدة والصفوف 1 على الأقل في كلتا الحالتين.",
    },
    "err_invalid_range": {
        "en": "Invalid label range: {detail}",
        "de": "Ungültiger Beschriftungsbereich: {detail}",
        "es": "Rango de etiquetas no válido: {detail}",
        "fr": "Plage d'étiquettes invalide : {detail}",
        "ru": "Недопустимый диапазон подписей: {detail}",
        "zh": "标注范围无效:{detail}",
        "ar": "نطاق تسمية غير صالح: {detail}",
    },
    "err_bad_label_format": {
        "en": "Cell label format '{fmt}' is invalid ({error}). Use only the placeholders {{col}} and {{row}}.",
        "de": "Format der Zellbeschriftung '{fmt}' ist ungültig ({error}). Nur die Platzhalter {{col}} und {{row}} verwenden.",
        "es": "El formato de etiqueta de celda '{fmt}' no es válido ({error}). Use solo los marcadores {{col}} y {{row}}.",
        "fr": "Le format d'étiquette de cellule « {fmt} » est invalide ({error}). N'utilisez que les paramètres {{col}} et {{row}}.",
        "ru": "Формат подписи ячейки '{fmt}' недопустим ({error}). Используйте только плейсхолдеры {{col}} и {{row}}.",
        "zh": "单元格标注格式 '{fmt}' 无效({error})。请仅使用占位符 {{col}} 和 {{row}}。",
        "ar": "تنسيق تسمية الخلية '{fmt}' غير صالح ({error}). استخدم فقط العناصر النائبة {{col}} و{{row}}.",
    },
    "info_custom_size_ignores_range": {
        "en": "Using a custom cell size: column/row count comes from the extent, so only the 'from' range values are used as starting labels - the 'to' values are ignored.",
        "de": "Eigene Zellgröße wird verwendet: Spalten-/Zeilenanzahl ergibt sich aus der Ausdehnung, daher werden nur die 'von'-Werte als Startbeschriftung verwendet - die 'bis'-Werte werden ignoriert.",
        "es": "Usando un tamaño de celda personalizado: el número de columnas/filas proviene de la extensión, así que solo se usan los valores 'desde' como etiquetas iniciales - los valores 'hasta' se ignoran.",
        "fr": "Utilisation d'une taille de cellule personnalisée : le nombre de colonnes/lignes provient de l'emprise, donc seules les valeurs « de » servent d'étiquettes de départ - les valeurs « à » sont ignorées.",
        "ru": "Используется свой размер ячейки: количество столбцов/строк определяется охватом, поэтому используются только значения «от» как начальные подписи - значения «до» игнорируются.",
        "zh": "正在使用自定义单元格大小:列/行数由范围决定,因此仅使用「从」的值作为起始标注 - 「到」的值将被忽略。",
        "ar": "يُستخدم حجم خلية مخصص: يُشتق عدد الأعمدة/الصفوف من النطاق، لذا تُستخدم فقط قيم 'من' كتسميات بداية - يتم تجاهل قيم 'إلى'.",
    },
    "err_too_many_cells": {
        "en": (
            "This would create {count} cells ({cols} columns x {rows} rows), "
            "which is more than the {limit} cell safety limit. Use a larger "
            "cell size, a smaller extent, or a smaller column/row count."
        ),
        "de": (
            "Dies würde {count} Zellen erzeugen ({cols} Spalten x {rows} Zeilen), "
            "mehr als das Sicherheitslimit von {limit} Zellen. Verwenden Sie eine "
            "größere Zellgröße, eine kleinere Ausdehnung oder weniger Spalten/Zeilen."
        ),
        "es": (
            "Esto crearía {count} celdas ({cols} columnas x {rows} filas), "
            "más que el límite de seguridad de {limit} celdas. Use un tamaño "
            "de celda mayor, una extensión menor o un número menor de "
            "columnas/filas."
        ),
        "fr": (
            "Cela créerait {count} cellules ({cols} colonnes x {rows} lignes), "
            "ce qui dépasse la limite de sécurité de {limit} cellules. "
            "Utilisez une taille de cellule plus grande, une emprise plus "
            "petite, ou un nombre de colonnes/lignes plus faible."
        ),
        "ru": (
            "Это создаст {count} ячеек ({cols} столбцов x {rows} строк), "
            "что превышает предел безопасности в {limit} ячеек. Используйте "
            "больший размер ячейки, меньший охват или меньшее количество "
            "столбцов/строк."
        ),
        "zh": (
            "这将创建 {count} 个单元格({cols} 列 x {rows} 行),超过了 "
            "{limit} 个单元格的安全限制。请使用更大的单元格大小、更小的范围或"
            "更少的列数/行数。"
        ),
        "ar": (
            "سيؤدي هذا إلى إنشاء {count} خلية ({cols} عمودًا × {rows} صفًا)، "
            "وهو أكثر من حد الأمان البالغ {limit} خلية. استخدم حجم خلية أكبر، "
            "أو نطاقًا أصغر، أو عدد أعمدة/صفوف أقل."
        ),
    },
    "info_grid_size": {
        "en": "Building a {cols} x {rows} grid ({count} cells) over the given extent.",
        "de": "Erstelle ein {cols} x {rows} Raster ({count} Zellen) über die angegebene Ausdehnung.",
        "es": "Creando una cuadrícula de {cols} x {rows} ({count} celdas) sobre la extensión indicada.",
        "fr": "Création d'une grille de {cols} x {rows} ({count} cellules) sur l'emprise donnée.",
        "ru": "Создание сетки {cols} x {rows} ({count} ячеек) над заданным охватом.",
        "zh": "正在给定范围上创建 {cols} x {rows} 的网格({count} 个单元格)。",
        "ar": "جارٍ إنشاء شبكة {cols} × {rows} ({count} خلية) فوق النطاق المحدد.",
    },
    "info_grid_extent": {
        "en": "Grid extent: {xmin}, {ymin} to {xmax}, {ymax} ({crs}) - {width} x {height}.",
        "de": "Rasterausdehnung: {xmin}, {ymin} bis {xmax}, {ymax} ({crs}) - {width} x {height}.",
        "es": "Extensión de la cuadrícula: {xmin}, {ymin} a {xmax}, {ymax} ({crs}) - {width} x {height}.",
        "fr": "Emprise de la grille : {xmin}, {ymin} à {xmax}, {ymax} ({crs}) - {width} x {height}.",
        "ru": "Охват сетки: {xmin}, {ymin} - {xmax}, {ymax} ({crs}) - {width} x {height}.",
        "zh": "网格范围:{xmin}, {ymin} 到 {xmax}, {ymax}({crs})- {width} x {height}。",
        "ar": "نطاق الشبكة: {xmin}, {ymin} إلى {xmax}, {ymax} ({crs}) - {width} × {height}.",
    },
    "info_grid_extent_layer_guess": {
        "en": "This extent matches the layer '{name}' (best guess, not guaranteed).",
        "de": "Diese Ausdehnung entspricht dem Layer '{name}' (bestmögliche Vermutung, keine Garantie).",
        "es": "Esta extensión coincide con la capa '{name}' (mejor estimación, no garantizada).",
        "fr": "Cette emprise correspond à la couche « {name} » (estimation, non garantie).",
        "ru": "Этот охват соответствует слою «{name}» (предположительно, без гарантии).",
        "zh": "此范围与图层 '{name}' 匹配(仅为推测,不保证准确)。",
        "ar": "يتطابق هذا النطاق مع الطبقة '{name}' (تخمين تقريبي، دون ضمان).",
    },
    "menu_name": {
        "en": "Reference Grid Labeler",
        "de": "Kartenraster-Beschriftung",
        "es": "Etiquetador de cuadrícula de referencia",
        "fr": "Étiqueteur de grille de référence",
        "ru": "Подписи координатной сетки",
        "zh": "参考网格标注器",
        "ar": "أداة تسمية الشبكة المرجعية",
    },
    "action_text": {
        "en": "Reference Grid Labeler...",
        "de": "Kartenraster-Beschriftung...",
        "es": "Etiquetador de cuadrícula de referencia...",
        "fr": "Étiqueteur de grille de référence...",
        "ru": "Подписи координатной сетки...",
        "zh": "参考网格标注器...",
        "ar": "أداة تسمية الشبكة المرجعية...",
    },
    "action_tooltip": {
        "en": "Build an atlas-style reference grid over the canvas or a layer's extent",
        "de": "Ein Kartenraster im Atlas-Stil über die Karten- oder Layerausdehnung erstellen",
        "es": "Crear una cuadrícula de referencia al estilo atlas sobre el lienzo o la extensión de una capa",
        "fr": "Créer une grille de référence de style atlas sur le canevas ou l'emprise d'une couche",
        "ru": "Создать координатную сетку в стиле атласа поверх охвата карты или слоя",
        "zh": "在画布或图层范围上创建图集风格的参考网格",
        "ar": "إنشاء شبكة مرجعية على طراز الأطالس فوق لوحة الخريطة أو نطاق طبقة",
    },
}


def tr(key, **kwargs):
    lang = current_language()
    entry = STRINGS.get(key, {})
    text = entry.get(lang) or entry.get("en") or key
    return text.format(**kwargs) if kwargs else text
