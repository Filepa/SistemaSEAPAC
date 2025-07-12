function redirect(url) {
  window.location.href = url;
}

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