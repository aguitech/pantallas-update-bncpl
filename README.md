<p align="center">
  <img src="https://aguitech.com/images/logo.png" alt="AGUITECH" width="120">
</p>

<h1 align="center">🎬 pantallas-update-bncpl</h1>

<p align="center">
  <strong>Cine Financiero · BanCoppel / Atore Coppel.</strong><br>
  Réplicas HTML navegables de las 56 pantallas del recorrido del visitante por estación.
</p>

<p align="center">
  <a href="#que-es">Qué es</a> ·
  <a href="#filosofia">Filosofía</a> ·
  <a href="#convencion-de-nombres">Nombres</a> ·
  <a href="#estructura">Estructura</a> ·
  <a href="#stack">Stack</a> ·
  <a href="#deploy">Deploy</a>
</p>

---

## ¿Qué es

`pantallas-update-bncpl` contiene las **réplicas HTML navegables de las 56
pantallas** del recorrido del visitante en el evento **Cine Financiero**
(BanCoppel / Afore Coppel). Cada archivo HTML replica una pantalla del
PDF original "Flujo interfaces / UX Cine Financiero" del 2026-10-01.

### Estaciones incluidas

| Estación | # pantallas | Rango |
|----------|-------------|-------|
| **0 · Prerregistro** | 11 | 0.01 — 0.11 |
| **1 · Casting** | 7 | 1.01 — 1.07 |
| **3 · Foro (preparación)** | 9 | 3.01 — 3.09 |
| **3 · Foro (grabación)** | 9 | 3.10 — 3.20 |
| **4 · Decisiones** | 13 | 4.01 — 4.13 |
| **6 · Correo / Contenidos** | 3 | 6.01 — 6.03 |
| **7 · Encuesta** | 2 | 7.01 — 7.02 |
| **TOTAL** | **56** | — |

### ¿Qué NO es este repo?

- ❌ No es la app productiva.
- ❌ No es un sistema de diseño.
- ❌ No es el código del backend ni del front funcional.

**Es una galería navegable que permite previsualizar todas las pantallas
sin abrir el PDF.**

## Filosofía

> Cada pantalla cuenta **el tiempo** — qué cambió, por qué cambió, y qué
> aprendimos del cambio.

Cuando agregas una iteración nueva, el commit message debe contar la historia:

```
v3.04-cuenta-1: Countdown ahora es animado (3→2→1) en vez de estático.
Aprendizaje: usuarios pausaban antes de los 3 segundos porque no sabían
que era interactivo.
```

## Convención de nombres

```
[v].[iter]-[pantalla]
```

| Parte | Significado | Ejemplo |
|-------|-------------|---------|
| `v` | Estación / versión del flow | `v3` (Estación 3 Rodaje) |
| `iter` | Iteración de la pantalla | `v0` (primera), `v1` (refinamiento), ... |
| `pantalla` | Nombre legible | `cuenta-1`, `guion-1`, `posicionamiento` |

### Carpetas dentro de cada pantalla

```
v3.02-bienvenida/
├── v0/        # primera propuesta
├── v1/        # refinamiento 1
├── v2/        # refinamiento 2 (la actual)
└── CHANGELOG.md   # qué cambió entre versiones
```

## Estructura

```
pantallas-update-bncpl/
├── index.html                   # índice navegable de todas las pantallas
├── assets/
│   └── styles.css              # hoja de estilos compartida
├── v3.0/                       # Estación 3 Rodaje
│   ├── v3.01-posicionamiento/
│   │   ├── v0/
│   │   ├── v1/
│   │   └── CHANGELOG.md
│   ├── v3.02-bienvenida/
│   ├── v3.03-guion-1/
│   ├── v3.04-cuenta-1/
│   ├── v3.05-grabacion-1/
│   ├── v3.06-clip-guardado/
│   ├── v3.07-guion-2/
│   ├── v3.08-cuenta-2/
│   └── v3.09-grabacion-2/
├── v4.0/                       # Estación 4 (cuando exista)
└── README.md
```

## Pantallas actualmente iteradas

| Pantalla | v0 | v1 | v2 | Estado |
|----------|----|----|----|----|
| 3.01 Posicionamiento | ✅ | 🚧 | — | primera iteración activa |
| 3.02 Bienvenida | ✅ | 🚧 | — | refactorizando header |
| 3.03 Guion 1 | ✅ | — | — | freeze |
| 3.04 Cuenta 1 | ✅ | — | — | freeze |
| 3.05 Grabación 1 | ✅ | — | — | freeze |
| 3.06 Clip guardado | ✅ | — | — | freeze |
| 3.07 Guion 2 | ✅ | — | — | freeze |
| 3.08 Cuenta 2 | ✅ | — | — | freeze |
| 3.09 Grabación 2 | ✅ | — | — | freeze |

✅ publicada · 🚧 en revisión · ⛔ deprecada · 🧊 freeze

## Stack

- **HTML + CSS + JavaScript vanilla** — sin build, sin frameworks.
- **Google Fonts (Inter)** — tipografía consistente con el sistema de diseño.
- **Sin tracking, sin analytics** — esto es un repo de revisión, no de producto.
- ✅ Imports relativos entre `assets/` e iteraciones.

## Run

```bash
# Opción 1 — abrir directo
open index.html

# Opción 2 — servidor local (recomendado)
python3 -m http.server 8080
# luego http://localhost:8080
```

## Deploy

- **Producción:** https://aguitech.github.io/pantallas-update-bncpl/

Push a `main` → Pages se actualiza automáticamente en 30-90s.

## Cuándo abrir un PR

- ✏️ Nueva iteración de una pantalla existente → PR con screenshots del antes/después.
- 🆕 Pantalla nueva → PR con `v0/` y `CHANGELOG.md` inicial.
- ⛔ Deprecar una versión → mover a `vN/_deprecated/` y dejar el changelog explicando el rollback.

## Identidad visual

| Token | valor |
|-------|--------|
| Azul BanCoppel | `#0a4d8c` |
| Amarillo acento | `#ffd400` |
| Rojo grabación | `#e53935` |
| Verde OK | `#2ec27e` |
| Tipografía | Inter (Google Fonts) |

## License

MIT — úsalo, modifícalo, repártelo. Si te late, menciónanos.

---

<p align="center">
  Hecho con 🇨 por <a href="https://aguitech.com"><strong>AGUITECH</strong></a> ·
  Ingeniería + Diseño + Sistemas
</p>