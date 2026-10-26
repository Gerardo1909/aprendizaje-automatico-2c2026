# Catálogo de movidas

Casi todas las derivaciones de la materia combinan unas pocas **movidas**. Las
notebooks, las fichas, los ejercicios de práctica y las correcciones las nombran
con este código (`M1`…`M10`). Si te trabás, lo primero que te preguntás es
**¿qué movida va acá?**

El **núcleo** (M1–M7) aparece en casi todas las clases. Las **específicas**
(M8–M10) aparecen en un bloque de temas.

Regla para sumar una movida nueva: que aparezca en **dos clases o más**. Si
aparece en una sola, es un resultado de esa clase, no una movida.

---

## Núcleo

### M1 — Derivar e igualar a 0
- **Señal:** "minimizar", "el valor que hace mínimo", "estimador de mínimos cuadrados".
- **Qué hacés:** derivás la pérdida respecto de la incógnita, la igualás a 0 y despejás. Después chequeás que es mínimo (segunda derivada > 0 o función convexa).
- **Mínimo:** $\frac{d}{dc}\sum(y_i-c)^2 = -2\sum(y_i-c)=0 \Rightarrow c=\bar y$.
- **Dónde:** clase 2 (ecuación normal $\mathbf X^T\mathbf X\beta=\mathbf X^T\mathbf y$), clase 4 (Ridge), clase 6 (logística: el gradiente $=0$ no tiene solución cerrada ⇒ M9), clase 7 §2.
- **Trampa:** derivada 0 da un punto crítico, no un mínimo.

### M2 — Sumar y restar un centro: el cruzado muere
- **Señal:** una esperanza de un cuadrado, $E[(A-c)^2]$, y te piden partirla en pedazos.
- **Qué hacés:** $(a-c)^2=(a-b)^2+(b-c)^2+2(a-b)(b-c)$ con $b$ = la media de lo aleatorio. El cruzado muere si un factor es constante y el otro tiene esperanza 0 (o si son independientes y uno tiene media 0).
- **Mínimo:** $E[(Y-c)^2]=\mathrm{Var}(Y)+(E[Y]-c)^2$ ⇒ el mejor $c$ es $E[Y]$.
- **Dónde:** clase 7 §2 (media condicional óptima), §3–§4 (ruido + sesgo² + varianza).
- **Trampa:** sacar el cruzado sin decir **por qué** muere. Esa justificación es lo que se evalúa.

### M3 — Condicionar en $x$: resolver punto por punto y después promediar
- **Señal:** una esperanza sobre $(X,Y)$ conjunta, o una integral contra $p(x)$.
- **Qué hacés:** $E_{X,Y}[\cdot]=E_X\big[E_{Y\mid X}[\cdot\mid x]\big]$. Si minimizás lo de adentro para cada $x$, minimizaste el promedio. La integral no se calcula.
- **Mínimo:** EPE$(f)=E_X\,E[(Y-f(X))^2\mid X]$ ⇒ en cada $x$ es M2 ⇒ $f(x)=E[Y\mid X=x]$.
- **Dónde:** clase 1, clase 7 §2, clasificador de Bayes (clase 6 §2).
- **Trampa:** creer que hay que resolver la integral.

### M4 — Lineal en $\mathbf y$ ⇒ $\mathrm{Var}(\mathbf a^T\mathbf y)=\mathbf a^T\mathrm{Cov}(\mathbf y)\,\mathbf a$
- **Señal:** "varianza del estimador / de la predicción", con $\mathbf X$ fija.
- **Qué hacés:** escribís la predicción como $\mathbf a^T\mathbf y$ (o $\mathbf H\mathbf y$) con pesos fijos. Con $\mathrm{Cov}(\mathbf y)=\sigma^2\mathbf I$ queda $\sigma^2\|\mathbf a\|^2$. Para promediar sobre los $x_i$ aparece una traza.
- **Mínimo:** $\mathrm{Var}(\bar y)=\mathrm{Var}(\tfrac1N\mathbf 1^T\mathbf y)=\sigma^2\cdot N\cdot\tfrac1{N^2}=\sigma^2/N$.
- **Dónde:** clase 2–3 (varianza de $\hat\beta$), clase 7 §4 (OLS y Ridge, $\mathrm{tr}\,\mathbf H$ = grados de libertad).
- **Trampa:** usarla con Lasso o con árboles: no son lineales en $\mathbf y$.

