"""
Chat local con Ollama (gratis). Requiere ollama instalado y un modelo descargado (ej. llama3.2).
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path


def _ollama_base() -> str:
    return os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def _ollama_model(cli_model: str | None) -> str:
    if cli_model:
        return cli_model
    return os.environ.get("CLAUDE_UDEA_OLLAMA_MODEL", "llama3.2")


def ollama_available(base: str | None = None) -> bool:
    base = base or _ollama_base()
    try:
        req = urllib.request.Request(f"{base}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status == 200
    except (OSError, urllib.error.URLError):
        return False


def list_models(base: str | None = None) -> list[str]:
    base = base or _ollama_base()
    try:
        req = urllib.request.Request(f"{base}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.load(r)
        return [m["name"] for m in data.get("models", [])]
    except (OSError, urllib.error.URLError, json.JSONDecodeError, KeyError):
        return []


def _pick_model(preferred: str, available: list[str]) -> str:
    if preferred in available:
        return preferred
    # coincidencia por nombre base (ej. llama3.2 vs llama3.2:latest)
    for name in available:
        if name == preferred or name.startswith(preferred + ":"):
            return name
    for name in available:
        if preferred.split(":")[0] in name:
            return name
    return preferred


def _read_claude_md(work_dir: Path) -> str:
    p = work_dir / "CLAUDE.md"
    if p.exists():
        return p.read_text(encoding="utf-8", errors="replace")
    return (
        "Sos un asistente académico para un estudiante de la UdeA. "
        "Respondé en español usando solo el contexto que te den (índice o archivos pegados)."
    )


def _read_index_snippet(transcripts_dir: Path, max_chars: int = 48_000) -> str:
    p = transcripts_dir / "index.json"
    if not p.exists():
        return "(No hay index.json; listá carpetas bajo transcripts/.)"
    raw = p.read_text(encoding="utf-8", errors="replace")
    if len(raw) <= max_chars:
        return raw
    return raw[:max_chars] + "\n\n[... index.json truncado por tamaño; usá /leer curso/archivo.vtt ...]"


def _skills_hint(work_dir: Path) -> str:
    skills = work_dir / ".claude" / "skills"
    if not skills.is_dir():
        return ""
    parts = []
    for f in sorted(skills.glob("*.md")):
        try:
            head = f.read_text(encoding="utf-8", errors="replace").split("\n")[:12]
            parts.append(f"- {f.stem}: " + " ".join(line.strip() for line in head if line.strip())[:200])
        except OSError:
            pass
    if not parts:
        return ""
    return "\nIdeas de tareas (skills del proyecto):\n" + "\n".join(parts[:8])


def _leer_vtt(transcripts_dir: Path, rel: str) -> str | None:
    rel = rel.strip().strip("/").replace("..", "")
    if not rel:
        return None
    path = (transcripts_dir / rel).resolve()
    try:
        path.relative_to(transcripts_dir.resolve())
    except ValueError:
        return None
    if not path.is_file() or path.suffix.lower() != ".vtt":
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    cap = 100_000
    if len(text) > cap:
        text = text[:cap] + "\n\n[... truncado; pedí un fragmento más chico ...]"
    return text


def _chat_stream_collect(base: str, model: str, messages: list[dict]) -> str:
    body = json.dumps({"model": model, "messages": messages, "stream": True}).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    parts: list[str] = []
    with urllib.request.urlopen(req, timeout=600) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("done"):
                break
            chunk = (obj.get("message") or {}).get("content") or ""
            if chunk:
                parts.append(chunk)
                print(chunk, end="", flush=True)
    print()
    return "".join(parts)


def _print_transcript_inventory(transcripts_dir: Path) -> None:
    """Muestra dónde están los .vtt (el repo git NO es esta carpeta)."""
    root = transcripts_dir.resolve()
    print("  ─── Tus transcripciones (carpeta de trabajo de claude_udea) ───")
    print(f"  Ruta completa:\n    {root}\n")
    if not transcripts_dir.is_dir():
        print("  (Aún no existe transcripts/; ejecutá claude_udea sin --dry-run primero.)\n")
        return
    subs = sorted(p for p in transcripts_dir.iterdir() if p.is_dir())
    if not subs:
        print("  (No hay subcarpetas de cursos todavía.)\n")
        return
    for d in subs:
        vtts = sorted(d.glob("*.vtt"))
        print(f"  📁 {d.name}/  ({len(vtts)} archivos .vtt)")
        for v in vtts[:6]:
            print(f"      • {v.name}")
        if len(vtts) > 6:
            print(f"      • … y {len(vtts) - 6} más")
    idx = transcripts_dir / "index.json"
    if idx.exists():
        print(f"\n  Índice JSON: {idx.name} (mismo directorio)")
    print()
    print("  Para cargar uno en el chat: /leer <carpeta>/<archivo.vtt>")
    print("  Ejemplo: /leer 500-501-ingles-v-grupo-13/2026-03-24_….vtt\n")


def run_session(work_dir: Path, transcripts_dir: Path, model: str | None = None) -> None:
    base = _ollama_base()
    if not ollama_available(base):
        print("  Ollama no responde en", base)
        print("  1) Instalá Ollama: https://ollama.com/download")
        print("  2) Descargá un modelo: ollama pull llama3.2")
        print("  3) Volvé a ejecutar con --ollama\n")
        return

    want = _ollama_model(model)
    models = list_models(base)
    if not models:
        print("  No hay modelos en Ollama. Ejecutá: ollama pull llama3.2\n")
        return

    use_model = _pick_model(want, models)
    if use_model != want and ":" not in want:
        print(f"  (Modelo '{want}' no encontrado; usando '{use_model}')\n")

    system = _read_claude_md(work_dir)
    system += "\n\n## Índice actual (JSON)\n" + _read_index_snippet(transcripts_dir)
    system += _skills_hint(work_dir)
    system += (
        f"\n\nRuta absoluta de transcripciones: {transcripts_dir.resolve()}\n"
        "Si necesitás el texto de una clase, el usuario puede usar el comando /leer curso/archivo.vtt "
        "en este chat para adjuntar ese VTT a su siguiente mensaje."
    )

    messages: list[dict] = [{"role": "system", "content": system}]
    pending_vtt: str | None = None

    _print_transcript_inventory(transcripts_dir)
    print("  Chat local (Ollama). Comandos:")
    print("    /listado     → volver a mostrar carpetas y .vtt")
    print("    /leer ruta   → adjuntar un .vtt al próximo mensaje")
    print("    /salir\n")

    while True:
        try:
            line = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Chau.\n")
            break

        if not line:
            continue
        low = line.lower()
        if low in ("/salir", "salir", "/exit", "/quit", "exit", "quit"):
            print("  Chau.\n")
            break

        if low in ("/listado", "/lista", "/ls", "/carpetas"):
            _print_transcript_inventory(transcripts_dir)
            continue

        if low.startswith("/leer "):
            rel = line[6:].strip()
            content = _leer_vtt(transcripts_dir, rel)
            if content is None:
                print("  No encontré ese .vtt. Ej: /leer 500-501-ingles-v-grupo-13/2026-03-24_....vtt\n")
            else:
                pending_vtt = content
                print(f"  Listo: cargué {rel} para el próximo mensaje.\n")
            continue

        user_msg = line
        if pending_vtt:
            user_msg = (
                "[Contenido del archivo VTT solicitado con /leer]\n\n"
                + pending_vtt
                + "\n\n---\nPregunta o instrucción del usuario:\n"
                + line
            )
            pending_vtt = None

        messages.append({"role": "user", "content": user_msg})
        print("IA: ", end="", flush=True)
        try:
            reply = _chat_stream_collect(base, use_model, messages)
        except urllib.error.HTTPError as e:
            print(f"\n  Error HTTP de Ollama: {e}\n")
            messages.pop()
            continue
        except (OSError, urllib.error.URLError) as e:
            print(f"\n  Error de red con Ollama: {e}\n")
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": reply or "(sin respuesta)"})

        # Mantener contexto acotado: system + últimos turnos
        if len(messages) > 25:
            messages = [messages[0]] + messages[-24:]


def parse_ollama_model_flag(args: list[str]) -> tuple[list[str], str | None]:
    """Quita --ollama-model X del argv y devuelve (args_filtrados, modelo o None)."""
    out: list[str] = []
    model: str | None = None
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--ollama-model="):
            model = a.split("=", 1)[1].strip() or None
            i += 1
            continue
        if a == "--ollama-model":
            if i + 1 < len(args):
                model = args[i + 1].strip() or None
                i += 2
                continue
            i += 1
            continue
        out.append(a)
        i += 1
    return out, model
