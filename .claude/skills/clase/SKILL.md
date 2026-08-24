---
name: clase
description: Procesa una notebook de clase de Aprendizaje Automático - normaliza su nombre, genera el notebook de ejercicios con placeholders y escribe la explicación pedagógica completa en src/notebooks/explained. Usar cuando el usuario escriba /clase, baje una notebook nueva a src/notebooks/raw, o pida "procesá la clase X", "explicame la clase de ...", "armá el material de estudio de ...".
---

# Procesar una clase

Convertís la notebook cruda de una clase en material de estudio: un `.md` que se
lea como un profesor particular explicando el tema, y un `.ipynb` de ejercicios
listo para resolver.

El `.md` es el 90% del trabajo. Todo lo demás es andamiaje que hace el script.

## Argumentos

| Invocación | Qué hace |
|---|---|
| `/clase` | Detecta la notebook sin procesar. Si hay más de una, preguntá cuál. |
| `/clase "Regresión Lineal..."` | Procesa esa notebook cruda. |
| `/clase 2_regresion_lineal_...` | Ya está procesada: reescribí o mejorá su `.md`. |

Todos los comandos se corren desde la raíz del repo.

---

## Paso 1 — Preparar el andamiaje

```bash
python3 src/scripts/preparar_clase.py detectar
```

Devuelve las notebooks pendientes y un `slug_propuesto` para cada una. El slug es
la clave que une los tres directorios (`raw/`, `explained/`, `exercises/`), así
que **mostrale el slug al usuario y esperá que lo confirme o lo corrija antes de
seguir**. Es un renombrado de archivo, y en este repo `src/` puede no estar
trackeado en git — no hay `undo` gratis.

**Si el usuario ya te dio el slug en el pedido, ya está confirmado: usalo y
seguí de largo.** No vuelvas a preguntar ni te quedes esperando una respuesta.

Con el slug confirmado:

```bash
python3 src/scripts/preparar_clase.py preparar --raw "<ruta cruda>" --slug <slug>
```

Renombra el raw, genera el `.ipynb` de ejercicios y el esqueleto del `.md`, e
imprime el **mapa de celdas** y los **ejercicios detectados**. Guardá esa salida:
la vas a usar todo el tiempo.

No pisa archivos existentes (el `.ipynb` puede tener resoluciones tuyas, el `.md`
puede tener explicación escrita). Si de verdad hay que regenerarlos, `--force`.

Si la clase ya estaba procesada, en vez de `preparar` corré:

```bash
python3 src/scripts/preparar_clase.py mapa --slug <slug>
```

## Paso 2 — Leer la clase entera

```bash
python3 src/scripts/preparar_clase.py fuentes --slug <slug>
```

Vuelca todas las celdas sin los outputs (una notebook con figuras pesa cientos de
KB en base64 que no aportan nada).

**Leé todas las celdas. No muestrees.** Estas notebooks son *slides*: celdas
markdown cortas que repiten encabezado y suman de a poco. Una celda suelta no se
entiende; la secuencia sí.

Mientras leés, anotá tres cosas:

1. **Qué se demuestra y qué se afirma sin demostrar.** Lo segundo es donde tenés
   que completar con el libro.
2. **Las preguntas retóricas que quedan colgadas.** Estas clases están llenas:
   *"¿Cómo estimamos $\sigma^2$?"*, *"¿cuál es su dimensión?"*, *"¿Se parece a lo
   que vimos antes?"*. El docente las tira y sigue. **Respondelas todas** en el
   `.md`: es exactamente lo que el alumno se quedó pensando y nunca resolvió.
3. **Los saltos de notación.** Cuando la clase cambia de convención a mitad de
   camino (por ejemplo, presenta lo mismo "a la Bishop" y después "a la Hastie"),
   el alumno cree que son dos temas distintos. Son el mismo. Decilo y dale la
   tabla de traducción.

## Paso 3 — Escribir el `.md`

Antes de escribir una línea, leé:

- `.claude/skills/clase/referencias/plantilla_explicacion.md` — el tono y el
  nivel de detalle, con una sección de ejemplo escrita entera. **Fija tono, no
  contenido**: su ejemplo sale de la clase de regresión lineal, así que si es
  justo la clase que estás escribiendo, no lo reutilices — buscá tu propia
  analogía y tu propia manera de encadenar la cuenta.
- `.claude/skills/clase/referencias/bibliografia.md` — el mapa tema → capítulo y
  la tabla de traducción ESL ↔ Bishop.

Escribís sobre el esqueleto que dejó el script, en
`src/notebooks/explained/<slug>.md`.

