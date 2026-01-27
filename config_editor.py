#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import os
import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from flask import Flask, Response, redirect, render_template_string, request, url_for
from waitress import serve

KV_RE = re.compile(r"^\s*([^#=\s][^=]*?)\s*=\s*(.*?)\s*$")
BOOL_TRUE = {"true", "1", "yes", "on"}
BOOL_FALSE = {"false", "0", "no", "off"}

@dataclass
class Line:
    kind: str  # "comment" | "blank" | "kv" | "other"
    raw: str
    key: Optional[str] = None
    value: Optional[str] = None

def parse_boolish(s: str) -> Optional[bool]:
    s2 = (s or "").strip().lower()
    if s2 in BOOL_TRUE:
        return True
    if s2 in BOOL_FALSE:
        return False
    return None

def bool_to_string(b: bool, style_like: str) -> str:
    orig = (style_like or "").strip()
    orig_l = orig.lower()

    if orig_l in {"0", "1"}:
        return "1" if b else "0"
    if orig == orig_l:
        return "true" if b else "false"
    return "True" if b else "False"

def parse_config(text: str) -> List[Line]:
    lines: List[Line] = []
    for raw in text.splitlines(keepends=True):
        stripped = raw.strip()

        if stripped == "":
            lines.append(Line(kind="blank", raw=raw))
            continue

        if stripped.startswith("#"):
            lines.append(Line(kind="comment", raw=raw))
            continue

        m = KV_RE.match(raw)
        if m:
            key = m.group(1).strip()
            value = m.group(2)
            lines.append(Line(kind="kv", raw=raw, key=key, value=value))
        else:
            lines.append(Line(kind="other", raw=raw))
    return lines

def render_config(lines: List[Line], new_values: Dict[str, str]) -> str:
    out: List[str] = []
    for line in lines:
        if line.kind == "kv" and line.key is not None:
            key = line.key
            if key in new_values:
                out.append(f"{key}={new_values[key]}\n")
            else:
                out.append(line.raw)
        else:
            out.append(line.raw)
    return "".join(out)

def backup_file(path: Path) -> Path:
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_suffix(path.suffix + f".bak.{ts}")
    backup_path.write_bytes(path.read_bytes())
    return backup_path

def build_items(lines: List[Line]) -> List[dict]:
    items: List[dict] = []
    comment_buf: List[str] = []

    for line in lines:
        if line.kind == "comment":
            raw = line.raw.lstrip("\ufeff")
            txt = raw.strip()
            if txt.startswith("#"):
                txt = txt[1:].lstrip()
            comment_buf.append(txt)
            continue

        if line.kind == "blank":
            if comment_buf:
                comment_buf.append("")
            continue

        if line.kind == "kv" and line.key is not None:
            comment = "\n".join(comment_buf).rstrip()
            comment_buf = []

            val = line.value or ""
            b = parse_boolish(val)
            is_bool = b is not None

            items.append(
                {
                    "key": line.key,
                    "value": val,
                    "comment": comment,
                    "is_bool": is_bool,
                    "bool_checked": bool(b) if is_bool else False,
                    "bool_style_hint": val.strip() if is_bool else "",
                }
            )
        else:
            comment_buf = []

    return items

def basic_auth_required() -> bool:
    return bool(os.getenv("CONFIG_EDITOR_USER")) or bool(os.getenv("CONFIG_EDITOR_PASS"))

def check_basic_auth(auth_header: Optional[str]) -> bool:
    user = os.getenv("CONFIG_EDITOR_USER", "")
    pw = os.getenv("CONFIG_EDITOR_PASS", "")
    if not user and not pw:
        return True

    if not auth_header or not auth_header.lower().startswith("basic "):
        return False

    try:
        b64 = auth_header.split(None, 1)[1].strip()
        decoded = base64.b64decode(b64).decode("utf-8", errors="replace")
        got_user, got_pw = decoded.split(":", 1)
    except Exception:
        return False

    return (got_user == user) and (got_pw == pw)

def run_configured_command(env_var: str, timeout_seconds: int = 10) -> Tuple[bool, str]:
    cmd = os.getenv(env_var, "").strip()
    if not cmd:
        return False, f"{env_var} is not set; action disabled."

    try:
        argv = shlex.split(cmd)
        if not argv:
            return False, f"{env_var} is empty after parsing."
        p = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        out = (p.stdout or "").strip()
        err = (p.stderr or "").strip()
        combined = "\n".join([x for x in [out, err] if x]).strip()

        if p.returncode == 0:
            return True, combined or "Command completed."
        return False, combined or f"Command failed with exit code {p.returncode}."
    except Exception as e:
        return False, f"Failed to run command: {e}"


