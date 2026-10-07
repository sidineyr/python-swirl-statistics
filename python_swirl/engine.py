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


def distribution(data, label="Dados", limits=None):
    """Gráfico SVG local e descrição textual, sem bibliotecas externas."""
    from html import escape
    import tempfile
    values = sorted(set(data))
    counts = {x: data.count(x) for x in values}
    description = label + ": " + "; ".join(f"valor {x}: {counts[x]} ocorrência(s)" for x in values)
    width, height = 700, 300
    lo, hi = limits if limits is not None else (min(data), max(data))
    if hi <= lo:
        hi = lo + 1
    if min(data) < lo or max(data) > hi:
        raise ValueError("Os limites devem incluir todos os dados.")
    description += f"; eixo de {lo} a {hi}"
    ticks = [lo + (hi-lo)*i/5 for i in range(6)]
    def xcoord(x):
        return 55 + 590 * (x - lo) / (hi - lo or 1)
    elements = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
                f'<title id="title">{escape(label)}</title><desc id="desc">{escape(description)}</desc>',
                '<rect width="700" height="300" fill="white"/>',
                f'<text x="30" y="28" font-size="18">{escape(label)}</text>',
                '<line x1="55" y1="235" x2="645" y2="235" stroke="black"/>']
    for tick in ticks:
        elements.append(f'<text x="{xcoord(tick)}" y="285" text-anchor="middle" font-size="13">{tick:g}</text>')
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
    """Execução local. Captura valores de print sem interpretar texto de stdout."""
    tree = ast.parse(source, mode="exec")
    output = io.StringIO()
    result = None
    printed = []
    existed = "print" in ns
    original_print = ns.get("print", print)
    def observed_print(*args, **kwargs):
        original_print(*args, **kwargs)
        printed.append(args[0] if len(args) == 1 else None)
    before = {name: value for name, value in ns.items() if not name.startswith("_")}
    ns["_swirl_before"] = before
    ns["_swirl_assigned"] = {target.id for node in tree.body if isinstance(node, (ast.Assign, ast.AnnAssign)) for target in (node.targets if isinstance(node, ast.Assign) else [node.target]) if isinstance(target, ast.Name)}
    ns["print"] = observed_print
    ns["_swirl_names"] = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    try:
        with contextlib.redirect_stdout(output):
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                exec(compile(ast.Module(body=tree.body[:-1], type_ignores=[]), "<estudante>", "exec"), ns)
                result = eval(compile(ast.Expression(tree.body[-1].value), "<estudante>", "eval"), ns)
            else:
                exec(compile(tree, "<estudante>", "exec"), ns)
            # Uma atribuição final também pode fornecer um resultado inequívoco.
            if result is None and tree.body and isinstance(tree.body[-1], ast.Assign):
                targets = tree.body[-1].targets
                if len(targets) == 1 and isinstance(targets[0], ast.Name):
                    result = ns[targets[0].id]
            if result is None and len(printed) == 1:
                result = printed[0]
            if result is not None and not printed:
                print(repr(result))
    finally:
        if existed:
            ns["print"] = original_print
        else:
            ns.pop("print", None)
    return result, output.getvalue()


def validate(step, ns, result):
    if "target" in step and step["target"] not in ns.get("_swirl_names", set()):
        return False
    value = ns.get(step["target"]) if "target" in step else result
    if "target" in step:
        target = step["target"]
        produced = target in ns.get("_swirl_assigned", set()) or ns.get("_swirl_before", {}).get(target) is not value
        if not produced and result is not value:
            return False
    rule = step["check"]
    if rule["kind"] == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            return False
        if "decimals" in rule:
            return round(value, rule["decimals"]) == round(rule["value"], rule["decimals"])
        return math.isclose(value, rule["value"], rel_tol=1e-7, abs_tol=1e-7)
    if rule["kind"] == "sequence":
        return isinstance(value, (list, tuple)) and list(value) == rule["value"]
    if rule["kind"] == "sample_means":
        if not isinstance(value, (list, tuple)) or len(value) != 200:
            return False
        rng = random.Random(42)
        expected = [statistics.mean(rng.sample(list(range(10, 110)), 5)) for _ in range(200)]
        return all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isclose(x, y, abs_tol=1e-7) for x, y in zip(value, expected))
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
        entry = self.data["lessons"].setdefault(lesson["id"], {"index": 0, "events": [], "revision": lesson.get("revision", 1)})
        if entry.get("revision", 1) < lesson.get("revision", 1):
            entry["previous_index"] = entry["index"]
            # A lição 3 ganhou apoio antes da simulação; preserve respostas e retome ali.
            if lesson["id"] == "amostragem" and entry["index"] >= 8:
                entry["index"] = 8
                for event in entry["events"]:
                    if isinstance(event.get("step"), int) and event["step"] >= 8:
                        event["step"] += 3
            entry["revision"] = lesson["revision"]
            entry["updated_notice"] = True
            self.save()
        return entry

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
        events = self.entry(lesson)["events"]
        last_reset = max((i for i, event in enumerate(events) if event["kind"] == "context_reset"), default=-1)
        for event in events[last_reset+1:]:
            if event["kind"] == "code":
                execute(event["source"], ns)
        return ns

    def reset(self, lesson):
        self.data["lessons"][lesson["id"]] = {"index": 0, "events": []}
        self.save()
