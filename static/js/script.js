// mudar página
document.addEventListener('DOMContentLoaded', function () {
  const cardsList = document.querySelectorAll('.cards-list');

  cardsList.forEach(card => {
    const id = card.dataset.id
    card.addEventListener('mouseup', () => {
      window.location.replace(`/${id}/perfil/`);
    });
  });
});

// mostrar e remover blocos de informação ocultos
function toggleBlocks() {
  const blocks = document.querySelectorAll('.hidden-block, .block-info.no-hidden');
  const seeMore = document.getElementById('see-more');

  const isHidden = blocks[0].classList.contains('hidden-block');

  blocks.forEach(block => {
    if (isHidden) {
      block.classList.remove('hidden-block');
      block.classList.add('block-info', 'no-hidden');
    } else {
      block.classList.remove('block-info', 'no-hidden');
      block.classList.add('hidden-block');
    }
  });

  seeMore.textContent = isHidden ? 'Ver menos' : 'Ver mais';
};

// mostrar o block data
document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.family-card.trigger');
  const target = document.getElementById('target');

  cards.forEach(card => {
    card.addEventListener('mouseup', () => {
      const dataInic = card.dataset.dataInic;
      const contato = card.dataset.contato;
      const id = card.dataset.id

      target.style.display = 'block';
      //resta saber se usar aquele href ali é correto
      target.innerHTML = `
        <div class='block-data'>
          <div class='block-data-head'>
            <h3>Detalhes da Família</h3>
            <a class='profile-access' href="${id}/perfil/"> 
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-in-left" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M10 3.5a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-2a.5.5 0 0 1 1 0v2A1.5 1.5 0 0 1 9.5 14h-8A1.5 1.5 0 0 1 0 12.5v-9A1.5 1.5 0 0 1 1.5 2h8A1.5 1.5 0 0 1 11 3.5v2a.5.5 0 0 1-1 0z"/>
                <path fill-rule="evenodd" d="M4.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H14.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708z"/>
              </svg>
            </a>
          </div>
          <h6>Início da Transição: </h6>
          <p>${dataInic}</p>
          <h6>Número para Contato</h6>
          <p>${contato}</p>
        </div>
        <div class='block-data'>
          <h3>Subsistemas - Cultivos</h3>
        </div>
      `;
      window.scrollTo({
        top: document.body.scrollHeight - 1030,
        behavior: 'smooth'
      });
    });
  });
});

// cor da tag de nível
document.addEventListener('DOMContentLoaded', function () {
  const tag = document.querySelectorAll('.tag-transition-level');
  tag.forEach(element => {
    const level = element.textContent.trim();
    switch (level) {
      case 'Avançado':
        element.style.backgroundColor = '#02a708ff';
        break;
      case 'Intermediário':
        element.style.backgroundColor = '#50db54ff';
        break;
      case 'Inicial':
        element.style.backgroundColor = '#8dd38fff';
        break;
    }
  });
});

// blocos do fluxograma
jsPlumb.ready(function() {
  jsPlumb.setContainer("sandbox");

  const blocks = ["block1", "block2", "block3", "block4"];

  const endpointOptions = {
    endpoint: "Dot",
    paintStyle: { fill: "transparent", radius: 6 },
    hoverPaintStyle: { fill: "#51d360", stroke: "transparent" },
    isSource: true,
    maxConnections: 10,
    connector: ["Bezier", { curviness: 80 }],
    connectorStyle: { stroke: "#51d360", strokeWidth: 3 },
    connectorOverlays: [
      ["Arrow", { width: 12, length: 12, location: 1 }],
      ["Label", { label: "produto", location: 0.5, id: "produto" }]
    ]
  };

  const anchors = ["Top", "Bottom", "Left", "Right"];

  blocks.forEach(function(block) {
    anchors.forEach(function(anchor) {
      jsPlumb.addEndpoint(block, {
        ...endpointOptions,
        anchor: anchor,
        isTarget: true
      });
    });

    jsPlumb.makeTarget(block, {
      anchor: "Continuous",
      allowLoopback: false,
      endpoint: "Blank",
      dropOptions: { hoverClass: "dropHover" }
    });
  });

  jsPlumb.bind("beforeDrop", function(info) {
      if (info.sourceId === info.targetId) {
        return false;
      }
      return true;
  });
});

// painel de controle, clique dos blocos e o cursor
document.addEventListener('DOMContentLoaded', () => {
  const subsystemBlocks = document.querySelectorAll('.subsystem-block');
  const overlay = document.getElementById('overlay');
  const panel = document.getElementById('panel');

  subsystemBlocks.forEach(block => {
    block.addEventListener('mouseenter', () => {
      block.style.cursor = 'pointer';
    });

    block.addEventListener('mouseup', () => {
      overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    });

    block.addEventListener('mouseleave', () => {
      block.style.cursor = '';
    });
  });

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  panel.addEventListener('click', (event) => {
    event.stopPropagation();
  });
});

//calendário de agendamento de visitas
document.addEventListener('DOMContentLoaded', function () {
  const Draggable = FullCalendar.Draggable;

  new Draggable(document.getElementById('external-events'), {
    itemSelector: '.external-event',
    eventData: function (eventEl) {
      return {
        title: eventEl.innerText.trim(),
      };
    }
  });

  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      right: 'prev,next today',
      left: 'title',
    },
    editable: true,
    droppable: true,
    timeZone: 'local',

    events: '/api/events/',
    
    eventClick: function(info) {
      if (confirm("Deseja deletar este evento?")) {
        fetch(`/api/events/delete/${info.event.id}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
          }
        }).then(response => {
          if (response.ok) {
            info.event.remove();
          } else {
            alert('Erro ao deletar evento');
          }
        });
      }
    },

    drop: function (info) {
      const dateStr = info.date.toISOString();
      
      fetch('/api/events/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({
          title: info.draggedEl.innerText,
          start: dateStr
        })
      }).then(response => response.json())
        .then(data => {
          if (data.status === 'ok') {
            calendar.refetchEvents();
          }
      });
    }
  });

  calendar.render();
});