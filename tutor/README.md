# Método de estudio

**Por qué existe.** En el 1P no alcanzó con leer: el examen pide **producir** una
derivación corta con un giro, y leer entrena solo a **reconocerla**. De ahora en
más el tiempo se reparte **30 % leer, 70 % producir**.

## Qué hay en esta carpeta

```
tutor/
├── README.md            ← este archivo: el método
├── movidas.md           ← las "vueltas" (M1…M10) que arman todas las derivaciones
├── diario_errores.md    ← dónde fallaste y en qué estado está cada cosa
├── fichas/
│   ├── _plantilla.md    ← copiala para cada clase
│   └── <n>_<tema>.md    ← tus fichas (las escribís vos)
└── practica/
    └── <tema>_<n>.md    ← ejercicios de /tutor practica (resolución al final: no la mires)
```

## Después de una clase: checklist

```
Día 0  ─ leer poco ─────────▶ escribir ficha ─────▶ /tutor ficha <n>
Día 1  ─ 🧮 en hoja en blanco ─▶ trabado? movida → /tutor duda → notebook (1 línea)
                              └▶ /tutor corregir  (si hubo error → diario)
Día 3-4 ─ /tutor practica <tema> ─▶ resolver contra reloj ─▶ /tutor corregir
Semanal ─ /tutor diario  (2-3 entradas de otros temas)
```

- [ ] **Día 0** · Leer de la notebook explicada solo: 🗺️ mapa, 🧰 movidas, "La idea en criollo", 🧵 hilo. Cerrarla.
- [ ] **Día 0** · `cp tutor/fichas/_plantilla.md tutor/fichas/<n>_<tema>.md` y completarla sin mirar.
- [ ] **Día 0** · `/tutor ficha <n>`: el tutor marca huecos, no la escribe por vos.
- [ ] **Día 1** · Cada derivación de *🧮 Para derivar en frío* en hoja en blanco. Pegarla en `/tutor corregir`.
- [ ] **Día 3–4** · `/tutor practica <tema>` y resolverlo en 10–15 min. Pegarlo en `/tutor corregir`.
- [ ] **Semanal** · `/tutor diario` y repasar lo que proponga.

## Para qué sirve cada cosa

| Material | Rol | Cuándo se abre |
|---|---|---|
| `tutor/movidas.md` | El **vocabulario**: las pocas movidas que arman todas las derivaciones | Siempre que te trabás |
| `src/notebooks/explained/` | **Diccionario**. No se estudia de punta a punta | Cuando ya probaste con la movida y seguís trabado |
| `.claude/skills/tutor/referencias/mapa_parcial.md` | **Qué hay que producir** (las 🧮) | Al empezar cada tema |
| `tutor/fichas/` | **Lo que estudiás**. Lo escribís vos | Siempre |
| `/tutor practica` + `/tutor corregir` | **El entrenamiento** | Una vez por semana como mínimo |
| `tutor/diario_errores.md` | **Qué repasar** | Una vez por semana |

## El ciclo de cada clase

**Día 0, después de la clase (30 min).** De la notebook explicada leés el mapa,
el recuadro 🧰 *Movidas de esta clase*, "La idea en criollo" de cada sección y el
hilo conductor. **La cerrás** y escribís tu ficha en `tutor/fichas/` copiando
`_plantilla.md`. Sin mirar: si te sale incompleta, mejor, porque los huecos te
dicen qué repasar. Después corré `/tutor ficha <n>`.

**Día 1 (40 min).** En hoja en blanco, las derivaciones de la sección
*🧮 Para derivar en frío* (antes del hilo conductor). Si te trabás, consultás en este
orden y parás en el primero que te destrabe:

1. el nombre de la movida (tu ficha o `movidas.md`),
2. `/tutor duda`,
3. la notebook: **una línea**, y la cerrás.

Si llegaste al paso 3, eso va al diario.

**Día 3–4 (20 min).** `/tutor practica <tema>`: un ejercicio con giro, contra el reloj.

**Una vez por semana (30 min).** `/tutor diario`: 2 o 3 entradas viejas de
**otros** temas. En el examen nadie te avisa de qué tema es cada ejercicio, por
eso conviene mezclar.

**Antes del parcial.** Simulacro cronometrado con temas mezclados.

## Cuándo está estudiado un concepto

Tiene que pasar las cuatro pruebas **sin mirar nada**:

1. **Decirlo:** 2–3 frases sin símbolos sobre qué dice y por qué importa.
2. **Derivarlo:** hoja en blanco, ≤ 10 min, nombrando cada movida.
3. **Repetirlo días después:** lo volvés a sacar **≥ 3 días** más tarde. Sacarlo el mismo día no cuenta.
4. **Aplicarlo con giro:** resolvés bien una variante que no viste.

Estados del diario:

- `pendiente`: todavía no salió solo.
- `repasar`: salió una vez en frío (pruebas 1 y 2, en la misma sesión).
- `dominado (fecha)`: salió otra vez ≥ 3 días después **y** salió una variante (pruebas 3 y 4).
- Un ✘ en `dominado` lo devuelve a `repasar`.
