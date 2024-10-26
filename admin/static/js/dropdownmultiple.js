window.onload = function () {
  crear_multi_select();
};

function isMobileDevice() {
  return (
    typeof window.orientation !== "undefined" ||
    navigator.userAgent.indexOf("IEMobile") !== -1
  );
}

var li_multi = new Array();
function crear_multi_select() {
  var div_cont_multi_select = document.querySelectorAll(
    "[data-multi-select='active']"
  );
  var select_multi = "";
  for (var e = 0; e < div_cont_multi_select.length; e++) {
    div_cont_multi_select[e].setAttribute("data-indx-multi-select", e);
    div_cont_multi_select[e].setAttribute("data-multi-selec-open", "false");
    var ul_cont = document.querySelectorAll(
      "[data-indx-multi-select='" + e + "'] > .cont_list_multi_select > ul"
    );
    select_multi = document.querySelectorAll(
      "[data-indx-multi-select='" + e + "'] > select"
    )[0];
    if (isMobileDevice()) {
      select_multi.addEventListener("change", function () {
        _select_multi_option(select_multi.selectedIndex, e);
      });
    }
    var select_options_multi = select_multi.options;
    document
      .querySelectorAll(
        "[data-indx-multi-select='" + e + "']  > .multi_selecionado_opcion "
      )[0]
      .setAttribute("data-multi-n-select", e);
    document
      .querySelectorAll(
        "[data-indx-multi-select='" + e + "']  > .multi_icon_select "
      )[0]
      .setAttribute("data-multi-n-select", e);
    for (var i = 0; i < select_options_multi.length; i++) {
      li_multi[i] = document.createElement("li");
      if (
        select_options_multi[i].selected == true ||
        select_multi.value == select_options_multi[i].innerHTML
      ) {
        li_multi[i].className = "multi_active";
        document.querySelector(
          "[data-indx-multi-select='" + e + "']  > .multi_selecionado_opcion "
        ).innerHTML = select_options_multi[i].innerHTML;
      }
      li_multi[i].setAttribute("data-index", i);
      li_multi[i].setAttribute("data-multi-selec-index", e);
      li_multi[i].addEventListener("click", function () {
        _select_multi_option(
          this.getAttribute("data-index"),
          this.getAttribute("data-multi-selec-index")
        );
      });

      li_multi[i].innerHTML = select_options_multi[i].innerHTML;
      ul_cont[0].appendChild(li_multi[i]);
    }
  }
}

var cont_multi_slc = 0;
function open_multi_select(idx) {
  var idx1 = idx.getAttribute("data-multi-n-select");
  var ul_cont_li = document.querySelectorAll(
    "[data-indx-multi-select='" + idx1 + "'] .cont_multi_select_int > li"
  );
  var hg = 0;
  var multi_selec_open = document
    .querySelectorAll("[data-indx-multi-select='" + idx1 + "']")[0]
    .getAttribute("data-multi-selec-open");
  var multi_slect_element_open = document.querySelectorAll(
    "[data-indx-multi-select='" + idx1 + "'] select"
  )[0];
  if (isMobileDevice()) {
    if (window.document.createEvent) {
      var evt = window.document.createEvent("MouseEvents");
      evt.initMouseEvent(
        "mousedown", false, true,
        window, 0, 0, 0, 0, 0, false, false, false, false, 0, null
      );
      multi_slect_element_open.dispatchEvent(evt);
    } else if (multi_slect_element_open.fireEvent) {
      multi_slect_element_open.fireEvent("onmousedown");
    } else {
      multi_slect_element_open.click();
    }
  } else {
    for (var i = 0; i < ul_cont_li.length; i++) {
      hg += ul_cont_li[i].offsetHeight;
    }
    if (multi_selec_open == "false") {
      document
        .querySelectorAll("[data-indx-multi-select='" + idx1 + "']")[0]
        .setAttribute("data-multi-selec-open", "true");
      document.querySelectorAll(
        "[data-indx-multi-select='" + idx1 + "'] > .cont_list_multi_select > ul"
      )[0].style.height = hg + "px";
      document.querySelectorAll(
        "[data-indx-multi-select='" + idx1 + "'] > .multi_icon_select"
      )[0].style.transform = "rotate(180deg)";
    } else {
      document
        .querySelectorAll("[data-indx-multi-select='" + idx1 + "']")[0]
        .setAttribute("data-multi-selec-open", "false");
      document.querySelectorAll(
        "[data-indx-multi-select='" + idx1 + "'] > .multi_icon_select"
      )[0].style.transform = "rotate(0deg)";
      document.querySelectorAll(
        "[data-indx-multi-select='" + idx1 + "'] > .cont_list_multi_select > ul"
      )[0].style.height = "0px";
    }
  }
}

function salir_multi_select(indx) {
  var select_multi = document.querySelectorAll(
    "[data-indx-multi-select='" + indx + "'] > select"
  )[0];
  document.querySelectorAll(
    "[data-indx-multi-select='" + indx + "'] > .cont_list_multi_select > ul"
  )[0].style.height = "0px";
  document.querySelector(
    "[data-indx-multi-select='" + indx + "'] > .multi_icon_select"
  ).style.transform = "rotate(0deg)";
  document
    .querySelectorAll("[data-indx-multi-select='" + indx + "']")[0]
    .setAttribute("data-multi-selec-open", "false");
}

function _select_multi_option(indx, selc) {
  var select_multi = document.querySelectorAll(
    "[data-indx-multi-select='" + selc + "'] > select"
  )[0];
  var li_multi_s = document.querySelectorAll(
    "[data-indx-multi-select='" + selc + "'] .cont_multi_select_int > li"
  );
  var selected_text = document.querySelectorAll(
    "[data-indx-multi-select='" + selc + "'] > .multi_selecionado_opcion"
  )[0];
  
  li_multi_s[indx].classList.toggle("multi_active");
  var selected_items = [];
  var select_options_multi = document.querySelectorAll(
    "[data-indx-multi-select='" + selc + "'] > select > option"
  );
  
  for (var i = 0; i < li_multi_s.length; i++) {
    if (li_multi_s[i].classList.contains("multi_active")) {
      selected_items.push(li_multi_s[i].innerHTML);
      select_options_multi[i].selected = true;
    } else {
      select_options_multi[i].selected = false;
    }
  }
  
  selected_text.innerHTML = selected_items.length
    ? selected_items.join(", ")
    : "Selecciona una opción";
}

