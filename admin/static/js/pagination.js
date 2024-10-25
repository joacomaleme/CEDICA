document.addEventListener('DOMContentLoaded', function() {
  var pageNum = document.querySelectorAll('.pageNum');
  var page = document.getElementById('page');
  var form = document.getElementById("search-options");
  var prev = document.getElementById('prev');
  var next = document.getElementById('next');

  if (!pageNum || !page || !form || !prev || !next) return;

  pageNum.forEach(function(item) {
      item.addEventListener('click', function() {
          if (!item.parentElement.classList.contains('active')) {
              pageNum.forEach(function(elem) {
                  elem.parentElement.classList.remove('active');
              });
              item.parentElement.classList.add('active');
              page.value = item.textContent;
              form.submit();
          }
      });
  });

  prev.addEventListener('click', function() {
      var currentPage = startPage;
      if (currentPage > 1) {
          page.value = currentPage - 1;
          form.submit();
      }
  });

  next.addEventListener('click', function() {
      var currentPage = startPage;
      var totalPages = pages;
      if (currentPage < totalPages) {
          page.value = currentPage + 1;
          form.submit();
      }
  });
});
