import contextlib
import io
import json
import statistics
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from python_swirl.engine import Progress, load_lessons, namespace, execute, validate, distribution
from python_swirl.__main__ import run_lesson


class CourseTests(unittest.TestCase):
    def setUp(self):
        self.lessons = load_lessons()

    def test_all_lessons_reference_solutions_and_resume(self):
        for lesson in self.lessons:
            with self.subTest(lesson=lesson['id']), tempfile.TemporaryDirectory() as folder:
                progress = Progress(Path(folder)/'p.json')
                ns = namespace(lesson)
                for step in lesson['steps']:
                    if step['type'] == 'code':
                        result, _ = execute(step['solution'], ns)
                        self.assertTrue(validate(step, ns, result), step['text'])
                        progress.record(lesson, {'kind':'code','source':step['solution']}, True)
                    else:
                        progress.record(lesson, {'kind':'answer','text':'teste'}, True)
                resumed = Progress(progress.path)
                restored = resumed.restore(lesson)
                self.assertEqual(resumed.entry(lesson)['index'], len(lesson['steps']))
                for key, value in ns.items():
                    if isinstance(value, list):
                        self.assertEqual(restored[key], value)

    def test_equivalent_code_and_wrong_numbers(self):
        lesson = self.lessons[0]
        step = next(s for s in lesson['steps'] if s['type']=='code')
        ns = namespace(lesson)
        result, _ = execute('sum(tempos) / len(tempos)', ns)
        self.assertTrue(validate(step, ns, result))
        self.assertFalse(validate(step, ns, 13))
        self.assertFalse(validate(step, ns, True))
        self.assertFalse(validate(step, ns, float('nan')))

    def test_dispersion_and_sampling_values(self):
        ns = namespace(self.lessons[1])
        self.assertEqual(statistics.mean(ns['turma_a']), statistics.mean(ns['turma_b']))
        self.assertLess(statistics.pstdev(ns['turma_a']),statistics.pstdev(ns['turma_b']))
        ns = namespace(self.lessons[2])
        self.assertEqual(statistics.mean(ns['populacao']),59.5)
        self.assertEqual(statistics.mean(ns['primeira']),55.4)
        self.assertEqual(statistics.mean(ns['segunda']),46.6)

    def test_fake_simulation_rejected(self):
        lesson = self.lessons[2]
        ns = namespace(lesson)
        step = next(s for s in lesson['steps'] if s.get('target')=='medias')
        ns['medias'] = [59.5]*200
        self.assertFalse(validate(step,ns,None))
        execute(step['solution'],ns)
        self.assertTrue(validate(step,ns,None))

    def test_invalid_progress_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'p.json'
            path.write_text('{broken')
            with self.assertRaises(ValueError):
                Progress(path)
            self.assertEqual(path.read_text(),'{broken')

    def test_failed_attempt_and_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            lesson=self.lessons[0]
            p=Progress(Path(folder)/'p.json')
            p.record(lesson,{'kind':'code','source':'teste = 9'})
            self.assertEqual(p.entry(lesson)['index'],0)
            self.assertEqual(Progress(p.path).restore(lesson)['teste'],9)
            p.reset(lesson)
            self.assertNotIn('teste',p.restore(lesson))

    def test_cli_entire_course(self):
        for lesson in self.lessons:
            with self.subTest(lesson=lesson['id']), tempfile.TemporaryDirectory() as folder:
                p=Progress(Path(folder)/'p.json')
                answers=[]
                for s in lesson['steps']:
                    answers.append(s['solution'] if s['type']=='code' else str(s['answer']) if s['type']=='choice' else 'Minha reflexão sobre estes dados.' if s['type']=='reflection' else '')
                with patch('builtins.input',side_effect=answers),contextlib.redirect_stdout(io.StringIO()) as out:
                    run_lesson(lesson,p)
                self.assertIn('Lição concluída',out.getvalue())
                self.assertEqual(p.entry(lesson)['index'],len(lesson['steps']))

    def test_pause_resume_and_hint(self):
        lesson=self.lessons[0]
        with tempfile.TemporaryDirectory() as folder:
            p=Progress(Path(folder)/'p.json')
            with patch('builtins.input',side_effect=['',':dica','Prevejo mudança',':sair']),contextlib.redirect_stdout(io.StringIO()) as out:
                run_lesson(lesson,p)
            self.assertEqual(p.entry(lesson)['index'],2)
            self.assertIn('Pausa salva',out.getvalue())
            self.assertEqual(Progress(p.path).entry(lesson)['index'],2)

    def test_execution_error_does_not_corrupt_lesson(self):
        lesson=self.lessons[0]
        with tempfile.TemporaryDirectory() as folder:
            p=Progress(Path(folder)/'p.json')
            answers=['','Minha previsão','', 'tempos = [1]; 1 / 0', 'sum(tempos) / len(tempos)', ':sair']
            with patch('builtins.input',side_effect=answers),contextlib.redirect_stdout(io.StringIO()) as out:
                run_lesson(lesson,p)
            self.assertIn('ZeroDivisionError',out.getvalue())
            self.assertEqual(p.entry(lesson)['index'],4)
            self.assertEqual(p.restore(lesson)['tempos'],[10,12,14,16,18])

    def test_svg_has_accessible_description(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            distribution([6,7,7,7,8],'Turma <A>')
        target=Path(out.getvalue().split('Gráfico de pontos salvo em: ')[1].split(' (abra')[0])
        from xml.etree import ElementTree
        parsed=ElementTree.fromstring(target.read_text(encoding='utf-8'))
        self.assertEqual(parsed.attrib['role'],'img')
        self.assertIn('valor 7: 3 ocorrência(s)',target.read_text(encoding='utf-8'))
        self.assertIn('&lt;A&gt;',target.read_text(encoding='utf-8'))
        target.unlink()


if __name__=='__main__':
    unittest.main()
