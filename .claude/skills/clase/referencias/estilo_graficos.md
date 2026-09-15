# Estilo de gráficos

Convención única para que todos los gráficos de `explained/` se vean como si
salieran del mismo lugar, sin importar qué clase los generó. Leé esto **antes**
de escribir la primera celda de código que grafique algo.

## El snippet de Setup

Va una sola vez, en la primera celda de código de la notebook (la que el
esqueleto deja como `# Setup — pegar acá el snippet de referencias/estilo_graficos.md`).
El resto de las celdas de código de la notebook no vuelven a tocar el estilo:
ya queda seteado para toda la sesión del kernel.

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid", palette="colorblind")
plt.rcParams.update({
    "figure.figsize": (7, 4.5),
    "figure.dpi": 110,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "legend.frameon": False,
})
```

Ajustá los `import` a lo que la sección realmente use (no importes `sklearn`
si no aparece en esa celda), pero el bloque de `sns.set_theme` +
`plt.rcParams.update` va siempre igual, tal cual.

## Por qué esta elección

- **`whitegrid`**: grilla sutil de fondo que ayuda a leer valores en gráficos
  de dispersión y líneas (frecuentes en esta materia: residuos, curvas de
  aprendizaje, fronteras de decisión) sin ensuciar la figura.
- **Paleta `colorblind`**: paleta categórica de seaborn pensada para
  daltonismo. Si una sección necesita distinguir 3 o más grupos (clases,
  modelos, folds), esta paleta ya viene bien elegida — no armes una paleta de
  colores a mano.
- **`figure.figsize` y `dpi` fijos**: todos los gráficos entran en el ancho de
  lectura de un notebook sin verse ni gigantes ni microscópicos, y con
  suficiente resolución para que una curva o un punto se distingan bien.
- **`axes.titleweight: bold`**: el título del gráfico es lo primero que se lee;
  que se note sin necesitar leer el eje.

## Cuándo el gráfico necesita algo más

- **Escala de color continua** (heatmap de una matriz, superficie de error):
  usá `cmap="viridis"` explícito en esa llamada puntual. `colorblind` es
  categórica, no sirve para esto.
- **Resaltar un único punto o curva** (el mínimo de una función de costo, el
  óptimo de un hiperparámetro): un solo color de acento alcanza, no hace falta
  tocar la paleta global — marcalo con `color="crimson"` o similar solo en esa
  serie.
- **Dos paneles comparando "a mano" vs. "librería"**: `plt.subplots(1, 2, figsize=(11, 4.5))`,
  mismo eje `y` en ambos (`sharey=True`) para que la comparación sea justa a
  simple vista.

## Qué no hacer

- No reinventes el estilo por sección: si una celda de código necesita
  `plt.style.use(...)` o una paleta distinta a `colorblind`, es señal de que
  se te fue de tema — volvé al snippet de Setup.
- No dejes un gráfico sin `ax.set_xlabel` / `ax.set_ylabel` / título. El punto
  de graficar acá es que se entienda solo, sin tener que leer el código que lo
  generó.
