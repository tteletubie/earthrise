lucide.createIcons();

const backToCatalog = document.querySelector('#botnContainer1');
if (backToCatalog) {
    backToCatalog.addEventListener('click', () => {
        window.location.href = '../teacher_guide/teacher_guide.html';
    });
}