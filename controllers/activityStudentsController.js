lucide.createIcons();

const activityForGroup = document.querySelector('#detailView');
if (activityForGroup) {
    activityForGroup.addEventListener('click', () => {
        window.location.href = '../projection/projection.html';
    });
}
