form = document.getElementById('search-options');
checkbox = document.getElementById("cb5");
date = document.getElementById("from");
date2 = document.getElementById("until");

date.addEventListener("blur", function(){
    if (date.value.length === 10) {
        form.submit();
}})
date2.addEventListener("blur", function(){
    if (date2.value.length === 10) {
        form.submit();
}});
checkbox.addEventListener('change', function(){setTimeout(() => {form.submit();}, 300)});