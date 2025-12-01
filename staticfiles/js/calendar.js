document.addEventListener('DOMContentLoaded', function() {
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
      const escolha = prompt(
        "Escolha uma ação para este evento:\n" +
        "1 - Confirmar visita\n" +
        "2 - Deletar visita\n" +
        "3 - Cancelar"
      );

  if (escolha === '1') {
    fetch(`/api/events/confirm/${info.event.id}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',
      },
    }).then(response => response.json())
      .then(data => {
        if (data.status === 'ok') {
          info.event.setProp('backgroundColor', '#4CAF50');
          alert('Visita confirmada!');
        } else {
          alert('Erro ao confirmar visita.');
        }
      });

  } else if (escolha === '2') {
    if (confirm("Tem certeza que deseja deletar esta visita?")) {
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
          alert('Erro ao deletar visita.');
        }
      });
    }

    } else {
      alert("Ação cancelada.");
    }
  },

    eventReceive: function(info) {
      // ✅ Remove o evento temporário criado pelo FullCalendar
      info.event.remove();

      fetch('/api/events/create/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({
          title: info.event.title,
          start: info.event.start.toISOString()
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'ok') {
          calendar.refetchEvents(); // agora vem só do banco
        } else {
          alert(data.message);
        }
      });
    }
  });

  calendar.render();
});