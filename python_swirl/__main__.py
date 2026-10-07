import argparse
import json
from pathlib import Path
from .engine import Progress, load_lessons, execute, validate

HELP = "Comandos: :ajuda | :dica | :repetir | :explorar | :reiniciar | :sair\nCódigo: uma linha; use :bloco para várias linhas e termine com uma linha contendo apenas ."


def ask(prompt):
    return input(prompt).strip()


def run_lesson(lesson, progress):
    entry = progress.entry(lesson)
    print(f"\n{lesson['title']}\n{lesson['intro']}\nObjetivos: " + "; ".join(lesson['objectives']))
    if entry['index'] >= len(lesson['steps']):
        print("Lição concluída. Respostas preservadas. Digite :reiniciar no menu para refazer.")
        return
    print("Retomada: códigos anteriores serão executados novamente, com os mesmos privilégios de Python local.")
    try:
        ns = progress.restore(lesson)
    except Exception as exc:
        print(f"Não foi possível restaurar as variáveis: {exc}. Use :reiniciar no menu para esta lição.")
        return
    hint = 0
    shown = -1
    while entry['index'] < len(lesson['steps']):
        index = entry['index']
        step = lesson['steps'][index]
        if shown != index:
            print(f"\nEtapa {index+1}/{len(lesson['steps'])} · {step['type']}\n{step['text']}")
            if 'options' in step:
                for n, option in enumerate(step['options'], 1):
                    print(f"  {n}. {option}")
            shown = index
        answer = ask("Python > " if step['type'] == 'code' else "Resposta > ")
        if answer == ':sair':
            progress.save()
            print("Pausa salva. Até a próxima!")
            return
        if answer == ':ajuda':
            print(HELP)
            continue
        if answer == ':repetir':
            shown = -1
            continue
        if answer == ':reiniciar':
            progress.reset(lesson)
            return run_lesson(lesson, progress)
        if answer == ':dica':
            tips = step.get('hints', ["Releia a pergunta e compare com os resultados observados."])
            print(tips[min(hint, len(tips)-1)])
            hint += 1
            continue
        if answer == ':explorar':
            source = ask("Experimente uma linha Python (sem avançar): ")
            try:
                _, output = execute(source, ns)
                print(output or "Código executado.")
                progress.record(lesson, {"kind": "code", "source": source})
            except Exception as exc:
                print(f"{type(exc).__name__}: {exc}")
                ns = progress.restore(lesson)
            continue
        if answer == ':bloco' and step['type'] == 'code':
            print("Digite as linhas com indentação; termine com .")
            lines = []
            while True:
                line = input("... ")
                if line == '.':
                    break
                lines.append(line)
            answer = '\n'.join(lines)
        if answer.startswith(':'):
            print(HELP)
            continue
        if not answer and step['type'] not in ('info',):
            print("Escreva uma resposta ou use :dica.")
            continue
        if step['type'] == 'code':
            try:
                result, output = execute(answer, ns)
                print(output or "Código executado.")
                correct = validate(step, ns, result)
                progress.record(lesson, {"kind": "code", "source": answer}, correct)
                if not correct:
                    print(step['feedback_wrong'])
                    continue
            except SyntaxError as exc:
                print(f"Vamos ajustar a escrita do código: {exc.msg}. Use :dica.")
                ns = progress.restore(lesson)
                continue
            except Exception as exc:
                print(f"O código não terminou: {type(exc).__name__}: {exc}. Use :dica.")
                ns = progress.restore(lesson)
                continue
        elif step['type'] == 'choice':
            if answer != str(step['answer']):
                print(step.get('feedbacks', {}).get(answer, step['feedback_wrong']))
                continue
            progress.record(lesson, {"kind": "answer", "step": index, "text": answer}, True)
        elif step['type'] == 'reflection':
            print("Resposta registrada para autoavaliação, sem correção automática.\n" + step['rubric'])
            progress.record(lesson, {"kind": "answer", "step": index, "text": answer}, True)
        else:
            progress.record(lesson, {"kind": "answer", "step": index, "text": answer}, True)
        print(step.get('feedback_ok', "Etapa registrada."))
        hint = 0
    print("\nLição concluída. Releia suas interpretações com --exportar. Concluir etapas não comprova aprendizagem.")


def main():
    parser = argparse.ArgumentParser(description="Python Swirl · Aprenda estatística em Python")
    parser.add_argument('--progress', default=str(Path.home() / '.python-swirl' / 'progresso.json'))
    parser.add_argument('--listar', action='store_true')
    parser.add_argument('--licao', type=int, help='Número da lição')
    parser.add_argument('--exportar', metavar='ARQUIVO', help='Exportar respostas e códigos para JSON')
    args = parser.parse_args()
    lessons = load_lessons()
    choices = [str(n) for n in range(1, len(lessons)+1)]
    if args.licao is not None and not 1 <= args.licao <= len(lessons):
        parser.error(f'Escolha uma lição de 1 a {len(lessons)}')
    if args.listar:
        for n, lesson in enumerate(lessons, 1):
            print(f"{n}. {lesson['title']}")
        return
    try:
        progress = Progress(args.progress)
        if args.exportar:
            target = Path(args.exportar)
            if target.exists():
                print("Escolha um arquivo novo para não sobrescrever uma exportação.")
                return
            target.write_text(json.dumps(progress.data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"Respostas exportadas: {target}")
            return
        print("\nPYTHON SWIRL · Aprenda estatística praticando em Python\n" + HELP)
        print("Sem conta e sem envio de dados. Código executado localmente, sem isolamento. Use código de confiança.")
        if args.licao is not None:
            run_lesson(lessons[args.licao-1], progress)
            return
        while True:
            print("\nEscolha uma lição:")
            for n, lesson in enumerate(lessons, 1):
                current = progress.entry(lesson)['index']
                print(f"{n}. {lesson['title']} ({current}/{len(lesson['steps'])} etapas)")
            selection = ask(", ".join(choices) + " ou :sair > ")
            if selection == ':sair':
                return
            if selection == ':reiniciar':
                choice = ask("Qual lição reiniciar? " + ", ".join(choices) + " > ")
                if choice in choices:
                    progress.reset(lessons[int(choice)-1])
                continue
            if selection in choices:
                run_lesson(lessons[int(selection)-1], progress)
            else:
                print(HELP)
    except (EOFError, KeyboardInterrupt):
        print("\nPausa. O progresso das etapas registradas está salvo.")
    except (OSError, ValueError) as exc:
        print(f"Não foi possível continuar: {exc}")


if __name__ == '__main__':
    main()
