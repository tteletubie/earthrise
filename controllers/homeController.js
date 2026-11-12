lucide.createIcons();

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
