# Descomposición de matrices: del teorema espectral al SVD

> Notas de repaso de álgebra lineal orientadas a Aprendizaje Automático.
> Hilo conductor: **toda descomposición separa una matriz en piezas con significado propio**, y en ML casi siempre nos importan más las piezas que la matriz original.

---

## 1. ¿Qué significa "descomponer" una matriz?

Una matriz es, antes que una tabla de números, una **transformación**: toma un vector y devuelve otro. El problema es que mirando las entradas de $A$ no se ve *qué hace* — se ve todo mezclado.

Descomponer (o factorizar) una matriz es escribirla como producto de matrices más simples:

$$A = B\,C\,D\,\dots$$

donde cada factor hace **una sola cosa reconocible**: rotar, escalar por ejes, proyectar, triangular. Es el equivalente algebraico de factorizar un número entero: $60$ no te dice mucho, pero $2^2\cdot 3\cdot 5$ te dice todo sobre su divisibilidad.

Descomponer sirve para tres cosas distintas, y conviene tenerlas separadas desde el principio:

1. **Resolver más barato.** Un sistema $Ax=b$ es difícil en general, pero trivial si $A$ es triangular o diagonal. Descomponer convierte un problema duro en varios fáciles encadenados.
2. **Entender la geometría.** Los factores revelan direcciones privilegiadas y magnitudes asociadas: dónde la transformación estira mucho, dónde casi no hace nada.
3. **Comprimir / quedarse con lo importante.** Si los factores vienen ordenados por importancia, podés truncarlos y quedarte con una aproximación mucho más chica. Esto es literalmente reducción de dimensionalidad.

En ML el punto 2 y el 3 son los que dominan.

---

## 2. El mapa de las descomposiciones

Antes de meternos en una, conviene ver el panorama. Cada factorización pide condiciones distintas sobre $A$ y sirve para propósitos distintos:

| Descomposición | Forma | Requiere | Para qué se usa |
|---|---|---|---|
| **LU** | $A = LU$ | cuadrada (con pivoteo, casi siempre) | resolver $Ax=b$, determinantes, inversas |
| **QR** | $A = QR$ | cualquiera | mínimos cuadrados, bases ortonormales, estabilidad numérica |
| **Cholesky** | $A = LL^T$ | simétrica definida positiva | covarianzas, muestreo gaussiano, optimización (Newton) |
| **Diagonalización** | $A = PDP^{-1}$ | cuadrada y diagonalizable | potencias de matrices, sistemas dinámicos |
| **Espectral** | $A = Q\Lambda Q^T$ | **simétrica** | PCA, Hessianos, kernels |
| **SVD** | $A = U\Sigma V^T$ | **cualquiera** (¡incluso rectangular!) | PCA, compresión, pseudoinversa, bajo rango |

Notá la progresión: cada fila va relajando requisitos o ganando estructura. Y hay una jerarquía clara entre las últimas tres:

$$\text{SVD} \;\supset\; \text{Espectral} \;\subset\; \text{Diagonalización}$$

- La **espectral** es un caso particular de diagonalización, pero *mejorado*: la matriz de cambio de base es ortogonal ($Q^{-1}=Q^T$, gratis de invertir) en vez de una $P$ cualquiera.
- El **SVD** es la generalización de la espectral a matrices que ni son cuadradas ni simétricas.

El resto de estas notas recorre ese camino: espectral primero (porque es donde la intuición geométrica se ve más limpia), SVD después.

---

## 3. Descomposición espectral

### 3.1 La idea en términos simples

Pensá una matriz simétrica como una **máquina que deforma vectores**: los estira, los achica, a veces los rota.

El teorema espectral dice que, si la matriz es simétrica, siempre existen **direcciones especiales** (los autovectores) que la matriz **no rota** — solo las estira o las achica por un factor (el autovalor).

Entonces, en lugar de pensar $A$ como "una transformación complicada", podés pensarla como una receta de tres pasos:

> **rotá** el espacio para alinearlo con esas direcciones especiales → **estirá** cada dirección por su factor propio → **rotá de vuelta**

Eso es exactamente lo que dice la fórmula $A = Q\Lambda Q^T$, leída de derecha a izquierda.

### 3.2 Con rigor técnico

Si $A \in \mathbb{R}^{n\times n}$ es simétrica ($A = A^T$), el **teorema espectral** garantiza:

1. Todos sus autovalores $\lambda_1,\dots,\lambda_n$ son **reales**.
2. Existe una **base ortonormal de $\mathbb{R}^n$** formada por autovectores $q_1,\dots,q_n$ de $A$.
   - Autovectores asociados a autovalores *distintos* son automáticamente ortogonales.
   - Si hay autovalores repetidos, el autoespacio asociado tiene dimensión igual a la multiplicidad, y ahí elegimos una base ortonormal dentro de ese subespacio.

