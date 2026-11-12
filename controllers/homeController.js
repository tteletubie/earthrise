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
profileDialog?.querySelector('.guardar-y-continuar')?.addEventListener('click', closeProfileDialog);
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
