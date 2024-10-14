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

  const ascending = document.getElementById("ascending");
  const sortAttr = document.getElementById("sortAttr");

  ascending.addEventListener('change', submitForm)
  sortAttr.addEventListener('change', submitForm)

  function submitForm() {
      form.submit();
  }
});