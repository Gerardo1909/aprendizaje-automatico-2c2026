# Plantilla del `.md` explicado

El script ya deja el esqueleto. Este archivo muestra **cómo se ve una sección
bien escrita**, para que el tono y la profundidad no cambien entre clases.

> ⚠️ **Esto fija tono y profundidad, nunca contenido.** El ejemplo desarrollado
> sale de la clase de regresión lineal. Si estás escribiendo justamente esa
> clase, **no lo reutilices**: buscá tu propia analogía, tu propio orden para
> encadenar la cuenta y tus propios centros. Copiarlo es el modo de fallar más
> fácil de esta skill.

---

## Estructura completa

```
# <N> — <Título limpio de la clase>
📓 Notebook · ✏️ Ejercicios · 📕 ESL

> **TL;DR** (5 bullets)

## 🗺️ Mapa de la clase        tabla bloque → sección (checklist de cobertura)
## 0. Notación y convenciones  (solo si la clase introduce notación nueva)
## 1..N. <Secciones temáticas> (el patrón de 5 pasos)
## 🧵 El hilo conductor
## ✅ Autoevaluación
## 🎯 Centros para los ejercicios
```

---

## Ejemplo de TL;DR

> **TL;DR**
>
> - La regresión lineal no asume que el mundo sea lineal: asume que **$E(Y\mid X)$**
>   se aproxima bien con una recta (o un plano). Es una afirmación sobre el
>   promedio condicional, no sobre cada punto.
> - "Lineal" es **en los parámetros $\beta$**, no en las variables. $X_1^2$ y
>   $X_1 X_2$ son predictores perfectamente válidos.
> - Minimizar $RSS$ tiene solución cerrada: $\hat\beta = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$.
>   Es un **mínimo** garantizado porque $RSS$ es convexa en $\beta$.
> - Geométricamente, $\hat{\mathbf{y}}$ es la **proyección ortogonal** de $\mathbf{y}$
>   sobre el subespacio que generan las columnas de $\mathbf{X}$.
> - Para hablar de sesgo, varianza o $p$-valores hacen falta **supuestos extra**
>   (errores independientes, varianza constante, normalidad). Para *predecir*, no.

Cinco bullets. Cada uno es una idea completa, no un título. Si el alumno lee
solo esto en el colectivo camino al parcial, tiene que zafar.

---

## Ejemplo de sección completa

Así se ve el patrón de 5 pasos aplicado en serio:

---

### 3. Cuadrados mínimos: de dónde sale la ecuación normal

📓 celdas 5–7 · 📕 ESL §3.2 · 📘 Bishop §3.1.1

#### La idea en criollo

Imaginate que tenés tu casa en el medio del campo y una ruta recta que pasa
cerca. Querés el punto de la ruta más cercano a tu casa. ¿Qué hacés? Trazás la
**perpendicular** a la ruta. Cualquier otro punto de la ruta te queda más lejos,
y eso lo sabés sin probar punto por punto.

Cuadrados mínimos es exactamente eso. Tu "casa" es el vector de respuestas
observadas $\mathbf{y}$. La "ruta" es el conjunto de **todas las predicciones que
tu modelo es capaz de generar** cuando barrés todos los $\beta$ posibles. Buscás
el punto de ese conjunto más cercano a $\mathbf{y}$.

> **Dónde se rompe la analogía.** La ruta es una línea en el plano: dos
> dimensiones, fácil de dibujar. Acá $\mathbf{y}$ vive en $\mathbb{R}^N$ —una
> dimensión por **observación**, no por variable— y la "ruta" es un subespacio de
> hasta $p+1$ dimensiones. No lo podés dibujar, pero la cuenta de la
> perpendicular es idéntica. Y ojo: la distancia que minimizamos es entre
> **vectores de $N$ componentes**, no entre puntos del gráfico $x$ vs $y$ que
> tenés en la cabeza.

#### Formalizándolo

Arrancamos de la función de costo escrita en forma matricial:

$$RSS(\beta) = \|\mathbf{y} - \mathbf{X}\beta\|^2 = (\mathbf{y} - \mathbf{X}\beta)^T(\mathbf{y} - \mathbf{X}\beta)$$

(Acordate: $\|v\|^2 = v^T v$. La norma al cuadrado de un vector es él consigo
mismo. Nada más que eso.)

Abrimos el producto, como cualquier binomio:

