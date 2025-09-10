// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
  initializeCounterAnimations();
  calendar()
});

function redirect(url) {
  window.location.href = url;
}

// Counter animation for stats
function initializeCounterAnimations() {
  document.querySelectorAll('.stat-value').forEach(element => {
    const target = parseInt(element.textContent, 10);
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 16);
  });
}

function addRow() {
  
}

// blocos do fluxograma
jsPlumb.ready(function() {
    jsPlumb.setContainer("sandbox");

    const sandbox = document.getElementById('sandbox');
    const blocks = document.querySelectorAll('.subsystem-block');

    const subsystemIdMap = {};
    blocks.forEach(block => {
        const blockName = block.getAttribute('data-name');
        const blockId = block.id;
        if (blockName && blockId) {
            subsystemIdMap[blockName.trim().toLowerCase()] = blockId;
        }
    });

    let familyData = { subsistemas: [] };
    const subsystemsDataAttr = sandbox.getAttribute('data-subsystems');
    if (subsystemsDataAttr) {
        try {
            familyData.subsistemas = JSON.parse(subsystemsDataAttr);
        } catch (e) {
            console.error("Erro ao analisar dados JSON de subsistemas:", e);
        }
    }

    familyData.subsistemas.forEach(function(subsystem) {
        const sourceBlockId = subsystemIdMap[subsystem.nome_subsistema.trim().toLowerCase()];

        if (!sourceBlockId) {
            console.error("ID de origem não encontrado para:", subsystem.nome_subsistema);
            return;
        }

        subsystem.produtos_saida.forEach(function(produto) {
            if (produto.fluxos && produto.fluxos.length > 0) {
                produto.fluxos.forEach(function(fluxo) {
                    if (fluxo.destino) {
                        const targetBlockId = subsystemIdMap[fluxo.destino.trim().toLowerCase()];

                        if (targetBlockId) {
                            const strokeWidth = fluxo.porcentagem ? (parseFloat(fluxo.porcentagem) / 10) + 1 : 1; 

                            jsPlumb.connect({
                                source: sourceBlockId,
                                target: targetBlockId,
                                anchors: ["AutoDefault", "AutoDefault"], 
                                connector: ["Bezier", { curviness: 80 }],
                                endpoint: "Blank", 
                                paintStyle: { stroke: "#51d360", strokeWidth: strokeWidth },
                                cssClass: "flow-connection", 
                                connectorOverlays: [
                                    ["Arrow", { width: 12, length: 12, location: 1 }],
                                    ["Label", { label: produto.nome, location: 0.5, id: "label" }]
                                ]
                            });
                        }
                    }
                });
            }
        });
    });
});

//calendário de agendamento de visitas
function calendar() {
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
};