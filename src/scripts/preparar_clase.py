#!/usr/bin/env python3
"""Andamiaje para el pipeline de estudio de la materia.

Hace la parte mecanica y determinista del flujo descrito en el README:

    src/notebooks/raw/<nombre crudo>.ipynb
        -> src/notebooks/raw/<slug>.ipynb          (renombrado normalizado)
        -> src/notebooks/exercises/<slug>.ipynb    (enunciados + placeholders)
        -> src/notebooks/explained/<slug>.ipynb    (esqueleto a completar y ejecutar)

La explicacion pedagogica no se genera aca: la escribe Claude siguiendo la
skill `clase` (.claude/skills/clase/SKILL.md). Este script solo le prepara el
terreno y le entrega un "mapa de celdas" para que pueda citar la notebook
original sin inventar numeros.

Solo biblioteca estandar: el proyecto no declara dependencias.

Uso:
    python src/scripts/preparar_clase.py detectar
    python src/scripts/preparar_clase.py preparar --raw <path> --slug <slug>
    python src/scripts/preparar_clase.py mapa --slug <slug>
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------
# Rutas del repo (este archivo vive en src/scripts/)
# --------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent.parent
DIR_RAW = RAIZ / "src" / "notebooks" / "raw"
DIR_EXPLAINED = RAIZ / "src" / "notebooks" / "explained"
DIR_EXERCISES = RAIZ / "src" / "notebooks" / "exercises"
DIR_FIGURAS = RAIZ / "src" / "figuras"

RE_SLUG = re.compile(r"^\d+_[a-z0-9_]+$")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$", re.MULTILINE)
RE_IMG = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)
RE_MARCA_EJERCICIO = re.compile(r"^\*\*Ejercicio\b", re.MULTILINE)
RE_SUBITEM = re.compile(r"^\s*\d+\.\s+(.*)$", re.MULTILINE)
# Encabezados de portada: aparecen en la primera slide de toda clase y no
# describen ningun tema, asi que no deben formar parte de la clave del bloque.
RE_PORTADA = re.compile(r"^(Aprendizaje Autom[áa]tico|(Primer|Segundo) cuatrimestre \d{4})$", re.IGNORECASE)

# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------


# Palabras que no aportan a identificar la clase y solo alargan el slug.
VACIAS = {"de", "del", "la", "las", "el", "los", "por", "y", "e", "a", "al",
          "un", "una", "con", "en", "para"}


def slugify(texto: str, max_palabras: int = 5) -> str:
    """'Regresión Lineal, cuadrados mínimos' -> 'regresion_lineal_cuadrados_minimos'."""
    sin_tildes = unicodedata.normalize("NFKD", texto)
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    limpio = re.sub(r"[^a-zA-Z0-9]+", "_", sin_tildes).strip("_").lower()
    palabras = [w for w in limpio.split("_") if w and w not in VACIAS]
    return "_".join(palabras[:max_palabras])


def cargar_nb(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def fuente(celda: dict) -> str:
    src = celda.get("source", "")
    return src if isinstance(src, str) else "".join(src)


def como_lineas(texto: str) -> list[str]:
    """Formato `source` de nbformat: lista de lineas con \\n salvo la ultima."""
    lineas = texto.splitlines(keepends=True)
    return lineas if lineas else [""]


def headings(celda: dict) -> list[str]:
    if celda.get("cell_type") != "markdown":
        return []  # en una celda de codigo, '# algo' es un comentario de Python
    crudos = [m.group(2).replace("**", "").strip()
              for m in RE_HEADING.finditer(fuente(celda))]
    return [h for h in crudos if not RE_PORTADA.match(h)]


def resumir(texto: str, largo: int = 90) -> str:
    """Primera oracion util, en una sola linea, para usar como titulo/comentario."""
    primera = texto.strip().split("\n", 1)[0]
    plano = re.sub(r"\s+", " ", primera).strip()
    plano = re.sub(r"^\*\*Ejercicio:?\*\*\s*", "", plano)
    plano = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", plano)  # links markdown
    plano = plano.replace("*", "").replace("`", "")
    corte = re.split(r"(?<=[.?:])\s", plano, maxsplit=1)[0]
    if len(corte) > largo:
        corte = corte[: largo - 1].rsplit(" ", 1)[0] + "…"
    return corte.strip(" .:")


def proximo_numero() -> int:
    numeros = [
        int(m.group(1))
        for p in DIR_RAW.glob("*.ipynb")
        if (m := re.match(r"^(\d+)_", p.stem))
    ]
    return max(numeros, default=0) + 1


# --------------------------------------------------------------------------
# Mapa de celdas: el puente entre el script y la skill
# --------------------------------------------------------------------------


def construir_mapa(nb: dict, titulo: str = "") -> dict:
    """Describe la notebook celda por celda y la agrupa en bloques tematicos.

    Estas notebooks son "slides": muchas celdas markdown cortas que repiten el
    mismo encabezado y van sumando contenido de a poco. Agrupar celdas
    consecutivas que comparten encabezado da la unidad real de explicacion.
    """
    celdas: list[dict] = []
    bloques: list[dict] = []
    clave_actual: tuple[str, ...] | None = None

    for i, celda in enumerate(nb.get("cells", [])):
        src = fuente(celda)
        hs = headings(celda)
        imagenes = RE_IMG.findall(src)
        es_ej = bool(RE_MARCA_EJERCICIO.search(src)) or any(
            "ejercicio" in h.lower() for h in hs
        )

        celdas.append(
            {
                "indice": i,
                "tipo": celda.get("cell_type"),
                "encabezados": hs,
                "preview": resumir(re.sub(r"^#+\s+.*$", "", src, flags=re.MULTILINE), 120),
                "lineas": len(src.splitlines()),
                "tiene_formulas": "$$" in src,
                "imagenes": imagenes,
                "es_ejercicio": es_ej,
            }
        )

        if es_ej:
            clave_actual = None  # los ejercicios no forman bloque tematico
            continue
        if not src.strip():
            continue

        # Una celda sin encabezado (o de codigo) continua el bloque anterior.
        clave = tuple(hs) if hs else clave_actual
        if clave is None:
            clave = ("(sin titulo)",)

        if bloques and clave == clave_actual:
            bloques[-1]["celdas"][1] = i
        else:
            bloques.append({"titulo": " › ".join(clave), "celdas": [i, i]})
        clave_actual = clave

    referenciadas = sorted({img for c in celdas for img in c["imagenes"]})

    return {
        "total_celdas": len(celdas),
        "titulo_clase": titulo or tema_portada(nb) or "Clase sin título",
        "tema_portada": tema_portada(nb),
        "bloques": bloques,
        "celdas": celdas,
        "figuras_referenciadas": referenciadas,
        "figuras_disponibles": {img: buscar_figura(img) for img in referenciadas},
    }


def buscar_figura(referencia: str) -> str | None:
    """Busca en src/figuras/ el archivo que citaba la notebook cruda.

    La notebook cruda referencia rutas tipo 'Figuras/<archivo>.png'; acá esa
    carpeta se llama 'src/figuras/'. Compara solo el nombre de archivo (sin la
    carpeta), asi que un cambio de mayusculas/carpeta no rompe la busqueda.
    Devuelve la ruta relativa a la raiz del repo si existe, o None.
    """
    nombre = Path(referencia).name
    candidato = DIR_FIGURAS / nombre
    if candidato.exists():
        return str(candidato.relative_to(RAIZ))
    return None


def tema_portada(nb: dict) -> str:
    """El primer encabezado `##` de la notebook.

    La celda 0 suele ser '# Aprendizaje Automático / #### <cuatrimestre> / ## <tema>'.
    """
    for celda in nb.get("cells", []):
        if celda.get("cell_type") != "markdown":
            continue
        for m in RE_HEADING.finditer(fuente(celda)):
            if len(m.group(1)) == 2:
                return m.group(2).replace("**", "").strip()
    return ""


# --------------------------------------------------------------------------
# Ejercicios
# --------------------------------------------------------------------------

# Si el encabezado del enunciado matchea esto, la consigna es de leer / pensar /
# decidir, aunque mencione librerias o codigo. Se chequea primero a proposito:
# "Ir a la documentación y al código de la regresión lineal en Scikit-Learn"
# NO es un ejercicio de programar.
MARCAS_CONCEPTUAL = (
    "ir a la documentaci", "familiarizarse", "leer acerca", "leer el",
    "investigar", "reflexionar", "elegir", "decidir", "dados los siguientes",
    "qué otros", "que otros", "discutir", "justificar por qué",
)
MARCAS_CODIGO = (
    "implementar", "graficar", "reproducir", "dataset", "numpy", "pandas",
    "statsmodels", "scikit", "sklearn", "matplotlib", "ajustar el modelo",
    "obtener el error", "simular", "calcular numéricamente", "entrenar",
)
MARCAS_TEORICO = (
    "mostrar que", "demostrar", "probar que", "deducir", "derivar",
    "encontrar el mínimo", "escribir la función", "expandir la expresión",
    "plantear la expresión", "minimiza", "maximiza", "escribir la expresión",
    "verificar que", "obtener la expresión",
)


def clasificar(enunciado: str) -> str:
    cuerpo = enunciado.lower()
    cabeza = cuerpo.split("\n", 1)[0]

    if any(m in cabeza for m in MARCAS_CONCEPTUAL):
        return "conceptual"
    if any(m in cabeza for m in MARCAS_CODIGO) or any(m in cuerpo for m in MARCAS_CODIGO):
        return "codigo"
    if any(m in cuerpo for m in MARCAS_TEORICO):
        return "teorico"
    return "conceptual"


def extraer_ejercicios(nb: dict) -> list[dict]:
    """Parte las celdas de ejercicios en consignas individuales.

    El enunciado se conserva verbatim: solo se le saca el prefijo '**Ejercicio:**',
    que pasa a ser el encabezado de la celda.
    """
    ejercicios: list[dict] = []
    for celda in nb.get("cells", []):
        if celda.get("cell_type") != "markdown":
            continue
        src = fuente(celda)
        if not RE_MARCA_EJERCICIO.search(src):
            continue
        for chunk in re.split(r"(?m)^(?=\*\*Ejercicio\b)", src):
            chunk = chunk.strip()
            if not chunk.startswith("**Ejercicio"):
                continue  # el encabezado '### Ejercicios' de la celda
            cuerpo = re.sub(r"^\*\*Ejercicio:?\*\*\s*", "", chunk).strip()
            subitems = [
                re.sub(r"\s+", " ", s).strip()
                for s in RE_SUBITEM.findall(cuerpo)
            ]
            ejercicios.append(
                {
                    "numero": len(ejercicios) + 1,
                    "titulo": resumir(cuerpo, 70),
                    "enunciado": cuerpo,
                    "subitems": subitems,
                    "tipo_sugerido": clasificar(cuerpo),
                }
            )

    return ejercicios


# --------------------------------------------------------------------------
# Generacion del notebook de ejercicios
# --------------------------------------------------------------------------


def celda_md(texto: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": como_lineas(texto)}


def celda_code(texto: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": como_lineas(texto),
    }


def placeholders(ej: dict) -> list[dict]:
    n = ej["numero"]
    items = ej["subitems"] or [""]
    tipo = ej["tipo_sugerido"]

    if tipo == "codigo":
        celdas = []
        for j, item in enumerate(items, start=1):
            etiqueta = f"# {n}.{j} — {resumir(item, 80)}" if item else f"# {n}"
            celdas.append(celda_code(f"{etiqueta}\n# TODO\n"))
        return celdas

    encabezado = "**Mi resolución:**" if tipo == "teorico" else "**Mi respuesta:**"
    vineta = "" if tipo == "teorico" else "- "

    if not ej["subitems"]:
        return [celda_md(f"{encabezado}\n\n{vineta}\n")]

    partes = [encabezado, ""]
    for j, item in enumerate(ej["subitems"], start=1):
        partes += [f"<!-- {n}.{j} — {resumir(item, 100)} -->", vineta, ""]
    return [celda_md("\n".join(partes).rstrip() + "\n")]


def construir_notebook_ejercicios(nb: dict, ejercicios: list[dict], slug: str,
                                  titulo: str) -> dict:
    cabecera = (
        f"# Ejercicios — {titulo}\n"
        "\n"
        f"- 📘 Explicación: [`../explained/{slug}.ipynb`](../explained/{slug}.ipynb)\n"
        f"- 📓 Notebook de clase: [`../raw/{slug}.ipynb`](../raw/{slug}.ipynb)\n"
        "\n"
        "> Los enunciados están tal cual los dio la cátedra. Las pistas ("
        "*centros*) están al final de la notebook explicada.\n"
    )
    celdas = [celda_md(cabecera)]

    if any(e["tipo_sugerido"] == "codigo" for e in ejercicios):
        celdas.append(
            celda_code(
                "from pathlib import Path\n"
                "\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "\n"
                'DATA_DIR = Path("../../datasets")\n'
            )
        )

    for ej in ejercicios:
        celdas.append(
            celda_md(
                f"---\n\n### Ejercicio {ej['numero']} — {ej['titulo']}\n\n"
                f"{ej['enunciado']}\n"
            )
        )
        celdas.extend(placeholders(ej))

    return {
        "cells": celdas,
        "metadata": nb.get("metadata", {}),
        "nbformat": nb.get("nbformat", 4),
        "nbformat_minor": nb.get("nbformat_minor", 5),
    }


# --------------------------------------------------------------------------
# Generacion del esqueleto de la notebook explicada
# --------------------------------------------------------------------------

PATRON_BLOQUE_MD = """## 1. <Título de la sección>

