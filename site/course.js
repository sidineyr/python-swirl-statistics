/* Numerical checking only. Python executes in notebooks, never in JavaScript. */
(() => {
  'use strict';
  const KEY = 'python-swirl-online-v1';
  const status = document.getElementById('storage-status') || document.getElementById('lesson-status');
  const announce = text => { if (status) status.textContent = text; };
  let state = {version: 1, modules: {}, last: null}, durable = true;
  try {
    const raw = localStorage.getItem(KEY);
    if (raw) { const parsed = JSON.parse(raw); if (validState(parsed)) state = parsed; else throw new Error('Formato desconhecido'); }
  } catch (_) { durable = false; announce('Não foi possível ler o progresso. Esta sessão não será salva; exporte suas respostas.'); }
  function validState(s) {
    return s && s.version === 1 && s.modules && typeof s.modules === 'object' && !Array.isArray(s.modules) && Object.entries(s.modules).every(([key,m]) => /^\d{2}-[a-z-]+$/.test(key) && m && typeof m === 'object' && !Array.isArray(m) && (!m.notes || (!Array.isArray(m.notes) && typeof m.notes === 'object' && Object.entries(m.notes).every(([k,v]) => ['prediction','explanation','reflection'].includes(k) && typeof v === 'string'))) && ['checks','criteria'].every(k => !m[k] || (!Array.isArray(m[k]) && typeof m[k] === 'object' && Object.values(m[k]).every(v => typeof v === 'boolean'))) && (!m.answers || (!Array.isArray(m.answers) && typeof m.answers === 'object' && Object.values(m.answers).every(v => typeof v === 'string'))));
  }
  function save() {
    try { if (durable) localStorage.setItem(KEY, JSON.stringify(state)); }
    catch (_) { durable = false; announce('Armazenamento indisponível. Seus textos ficam só nesta sessão; exporte suas respostas na página inicial.'); }
  }
  const root = document.getElementById('course-lesson');
  if (root) {
    const slug = root.dataset.module;
    const m = state.modules[slug] ||= {};
    m.notes ||= {}; m.checks ||= {}; m.criteria ||= {}; m.answers ||= {};
    m.visited = true; state.last = slug; save();
    if (durable) announce(m.completed ? 'Atividade concluída por conferência e autoavaliação. Você pode revisar.' : 'Aula visitada. Respostas e autoavaliação ficam salvas neste navegador.');
    for (const area of root.querySelectorAll('[data-note]')) {
      const key = area.dataset.note; area.value = m.notes[key] || '';
      area.addEventListener('input', () => { m.notes[key] = area.value; m.completed = false; save(); });
    }
    const executed = root.querySelector('[data-note-check]');
    executed.checked = !!m.executed;
    executed.addEventListener('change', () => { m.executed = executed.checked; m.completed = false; save(); });
    for (const checkbox of root.querySelectorAll('[data-criterion]')) {
      const key = checkbox.dataset.criterion; checkbox.checked = !!m.criteria[key];
      checkbox.addEventListener('change', () => { m.criteria[key] = checkbox.checked; m.completed = false; save(); });
    }
    const questions = [...root.querySelectorAll('.question')];
    for (const q of questions) {
      const key = q.dataset.question, input = q.querySelector('input'), feedback = q.querySelector('.answer-feedback');
      input.value = m.answers[key] || '';
      if (m.checks[key]) feedback.textContent = 'Resultado já conferido. ' + feedback.dataset.ok;
      input.addEventListener('input', () => { m.answers[key] = input.value; m.checks[key] = false; m.completed = false; feedback.textContent = ''; save(); });
      q.querySelector('.check-answer').addEventListener('click', () => {
        const raw = input.value.trim().replace(',', '.');
        const value = Number(raw);
        if (!raw || !/^[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(raw) || !Number.isFinite(value)) {
          feedback.textContent = 'Formato: informe somente o resultado numérico. Execute seu código no notebook; não cole código neste campo.'; m.checks[key] = false;
        } else if (Math.abs(value - Number(q.dataset.expected)) > Number(q.dataset.tolerance)) {
          feedback.textContent = 'Cálculo: o resultado ainda não corresponde ao pedido. ' + feedback.dataset.hint; m.checks[key] = false;
        } else { feedback.textContent = 'Resultado conferido. ' + feedback.dataset.ok + ' Agora explique seu procedimento.'; m.checks[key] = true; }
        m.answers[key] = input.value; m.completed = false; save();
      });
    }
    document.getElementById('complete-lesson').addEventListener('click', () => {
      const target = document.getElementById('completion-feedback');
      if (!m.executed) target.textContent = 'Execute as células do notebook e registre essa prática antes de concluir.';
      else if (!questions.every(q => m.checks[q.dataset.question])) target.textContent = 'Confira o resultado das duas questões antes de concluir.';
      else if (!(m.notes.explanation || '').trim() || !(m.notes.reflection || '').trim()) target.textContent = 'Registre o procedimento e sua conclusão. O conteúdo será revisado por você com a rubrica.';
      else if (![...root.querySelectorAll('[data-criterion]')].every(c => c.checked)) target.textContent = 'Revise sua entrega com todos os critérios. Use as pistas para melhorar o que ainda falta.';
      else { m.completed = true; save(); target.textContent = 'Atividade concluída por conferência numérica e autoavaliação. Seu notebook deve ser salvo separadamente. Isso não certifica domínio.'; }
    });
    document.getElementById('redo-lesson').addEventListener('click', () => {
      m.checks = {}; m.criteria = {}; m.executed = false; m.completed = false;
      root.querySelectorAll('input[type=checkbox]').forEach(c => c.checked = false);
      root.querySelectorAll('.answer-feedback').forEach(p => p.textContent = '');
      save(); document.getElementById('completion-feedback').textContent = 'Conferências reiniciadas. Seus textos e resultados foram preservados.';
    });
    for (const button of root.querySelectorAll('.load-video')) button.addEventListener('click', () => {
      const frame = document.createElement('iframe'); frame.title = button.dataset.title;
      frame.src = 'https://www.youtube-nocookie.com/embed/' + button.dataset.video;
      frame.allow = 'encrypted-media; picture-in-picture'; frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      button.parentElement.querySelector('.video-slot').replaceChildren(frame); button.hidden = true;
    });
  }
  const cards = [...document.querySelectorAll('[data-card]')];
  if (cards.length) {
    function render() {
      let visited = 0, complete = 0;
      for (const c of cards) {
        const m = state.modules[c.dataset.card] || {};
        if (m.visited) visited++; if (m.completed) complete++;
        c.querySelector('.module-state').textContent = m.completed ? 'Atividade concluída por autoavaliação' : m.visited ? 'Visitado · atividade pendente' : 'Ainda não visitado';
      }
      document.getElementById('course-progress').textContent = `${visited} de 10 aulas visitadas · ${complete} de 10 atividades concluídas`;
      const resume = document.getElementById('resume-course');
      if (state.last && cards.some(c => c.dataset.card === state.last)) { resume.href = state.last + '.html'; resume.textContent = 'Retomar minha última aula'; }
    }
    render();
    document.getElementById('export-course').addEventListener('click', () => {
      const url = URL.createObjectURL(new Blob([JSON.stringify(state, null, 2)], {type:'application/json'}));
      const a = document.createElement('a'); a.href = url; a.download = 'python-swirl-respostas.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    document.getElementById('import-course').addEventListener('change', async event => {
      const file = event.target.files[0]; if (!file) return;
      if (file.size > 2 * 1024 * 1024) { announce('Arquivo grande demais; limite de importação: 2 MB.'); return; }
      try {
        const incoming = JSON.parse(await file.text());
        if (!validState(incoming) || Object.keys(incoming.modules).some(k => !cards.some(c => c.dataset.card === k))) throw new Error('Arquivo inválido');
        for (const [slug,m] of Object.entries(incoming.modules)) {
          const current = state.modules[slug];
          if (!current) state.modules[slug] = m;
          else {
            const notes = {...(current.notes || {})};
            for (const [key,value] of Object.entries(m.notes || {})) {
              if (!notes[key]) notes[key] = value;
              else if (notes[key] !== value) notes[key] += '\n\n[Texto recuperado da exportação]\n' + value;
            }
            state.modules[slug] = {...current, notes, visited: !!(current.visited || m.visited), completed: false, checks:{}, criteria:{}, executed:false};
          }
        }
        if (cards.some(c => c.dataset.card === incoming.last)) state.last = incoming.last;
        save(); render(); announce(durable ? 'Respostas restauradas. Conflitos preservam textos e pedem nova conferência.' : 'Respostas restauradas somente nesta sessão. Exporte antes de sair.');
      } catch (_) { announce('Não foi possível importar. Use uma exportação JSON válida do Python Swirl. Seus registros atuais foram preservados.'); }
    });
  }
})();
