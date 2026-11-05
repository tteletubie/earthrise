lucide.createIcons();

document.querySelectorAll('.botn').forEach((bookButton) => {
  bookButton.addEventListener('click', () => {
    window.location.href = '../book_detail/book_detail.html';
  });
});
