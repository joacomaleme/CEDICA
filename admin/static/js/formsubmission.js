const form = document.getElementById('search-options');
const checkbox = document.getElementById("cb5");
const from = document.getElementById("from");
const until = document.getElementById("until");

from.addEventListener("change", () => form.submit())
until.addEventListener("change", () => form.submit())

checkbox.addEventListener('change', function(){setTimeout(() => {form.submit();}, 300)});