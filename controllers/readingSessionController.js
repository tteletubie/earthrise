lucide.createIcons();

const backToBook = document.querySelector('#backToBook');
if (backToBook) {
    backToBook.addEventListener('click', () => {
        window.location.href = '../book_detail/book_detail.html';
    });
}

const finishActivity = document.querySelector('#finishActivity');
const returnToBook = () => {
    window.location.href = '../book_detail/book_detail.html';
};

finishActivity?.addEventListener('click', returnToBook);
finishActivity?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        returnToBook();
    }
});

const projectActivity = document.querySelector('#projectActivity');
const openStudentActivity = () => {
    window.location.href = '../activity_students/activity_students.html';
};

projectActivity?.addEventListener('click', openStudentActivity);
projectActivity?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openStudentActivity();
    }
});
