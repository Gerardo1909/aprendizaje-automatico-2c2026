# Repositorio para la materia "Aprendizaje Automático" - 2do cuatrimestre, 2026

Este es mi repositorio personal para desarrollar los ejercicios de la materia, entender los temas y asi poder profundizar. 

La idea es seguir el siguiente flujo: 

1. Los notebooks que presentan en clase los bajo dentro de `src/notebooks/raw`, asi tal como vienen. Aqui una pequeña transformación que haremos es cambiar el nombre para normalizarlo, algo del estilo: "Introducción - Teoría de la Decisión" -> "1_intro_teoria_decision" y ese nombre es el que usamos para identificar a otros documentos relacionados

2.  Mediante claude proceso el notebook "crudo" y genero una explicación, con analogías, ejemplos y otras referencias dentro de `src/notebooks/explained` . Esto es lo que leeria despues de una clase y antes de iniciar a hacer los ejercicios, me debería de dejar listo. El formato debe ser un .md, con sus snippets de codigo y formateo para hacerlo visual pero sin perder rigor tecnico

3. En paralelo con 2. la idea es que se genere un notebook que contenga unicamente los enunciados de los ejercicios dentro de `src/notebooks/exercises` y placeholders para posteriormente resolverlos. 

>  Algo trasversal que deberia ocurrir con toda esta linea de notebooks y archivos .md es que todos tienen el mismo nombre en cada uno de los 3 directorios, los diferencia su ruta absoluta dentro del repo.

## Herramientas

El flujo de arriba está automatizado en la skill **`/clase`** (vive en
`.claude/skills/clase/`, versionada en el repo para que funcione en cualquier
máquina).

```
/clase                          # detecta la notebook sin procesar en src/notebooks/raw
/clase "Regresión Lineal..."    # procesa esa notebook
/clase 2_regresion_lineal_...   # reescribe el .md de una clase ya procesada
```

Hace los tres pasos de una: renombra el crudo, genera el `.ipynb` de ejercicios
con placeholders y escribe la explicación en `explained/`.

La parte mecánica la hace `src/scripts/preparar_clase.py`, que también sirve
suelto (solo biblioteca estándar):

```bash
python3 src/scripts/preparar_clase.py detectar                        # qué falta procesar
python3 src/scripts/preparar_clase.py preparar --raw <ruta> --slug <slug>
python3 src/scripts/preparar_clase.py mapa --slug <slug>              # mapa de celdas
python3 src/scripts/preparar_clase.py fuentes --slug <slug>           # celdas sin outputs
python3 src/scripts/preparar_clase.py html --slug <slug> --abrir      # vista con fórmulas
```

### Ver las fórmulas

Los `.md` de `explained/` usan LaTeX (`$...$` y `$$...$$`). Se renderizan solos
en **GitHub** y en el preview de **Cursor / VS Code**, pero **Zed no procesa
matemática** y muestra el LaTeX crudo. Para esos casos:

```bash
python3 src/scripts/preparar_clase.py html --slug 1_intro_teoria_decision --abrir
```

Genera un `.html` al lado del `.md` y lo abre en el navegador, con las fórmulas
compuestas por MathJax. Es un archivo derivado y está en `.gitignore`: se
regenera cuando haga falta. Necesita internet la primera vez (baja MathJax de
un CDN); después queda en la caché del navegador.

`preparar` nunca pisa un `.md` o un `.ipynb` que ya exista (usá `--force` si de
verdad querés regenerarlos): los ejercicios pueden tener resoluciones escritas.

## Bibliografía para esta materia:

The Elements of Statistical Learning. Trevor Hastie, Robert Tibshirani, Jerome Friedman. (https://hastie.su.domains/ElemStatLearn/) - **REFERENCIA PRINCIPAL**
An Introduction to Statistical Learning. (https://www.statlearning.com/) Muy útil como primera aproximación, pero más superficial, a los temas. 
Pattern Recognition and Machine Learning. (https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf) Christopher M. Bishop.
