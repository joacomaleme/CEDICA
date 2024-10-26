document.addEventListener('DOMContentLoaded', function() {
  const closeButtons = document.querySelectorAll('.close');

  closeButtons.forEach(button => {
      button.addEventListener('click', function() {
          const messageElement = this.parentElement;

          messageElement.classList.add('fade-out');

          messageElement.addEventListener('transitionend', function() {
              messageElement.style.display = 'none';
          }, { once: true });
      });
  });
});