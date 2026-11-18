lucide.createIcons();

const backToCatalog = document.querySelector('#salirProyeccion');
if (backToCatalog) {
    backToCatalog.addEventListener('click', () => {
        window.location.href = '../book_detail/book_detail.html';
    });
}

const activityForGroup = document.querySelector('#readingSession');
if (activityForGroup) {
    activityForGroup.addEventListener('click', () => {
        window.location.href = '../reading_session/reading_session.html';
    });
}