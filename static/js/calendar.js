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
      if (confirm("Marcar esta visita como realizada?")) {
        fetch(`/api/events/confirm/${info.event.id}/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': '{{ csrf_token }}',
          },
        }).then(response => response.json())
          .then(data => {
            if (data.status === 'ok') {
              info.event.setProp('backgroundColor', '#4CAF50');
            } else {
              alert('Erro ao confirmar evento');
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