$$(\mathbf{y}^T - \beta^T\mathbf{X}^T)(\mathbf{y} - \mathbf{X}\beta) = \mathbf{y}^T\mathbf{y} - \mathbf{y}^T\mathbf{X}\beta - \beta^T\mathbf{X}^T\mathbf{y} + \beta^T\mathbf{X}^T\mathbf{X}\beta$$

Los dos términos del medio parecen distintos, pero son el **mismo número**.
Fijate en las dimensiones: $\mathbf{y}^T$ es $1 \times N$, $\mathbf{X}$ es
$N \times (p{+}1)$, $\beta$ es $(p{+}1) \times 1$. El producto es $1 \times 1$:
un escalar. Y un escalar es igual a su transpuesta, así que
$\mathbf{y}^T\mathbf{X}\beta = (\mathbf{y}^T\mathbf{X}\beta)^T = \beta^T\mathbf{X}^T\mathbf{y}$.
Los juntamos:

$$RSS(\beta) = \mathbf{y}^T\mathbf{y} - 2\,\mathbf{y}^T\mathbf{X}\beta + \beta^T\mathbf{X}^T\mathbf{X}\beta$$

Esto es una **cuadrática en $\beta$**: constante, término lineal, término
cuadrático. La misma forma que $c - 2b\beta + a\beta^2$, pero con vectores.

Derivamos respecto de $\beta$ usando dos reglas del cálculo matricial:

- $\dfrac{\partial (a^T\beta)}{\partial \beta} = a$ &nbsp; (análogo a $\frac{d}{dx}(bx) = b$)
- $\dfrac{\partial (\beta^T A \beta)}{\partial \beta} = 2A\beta$ cuando $A$ es simétrica &nbsp; (análogo a $\frac{d}{dx}(ax^2) = 2ax$)

y notando que $\mathbf{X}^T\mathbf{X}$ **es** simétrica:

$$\frac{\partial RSS}{\partial \beta} = -2\mathbf{X}^T\mathbf{y} + 2\mathbf{X}^T\mathbf{X}\beta = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\beta)$$

Igualamos a cero. Eso da la **ecuación normal**:

$$\mathbf{X}^T(\mathbf{y} - \mathbf{X}\hat\beta) = 0 \quad\Longleftrightarrow\quad \mathbf{X}^T\mathbf{X}\hat\beta = \mathbf{X}^T\mathbf{y}$$

y si $\mathbf{X}^T\mathbf{X}$ es invertible:

$$\hat\beta = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

**Falta un paso que casi todo el mundo saltea**: derivada primera cero te dice
que es un punto crítico, no que sea un mínimo. Podría ser un máximo o una silla.
La segunda derivada es $2\mathbf{X}^T\mathbf{X}$, que es semidefinida positiva
siempre (para cualquier $v$, $v^T\mathbf{X}^T\mathbf{X}v = \|\mathbf{X}v\|^2 \geq 0$)
y **definida** positiva si $\mathbf{X}$ tiene rango columna completo. Con eso
$RSS$ es estrictamente convexa y el punto crítico es el mínimo global. Recién
ahí la cuenta está cerrada.

#### ¿Por qué nos importa?

Porque es de las poquísimas veces en toda la materia que vas a tener **solución
cerrada**. No hay que iterar, no hay tasa de aprendizaje que tunear, no hay
mínimos locales de los que preocuparse: escribís la fórmula y listo.

Ese lujo se paga: te lo da la combinación de un modelo lineal en $\beta$ con una
pérdida cuadrática. Cambiá cualquiera de las dos —pérdida absoluta, regresión
logística, una red neuronal— y se te acaba. Por eso el resto de la materia
optimiza numéricamente. Guardate esto como el caso de referencia contra el cual
comparás todo lo demás.

#### En código

```python
import numpy as np

# X ya viene con la columna de unos para el intercepto.
XtX, Xty = X.T @ X, X.T @ y

beta_mal = np.linalg.inv(XtX) @ Xty   # ❌ traduce la fórmula, pero no se hace así
beta_ok = np.linalg.solve(XtX, Xty)   # ✅ resuelve el sistema sin invertir nada
beta_mejor, *_ = np.linalg.lstsq(X, y, rcond=None)  # ✅✅ ni siquiera forma X^T X
```

Los tres dan lo mismo con datos bien portados. Cuando las columnas de
$\mathbf{X}$ están muy correlacionadas, `inv` amplifica el error numérico: al
formar $\mathbf{X}^T\mathbf{X}$ el condicionamiento se **eleva al cuadrado**.
`lstsq` trabaja directo sobre $\mathbf{X}$ vía descomposición QR/SVD y esquiva
el problema. Es lo que usa `sklearn` por dentro.