Lo primero: **reescribí el `# H1`**. El script pone ahí el nombre del archivo
crudo, que suele ser largo y poco prolijo (`Regresión Lineal introducción,
cuadrados mínimos, descenso por gradiente`). Poné un título humano y corto,
manteniendo el número de clase: `# 2 — Regresión lineal y cuadrados mínimos`.

### Cómo agrupar

El mapa de celdas trae 10, 20 o 30 bloques. **No hagas una sección por bloque**:
agrupalos en **5 a 10 secciones temáticas**. La tabla del "Mapa de la clase" del
esqueleto lista todos los bloques y su última columna dice en qué sección quedó
cada uno — completala. Es tu checklist de cobertura y le queda al usuario como
índice para volver de la explicación a la clase.

### El patrón de cada sección

```
## N. <Título>
📓 celdas <n>–<m> · 📕 ESL §<x.y>

### La idea en criollo
### Formalizándolo
### ¿Por qué nos importa?
### En código
### ⚠️ Confusión típica
### ❓ La pregunta que quedó abierta   (si la clase dejó una)
### 🖼️ La figura de la clase            (si la clase mostraba una)
```

Ese es el orden, siempre. Los cuatro primeros no se negocian. "En código" es el
único de los cinco que podés omitir, y solo cuando la sección es puramente
conceptual y cualquier snippet sería relleno.

Las dos últimas son condicionales: si la clase no dejó una pregunta colgada ni
mostraba una figura, **no pongas el encabezado**. Nada de secciones con "no
aplica" adentro.

### Voz

Sos un profesor particular explicándole a **una** persona.

- Español rioplatense, **voseo**, segunda persona del singular: *fijate*,
  *acordate*, *tenés*, *guardate*. El "nosotros" solo cuando arrastran una cuenta
  juntos: *"abrimos el producto"*.
- Frases cortas. Una idea por párrafo.
- **Prohibidas**: "simplemente", "obviamente", "trivialmente", "es fácil ver
  que", "no es difícil notar". Si es fácil, mostralo; si no, no mientas.
- Cada símbolo se presenta **en palabras** la primera vez que aparece:
  *"$\hat\beta$ (leelo 'beta sombrero': los coeficientes **estimados**, para
  distinguirlos del $\beta$ verdadero que nunca vamos a conocer)"*.
- **Una analogía por sección como mucho**, concreta y del mundo real, y
  **siempre seguida de dónde se rompe**. Una analogía linda sin su límite
  construye un modelo mental falso, que es peor que no tener ninguno.
- Nada de emojis decorativos en el cuerpo del texto. Los que aparecen en los
  encabezados de la plantilla son señalización, no adorno.

### Rigor

- **Ningún paso de cuenta se saltea.** Cada línea de una derivación viene con su
  justificación: *"acá usamos que $\mathbf{y}^T\mathbf{X}\beta$ es un escalar, y
  un escalar es igual a su transpuesta"*.
- Si a propósito salteás algo, decilo y aclará qué hay que llevarse igual.
- Cuando la clase llega a un resultado por un atajo, mostrá el paso que faltaba.
  El caso típico: derivada primera igual a cero prueba que hay un punto crítico,
  no que sea un mínimo.
- Notación: la de **ESL**, que es la de la cátedra. Si la clase usa otra en algún
  tramo, traducila explícitamente.

### Código

- Snippets cortos (menos de 25 líneas), ejecutables, con `numpy` / `pandas` /
  `matplotlib` / `sklearn`.
- Los comentarios explican el **porqué**, no el qué.
- Cuando el punto es entender la fórmula, primero la versión a mano con `numpy`
  y después la de la librería. Cuando el punto es la práctica, al revés.
- El código ilustra el concepto; no lo reemplaza.

### Referencias

El usuario quiere que el `.md` se apoye fuerte en el libro. Cada sección abre con
su línea de anclas:

```
📓 celdas 41–47 · 📕 ESL §2.4 · 📘 Bishop §1.5
```

- **ESL es la referencia principal.** Citá sección. Solo citá tabla o figura
  numerada si está en la lista de "cosas que sí podés citar con número" de
  `bibliografia.md`.
- **Si no estás seguro del número exacto, citá el capítulo o no cites nada.**
  Nunca inventes un número de ecuación ni de página: el usuario los va a buscar.
- **Poné solo las siglas que apliquen.** Hay temas que un libro no cubre: el
  descenso por gradiente estocástico está en Bishop §3.1.3 y no tiene entrada en
  ESL. En ese caso la línea va sin 📕, y listo. Tres siglas no es una cuota.
- Cuando la clase y el libro difieren en notación, orden o énfasis, decilo.
- Referencias a la propia notebook: siempre por número de celda, tomado del mapa.

### Hasta dónde traer material del libro

El `.md` explica **esta clase**. No reemplaza el capítulo.

