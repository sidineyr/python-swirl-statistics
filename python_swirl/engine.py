import ast
import contextlib
import io
import json
import math
import os
import random
import statistics
from pathlib import Path

LESSONS = Path(__file__).parent / "lessons"


def load_lessons():
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(LESSONS.glob("*.json"))]


def distribution(data, label="Dados"):
    """Gráfico SVG local e descrição textual, sem bibliotecas externas."""
    from html import escape
    import tempfile
    values = sorted(set(data))
    counts = {x: data.count(x) for x in values}
    description = label + ": " + "; ".join(f"valor {x}: {counts[x]} ocorrência(s)" for x in values)
    width, height = 700, 300
    lo, hi = min(data), max(data)
    def xcoord(x):
        return 55 + 590 * (x - lo) / (hi - lo or 1)
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                f'<title id="title">{escape(label)}</title><desc id="desc">{escape(description)}</desc>',
                '<rect width="700" height="300" fill="white"/>',
                f'<text x="30" y="28" font-size="18">{escape(label)}</text>',
                '<line x1="55" y1="235" x2="645" y2="235" stroke="black"/>']
    for x in values:
        for j in range(counts[x]):
            elements.append(f'<circle cx="{xcoord(x)}" cy="{220-j*18}" r="6" fill="#174b78"/>')
        elements.append(f'<text x="{xcoord(x)}" y="260" text-anchor="middle" font-size="13">{x}</text>')
    elements.append('</svg>')
    folder = Path(tempfile.gettempdir()) / "python-swirl-graficos"
    folder.mkdir(exist_ok=True)
    import uuid
    target = folder / (uuid.uuid4().hex + ".svg")
    target.write_text("\n".join(elements), encoding="utf-8")
    print(description)
    print(f"Gráfico de pontos salvo em: {target} (abra no navegador)")
    return None


def namespace(lesson):
    ns = {"__builtins__": __builtins__, "mean": statistics.mean,
          "median": statistics.median, "pstdev": statistics.pstdev,
          "stdev": statistics.stdev, "Random": random.Random,
          "grafico": distribution}
    exec(lesson["setup"], ns)
    return ns


def execute(source, ns):
    """Executa Python local; isto NÃO é uma sandbox."""
    tree = ast.parse(source, mode="exec")
    output = io.StringIO()
    result = None
    with contextlib.redirect_stdout(output):
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            prefix = ast.Module(body=tree.body[:-1], type_ignores=[])
            exec(compile(prefix, "<estudante>", "exec"), ns)
            result = eval(compile(ast.Expression(tree.body[-1].value), "<estudante>", "eval"), ns)
        else:
            exec(compile(tree, "<estudante>", "exec"), ns)
        if result is not None:
            print(repr(result))
    return result, output.getvalue()


def validate(step, ns, result):
    value = ns.get(step["target"]) if "target" in step else result
    rule = step["check"]
    if rule["kind"] == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isclose(value, rule["value"], rel_tol=1e-7, abs_tol=1e-7)
    if rule["kind"] == "sequence":
        return isinstance(value, (list, tuple)) and list(value) == rule["value"]
    if rule["kind"] == "sample_means":
        if not isinstance(value, (list, tuple)) or len(value) != 200:
            return False
        rng = random.Random(42)
        expected = [statistics.mean(rng.sample(ns["populacao"], 5)) for _ in range(200)]
        return all(isinstance(x, (int, float)) and math.isclose(x, y, abs_tol=1e-7) for x, y in zip(value, expected))
    raise ValueError("Validador desconhecido")


class Progress:
    def __init__(self, path):
        self.path = Path(path).expanduser()
        self.data = {"version": 1, "lessons": {}}
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text(encoding="utf-8"))
                if data.get("version") != 1 or not isinstance(data.get("lessons"), dict):
                    raise ValueError("Formato incompatível")
                for item in data["lessons"].values():
                    if not isinstance(item, dict) or not isinstance(item.get("index"), int) or item["index"] < 0 or not isinstance(item.get("events"), list):
                        raise ValueError("Progresso inválido")
                self.data = data
            except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError(f"Progresso ilegível. Preserve o arquivo e use --progress com outro caminho. {exc}") from exc

    def entry(self, lesson):
        return self.data["lessons"].setdefault(lesson["id"], {"index": 0, "events": []})

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temp, self.path)

    def record(self, lesson, event, advance=False):
        entry = self.entry(lesson)
        entry["events"].append(event)
        if advance:
            entry["index"] += 1
        self.save()

    def restore(self, lesson):
        ns = namespace(lesson)
        for event in self.entry(lesson)["events"]:
            if event["kind"] == "code":
                execute(event["source"], ns)
        return ns

    def reset(self, lesson):
        self.data["lessons"][lesson["id"]] = {"index": 0, "events": []}
        self.save()
