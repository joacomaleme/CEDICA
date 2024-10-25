const form = document.getElementById('search-options');
const checkbox = document.getElementById("cb5");
const from = document.getElementById("from");
const until = document.getElementById("until");

from.addEventListener("change", () => {
    var minDate = new Date("1/1/1000");
    if(new Date(from.value) >= minDate)
        setTimeout(() => {form.submit();}, 1000)
    })
until.addEventListener("change", () => {
    var minDate = new Date("1/1/1000");
    if(new Date(until.value) >= minDate)
        setTimeout(() => {form.submit();}, 1000)
    })

checkbox.addEventListener('change', function(){setTimeout(() => {form.submit();}, 300)});