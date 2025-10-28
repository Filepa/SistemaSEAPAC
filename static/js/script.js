function redirect(url) {
  window.location.href = url;
}

document.addEventListener('DOMContentLoaded', function() {
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
});

document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById('mobileMenuToggle');
  const sidebar = document.getElementById('sidebar');

  if (toggleButton && sidebar) {
      // Abre/fecha a sidebar ao clicar no botão
      toggleButton.addEventListener('click', function(e) {
          e.stopPropagation(); // evita conflito com o clique fora
          sidebar.classList.toggle('open');
      });

      // Fecha a sidebar se clicar fora dela
      document.addEventListener('click', function(e) {
          if (
              sidebar.classList.contains('open') &&
              !sidebar.contains(e.target) &&
              !toggleButton.contains(e.target)
          ) {
              sidebar.classList.remove('open');
          }
      });
  }
});