### M5 — La SVD (o autodescomposición) diagonaliza
- **Señal:** aparece $\mathbf X^T\mathbf X$, $(\mathbf X^T\mathbf X+\lambda\mathbf I)^{-1}$, $\Sigma^{-1}$, $|\Sigma|$, o "direcciones principales".
- **Qué hacés:** reemplazás $\mathbf X=\mathbf U\mathbf D\mathbf V^T$ (o $\Sigma=\mathbf U\mathbf D\mathbf U^T$). En la base de $\mathbf V$ el problema se separa en una cuenta escalar por dirección.
- **Mínimo:** Ridge encoge la dirección $j$ por $d_j^2/(d_j^2+\lambda)$.
- **Dónde:** clase 3 §5–§6 (SVD de $\mathbf X$ y de $\hat\beta$), clase 4 §8 (Ridge con SVD), clase 6 §5 (esferizar), clase 7 §4 (df de Ridge), PCA (`books/explained/cap14_5_pca_componentes_principales.ipynb`).
- **Trampa:** olvidar que $\mathbf V^T\mathbf V=\mathbf I$ es lo que hace que todo se simplifique.

### M6 — Estandarizar desacopla
- **Señal:** "predictores estandarizados / centrados", "correlación $\rho$".
- **Qué hacés:** usás la hipótesis oculta: $\sum_i x_{ij}=0$ y $\mathbf x_j^T\mathbf x_j=N$ (o 1). El intercepto se separa del resto y $\mathbf X^T\mathbf X/N$ es la matriz de correlaciones.
- **Mínimo:** con $x$ centrado, la ecuación de $\beta_0$ da $\beta_0=\bar y$ sin tocar a $\beta_1$.
- **Dónde:** 1P ej. 4 y 5, clase 4 §3 (estandarizar es parte de la definición de Ridge), clase 5 §0 y §5 (predictores estandarizados; coordinate descent), clase 7 §4 (intercepto con $\mathbf X$ centrada).
- **Trampa:** no usar la hipótesis porque el enunciado la dice una sola vez, al principio.

### M7 — No derivable ⇒ partir en tramos (o correr $c$ un $\delta$)
- **Señal:** $|\cdot|$, norma L1, $\max$, mediana.
- **Qué hacés:** separás los casos según el signo. Otra opción: correr el candidato un $\delta$ y ver si el costo sube o baja.
- **Mínimo:** al mover $c$ un $\delta$, $E|Y-c|$ cambia en $\delta\,(P(Y<c)-P(Y>c))$ ⇒ el óptimo es la mediana.
- **Dónde:** clase 1 §8 y clase 7 §2 (pérdida absoluta ⇒ mediana; derivada de $E|Y-c|$ en la autoevaluación), clase 5 (soft-thresholding de Lasso), 1P ej. 2.
- **Trampa:** "no es derivable ⇒ no se puede minimizar". Falso.

---

## Específicas

### M8 — Restricción de igualdad ⇒ Lagrange
- **Señal:** "con $\|v\|=1$", "sujeto a".
- **Qué hacés:** $\nabla f=\gamma\nabla g$. Con $f=v^T\mathbf Av$ y $g=v^Tv$ queda $\mathbf Av=\gamma v$: es un autovector, y el objetivo vale $\gamma$.
- **Dónde:** clase 4 §3 y ej. 3 (Ridge como problema con restricción; Lagrange), clase 5 §9 (forma lagrangiana ↔ restricción), PCA (`books/explained/cap14_5_pca_componentes_principales.ipynb`, §2: $\|v\|=1$ ⇒ autovector).

### M9 — Newton: raíz por la tangente; optimizar = Newton sobre $f'$
- **Señal:** "no hay forma cerrada", "iterativo", "Hessiano".
- **Qué hacés:** $x\leftarrow x-g(x)/g'(x)$. Para optimizar, $g=f'$: $\theta\leftarrow\theta-\mathbf H^{-1}\nabla$.
- **Dónde:** clase 6 §6 y §9 (IRLS).

### M10 — Verosimilitud: el log convierte producto en suma
- **Señal:** "máxima verosimilitud", "modelo probabilístico", "Bernoulli/Gaussiana".
- **Qué hacés:** la verosimilitud es $\prod_i p(y_i\mid x_i;\theta)$. Le tomás log, maximizás la suma (M1, o M9 si no hay forma cerrada).
- **Dónde:** clase 3 (OLS = MV con ruido gaussiano), clase 6 §8 (logística).
