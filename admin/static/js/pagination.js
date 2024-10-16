$(document).ready(function() {
    var pageNum = $('.pageNum');
    var page = document.getElementById('page');
    var form = document.getElementById("search-options");
    var prev = document.getElementById('prev');
    var next = document.getElementById('next');

    pageNum.click(function() {
        if(!$(this).parent().hasClass('active')) {
            pageNum.parent().removeClass('active');
            $(this).parent().addClass('active');
            page.value = this.textContent;
            form.submit();
        }
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