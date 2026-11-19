lucide.createIcons();

const adminBooksLink = document.querySelector('.icono-maestro:not(.cap-home)');
const openBooksAdmin = () => {
  const isAdminHome = window.location.pathname.includes('/views/admin/home/');
  window.location.href = isAdminHome
    ? '../books_admin/books_admin.html'
    : '../admin/home/home.html';
};

const teacherHomeLink = document.querySelector('.cap-home');
const openTeacherHome = () => {
  window.location.href = '../../home/home.html';
};

adminBooksLink?.addEventListener('click', openBooksAdmin);
adminBooksLink?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openBooksAdmin();
  }
});

teacherHomeLink?.addEventListener('click', openTeacherHome);
teacherHomeLink?.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openTeacherHome();
  }
});

document.querySelectorAll('.botn').forEach((bookButton) => {
  bookButton.addEventListener('click', () => {
    window.location.href = '../book_detail/book_detail.html';
  });
});

const profileDialog = document.querySelector('.registro-del-maestro');
const closeProfileDialog = () => {
  profileDialog?.remove();
  document.body.style.overflow = '';
};

profileDialog?.querySelector('.cancelar')?.addEventListener('click', closeProfileDialog);
const saveProfileButton = profileDialog?.querySelector('.guardar-y-continuar');
saveProfileButton?.addEventListener('click', async () => {
  const nombre = profileDialog.querySelector('[name="nombre"]')?.value.trim();
  const apellido = profileDialog.querySelector('[name="apellido"]')?.value.trim();
  const id_grado = Number(profileDialog.querySelector('[name="grado"]')?.value);

  if (!nombre || !apellido || !id_grado) {
    return;
  }

  if (!window.api?.usuario) {
    console.error('La API de usuario no está disponible.');
    return;
  }

  saveProfileButton.disabled = true;
  const result = await window.api.usuario.create({
    nombre,
    apellido_paterno: apellido,
    id_grado
  });
  saveProfileButton.disabled = false;

  if (!result.success) {
    console.error(result.error);
    return;
  }

  closeProfileDialog();
});
profileDialog?.addEventListener('click', (event) => {
  if (event.target === profileDialog) {
    closeProfileDialog();
  }
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeProfileDialog();
  }
});