- **Sí**: completar lo que la clase *usa sin explicar*, *afirma sin demostrar* o
  *pregunta sin responder*. Eso es el trabajo.
- **No**: agregar temas que la clase no tocó porque figuran en
  `bibliografia.md`. Si la clase no menciona Gauss–Markov, no le dediques un
  apartado a Gauss–Markov.
- **El puente sí vale**: una línea al cierre de la sección del tipo *"esto sigue
  en 📕 ESL §3.2.2, que es donde se prueba que OLS es el mejor estimador lineal
  insesgado"* le deja al alumno el hilo para tirar sin desviar la explicación.

### Figuras

Las clases referencian imágenes en `Figuras/*.png` que **no están en el repo**.
El script te lista cuáles en un comentario del esqueleto. Donde la clase mostraba
una, escribí un bloque `### 🖼️ La figura de la clase` describiendo **en palabras**
qué mostraba y qué había que ver en ella. No pongas la imagen rota ni inventes
código para regenerarla.

### Las tres secciones de cierre

**🧵 El hilo conductor.** Cómo se encadena todo lo de la clase, de dónde venimos
(la clase anterior, si existe en `explained/`) y hacia dónde vamos. Dos o tres
párrafos, no una lista.

**✅ Autoevaluación.** De 6 a 10 preguntas, de menor a mayor dificultad, cada
respuesta dentro de un `<details>`. Al menos dos que exijan hacer una cuenta y
una del tipo *"¿qué pasa si...?"*. La respuesta explica, no confirma.

**🎯 Centros para los ejercicios.** Uno por ejercicio del `.ipynb`, con el mismo
número. Cuatro viñetas:

- **De qué va realmente** — el concepto detrás de la consigna.
- **Por dónde arrancar** — el primer paso concreto, nada más.
- **Con qué chequear** — cómo sabe el alumno que le dio bien: un valor del libro,
  una propiedad que se tiene que cumplir, una función contra la cual comparar.
- **⚠️ Dónde te vas a trabar** — el punto exacto donde se va a frenar.

**Nunca la resolución.** Ni el código final, ni el resultado algebraico si el
ejercicio es justamente demostrarlo. Un centro se pasa para que la meta el otro.

### Profundidad

Exhaustivo. Este es un documento de estudio, no un resumen: el usuario lo lee
después de la clase y antes de sentarse a hacer los ejercicios, y tiene que
quedar listo. Ninguna celda de la notebook queda sin cubrir.

Para calibrar, medí **por sección, no por documento**: cada sección temática
pesa entre **100 y 200 líneas**. Con 5 a 10 secciones más el cierre, un `.md`
típico cae entre 800 y 1800 líneas — pero el número que importa es el de la
sección, porque es el que hace que la profundidad no dependa del tamaño de la
notebook. Una clase de 58 celdas cortas no se explica más flojo que una de 20
celdas largas.

Y es un **síntoma, no una cuota**: si te sale mucho más corto, hay algo que
quedó nombrado en vez de explicado; si te sale mucho más largo, probablemente
estés rellenando o metiendo temas que la clase no dio.

## Paso 4 — Revisar el notebook de ejercicios

El script lo generó con heurísticas. Revisá `src/notebooks/exercises/<slug>.ipynb`
y corregí dos cosas:

1. **El tipo de placeholder.** Cada ejercicio recibió celda markdown (teórico o
   conceptual) o celdas de código, según palabras clave. Si se equivocó, cambialo.
2. **Los títulos.** El script arma `### Ejercicio N — <primera línea recortada>`,
   que a veces queda largo o feo. Reescribilos por títulos cortos y descriptivos,
   y **usá esos mismos títulos en los centros del `.md`**.

Los **enunciados no se tocan**: van verbatim como los dio la cátedra.

## Paso 5 — Chequeo final

Antes de reportar:

- [ ] Cada fila de la tabla "Mapa de la clase" tiene una sección asignada.
- [ ] Todas las preguntas retóricas de la clase están respondidas.
- [ ] Ninguna referencia a ESL con número de ecuación o página no verificable.
- [ ] Ninguna analogía sin su "dónde se rompe".
- [ ] Ningún centro que resuelva el ejercicio.
- [ ] El `.ipynb` de ejercicios abre: `python3 -c "import json; json.load(open('src/notebooks/exercises/<slug>.ipynb'))"`.
- [ ] Los títulos de los ejercicios coinciden entre el `.ipynb` y los centros.

Cerrá con las tres rutas generadas y un resumen de dos o tres líneas de qué
cubre la clase.

Y recordale al usuario que, si lo va a leer en un visor sin soporte de LaTeX
(Zed, por ejemplo), tiene la vista HTML:

```bash
python3 src/scripts/preparar_clase.py html --slug <slug> --abrir
```
