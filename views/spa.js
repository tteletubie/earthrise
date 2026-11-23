(function () {
  const app = document.getElementById('app');
  const routes = {
    '#home': 'pages/home.njk'
  };

  function showLoading() {
    app.textContent = 'Loading...';
  }

  function showError(message) {
    app.textContent = `Error: ${message}`;
  }

  async function renderCurrentRoute() {
    showLoading();

    let hash = window.location.hash;
    if (!hash) {
      window.history.replaceState(null, '', '#home');
      hash = '#home';
    }

    const templateName = routes[hash];
    if (!templateName) {
      showError('Ruta no encontrada.');
      return;
    }

    try {
      const result = await window.api.templates.render(templateName);
      if (!result || result.success !== true) {
        showError(result && result.error ? result.error : 'The view could not be rendered.');
        return;
      }
      app.innerHTML = result.html;
    } catch (error) {
      showError(error && error.message ? error.message : 'The view could not be rendered.');
    }
  }

  window.addEventListener('hashchange', renderCurrentRoute);
  renderCurrentRoute();
})();
