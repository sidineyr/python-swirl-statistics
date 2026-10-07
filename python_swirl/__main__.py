import argparse
import json
from pathlib import Path
from .engine import Progress, load_lessons, execute, validate, namespace

HELP = "Comandos: :ajuda | :dica | :repetir | :explorar | :restaurar | :revisar | :editar | :reiniciar | :sair\nCódigo: uma linha; use :bloco para várias linhas e termine com uma linha contendo apenas ."


LABELS = {"info": "Leia", "code": "Pratique em Python", "choice": "Escolha", "reflection": "Explique"}


def review(lesson, progress):
    print("\nRevisão · " + lesson["title"])
    entry = progress.entry(lesson)
    for event in entry["events"]:
        if event["kind"] == "code":
            index = event.get("step")
            status = "resultado conferido" if event.get("correct") else "tentativa registrada; confira a tarefa"
            print(f"Código · etapa {index+1 if index is not None else '?'} · {status}:\n{event['source']}")
        elif event["kind"] in ("answer", "revision") and event.get("text"):
            index = event.get("step")
            print(f"Etapa {index+1 if index is not None else '?'}: {event['text']}")
            if isinstance(index, int) and index < len(lesson["steps"]):
                print(lesson["steps"][index].get("rubric", ""))
    print("Respostas abertas são autoavaliação; conclusão não comprova domínio.")


def edit_reflection(lesson, progress):
    entry = progress.entry(lesson)
    review(lesson, progress)
    raw = ask("Número da etapa de reflexão a revisar > ")
    if raw.isdigit() and 1 <= int(raw) <= min(entry['index'], len(lesson['steps'])) and lesson['steps'][int(raw)-1]['type'] == 'reflection':
        text = ask("Sua nova explicação > ")
        if text:
            progress.record(lesson, {"kind": "revision", "step": int(raw)-1, "text": text})
            print("Revisão registrada; a resposta anterior permanece no histórico.")
    else:
        print("Escolha uma etapa de reflexão já registrada; consulte :revisar.")


def confirm_reset(lesson, progress):
    answer = ask("Isso apaga o progresso desta lição. Digite REINICIAR para confirmar > ")
    if answer != "REINICIAR":
        print("Progresso preservado.")
        return False
    progress.reset(lesson)
    return True


def ask(prompt):
    return input(prompt).strip()