Formando $Q = \begin{pmatrix} q_1 & \cdots & q_n\end{pmatrix}$ (ortogonal: $Q^TQ = QQ^T = I$) y $\Lambda = \mathrm{diag}(\lambda_1,\dots,\lambda_n)$:

$$\boxed{A = Q\Lambda Q^T}$$

Esto no es más que $Aq_i = \lambda_i q_i$ para cada $i$, escrito matricialmente para todos los autovectores a la vez.

### 3.3 La geometría

- $Q^T$ rota (o refleja) el espacio para que los ejes coincidan con los autovectores de $A$.
- $\Lambda$ estira cada eje por su autovalor.
- $Q$ deshace la rotación inicial.

Resultado: la acción de $A$ sobre cualquier vector es **"rotar, estirar por ejes, rotar de vuelta"** — sin ningún corte ni deformación oblicua. Si aplicás $A$ a la esfera unitaria, obtenés un **elipsoide** cuyos ejes son las direcciones $q_i$ y cuyos semiejes miden $|\lambda_i|$.

### 3.4 ¿Por qué "dos vueltas"?

Una duda natural: si $Q^T$ gira y $Q$ gira de vuelta, ¿no se cancelan? ¿Por qué nos interesa dar dos vueltas?

No es un capricho: es una **necesidad de coordenadas**. $A$ recibe un vector en la base estándar y debe devolver un vector en la base estándar. Leamos $Ax = Q\Lambda Q^T x$ de derecha a izquierda:

1. **$Q^Tx$** — $x$ está expresado en la base estándar ($e_1,\dots,e_n$). Multiplicar por $Q^T$ **no mueve el vector**: lo *reescribe* en coordenadas de los autovectores. Es un cambio de base, un traductor de idioma.
2. **$\Lambda(Q^Tx)$** — ahora que el vector está en el "idioma" de los autovectores, estirás cada componente por su factor propio. Esto es lo único que $A$ *hace* en esencia.
3. **$Q(\Lambda Q^Tx)$** — el resultado sigue en coordenadas de autovectores. Como querés compararlo con el $x$ original, sumarlo con otros vectores o graficarlo, hay que **traducir de vuelta** a la base estándar.

Entonces las dos vueltas son **ida** (traducir al idioma natural del problema) y **vuelta** (traducir al idioma con el que trabajás normalmente). Si no volvieras, tu resultado quedaría en un sistema de coordenadas distinto al de la entrada.

### 3.5 ¿La descomposición es única?

Enunciados del tipo *"encontrá **una** descomposición espectral de la forma $A = Q\Lambda Q^T$"* usan el "una" a propósito. Hay dos lecturas, y conviene no mezclarlas:

**(a) "De la forma $Q\Lambda Q^T$" especifica *cuál* factorización piden.** Existen LU, QR, Cholesky, SVD, y la diagonalización general $A = PDP^{-1}$. Esa frase te dice: quiero la espectral, con $Q$ ortogonal — no una $P$ cualquiera.

**(b) La misma $A$ admite varias $Q$ y $\Lambda$ válidas:**

- **Orden de los autovalores.** Podés listarlos en cualquier orden, siempre que reordenes las columnas de $Q$ igual.
- **Signo de los autovectores.** Si $q$ es autovector unitario, $-q$ también lo es. Misma dirección, sentido opuesto, misma validez.
- **Autovalores repetidos.** Si un autovalor tiene multiplicidad $>1$, su autoespacio tiene dimensión $>1$ y hay **infinitas** bases ortonormales posibles ahí adentro.

**Lo que sí es único:** el *conjunto* de autovalores y las *direcciones* (rectas) de los autoespacios.
**Lo que no:** el orden, el signo, y la base elegida dentro de un autoespacio de dimensión mayor.

### 3.6 ¿Nos importa la matriz o la geometría?

Acá está la clave de por qué esto es tan central en ML: **en la práctica casi nunca queremos reconstruir $A$**. Nos importan $Q$ y $\Lambda$ **por separado**, precisamente por lo que representan geométricamente.

