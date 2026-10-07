import contextlib
import io
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET
from python_swirl.engine import Progress, load_lessons, namespace, execute, validate, distribution
from python_swirl.__main__ import run_lesson


class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.lessons = load_lessons()

    def test_expression_print_assignment_and_not_stdout_text(self):
        lesson = self.lessons[0]
        step = next(s for s in lesson['steps'] if s['type'] == 'code')
        for source in ['mean(tempos)', 'print(mean(tempos))', 'resposta = sum(tempos)/len(tempos)']:
            with self.subTest(source=source):
                ns = namespace(lesson)
                result, _ = execute(source, ns)
                self.assertTrue(validate(step, ns, result))
        for source in ["print('14')", 'print(14, 15)', 'print(14); print(15)', 'True']:
            ns = namespace(lesson)
            result, _ = execute(source, ns)
            self.assertFalse(validate(step, ns, result))

    def test_adulterated_population_and_stale_target_rejected(self):
        lesson = self.lessons[2]
        step = next(s for s in lesson['steps'] if s.get('target') == 'medias')
        ns = namespace(lesson)
        result, _ = execute('populacao = [59.5]*100; medias = [59.5]*200', ns)
        self.assertFalse(validate(step, ns, result))
        ns = namespace(lesson)
        result, _ = execute(step['solution'], ns)
        self.assertTrue(validate(step, ns, result))
        for source in ['0', 'lambda: medias', 'if False:\n    medias = []']:
            result, _ = execute(source, ns)
            self.assertFalse(validate(step, ns, result), source)
        result, _ = execute('medias', ns)
        self.assertTrue(validate(step, ns, result))

    def test_equivalent_loop_and_sampling_order(self):
        lesson = self.lessons[2]
        step = next(s for s in lesson['steps'] if s.get('target') == 'medias')
        ns = namespace(lesson)
        source = 'rng = Random(42)\nmedias = []\nfor _ in range(200):\n    medias.append(sum(rng.sample(populacao, 5))/5)'
        result, _ = execute(source, ns)
        self.assertTrue(validate(step, ns, result))
        result, _ = execute('medias = medias[::-1]', ns)
        self.assertFalse(validate(step, ns, result))

    def test_declared_precision_and_independent_statistics(self):
        lesson = self.lessons[1]
        for name, values in [('turma_a', [6,7,7,7,8]), ('turma_b', [3,5,7,10,10])]:
            expected = math.sqrt(sum((x - sum(values)/len(values))**2 for x in values)/len(values))
            step = next(s for s in lesson['steps'] if s.get('solution') == f'pstdev({name})')
            self.assertAlmostEqual(step['check']['value'], expected)
            for source in [f'pstdev({name})', f'round(pstdev({name}), 2)']:
                ns = namespace(lesson); result, _ = execute(source, ns)
                self.assertTrue(validate(step, ns, result))
            ns = namespace(lesson); result, _ = execute(f'stdev({name})', ns)
            self.assertFalse(validate(step, ns, result))
        ns = namespace(self.lessons[2])
        self.assertEqual(sum(range(10,110))/100, 59.5)
        self.assertEqual(sum([91,24,13,104,45])/5, 55.4)
        self.assertEqual(sum([41,38,27,104,23])/5, 46.6)

    def test_exploration_isolated_context_reset_keeps_answers(self):
        lesson = self.lessons[0]
        with tempfile.TemporaryDirectory() as folder:
            p = Progress(Path(folder)/'progress.json')
            answers = ['', 'Previsão original', '', ':explorar', 'tempos = [1]', 'tempos = [1]', ':restaurar', 'print(mean(tempos))', ':sair']
            with patch('builtins.input', side_effect=answers), contextlib.redirect_stdout(io.StringIO()) as out:
                run_lesson(lesson, p)
            self.assertEqual(p.entry(lesson)['index'], 4)
            self.assertEqual(p.restore(lesson)['tempos'], [10,12,14,16,18])
            self.assertIn('Exploração separada', out.getvalue())
            self.assertTrue(any(e.get('text') == 'Previsão original' for e in p.entry(lesson)['events']))

    def test_reading_requires_enter_and_reset_confirmation(self):
        lesson = self.lessons[0]
        with tempfile.TemporaryDirectory() as folder:
            p = Progress(Path(folder)/'p.json')
            with patch('builtins.input', side_effect=['banana', '', ':reiniciar', 'não', ':sair']), contextlib.redirect_stdout(io.StringIO()) as out:
                run_lesson(lesson, p)
            self.assertEqual(p.entry(lesson)['index'], 1)
            self.assertIn('somente Enter', out.getvalue())
            self.assertIn('Progresso preservado', out.getvalue())

    def test_review_edit_preserves_original(self):
        lesson = self.lessons[0]
        with tempfile.TemporaryDirectory() as folder:
            p = Progress(Path(folder)/'p.json')
            with patch('builtins.input', side_effect=['', 'Primeira previsão', ':editar', '2', 'Previsão revisada', ':revisar', ':sair']), contextlib.redirect_stdout(io.StringIO()) as out:
                run_lesson(lesson,p)
            self.assertIn('Primeira previsão', out.getvalue())
            self.assertIn('Previsão revisada', out.getvalue())
            self.assertEqual(p.entry(lesson)['index'], 2)

    def test_old_sampling_progress_migrated_without_loss(self):
        lesson = self.lessons[2]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'p.json'
            old = {'version':1,'lessons':{'amostragem':{'index':13,'events':[{'kind':'answer','step':12,'text':'Meu relatório antigo'}]}}}
            path.write_text(json.dumps(old),encoding='utf-8')
            p = Progress(path)
            entry = p.entry(lesson)
            self.assertEqual(entry['index'], 8)
            self.assertEqual(entry['events'][0]['text'], 'Meu relatório antigo')
            self.assertEqual(entry['events'][0]['step'], 15)
            self.assertEqual(Progress(path).entry(lesson)['index'], 8)

    def test_common_graph_domain_coordinates(self):
        outputs = []
        for values in [[6,7,7,7,8], [3,5,7,10,10]]:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                distribution(values, 'Notas', limits=(0,10))
            path = Path(out.getvalue().split('Gráfico de pontos salvo em: ')[1].split(' (abra')[0])
            outputs.append(ET.fromstring(path.read_text(encoding='utf-8')))
            path.unlink()
        ns = {'s':'http://www.w3.org/2000/svg'}
        a = [float(c.attrib['cx']) for c in outputs[0].findall('s:circle',ns)]
        b = [float(c.attrib['cx']) for c in outputs[1].findall('s:circle',ns)]
        self.assertLess(max(a)-min(a), max(b)-min(b))
        self.assertEqual(a[1], b[2])  # nota 7 ocupa exatamente a mesma posição
        with self.assertRaises(ValueError):
            distribution([12],limits=(0,10))

    def test_real_cli_all_lessons_and_pause_resume(self):
        with tempfile.TemporaryDirectory() as folder:
            for number, lesson in enumerate(self.lessons,1):
                path = Path(folder)/f'{number}.json'
                answers = [s['solution'] if s['type']=='code' else str(s['answer']) if s['type']=='choice' else 'Minha interpretação e limites.' if s['type']=='reflection' else '' for s in lesson['steps']]
                proc = subprocess.run([sys.executable,'-m','python_swirl','--licao',str(number),'--progress',str(path)], input='\n'.join(answers)+'\n',text=True,capture_output=True,timeout=20)
                self.assertEqual(proc.returncode,0,proc.stderr)
                self.assertIn('Lição concluída',proc.stdout)
                self.assertEqual(Progress(path).entry(lesson)['index'],len(lesson['steps']))
            path = Path(folder)/'pause.json'
            command = [sys.executable,'-m','python_swirl','--licao','1','--progress',str(path)]
            proc = subprocess.run(command,input='\n:dica\nMinha previsão\n:sair\n',text=True,capture_output=True,timeout=20)
            self.assertIn('Pausa salva',proc.stdout)
            proc = subprocess.run(command,input='\nmean(\nprint(mean(tempos))\n:sair\n',text=True,capture_output=True,timeout=20)
            self.assertIn('Vamos ajustar',proc.stdout)
            self.assertEqual(Progress(path).entry(self.lessons[0])['index'],4)
