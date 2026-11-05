const message = document.querySelector('#message');
const changeMessageButton = document.querySelector('#change-message');

changeMessageButton.addEventListener('click', () => {
  message.textContent =
    message.textContent === window.appModel.message
      ? window.appModel.alternateMessage
      : window.appModel.message;
});
