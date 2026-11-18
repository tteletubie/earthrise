lucide.createIcons();

const backToCatalog = document.querySelector('#volverAlCatlogo');
if (backToCatalog) {
  backToCatalog.addEventListener('click', () => {
    window.location.href = '../home/home.html';
  });
}

const projectForGroup = document.querySelector('#proyectarGrupo');
if (projectForGroup) {
  projectForGroup.addEventListener('click', () => {
    window.location.href = '../projection/projection.html';
  });
}

const activityForGroup = document.querySelector('#activitySession');
if (activityForGroup) {
  activityForGroup.addEventListener('click', () => {
    window.location.href = '../activity_students/activity_students.html';
  });
}
