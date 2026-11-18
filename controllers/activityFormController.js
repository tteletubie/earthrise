lucide.createIcons();

const activityForGroup = document.querySelector('#agregarLibro');
if (activityForGroup) {
    activityForGroup.addEventListener('click', () => {
        window.location.href = '../admin/activity_form/activity_form.html';
    });
}