def run_lesson(lesson, progress):
    entry = progress.entry(lesson)
    print(f"\n{lesson['title']}\n{lesson['intro']}\nObjetivos: " + "; ".join(lesson['objectives']))
    if entry['index'] >= len(lesson['steps']):
        print("Lição concluída. Respostas preservadas. Digite :reiniciar no menu para refazer.")
        review(lesson, progress)
        return
    if entry.pop("updated_notice", False):
        print("A lição ganhou etapas de apoio. Suas respostas foram preservadas; revise a sequência a partir daqui.")
        progress.save()
    if entry['index']:
        print("Retomada: códigos anteriores serão executados novamente, com os mesmos privilégios de Python local.")
    print("Use :dica para apoio, :ajuda para comandos e :sair para pausar.")
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
            print(f"\nEtapa {index+1}/{len(lesson['steps'])} · {LABELS[step['type']]}\n{step['text']}")
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
            if confirm_reset(lesson, progress):
                return run_lesson(lesson, progress)
            continue
        if answer == ':restaurar':
            progress.record(lesson, {"kind": "context_reset"})
            ns = namespace(lesson)
            print("Dados originais restaurados; respostas e posição preservadas. Variáveis criadas por você devem ser recalculadas.")
            continue
        if answer == ':revisar':
            review(lesson, progress)
            continue
        if answer == ':editar':
            edit_reflection(lesson, progress)
            continue
        if answer == ':dica':
            tips = step.get('hints', ["Releia a pergunta e compare com os resultados observados."])
            print(tips[min(hint, len(tips)-1)])
            hint += 1
            continue
        if answer == ':explorar':
            source = ask("Experimente uma linha Python (sem avançar): ")
            try:
                exploration = progress.restore(lesson)
                _, output = execute(source, exploration)
                print(output or "Código executado.")
                print("Exploração separada: alterações não entram na resposta nem na retomada.")
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
                progress.record(lesson, {"kind": "code", "source": answer, "step": index, "correct": correct}, correct)
                if not correct:
                    if 'target' in step and step['target'] not in ns.get('_swirl_names', set()):
                        print(f"Esta tentativa deve criar ou mostrar a variável {step['target']}; um valor antigo sozinho não valida a nova entrada.")
                    elif result is None:
                        print("Mostre um valor com uma expressão, uma atribuição final ou print com um único argumento.")
                    elif isinstance(result, (int, float)) and step['check']['kind'] == 'number' and 'decimals' not in step['check'] and abs(result - step['check']['value']) < 0.01:
                        print("O valor está próximo, mas esta etapa pede precisão completa. Use a função sem round e mostre o resultado.")
                    else:
                        print(step['feedback_wrong'])
                    print("Use ponto decimal no código. Para recuperar dados alterados: :restaurar. Para apoio: :dica.")
                    continue
            except SyntaxError as exc:
                print(f"Vamos ajustar a escrita do código: {exc.msg}. Use :dica.")
                ns = progress.restore(lesson)
                continue
            except NameError as exc:
                print(f"Nome não encontrado: {exc}. Confira a grafia da variável; :dica orienta o código e :restaurar recupera dados originais.")
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
            if answer:
                print("Esta é uma etapa de leitura. Pressione somente Enter para continuar, ou use :ajuda.")
                continue
            progress.record(lesson, {"kind": "answer", "step": index, "text": answer}, True)
        print(step.get('feedback_ok', "Etapa registrada."))
        hint = 0
    print("\nLição concluída. Você praticou: " + "; ".join(lesson["objectives"]))
    review(lesson, progress)
    lessons = load_lessons()
    position = next(i for i, item in enumerate(lessons) if item["id"] == lesson["id"])
    if position + 1 < len(lessons):
        print(f"Próxima lição: {lessons[position+1]['title']}. No menu, escolha {position+2}; ou execute com --licao {position+2}.")
    print("Para revisar depois: --revisar N. Para corrigir uma reflexão, inclusive concluída: --editar N ou :editar no menu. Exportação JSON: --exportar ARQUIVO.")


def main():
    parser = argparse.ArgumentParser(description="Python Swirl · Aprenda estatística em Python")
    parser.add_argument('--progress', default=str(Path.home() / '.python-swirl' / 'progresso.json'))
    parser.add_argument('--listar', action='store_true')
    parser.add_argument('--revisar', type=int, help='Ler respostas de uma lição')
    parser.add_argument('--editar', type=int, help='Revisar reflexão de uma lição, inclusive concluída')
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
        if args.editar is not None:
            if not 1 <= args.editar <= len(lessons):
                parser.error("Escolha uma lição existente para editar")
            edit_reflection(lessons[args.editar-1], progress)
            return
        if args.revisar is not None:
            if not 1 <= args.revisar <= len(lessons):
                parser.error("Escolha uma lição existente para revisar")
            review(lessons[args.revisar-1], progress)
            return
        if args.exportar:
            target = Path(args.exportar)
            if target.exists():
                print("Escolha um arquivo novo para não sobrescrever uma exportação.")
                return
            target.write_text(json.dumps(progress.data, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f"Respostas exportadas: {target}")
            return
        print("\nPYTHON SWIRL · Aprenda estatística praticando em Python\nUse :ajuda para ver os comandos.")
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
                    confirm_reset(lessons[int(choice)-1], progress)
                continue
            if selection == ':editar':
                choice = ask("Qual lição revisar? " + ", ".join(choices) + " > ")
                if choice in choices:
                    edit_reflection(lessons[int(choice)-1], progress)
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
