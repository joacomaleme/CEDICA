document.addEventListener("DOMContentLoaded", () => {
  const pageNums = document.querySelectorAll('.pageNum');
  const page = document.getElementById('page');
  const form = document.getElementById("search-options");
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');

  // Cuando clickeo en uno itero por todos y les saco el 'active'
  pageNums.forEach((item) => {
    item.addEventListener('click', () => {
      const parent = this.parentElement;

      if (!parent.classList.contains('active')) {
        pageNums.forEach((el) => {
          el.parentElement.classList.remove('active');
        });
        
        parent.classList.add('active');
        page.value = this.textContent;
        form.submit();
      }
    });
  });
  
  // Resto uno al startPage
  prev.addEventListener('click', () => {
      if (startPage > 1) {
          page.value = startPage - 1;
          form.submit();
      }
  });

  // Sumo uno al startPage
  next.addEventListener('click', () => {
      if (startPage < pages) {
          page.value = startPage + 1;
          form.submit();
      }
  });

  const checkOne = document.getElementById("check-banned");
  const checkTwo = document.getElementById("check-unbanned");

  const atLeastOne = document.getElementById("atLeastOne");

  const dateCheck = document.getElementById("cb5");

  const descending = document.getElementById("descending");

  descending.addEventListener('change', submitForm)
  dateCheck.addEventListener('change', () => setTimeout(() => {submitForm();}, 300))

  checkOne.addEventListener('change', () => {
    checkTwo.checked = false; atLeastOne.checked = checkOne.checked;
  });
  checkTwo.addEventListener('change', () => {
    checkOne.checked = false; atLeastOne.checked = checkTwo.checked;
  });

  checkOne.addEventListener('change', () => setTimeout(() => {submitForm();}, 605));
  checkTwo.addEventListener('change', () => setTimeout(() => {submitForm();}, 605));

  function submitForm() {
      form.submit();
  }
});