- **PCA.** Tenés la matriz de covarianza $\Sigma$ de tus datos. No querés reconstruirla — ya la tenés. Querés descomponerla para quedarte con las columnas de $Q$ de mayor $\lambda$ (las direcciones de máxima varianza) y **descartar** el resto. Literalmente tirás partes de $Q$ y $\Lambda$; reconstruir la matriz completa sería lo contrario del objetivo.
- **Optimización / condicionamiento.** En descenso por gradiente te importa la razón $\lambda_{\max}/\lambda_{\min}$ del Hessiano (número de condición). Te dice si el paisaje del costo es una taza redonda (converge rápido) o un valle alargado (converge lento, en zigzag). Ahí usás **solo** $\Lambda$.
- **Whitening / decorrelación.** Transformás $x \mapsto Q^Tx$ para llevar los datos a los ejes de sus componentes principales, sin recomponer nada nunca.
- **Kernels y SVM.** Las matrices de Gram son simétricas semidefinidas positivas; su espectro determina propiedades del espacio de características.

**La geometría es el propósito, no un efecto secundario.** La igualdad $A = Q\Lambda Q^T$ funciona como *certificado* de que $Q$ y $\Lambda$ capturan toda la información de $A$ (por eso los ejercicios piden verificar multiplicando), pero el valor práctico está en separar esa información en **direcciones** ($Q$) y **magnitudes/importancias** ($\Lambda$), y usar cada pieza según haga falta.

---

## 4. De la espectral al SVD: el paso a matrices reales

La espectral tiene una limitación fuerte: **solo funciona para matrices cuadradas simétricas**.

¿Por qué? Porque hablar de "autovector" exige que $A$ mande el espacio **a sí mismo** — la ecuación $Av = \lambda v$ compara la salida con la entrada, así que ambas tienen que vivir en el mismo espacio. Pero una matriz de datos $A \in \mathbb{R}^{N\times p}$ manda $\mathbb{R}^p \to \mathbb{R}^N$: dominio y codominio son espacios **distintos**, y ahí "autovector" no significa nada.

Y las matrices de ML son casi siempre así: $N$ observaciones (filas) × $p$ features (columnas), rectangulares y sin ninguna simetría.

**La solución del SVD:** en vez de un solo conjunto de direcciones especiales, usar **dos** — uno ortonormal para el espacio de entrada y otro ortonormal para el de salida.

---

## 5. SVD (descomposición en valores singulares)

### 5.1 El enunciado

Para **cualquier** $A \in \mathbb{R}^{N\times p}$ (sin pedir simetría, ni siquiera que sea cuadrada) existe:

$$\boxed{A = U\Sigma V^T}$$

donde:

- $U \in \mathbb{R}^{N\times N}$ es **ortogonal**; sus columnas $u_1,\dots,u_N$ son los **vectores singulares izquierdos** (base ortonormal del codominio).
- $V \in \mathbb{R}^{p\times p}$ es **ortogonal**; sus columnas $v_1,\dots,v_p$ son los **vectores singulares derechos** (base ortonormal del dominio).
- $\Sigma \in \mathbb{R}^{N\times p}$ es **diagonal rectangular**, con entradas $\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_{\min(N,p)} \ge 0$ (los **valores singulares**) y cero fuera de esa diagonal.

Comparado con $A = Q\Lambda Q^T$: la misma estructura "rotar–estirar–rotar", pero con **dos** matrices ortogonales distintas en vez de la misma $Q$ a ambos lados, y con una $\Sigma$ que además puede cambiar la dimensión.

### 5.2 La conexión exacta con la espectral

Acá se cierra el círculo. Aunque $A$ no sea simétrica ni cuadrada, las matrices $A^TA$ ($p\times p$) y $AA^T$ ($N\times N$) **siempre** son simétricas y semidefinidas positivas. Entonces sí admiten descomposición espectral, y sustituyendo $A = U\Sigma V^T$:

$$A^TA = V\Sigma^T\Sigma V^T \qquad\qquad AA^T = U\Sigma\Sigma^TU^T$$

Es decir:

- los $v_i$ son los **autovectores de $A^TA$**,
- los $u_i$ son los **autovectores de $AA^T$**,
- $\sigma_i = \sqrt{\lambda_i}$, con $\lambda_i$ los autovalores (compartidos, salvo ceros extra) de ambas.

**El SVD de $A$ es la descomposición espectral de $A^TA$ y de $AA^T$, empaquetadas juntas.** Por eso decimos que es la generalización natural, no una herramienta aparte.

Y si $A$ ya era simétrica y semidefinida positiva, el SVD **coincide** con la espectral: $U = V = Q$ y $\Sigma = \Lambda$. (Con autovalores negativos aparecen diferencias de signo, absorbidas por $U$.)

### 5.3 La geometría

Misma receta de tres pasos, con la salvedad de que entrada y salida viven en espacios distintos. Leyendo $Ax = U\Sigma V^Tx$ de derecha a izquierda:

