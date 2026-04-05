<p align="center">
  <h1 align="center">🎓 claude_udea</h1>
  <p align="center">
    <strong>Tu asistente académico con IA para la Universidad de Antioquia</strong>
  </p>
  <p align="center">
    Transcripciones de Zoom desde Moodle (UdeArroba) o Ingenia (Virtual Ingeniería) → Claude Code
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-≥3.10-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Claude_Code-CLI-orange?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code">
    <img src="https://img.shields.io/badge/plataforma-Windows_|_macOS_|_Linux-green?style=flat-square" alt="Cross-platform">
  </p>
</p>

---

## ¿Qué es?

`claude_udea` es una herramienta de línea de comandos que:

1. **🔍 Scrapea** las grabaciones de Zoom desde **Moodle (UdeArroba)** y/o desde **[Ingenia](https://ingenia.udea.edu.co/)** (archivo de clases de Virtual Ingeniería)
2. **📥 Descarga** las transcripciones (y opcionalmente los videos)
3. **🤖 Abre Claude Code** como asistente académico personalizado con tus clases

Todo en un solo comando: `claude_udea`

---

## ✨ Características

- **Setup interactivo** — la primera vez te guía para configurar tus asignaturas
- **Instalación automática** — detecta e instala dependencias faltantes (incluido Claude Code)
- **Sesión persistente (Moodle)** — guarda tu sesión de UdeArroba para no pedir login cada vez (no aplica a fuentes solo-Ingenia)
- **Ingenia / Virtual Ingeniería** — podés usar la URL de la reunión `https://ingenia.udea.edu.co/zoom/meeting/<ID>` o solo el número de ID; sin login en Moodle si todas tus materias vienen de ahí
- **Scraping invisible** — después del login, el navegador se oculta mientras trabaja
- **Descarga incremental** — nunca re-descarga lo que ya tenés
- **Deduplicación inteligente** — identifica grabaciones por fecha, sin duplicados
- **Cross-platform** — funciona en Windows, macOS y Linux
- **Skills de Claude** — comandos especializados para estudiar con IA

---

## 📋 Requisitos previos

| Requisito | Para qué | Cómo instalar |
|-----------|----------|---------------|
| **Python ≥ 3.10** | Ejecutar la herramienta | [python.org](https://www.python.org/downloads/) |
| **Node.js ≥ 18** | Instalar Claude Code | [nodejs.org](https://nodejs.org/) (LTS) |
| **Git** | Clonar el repositorio | [git-scm.com](https://git-scm.com/) |

> 💡 Las demás dependencias (Playwright, Chromium, Claude Code, etc.) se instalan automáticamente en la primera ejecución.

---

## 🚀 Instalación

### Opción 1: Desde GitHub (recomendado)

```bash
pip install git+https://github.com/gjcardonam/claude-udea.git
```

### Opción 2: Clonar y desarrollo local

```bash
git clone https://github.com/gjcardonam/claude-udea.git
cd claude-udea
pip install -e .
```

---

## 🎯 Uso

### Primera vez

> ⚠️ **Antes de empezar**: tené listos los enlaces de **cada** asignatura: o bien la lista de grabaciones en **Moodle**, o bien la página de la reunión en **Ingenia** (Virtual Ingeniería).
> Solo se piden **una vez** en el setup — después el CLI los usa en cada ejecución.

#### ¿Cómo conseguir el link? (Moodle — UdeArroba)

1. Entrá a [UdeArroba](https://udearroba.udea.edu.co/)
2. Abrí la asignatura
3. Buscá la actividad de **Zoom** donde están las grabaciones
4. Copiá la URL de esa página — es algo como `https://udearroba.udea.edu.co/mod/zoom/view.php?id=XXXXX`

#### ¿Cómo conseguir el link? (Ingenia — Virtual Ingeniería)

1. Entrá al buscador de clases en [Ingenia](https://ingenia.udea.edu.co/) (portal ligado a [Virtual Ingeniería](https://virtualingenieriaudea.co/))
2. Localizá tu curso y abrí la página de esa reunión Zoom
3. Copiá la URL del navegador — tiene esta forma:

   `https://ingenia.udea.edu.co/zoom/meeting/96660122811`

   (el número final es el **ID de reunión**; también podés pegar **solo ese número** en el setup y la herramienta arma la URL)

#### Ejecutar

```bash
claude_udea
```

Se va a:

1. ✅ Verificar e instalar dependencias faltantes
2. ✅ Pedir los links de grabaciones de cada asignatura (solo la primera vez)
3. ✅ Abrir un navegador para login en **Moodle** solo si tenés al menos una materia en UdeArroba (si todas son Ingenia, este paso se omite)
4. ✅ Scrapear las grabaciones automáticamente (Moodle e Ingenia)
5. ✅ Descargar las transcripciones
6. ✅ Abrir Claude Code como tu asistente académico

### Ejecuciones siguientes

```bash
claude_udea              # Actualiza todo y abre Claude Code
```

Si tu sesión de Moodle sigue activa y no hace falta volver a autenticarte, **no abre ningún navegador** para eso — el scraping sigue en segundo plano. (Las materias solo-Ingenia nunca requieren login en UdeArroba.)

### Opciones

```bash
claude_udea --status          # Ver estado de descargas por asignatura
claude_udea --skip-scrape     # Solo descargar (sin re-scrapear Moodle/Ingenia)
claude_udea --skip-video      # Solo transcripciones (sin preguntar)
claude_udea --all             # Video + transcripciones (sin preguntar)
claude_udea --dry-run         # Simular sin descargar nada
claude_udea --add-course      # Agregar una nueva asignatura
```

### Filtrar por asignatura

```bash
claude_udea calidad-de-software          # Solo una asignatura
claude_udea ingenieria-web optimizacion  # Varias específicas
```

---

## 🤖 Skills de Claude Code

Una vez dentro de Claude Code, tenés comandos especializados:

| Comando | Qué hace |
|---------|----------|
| `/enseñar [tema]` | Enseña un tema visto en clase con referencias a la grabación y minuto |
| `/pendientes` | Lista todos los compromisos: parciales, tareas, quices, entregas |
| `/planear` | Ayuda a organizar tu tiempo y crear horarios de estudio |
| `/buscar [término]` | Busca una palabra o frase en todas las transcripciones |
| `/temas` | Muestra todos los temas vistos, organizados cronológicamente |
| `/ejemplos [tema]` | Da ejemplos prácticos sobre un tema de clase |
| `/taller` | Ayuda a resolver un taller con base en lo visto en clase |

### Ejemplo de uso

```
> /pendientes

📋 Compromisos encontrados:

  ✦ Parcial 2 - Calidad de Software
    📅 2026-03-25 | calidad-clase-15.vtt | ~min 45
    "El parcial va a ser sobre testing y métricas"

  ✦ Entrega Taller 3 - Ingeniería Web
    📅 2026-03-28 | ingenieria-clase-12.vtt | ~min 32
    "El taller es en grupos de 3, entrega por Moodle"
```

---

## 📁 Estructura de archivos

```
~/claude-udea/                    # macOS/Linux
C:\claude-udea\                   # Windows
├── CLAUDE.md                     # Instrucciones para Claude Code (auto-generado)
├── config.json                   # Asignaturas (moodle_url = lista Moodle o URL Ingenia /zoom/meeting/<ID>)
├── recordings.json               # Registro de grabaciones encontradas
├── .session-state.json           # Sesión de Moodle (cookies)
├── .browser-data/                # Perfil del navegador
├── .claude/
│   ├── rules.md                  # Reglas del asistente
│   └── skills/                   # Comandos disponibles
│       ├── enseñar.md
│       ├── pendientes.md
│       ├── planear.md
│       ├── buscar.md
│       ├── temas.md
│       ├── ejemplos.md
│       └── taller.md
└── downloads/
    ├── calidad-de-software/      # Archivos descargados por asignatura
    ├── ingenieria-web/
    └── transcripts/              # Transcripciones organizadas
        ├── index.json            # Índice por fecha y asignatura
        ├── calidad-de-software/
        │   ├── 2026-03-09_Clase 15 [...].vtt
        │   └── 2026-03-12_Clase 16 [...].vtt
        └── ingenieria-web/
            └── ...
```

---

## 🔧 Cómo funciona

Las asignaturas pueden mezclarse: unas con lista en **Moodle**, otras con página en **Ingenia** (`/zoom/meeting/<ID>`). El `config.json` guarda el mismo campo `moodle_url` para cualquiera de los dos (nombre histórico).

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│ Moodle y/o   │────▶│   Scraping    │────▶│  Descarga    │────▶│  Claude Code  │
│ Ingenia      │     │  (Playwright) │     │  (yt-dlp)    │     │  (Asistente)  │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
       │                    │                    │                     │
   Login solo si          Lista de            Baja VTTs           Lee transcripciones
   hay Moodle            enlaces Zoom        + metadata           y responde preguntas
```

1. **Scraping**: Playwright usa stealth cuando hace falta; en **Moodle** lee la tabla de grabaciones; en **Ingenia** recorre las tarjetas (incluida la paginación «Siguiente») y toma el enlace «Ver grabación de video»
2. **Descarga**: yt-dlp descarga las transcripciones (`.vtt`) y opcionalmente los videos. Cada VTT se enriquece con metadata (fecha, asignatura, duración)
3. **Claude Code**: Se abre con un `CLAUDE.md` personalizado que le dice qué asignaturas tenés, dónde están las transcripciones, y cómo responder

---

## 🔒 Privacidad y seguridad

- Tus credenciales de Moodle **nunca se guardan** — el login es manual en un navegador real
- Las páginas de reuniones en Ingenia se consultan como en un navegador normal; **no usan** la sesión de UdeArroba
- Las cookies de sesión de Moodle se guardan localmente en `.session-state.json`
- Todo se procesa localmente en tu máquina
- Las transcripciones nunca se suben a ningún servidor externo
- Claude Code lee los archivos locales directamente

---

## ❓ Solución de problemas

### "Claude Code no está instalado"
```bash
npm install -g @anthropic-ai/claude-code
```

### "Playwright no encuentra Chromium"
```bash
python -m playwright install chromium
```

### "La sesión de Moodle siempre expira"
Es normal que expire después de varias horas. Al ejecutar `claude_udea` de nuevo, te pedirá login solo si es necesario.

### "Se descargan grabaciones duplicadas"
Esto se corrigió automáticamente. Si tenés datos viejos, borrá `recordings.json` y ejecutá de nuevo:
```bash
# Windows
del C:\claude-udea\recordings.json

# macOS/Linux
rm ~/claude-udea/recordings.json
```

### Resetear todo
```bash
# Windows
rmdir /s /q C:\claude-udea\downloads C:\claude-udea\.browser-data
del C:\claude-udea\recordings.json C:\claude-udea\.session-state.json

# macOS/Linux
rm -rf ~/claude-udea/downloads ~/claude-udea/.browser-data
rm ~/claude-udea/recordings.json ~/claude-udea/.session-state.json
```

---

## 📄 Licencia

MIT

---

<p align="center">
  Hecho con ☕ para estudiantes de la <strong>Universidad de Antioquia</strong>
</p>
