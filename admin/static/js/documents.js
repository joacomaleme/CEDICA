// Parte del cambiar a documentos
const subtitleGeneral = document.querySelector("#subtitle-general");
const subtitleDocuments = document.querySelector("#subtitle-documents");

const formGeneral = document.querySelector("#form-general");
const formDocuments = document.querySelector("#search-options");

const documentTable = document.querySelector("#document-table");
const filesContainer = document.querySelector("#files-container");
const files = document.querySelector("#files");
const uploadForm = document.querySelector("#upload-form");

const pageSection = document.querySelector("#page-section");

// Si la tabla no tiene display none, entonces le agrego los event listeners
if (!documentTable.classList.contains("display-none")) applyEventListeners();

subtitleGeneral.addEventListener("click", (e) => {
  const clases = e.target.classList;

  if (!clases.contains("selected")) {
    subtitleDocuments.classList.remove("selected");
    subtitleGeneral.classList.add("selected");

    formDocuments.classList.add("display-none");
    documentTable.classList.add("display-none");
    filesContainer.classList.add("display-none");
    if (pageSection) pageSection.classList.add("display-none");
    formGeneral.classList.remove("display-none");
  }
});

subtitleDocuments.addEventListener("click", (e) => {
  const clases = e.target.classList;

  if (!clases.contains("selected")) {
    subtitleGeneral.classList.remove("selected");
    subtitleDocuments.classList.add("selected");

    formDocuments.classList.remove("display-none");
    documentTable.classList.remove("display-none");
    filesContainer.classList.remove("display-none");
    if (pageSection) pageSection.classList.remove("display-none");
    formGeneral.classList.add("display-none");
    applyEventListeners();
  }
});

files.addEventListener("change", () => uploadForm.submit());

function applyEventListeners() {
  // Get modal and cancel button
  const documentModal = document.getElementById("document-modal");
  const documentCancelBtn = document.getElementById("document-cancel-btn");

  const deleteButtons = document.querySelectorAll(".delete-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();

      // Get document ID from data attribute
      const documentId = button.getAttribute("data-document-id");

      // Update form action with document ID
      const documnetDelForm = document.getElementById("documnetDelForm");
      documnetDelForm.action = `/document/destroy/${documentId}`; // or use url_for in templates if needed

      // Show the modal
      documentModal.showModal();
    });

    // Close modal on cancel
    documentCancelBtn.addEventListener("click", function () {
      documentModal.close();
    });
  });

  const linkBtn = document.getElementById("link-btn");
  const linkModal = document.getElementById("link-modal");
  const linkCancelBtn = document.getElementById("link-cancel-btn");

  if (linkBtn) {
    linkBtn.addEventListener("click", (event) => {
      event.preventDefault();
      linkModal.showModal();
    });
  
    linkCancelBtn.addEventListener("click", () => {
      linkModal.close();
    })
  }

  const ascending = document.getElementById("ascending");
  const sortAttr = document.getElementById("sortAttr");

  ascending.addEventListener('change', submitForm);
  sortAttr.addEventListener('change', submitForm);

  function submitForm(event) {
    event.preventDefault();
    formDocuments.submit();
  }
}