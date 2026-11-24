(function () {
  function initialize(app, navigate) {
    const backToCatalog = app.querySelector('#volverAlCatlogo');
    backToCatalog?.addEventListener('click', () => navigate('#home'));

    const projectForGroup = app.querySelector('#proyectarGrupo');
    projectForGroup?.addEventListener('click', () => {
      window.location.href = 'views/projection/projection.html';
    });

    const activityForGroup = app.querySelector('#activitySession');
    activityForGroup?.addEventListener('click', () => {
      window.location.href = 'views/activity_students/activity_students.html';
    });
  }

  window.BookDetailController = { initialize };
})();