1. **$V^Tx$** — reescribís el vector de entrada en la base $\{v_i\}$, las direcciones ortogonales especiales del dominio $\mathbb{R}^p$.
2. **$\Sigma(\cdot)$** — estirás cada componente por su $\sigma_i$. Como $\Sigma$ es rectangular, este paso además **cambia la dimensión**: agrega ejes con cero o descarta coordenadas, según $N$ vs. $p$.
3. **$U(\cdot)$** — traducís el resultado a la base estándar del codominio $\mathbb{R}^N$, usando la base $\{u_i\}$.

Consecuencia visual: la **esfera unitaria de $\mathbb{R}^p$** se transforma, vía $A$, en un **elipsoide** (posiblemente de dimensión menor, viviendo dentro de $\mathbb{R}^N$) cuyos ejes son los $u_i$ y cuyos semiejes miden los $\sigma_i$.

Los $\sigma_i$ nulos o casi nulos indican direcciones que $A$ **aplasta**: ahí se pierde información. Ese es el dato más útil de todo el SVD.

### 5.4 Aclaración sobre "$N > p$"

Se escucha seguido que el SVD "requiere $N > p$". **Matemáticamente es falso**: el SVD existe para cualquier $N$ y $p$, incluso $N < p$.

De dónde sale la confusión: en la convención de ML/estadística, $N$ = observaciones y $p$ = features, y ahí sí es **deseable** $N > p$ — pero por una razón **estadística, no algebraica**. Si tenés menos observaciones que features:

- $\mathrm{rank}(A) \le N$, así que quedan muchos $\sigma_i = 0$;
- el sistema está subdeterminado (overfitting, mal planteo al estimar covarianzas).

El SVD funciona igual; simplemente vas a tener a lo sumo $\min(N,p)$ valores singulares no triviales.

### 5.5 Thin SVD

En la práctica casi nunca se calcula $U$ completa de $N\times N$ (imaginate $N$ = un millón de filas). La versión **económica** o *thin SVD* calcula solo las primeras $\min(N,p)$ columnas de $U$, que son las únicas que multiplican valores singulares no nulos. Mucho más barata y es lo que usan las librerías por defecto.

### 5.6 Por qué el SVD es la herramienta central en ML aplicado

- **PCA vía SVD, no vía covarianza.** Si $X$ es tu matriz de datos centrada por columna, $X^TX \propto \mathrm{Cov}(X)$. Hacer PCA descomponiendo espectralmente $X^TX$ es *matemáticamente* equivalente a hacer SVD directo sobre $X$ — pero el SVD es **numéricamente más estable**, porque evita formar $X^TX$ explícitamente (esa operación eleva el número de condición al cuadrado y amplifica el error de redondeo). Por eso `sklearn.decomposition.PCA` usa SVD internamente.
- **Multicolinealidad.** Cuando hay columnas de $X$ correlacionadas entre sí, algunos $\sigma_i$ salen muy chicos o casi cero: esa es la **firma algebraica de la redundancia**. Ridge se entiende mucho mejor mirando cómo penaliza justamente las direcciones de $\sigma_i$ chico, donde el problema está mal condicionado.
- **Aproximación de bajo rango.** Truncar el SVD a los primeros $k$ valores singulares da la **mejor** aproximación de rango $k$ a $A$ (teorema de Eckart–Young). Base de: sistemas de recomendación por factorización matricial, compresión de imágenes, y LoRA en fine-tuning de redes neuronales modernas.
- **Pseudoinversa y mínimos cuadrados.** Cuando $X$ no es cuadrada o no es invertible, el SVD da la pseudoinversa de Moore–Penrose $X^+ = V\Sigma^+U^T$, que es como se resuelve la regresión lineal cuando $X^TX$ no es invertible directamente.

---

## 6. Síntesis

| | Espectral | SVD |
|---|---|---|
| Forma | $A = Q\Lambda Q^T$ | $A = U\Sigma V^T$ |
| Requiere | $A$ simétrica | nada |
| Bases | **una** (dominio = codominio) | **dos** (dominio y codominio) |
| Diagonal | autovalores $\lambda_i$ (signo libre) | valores singulares $\sigma_i \ge 0$, ordenados |
| Geometría | esfera → elipsoide, semiejes $\vert\lambda_i\vert$ | esfera → elipsoide (quizá degenerado), semiejes $\sigma_i$ |
| Relación | caso particular | $\sigma_i = \sqrt{\lambda_i(A^TA)}$ |

La idea que atraviesa todo:

> **Descomponer una matriz es separarla en "direcciones" y "magnitudes".** La espectral hace eso para matrices simétricas usando un solo juego de direcciones; el SVD lo hace para cualquier matriz usando dos. En ambos casos, lo valioso en ML no es la igualdad que reconstruye la matriz, sino poder mirar las direcciones y las magnitudes por separado — y quedarte solo con las que importan.
