// Parte del cambiar a documentos
const subtitleGeneral = document.querySelector("#subtitle-general");
const subtitleDocuments = document.querySelector("#subtitle-documents");

const formGeneral = document.querySelector("#form-general");
const formDocuments = document.querySelector("#form-documents");

const documentTable = document.querySelector("#document-table");
const filesInput = document.querySelector("#files-input");
const files = document.querySelector("#files");
const uploadForm = document.querySelector("#upload-form");

// Si la tabla no tiene display none, entonces le agrego los event listeners
if (!documentTable.classList.contains("display-none")) applyEventListeners();

subtitleGeneral.addEventListener("click", (e) => {
  const clases = e.target.classList;

  if (!clases.contains("selected")) {
    subtitleDocuments.classList.remove("selected");
    subtitleGeneral.classList.add("selected");

    formDocuments.classList.add("display-none");
    documentTable.classList.add("display-none");
    filesInput.classList.add("display-none");
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
    filesInput.classList.remove("display-none");
    formGeneral.classList.add("display-none");
    applyEventListeners();
  }
});

files.addEventListener("change", () => uploadForm.submit());

function applyEventListeners() {
  // Get modal and cancel button
  const documentModal = document.getElementById("document-modal");
  const documentCancelBtn = document.getElementById("document-cancel-btn");

  // Attach event listeners to all delete buttons
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
  });

  // Close modal on cancel
  documentCancelBtn.addEventListener("click", function () {
    documentModal.close();
  });
}