#### ⚠️ Confusión típica

Ver el $^{-1}$ en la fórmula y creer que hay que invertir una matriz. La fórmula
es *notación*; el algoritmo es *resolver un sistema lineal*. Si en el parcial te
preguntan cómo se calcula $\hat\beta$, la respuesta buena no es "invirtiendo
$\mathbf{X}^T\mathbf{X}$".

Segunda trampa, más conceptual: $(\mathbf{X}^T\mathbf{X})^{-1}$ existe **solo si**
$\mathbf{X}$ tiene rango columna completo. Se rompe si tenés más variables que
observaciones ($p+1 > N$) o si una columna es combinación lineal de otras
(clásico: codificar una categórica con una dummy por categoría *y además* dejar
el intercepto). Ahí no hay un $\hat\beta$: hay infinitos, todos con el mismo
$RSS$.

#### ❓ La pregunta que quedó abierta

En la celda 9 la clase pregunta *"¿cuál es la dimensión del subespacio generado
por las columnas de $\mathbf{X}$?"* y sigue de largo. La respuesta: el **rango**
de $\mathbf{X}$. Si tiene rango columna completo, es $p+1$ —una dimensión por
predictor más el intercepto—. Si dos columnas son linealmente dependientes, es
menos, y ese es exactamente el caso en que $(\mathbf{X}^T\mathbf{X})^{-1}$ no
existe. Las dos preguntas eran la misma pregunta.

---

## Ejemplo de ítem de autoevaluación

Pregunta corta, respuesta plegada. Que la respuesta explique, no que confirme.

```
**3.** Tenés $N = 50$ observaciones y $p = 80$ predictores. ¿Qué pasa con $\hat\beta$?

<details><summary>Respuesta</summary>

$\mathbf{X}$ es $50 \times 81$: no puede tener rango columna completo, porque el
rango está acotado por el mínimo entre filas y columnas ($\leq 50$). Entonces
$\mathbf{X}^T\mathbf{X}$ es singular y no hay un único $\hat\beta$: hay un
subespacio entero de soluciones que ajustan los 50 puntos **exactamente**
($RSS = 0$). El modelo no aprendió nada, memorizó. Este es el escenario que
motiva todo el capítulo 3 de ESL a partir de §3.3: selección de variables y
regularización.

</details>
```

---

## Ejemplo de "centro"

Ni la cuenta ni el código. El primer empujón, y con qué verificar. Este es de una
clase distinta a propósito, para que se vea el formato sin invitarte a copiarlo:

```
### Ejercicio 3 — k-vecinos más cercanos a mano

- **De qué va realmente:** ver con las manos que $k$ controla la **complejidad**
  del modelo, y que esa complejidad no se mide en cantidad de parámetros (k-NN
  no tiene ninguno) sino en qué tan flexible es la frontera de decisión. Es el
  primer contacto con el compromiso sesgo–varianza que después vas a ver
  formalizado en 📕 ESL §7.2.
- **Por dónde arrancar:** con un solo punto de test. Calculá las $N$ distancias
  con `np.linalg.norm(X_train - x_test, axis=1)`, ordenalas con `np.argsort`,
  quedate con los primeros $k$ índices y votá. Recién cuando eso ande, envolvelo
  en un loop sobre todo el conjunto de test.
- **Con qué chequear:** con $k=1$ el error de **entrenamiento** tiene que dar
  exactamente cero (cada punto es su propio vecino más cercano). Si no te da
  cero, tenés un bug de indexado. Después compará contra
  `sklearn.neighbors.KNeighborsClassifier` con el mismo $k$: te tiene que dar
  idéntico salvo empates.
- **⚠️ Dónde te vas a trabar:** en los empates y en las escalas. Si una variable
  está en miles y otra entre 0 y 1, la distancia euclídea la decide sola la
  primera. Preguntate si hay que estandarizar **antes** de escribir el loop, no
  después de que los resultados te den raros.
```

## Recordatorios de tono

- Voseo, segunda persona: *fijate*, *acordate*, *tenés*, *guardate*.
- "Nosotros" solo cuando arrastramos una cuenta juntos: *"abrimos el producto"*.
- Ninguna oración empieza con "Simplemente", "Obviamente" ni "Es fácil ver que".
- Cada símbolo nuevo se presenta en palabras la primera vez que aparece.
- Una analogía por sección **como mucho**, y siempre con su "dónde se rompe".
- Los pasos de cuenta no se saltean. Si se saltea uno, se dice y se aclara qué
  hay que llevarse igual.