PAGE_TMPL = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Config Editor</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin: 24px; }
    .wrap { max-width: 1020px; margin: 0 auto; }
    h1 { margin: 0 0 8px; }
    .bar { display: flex; gap: 12px; align-items: center; margin: 12px 0 18px; flex-wrap: wrap; }
    input[type="text"] { width: 100%; padding: 10px; font-size: 14px; box-sizing: border-box; }
    .row { border: 1px solid #ddd; border-radius: 10px; padding: 14px; margin: 12px 0; }
    .key { font-weight: 700; margin-bottom: 6px; display:flex; justify-content:space-between; gap:10px; }
    .comment { color: #555; font-size: 13px; margin-bottom: 10px; white-space: pre-wrap; }
    .actions { margin-top: 16px; display: flex; gap: 10px; flex-wrap: wrap; }
    button { padding: 10px 14px; border-radius: 10px; border: 1px solid #111; background: #111; color: #fff; cursor: pointer; }
    button.secondary { background: #fff; color: #111; }
    button.danger { background: #7a0f0f; border-color:#7a0f0f; }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    .msg { padding: 12px 14px; border-radius: 10px; margin: 12px 0; }
    .ok { background: #e9f7ec; border: 1px solid #a6dfb2; }
    .err { background: #fdecec; border: 1px solid #f3b1b1; }
    .small { font-size: 12px; color: #666; }
    .kvgrid { display: grid; grid-template-columns: 1fr; gap: 12px; }
    @media (min-width: 900px) { .kvgrid { grid-template-columns: 1fr 1fr; } }
    .boolwrap { display:flex; align-items:center; gap:10px; padding: 6px 0 2px; }
    .boolwrap input[type="checkbox"] { width: 20px; height: 20px; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Config Editor</h1>
    {% if message %}
      <div class="msg {{ 'ok' if message_kind=='ok' else 'err' }}">{{ message }}</div>
    {% endif %}
    <div class="bar">
      <!-- IMPORTANT: this button submits the BIG form below -->
      <button type="submit" form="saveForm">Save changes</button>
      <button class="secondary" type="button" onclick="window.location='{{ url_for('index') }}'">Reload</button>
    </div>
    <form id="saveForm" method="post" action="{{ url_for('save') }}">
      <div class="kvgrid">
        {% for item in items %}
          <div class="row">
            {% if item.comment %}
              <div class="comment">{{ item.comment }}</div>
            {% endif %}
            <div class="key">
              <span>{{ item.key }}</span>
              {% if item.is_bool %}
                <span class="small">boolean</span>
              {% endif %}
            </div>
            {% if item.is_bool %}
              <div class="boolwrap">
                <input type="hidden" name="t__{{ item.key|e }}" value="bool">
                <input type="hidden" name="b__{{ item.key|e }}" value="0">
                <input type="checkbox" name="b__{{ item.key|e }}" value="1" {% if item.bool_checked %}checked{% endif %} />
              </div>
            {% else %}
              <input type="text" name="k__{{ item.key|e }}" value="{{ item.value|e }}" />
            {% endif %}
          </div>
        {% endfor %}
      </div>
      <div class="actions">
        <button type="submit">Save changes</button>
        <button class="secondary" type="button" onclick="window.location='{{ url_for('index') }}'">Reload</button>
      </div>
    </form>
  </div>
</body>
</html>
"""
def create_app(cfg_path: Path) -> Flask:
    app = Flask(__name__)
    app.config["CFG_PATH"] = cfg_path

    def require_auth() -> Optional[Response]:
        if check_basic_auth(request.headers.get("Authorization")):
            return None
        return Response("Authentication required",401,{"WWW-Authenticate": 'Basic realm="Config Editor"'})

    @app.before_request
    def _auth_gate():
        if basic_auth_required():
            resp = require_auth()
            if resp is not None:
                return resp

    @app.get("/")
    def index():
        cfg_path = app.config["CFG_PATH"]
        text = cfg_path.read_text(errors="replace")
        lines = parse_config(text)
        items = build_items(lines)
        return render_template_string(
            PAGE_TMPL,
            items=items,
            cfg_path=str(cfg_path),
            loaded_at=dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message=request.args.get("msg"),
            message_kind=request.args.get("kind", "ok"),
            auth_on=basic_auth_required()
        )

    @app.post("/save")
    def save():
        cfg_path = app.config["CFG_PATH"]
        text = cfg_path.read_text(errors="replace")
        lines = parse_config(text)
        existing = {ln.key: ln for ln in lines if ln.kind == "kv" and ln.key}
        new_values: Dict[str, str] = {}
        for k, v in request.form.items():
            if k.startswith("k__"):
                key = k[3:]
                if key in existing:
                    new_values[key] = v
        for k, v in request.form.items():
            if k.startswith("t__"):
                key = k[3:]
                if key not in existing:
                    continue
                orig_val = (existing[key].value or "")
                if parse_boolish(orig_val) is None:
                    continue
                checked = request.form.get(f"b__{key}") == "1"
                new_values[key] = bool_to_string(checked, orig_val)
        try:
            bkp = backup_file(cfg_path)
            out_text = render_config(lines, new_values)
            cfg_path.write_text(out_text)
            return redirect(url_for("index", msg=f"Saved. A restart is required to apply changes.", kind="ok"))
        except Exception as e:
            return redirect(url_for("index", msg=f"Save failed: {e}", kind="err"))
    return app
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="/app/config/Nitrox/saves/My World/server.cfg")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", default=5000, type=int)
    args = p.parse_args()

    cfg_path = Path(args.config).expanduser()
    if not cfg_path.exists():
        raise SystemExit(f"Config file not found: {cfg_path}")

    app = create_app(cfg_path)
    serve(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
