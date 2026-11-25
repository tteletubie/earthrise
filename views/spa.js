(function () {
  const app = document.getElementById('app');
  const routes = {
    '#home': {
      template: 'home/home.njk',
      loadSharedFonts: true
    },
    '#book': {
      template: 'book_detail/book_detail.njk',
      stylesheet: 'views/book_detail/styles.css',
      controller: 'bookDetail',
      loadSharedFonts: true
    }
  };
  let activeViewStylesheet = null;

  function showLoading() {
    app.textContent = 'Loading...';
  }

  function showError(message) {
    app.textContent = `Error: ${message}`;
  }

  function loadViewStylesheet(stylesheetPath) {
    const stylesheetUrl = stylesheetPath
      ? new URL(stylesheetPath, window.location.href).href
      : null;

    if (activeViewStylesheet?.href === stylesheetUrl) {
      return Promise.resolve();
    }

    activeViewStylesheet?.remove();
    activeViewStylesheet = null;

    if (!stylesheetUrl) {
      return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = stylesheetUrl;
      link.onload = resolve;
      link.onerror = () => reject(new Error(`Stylesheet could not be loaded: ${stylesheetUrl}`));
      document.head.append(link);
      activeViewStylesheet = link;
    });
  }

  function navigate(hash) {
    if (window.location.hash !== hash) {
      window.history.pushState(null, '', hash);
    }
    renderCurrentRoute();
  }

  async function renderCurrentRoute() {
    showLoading();

    let hash = window.location.hash;
    if (!hash) {
      window.history.replaceState(null, '', '#home');
      hash = '#home';
    }

    const route = routes[hash];
    if (!route) {
      showError('Ruta no encontrada.');
      return;
    }

    try {
      await loadViewStylesheet(route.stylesheet);
      if (route.loadSharedFonts) {
        await window.loadFonts();
      }

      const result = await window.api.templates.render(route.template);
      if (!result || result.success !== true) {
        showError(result && result.error ? result.error : 'The view could not be rendered.');
        return;
      }
      app.innerHTML = result.html;
      if (window.lucide) {
        window.lucide.createIcons();
      }
      if (route.template === 'home/home.njk') {
        window.HomeController?.initialize(app, navigate);
      }
      if (route.controller === 'bookDetail') {
        window.BookDetailController?.initialize(app, navigate);
      }
    } catch (error) {
      showError(error && error.message ? error.message : 'The view could not be rendered.');
    }
  }

  window.addEventListener('hashchange', renderCurrentRoute);
  renderCurrentRoute();
})();
