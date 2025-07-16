// mudar página a partir da div
function redirect(url) {
  window.location.href = url;
}

// mostrar e esconder o block data
document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('.family-card.trigger');
  const target = document.getElementById('target');

  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      target.style.display = 'block';
    });
    card.addEventListener('mouseleave', () => {
      target.style.display = 'none';
    });
  });
});

//blocos do fluxograma
jsPlumb.ready(function() {
  jsPlumb.setContainer("sandbox");

  const blocks = ["block1", "block2", "block3", "block4"];
  jsPlumb.draggable(blocks.slice(1), { containment: "parent" });

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

//painel de controle, arrasto e clique dos blocos e o cursor
document.addEventListener('DOMContentLoaded', () => {
  const subsystemBlocks = document.querySelectorAll('.subsystem-block');
  const overlay = document.getElementById('overlay');
  const panel = document.getElementById('panel');

  let isDragging = false;
  let startX, startY;
  const DRAG_THRESHOLD = 3;

  subsystemBlocks.forEach(block => {
    block.addEventListener('mouseenter', () => {
      block.style.cursor = 'grab';
    });

    block.addEventListener('mousedown', (e) => {
      startX = e.clientX;
      startY = e.clientY;
      isDragging = false;
      block.style.cursor = 'grabbing';
    });

    block.addEventListener('mousemove', (e) => {
      if (e.buttons === 1) { 
        const dx = Math.abs(e.clientX - startX);
        const dy = Math.abs(e.clientY - startY);
        if (dx > DRAG_THRESHOLD || dy > DRAG_THRESHOLD) {
            isDragging = true;
        }
      }
    });

    block.addEventListener('mouseup', (e) => {
      block.style.cursor = 'grab';
      if (!isDragging) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
      isDragging = false;
    });

    block.addEventListener('mouseleave', () => {
      block.style.cursor = '';
    });

    block.addEventListener('dragstart', (e) => {
      e.preventDefault();
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