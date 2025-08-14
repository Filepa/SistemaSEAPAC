function redirect(url) {
  window.location.href = url;
}
// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeCounterAnimations();
    
});

function showProfile(id) {
  const overlay = document.getElementById('overlay');
  const panel = document.getElementById('panel');

  overlay.classList.add('active');
  document.body.style.overflow = 'hidden';

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      overlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  panel.addEventListener('click', (event) => {
    event.stopPropagation();
  });
};

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

// Add CSS for family score and no families state
const additionalStyles = `
    .family-score {
        margin-bottom: var(--space-4);
    }
    
    .score-label {
        font-size: var(--font-size-sm);
        color: var(--gray-600);
        margin-bottom: var(--space-2);
        font-weight: 500;
    }
    
    .score-value {
        font-size: var(--font-size-lg);
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: var(--space-2);
    }
    
    .score-bar {
        height: 8px;
        background-color: var(--gray-200);
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: var(--space-2);
    }
    
    .score-progress {
        height: 100%;
        background: linear-gradient(90deg, var(--accent-green), var(--light-green));
        transition: width 0.8s ease-in-out;
        border-radius: 4px;
    }
    
    .no-families {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: var(--space-16);
        text-align: center;
        color: var(--gray-500);
    }
    
    .no-families i {
        font-size: var(--font-size-4xl);
        margin-bottom: var(--space-4);
        color: var(--gray-400);
    }
    
    .no-families h3 {
        font-size: var(--font-size-xl);
        font-weight: 600;
        color: var(--gray-600);
        margin-bottom: var(--space-2);
    }
    
    .no-families p {
        color: var(--gray-500);
    }
`;

// Add the additional styles to the page
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// blocos do fluxograma
jsPlumb.ready(function() {
  jsPlumb.setContainer("sandbox");

  const blocks = ["block1", "block2", "block3", "block4", "block5", 
                  "block6", "block7", "block8", "block9", "block10", 
                  "block11", "block12", "block13", "block14", "block15", 
                  "block16", "block17", "block18", "block19", "block20"
  ];

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