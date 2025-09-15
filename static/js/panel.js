document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('fluxo-rows');
  if (!container) {
    console.warn('fluxo script: #fluxo-rows não encontrado — não executando JS de edição.');
    return;
  }

  const emptyTemplate = container.querySelector('#empty-form-row');
  const totalFormsInput = document.getElementById('id_fluxo-TOTAL_FORMS');

  if (!emptyTemplate || !totalFormsInput) {
    console.warn('fluxo script: elementos não encontrados', { container, emptyTemplate, totalFormsInput });
    return;
  }

  // Delegação de eventos: um handler para + e -
  container.addEventListener('click', function (e) {
    const addBtn = e.target.closest('.add-row');
    const remBtn = e.target.closest('.remove-row');

    if (addBtn) {
      e.preventDefault();
      const row = addBtn.closest('.fluxo-row');
      const produto = row.dataset.produto || (row.querySelector('.produto-name') && row.querySelector('.produto-name').textContent.trim());
      addRowAfter(row, produto || '');
      return;
    }

    if (remBtn) {
      e.preventDefault();
      const row = remBtn.closest('.fluxo-row');
      removeRow(row);
      return;
    }
  });

  function addRowAfter(row, produto) {
    const newIndex = parseInt(totalFormsInput.value, 10);
    const clone = emptyTemplate.cloneNode(true);

    clone.removeAttribute('id');
    clone.style.display = '';
    clone.dataset.produto = produto;

    // mostra o nome do produto na célula visível
    const prodCell = clone.querySelector('.produto-name');
    if (prodCell) prodCell.textContent = produto;

    // ajusta names/ids: substitui __prefix__ pelo índice (formset empty_form usa __prefix__)
    clone.querySelectorAll('input, select, textarea').forEach(el => {
      if (el.name) el.name = el.name.replace(/__prefix__|fluxo-\d+-/g, `fluxo-${newIndex}-`);
      if (el.id) el.id = el.id.replace(/__prefix__|fluxo-\d+-/g, `fluxo-${newIndex}-`);
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') el.value = '';
      if (el.tagName === 'SELECT') el.selectedIndex = 0;
    });

    // garante que o field nome_produto hidden receba o produto
    const nomeField = clone.querySelector('[name$="-nome_produto"]');
    if (nomeField) nomeField.value = produto;

    // insere depois da linha clicada (se for o template vazio e não houver linhas, coloca antes do template)
    row.insertAdjacentElement('afterend', clone);

    totalFormsInput.value = newIndex + 1;
    updateRowIndexes();
    refreshButtonsVisibility();
  }

  function removeRow(row) {
    // não remove o template escondido
    if (!row || row.id === 'empty-form-row') return;

    // se só houver 1 linha real, em vez de remover podemos apenas limpar valores (opcional)
    const realRows = getRealRows();
    if (realRows.length <= 1) {
      // limpa campos da única linha
      row.querySelectorAll('input, select, textarea').forEach(el => {
        if (el.tagName === 'SELECT') el.selectedIndex = 0;
        else el.value = '';
      });
      // e atualiza (não diminui TOTAL_FORMS)
      updateRowIndexes();
      refreshButtonsVisibility();
      return;
    }

    row.remove();
    updateRowIndexes();
    refreshButtonsVisibility();
  }

  function getRealRows() {
    return Array.from(container.querySelectorAll('.fluxo-row')).filter(r => r.id !== 'empty-form-row');
  }

  function updateRowIndexes() {
    const rows = getRealRows();
    rows.forEach((r, idx) => {
      r.querySelectorAll('input, select, textarea').forEach(el => {
        if (el.name) el.name = el.name.replace(/fluxo-\d+-/, `fluxo-${idx}-`);
        if (el.id) el.id = el.id.replace(/fluxo-\d+-/, `fluxo-${idx}-`);
      });
    });
    totalFormsInput.value = rows.length;
  }

  // mostra o + em todas as linhas e o - somente se houver >1 linha
  function refreshButtonsVisibility() {
    const rows = getRealRows();

    // agrupa linhas por produto
    const grupos = {};
    rows.forEach(r => {
      const produto = r.dataset.produto || (r.querySelector('.produto-name') && r.querySelector('.produto-name').textContent.trim());
      if (!grupos[produto]) grupos[produto] = [];
      grupos[produto].push(r);
    });

    // percorre cada grupo e decide botões
    Object.values(grupos).forEach(grupo => {
      grupo.forEach((r, idx) => {
        const addBtn = r.querySelector('.add-row');
        const remBtn = r.querySelector('.remove-row');
        if (addBtn) addBtn.style.display = ''; // sempre mostra +
        if (remBtn) {
          // só mostra - se esse produto tiver mais de uma linha
          remBtn.style.display = (grupo.length > 1) ? '' : 'none';
        }
      });
    });
  }

  // validação antes do submit (soma <=100 e sem destinos duplicados)
  const form = container.closest('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      const rows = getRealRows();
      const map = {};
      const errors = [];

      rows.forEach(r => {
        const produto = r.dataset.produto || (r.querySelector('.produto-name') && r.querySelector('.produto-name').textContent.trim());
        const destinoEl = r.querySelector('[name*="destino"]');
        const porcentagemEl = r.querySelector('[name*="porcentagem"]');

        const destino = destinoEl ? destinoEl.value : '';
        const porcentagem = porcentagemEl && porcentagemEl.value ? parseFloat(porcentagemEl.value) : 0;

        if (!map[produto]) map[produto] = { total: 0, destinos: {} };

        if (destino) {
          if (map[produto].destinos[destino]) {
            map[produto].hasDuplicate = true;
            map[produto].duplicateDestino = destino;
          } else {
            map[produto].destinos[destino] = true;
          }
        }
        map[produto].total += (porcentagem || 0);
      });

      Object.keys(map).forEach(prod => {
        if (map[prod].hasDuplicate) errors.push(`Destino duplicado para ${prod}: ${map[prod].duplicateDestino}`);
        if (map[prod].total > 100.0001) errors.push(`Soma das porcentagens para ${prod} é maior que 100% (${map[prod].total.toFixed(2)}%)`);
      });

      if (errors.length) {
        e.preventDefault();
        alert(errors.join('\n'));
        return false;
      }
    });
  }

  // inicializa visibilidade correta dos botões
  refreshButtonsVisibility();
});