📓 celdas <n>–<m> · 📕 ESL §<x.y>

### La idea en criollo

<!-- analogía concreta + dónde se rompe la analogía -->

### Formalizándolo

<!-- la matemática, paso a paso, cada paso justificado -->

### ¿Por qué nos importa?

<!-- qué habilita / qué se rompe sin esto -->
"""

PATRON_BLOQUE_CODE = """# En código: <qué muestra este snippet>
# TODO: reemplazar por código real y ejecutable (ver referencias/estilo_graficos.md
# si esta celda grafica algo). Correr nbconvert --execute antes de dar la sección
# por terminada.
"""

PATRON_BLOQUE_CIERRE_MD = """### ⚠️ Confusión típica

<!-- el error que vas a cometer acá -->
"""


def construir_esqueleto_notebook(mapa: dict, ejercicios: list[dict], slug: str,
                                 numero: int) -> dict:
    """Esqueleto de la notebook explicada, como celdas de .ipynb.

    No pre-crea una seccion por bloque a proposito: estas notebooks son slides y
    tienen 30+ bloques, pero el documento de estudio necesita 5-10 secciones
    tematicas. La tabla del mapa lista *todos* los bloques y su ultima columna
    ("Dónde lo explico") es la que garantiza que ninguno quede huerfano.

    Las celdas de codigo quedan vacias de contenido real (son placeholders):
    quien escribe la notebook las completa y las ejecuta con
    `jupyter nbconvert --execute` antes de darla por terminada.
    """
    intro = [
        f"# {numero} — {mapa['titulo_clase']}",
        "",
        f"📓 [Notebook de clase](../raw/{slug}.ipynb) · "
        f"✏️ [Ejercicios](../exercises/{slug}.ipynb) · "
        "📕 *ESL* (Hastie, Tibshirani & Friedman) como referencia principal",
        "",
        "> **TL;DR**",
        ">",
        "> <!-- 5 bullets: si te acordás solo de esto, zafaste -->",
        "",
        "## 🗺️ Mapa de la clase",
        "",
        "<!-- Agrupá estos bloques en 5–10 secciones temáticas y completá la",
        "     última columna. Ningún bloque puede quedar sin sección. -->",
        "",
        "| Bloque de la clase | Celdas | Dónde lo explico |",
        "|--------------------|--------|------------------|",
    ]

    for bloque in mapa["bloques"]:
        ini, fin = bloque["celdas"]
        rango = f"{ini}" if ini == fin else f"{ini}–{fin}"
        intro.append(f"| {bloque['titulo']} | {rango} | §? |")

    disponibles = mapa.get("figuras_disponibles", {})
    if mapa["figuras_referenciadas"]:
        encontradas = [f for f in mapa["figuras_referenciadas"] if disponibles.get(f)]
        faltantes = [f for f in mapa["figuras_referenciadas"] if not disponibles.get(f)]
        intro += ["", "<!-- Figuras que la clase mostraba:"]
        if encontradas:
            intro += ["     Están en src/figuras/: embebelas con"]
            intro += [f"       - {disponibles[f]}  (referenciada como {f})" for f in encontradas]
        if faltantes:
            intro += ["     NO están en src/figuras/: describilas en palabras, sin imagen rota:"]
            intro += [f"       - {f}" for f in faltantes]
        intro += ["-->"]

    intro += [
        "",
        "<!-- Si la clase introduce notación nueva, arrancá con una sección",
        "     '## 0. Notación y convenciones'. -->",
    ]

    celdas = [celda_md("\n".join(intro))]

    celdas.append(celda_code(
        "# Setup — pegar acá el snippet de referencias/estilo_graficos.md\n"
    ))

    celdas.append(celda_md(PATRON_BLOQUE_MD))
    celdas.append(celda_code(PATRON_BLOQUE_CODE))
    celdas.append(celda_md(PATRON_BLOQUE_CIERRE_MD))
    celdas.append(celda_md("<!-- ... repetí ese patrón (markdown + código + markdown) para cada sección ... -->"))

    cierre = [
        "## 🧵 El hilo conductor",
        "",
        "<!-- cómo se encadena todo: de dónde venimos, hacia dónde vamos -->",
        "",
        "## ✅ Autoevaluación",
        "",
        "<!-- 6 a 10 preguntas de menor a mayor, cada respuesta en <details> -->",
        "",
        "## 🎯 Centros para los ejercicios",
        "",
    ]

    for ej in ejercicios:
        cierre += [
            f"### Ejercicio {ej['numero']} — {ej['titulo']}",
            "",
            f"<!-- tipo detectado por el script: {ej['tipo_sugerido']} -->",
            "",
            "- **De qué va realmente:** <!-- -->",
            "- **Por dónde arrancar:** <!-- -->",
            "- **Con qué chequear:** <!-- -->",
            "- **⚠️ Dónde te vas a trabar:** <!-- -->",
            "",
        ]

    celdas.append(celda_md("\n".join(cierre)))

    return {
        "cells": celdas,
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


# --------------------------------------------------------------------------
# Subcomandos
# --------------------------------------------------------------------------


def cmd_detectar(_args: argparse.Namespace) -> int:
    pendientes = []
    siguiente = proximo_numero()

    for path in sorted(DIR_RAW.glob("*.ipynb")):
        normalizado = bool(RE_SLUG.match(path.stem))
        if normalizado:
            slug = path.stem
            falta = [
                d.name
                for d, ext in ((DIR_EXPLAINED, ".ipynb"), (DIR_EXERCISES, ".ipynb"))
                if not (d / f"{slug}{ext}").exists()
            ]
            if not falta:
                continue
            pendientes.append(
                {"raw": str(path.relative_to(RAIZ)), "slug": slug,
                 "estado": "renombrado, falta " + " y ".join(falta)}
            )
        else:
            pendientes.append(
                {
                    "raw": str(path.relative_to(RAIZ)),
                    "slug_propuesto": f"{siguiente}_{slugify(path.stem)}",
                    "estado": "sin procesar",
                }
            )
            siguiente += 1

    print(json.dumps({"pendientes": pendientes}, ensure_ascii=False, indent=2))
    if not pendientes:
        print("\n# Todo procesado: no hay nada pendiente en src/notebooks/raw/",
              file=sys.stderr)
    return 0


def cmd_preparar(args: argparse.Namespace) -> int:
    raw = Path(args.raw)
    if not raw.is_absolute():
        raw = (RAIZ / raw) if (RAIZ / raw).exists() else (DIR_RAW / raw)
    if not raw.exists():
        print(f"error: no existe {raw}", file=sys.stderr)
        return 1

    slug = args.slug
    if not RE_SLUG.match(slug):
        print(f"error: el slug '{slug}' no tiene la forma <n>_<palabras_con_guion_bajo>",
              file=sys.stderr)
        return 1

    numero = int(slug.split("_", 1)[0])
    destino_raw = DIR_RAW / f"{slug}.ipynb"
    destino_explained = DIR_EXPLAINED / f"{slug}.ipynb"
    destino_ej = DIR_EXERCISES / f"{slug}.ipynb"

    nb = cargar_nb(raw)
    # El nombre crudo del archivo es como la catedra nombro la clase y suele ser
    # mejor titulo que el encabezado de la portada. Si ya fue renombrado, no
    # sirve: se cae al encabezado '##' de la primera slide.
    titulo = "" if RE_SLUG.match(raw.stem) else re.sub(r"\s+", " ", raw.stem).strip()
    mapa = construir_mapa(nb, titulo)
    ejercicios = extraer_ejercicios(nb)

    if args.dry_run:
        print(json.dumps(
            {"renombraria": [str(raw.relative_to(RAIZ)), str(destino_raw.relative_to(RAIZ))],
             "mapa": mapa,
             "ejercicios": ejercicios},
            ensure_ascii=False, indent=2))
        return 0

    # 1. Renombrar el raw (via git para que quede registrado como rename).
    if raw.resolve() != destino_raw.resolve():
        if destino_raw.exists():
            print(f"error: ya existe {destino_raw}", file=sys.stderr)
            return 1
        try:
            subprocess.run(
                ["git", "mv", str(raw), str(destino_raw)],
                cwd=RAIZ, check=True, capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raw.rename(destino_raw)  # no trackeado o sin git disponible

    # 2 y 3. Andamios derivados. Nunca se pisan sin --force: los dos .ipynb
    # pueden tener resoluciones o explicacion ya escritas.
    escritos, saltados = [], []

    for destino, contenido in (
        (destino_ej, json.dumps(
            construir_notebook_ejercicios(nb, ejercicios, slug, mapa["titulo_clase"]),
            ensure_ascii=False, indent=1) + "\n"),
        (destino_explained, json.dumps(
            construir_esqueleto_notebook(mapa, ejercicios, slug, numero),
            ensure_ascii=False, indent=1) + "\n"),
    ):
        if destino.exists() and not args.force:
            saltados.append(str(destino.relative_to(RAIZ)))
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(contenido, encoding="utf-8")
        escritos.append(str(destino.relative_to(RAIZ)))

    print(json.dumps(
        {
            "slug": slug,
            "raw": str(destino_raw.relative_to(RAIZ)),
            "escritos": escritos,
            "saltados_ya_existian": saltados,
            "mapa": mapa,
            "ejercicios": ejercicios,
        },
        ensure_ascii=False, indent=2))
    return 0


def cmd_fuentes(args: argparse.Namespace) -> int:
    """Vuelca el contenido de todas las celdas, sin outputs.

    Una notebook de clase con figuras pesa cientos de KB de imagenes en base64.
    Esto imprime solo lo que hay que leer para entender la clase.
    """
    raw = DIR_RAW / f"{args.slug}.ipynb"
    if not raw.exists():
        print(f"error: no existe {raw}", file=sys.stderr)
        return 1
    nb = cargar_nb(raw)
    for i, celda in enumerate(nb.get("cells", [])):
        tipo = celda.get("cell_type")
        print(f"\n=== [{i}] {tipo} " + "=" * 50)
        print(fuente(celda).rstrip())
    return 0


def cmd_mapa(args: argparse.Namespace) -> int:
    raw = DIR_RAW / f"{args.slug}.ipynb"
    if not raw.exists():
        print(f"error: no existe {raw}", file=sys.stderr)
        return 1
    nb = cargar_nb(raw)
    print(json.dumps(
        {"mapa": construir_mapa(nb), "ejercicios": extraer_ejercicios(nb)},
        ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    subs = parser.add_subparsers(dest="cmd", required=True)

    subs.add_parser("detectar", help="lista notebooks sin procesar y propone slugs"
                    ).set_defaults(func=cmd_detectar)

    p = subs.add_parser("preparar", help="renombra el raw y genera los andamios")
    p.add_argument("--raw", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--force", action="store_true",
                   help="pisa los .ipynb de explained/ y exercises/ si ya existen")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(func=cmd_preparar)

    p = subs.add_parser("mapa", help="reimprime el mapa de celdas de una clase ya procesada")
    p.add_argument("--slug", required=True)
    p.set_defaults(func=cmd_mapa)

    p = subs.add_parser("fuentes", help="vuelca todas las celdas del raw, sin outputs")
    p.add_argument("--slug", required=True)
    p.set_defaults(func=cmd_fuentes)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
