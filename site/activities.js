/* MIT: lógica original. Conteúdo pedagógico original: CC BY 4.0. */
(function () {
  'use strict';
  const mean = values => values.reduce((a, b) => a + b, 0) / values.length;
  const median = values => { const s = [...values].sort((a, b) => a - b); const m = Math.floor(s.length / 2); return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
  const amplitude = values => Math.max(...values) - Math.min(...values);
  const number = text => /^[-+]?\d+(?:[.,]\d+)?$/.test(text.trim()) ? Number(text.trim().replace(',', '.')) : NaN;
  const tasks = {
    media: {expected:28, prediction:'0', next:'A média considera todos os valores. O atraso eleva a média para 28; a mediana continua em 14 minutos.', summary:'Primeiro grupo: média 28, mediana 14. Novo grupo: média 40, mediana 24. A mediana pode resumir o centro; a média também informa totais. Um valor extremo deve ser investigado, não apagado automaticamente.'},
    dispersao: {expected:7, prediction:'1', next:'A amplitude da turma B é 10 − 3 = 7 pontos; na A, 8 − 6 = 2. Ambas têm média 7. Isso não explica causas.', summary:'Médias iguais não garantem distribuições iguais. Amplitudes: A = 2 e B = 7 pontos. Desvios populacionais: aproximadamente 0,63 e 2,76 pontos. No novo caso, a unidade é minuto. Os dados não permitem atribuir causas ao professor.'},
    amostragem: {expected:55.4, prediction:'1', next:'A soma é 277 e há cinco pessoas: 277 / 5 = 55,4 minutos. O segundo sorteio tem média 46,6; a população simulada tem média 59,5.', summary:'Estimativas 55,4 e 46,6 variam porque os sorteios incluem pessoas diferentes. A população simulada tem média 59,5. Selecionar apenas tempos baixos produz viés neste exemplo; aumentar essa seleção não resolve automaticamente o problema. Dados simulados não descrevem uma escola real.'}
  };
  const api = {mean, median, amplitude, number, tasks};
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document === 'undefined') return;
  document.addEventListener('DOMContentLoaded', () => {
    const activity = document.getElementById('activity');
    if (!activity) return;
    const kind = activity.dataset.kind, task = tasks[kind];
    const el = id => document.getElementById(id);
    let stage = 0, attempts = [], prediction = '';
    const labels = ['Preveja', 'Tente e interprete', 'Explore', 'Transfira', 'Revise'];
    const display = value => new Intl.NumberFormat('pt-BR', {maximumFractionDigits:2}).format(value);
    function show(n) {
      stage = n;
      activity.querySelectorAll('[data-stage]').forEach(section => { section.hidden = Number(section.dataset.stage) !== n; });
      el('progress').textContent = `Etapa ${n + 1} de 5 · ${labels[n]}`;
      const heading = activity.querySelector(`[data-stage="${n}"] h2`);
      heading.tabIndex = -1;
      heading.focus();
    }
    el('predict').addEventListener('click', () => {
      if (!el('prediction').value) { el('prediction').focus(); return; }
      prediction = el('prediction').selectedOptions[0].textContent;
      show(1);
    });
    el('hint').addEventListener('click', () => { el('hint-text').hidden = false; el('feedback').textContent = el('hint-text').textContent; });
    el('attempt').addEventListener('submit', event => {
      event.preventDefault();
      const value = number(el('answer').value);
      if (!Number.isFinite(value)) { el('feedback').textContent = 'Digite um único número, por exemplo 12 ou 12,5. Não copie código Python neste campo.'; el('answer').focus(); return; }
      const correct = Math.abs(value - task.expected) < 1e-7;
      attempts.push({value, correct});
      el('feedback').textContent = (correct ? 'Resultado conferido. ' : 'Ainda não corresponde ao cálculo pedido. Confira a operação e tente novamente. ') + task.next;
      el('to-explore').hidden = !correct;
    });
    function dots(data, label) {
      const counts = {};
      const circles = data.map(value => { const row = counts[value] || 0; counts[value] = row + 1; return `<circle cx="${35 + 50 * value}" cy="${110 - 17 * row}" r="6" fill="#174b78"/>`; }).join('');
      const ticks = [0,2,4,6,8,10].map(value => `<text x="${35 + 50 * value}" y="148" text-anchor="middle">${value}</text>`).join('');
      return `<svg viewBox="0 0 580 170" role="img" aria-label="${label}: ${data.join(', ')}; eixo de notas de zero a dez"><text x="20" y="24">${label}</text><line x1="35" x2="535" y1="130" y2="130" stroke="black"/>${circles}${ticks}</svg>`;
    }
    function explore() {
      const v = Number(el('variation').value);
      if (kind === 'media') {
        const values = [10,12,14,16,v];
        el('exploration').textContent = `Último tempo: ${v} minutos. Dados: ${values.join(', ')}. Média: ${display(mean(values))}; mediana: ${display(median(values))}. Compare o centro e o efeito do último valor.`;
      } else if (kind === 'dispersao') {
        const a = [6,7,7,7,8], b = [3,5,7,v,v];
        el('exploration').textContent = `Maior nota B: ${v}. A: média ${display(mean(a))}, amplitude ${amplitude(a)}; B: média ${display(mean(b))}, amplitude ${amplitude(b)}. Agora as médias podem deixar de ser iguais. Mesma escala de 0 a 10 nos dois gráficos.`;
        el('chart').innerHTML = dots(a, 'Turma A') + dots(b, 'Turma B');
      } else {
        const values = Array.from({length:v}, (_, i) => i + 10);
        el('exploration').textContent = `Conveniência: primeiras ${v} pessoas, com valores de 10 a ${9+v}. Média ${display(mean(values))}; população inteira: 59,5. Selecionar mais pessoas somente nesse início ainda exclui tempos altos. Isso é viés de seleção, diferente da variabilidade entre sorteios aleatórios.`;
      }
    }
    el('to-explore').addEventListener('click', () => { show(2); explore(); });
    el('variation').addEventListener('input', explore);
    el('to-transfer').addEventListener('click', () => show(3));
    el('check-transfer').addEventListener('click', () => {
      if (!el('transfer').value) { el('transfer').focus(); return; }
      const correct = el('transfer').value === '0';
      el('transfer-feedback').textContent = correct ? 'Interpretação coerente com este caso. Explique agora com suas palavras e cite um limite.' : 'Reveja os dados e o contexto: uma medida não estabelece causas nem remove viés automaticamente. Tente outra interpretação.';
      el('to-review').hidden = !correct;
    });
    el('to-review').addEventListener('click', () => {
      el('summary').textContent = `Sua previsão: ${prediction}. ${task.summary} Compare isso com sua explicação. A reflexão não recebe avaliação automática.`;
      show(4);
    });
    el('review').addEventListener('click', () => {
      el('summary').textContent = `Sua previsão: ${prediction}. Suas tentativas: ${attempts.map(a => `${display(a.value)} (${a.correct ? 'resultado conferido' : 'a revisar'})`).join('; ')}. ${task.summary} Sua reflexão permanece no campo acima para revisão.`;
    });
    el('restart').addEventListener('click', () => {
      if (!window.confirm('Refazer apaga as respostas desta atividade na página. Deseja continuar?')) return;
      attempts = []; prediction = '';
      ['answer','prediction','transfer','reflection'].forEach(id => { el(id).value = ''; });
      ['feedback','transfer-feedback','summary'].forEach(id => { el(id).textContent = ''; });
      ['to-explore','to-review','hint-text'].forEach(id => { el(id).hidden = true; });
      el('variation').value = el('variation').defaultValue;
      show(0);
    });
  });
}());
