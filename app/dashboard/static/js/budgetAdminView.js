document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("click", (event) => {
    const button = document.getElementById("closeModalBtn");

    if (button && button.contains(event.target)) {
      const element = event.target;
      const modal =
        element.closest("[modal]") || exit("Error: Modal not found!");

      modal.classList.remove("fade-in-down");
      modal.classList.add("fade-out-up");

      setTimeout(() => {
        document.getElementById("modalContainer").remove();
      }, 300);
    }
  });

  document.addEventListener("input", async (event) => {
    const isRadElement = document.getElementById("is_rad");
    const isRad = isRadElement && isRadElement.value === "y";

    if (event.target.id === "account" && isRad) {
      const element = event.target;
      url = `/dashboard/get-rads?Account=${element.value}`;

      const response = await fetch(url);
      const data = await response.json();

      const optionsSelect = document.getElementById("rad");
      optionsSelect.innerHTML = "";

      if (data && data.length > 0) {
        data.forEach((option) => {
          const newOption = document.createElement("option");
          newOption.value = option;
          newOption.label = option;
          optionsSelect.appendChild(newOption);
        });
        optionsSelect.parentElement.classList.remove("hidden");
      } else {
        optionsSelect.parentElement.classList.add("hidden");
      }
    }
  });

  const fetchData = async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.text();
      appendModalHtml(data);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  document.querySelectorAll("[delete]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("rowId");
      fetchData(`/dashboard/budget-admin-view/delete?id=${id}`);
    });
  });

  document.querySelector("[create]").addEventListener("click", () => {
    fetchData("/dashboard/budget-admin-view/create");
  });

  document.addEventListener("click", async (event) => {
    const button = document.getElementById("createFormSubmitBtn");

    if (button && button.contains(event.target)) {
      event.preventDefault(); // Prevent default form submission

      const form = document.getElementById("createForm");
      const formData = new FormData(form);
      const url = form.action;
      const method = form.method;

      try {
        const response = await fetch(url, {
          method: method,
          body: formData,
        });

        if (response.redirected) {
          // If the server responds with a redirect, navigate to the new URL
          window.location.href = response.url;
        } else if (response.ok) {
          // If the response is OK, render the new form with error messages if needed
          const data = await response.text();
          appendModalHtml(data);
        }
      } catch (error) {
        throw new Error(
          "An error occurred while submitting the form. Please try again."
        );
      }
    }
  });

  // Element Updates for masking
  const elements = $("[masknumber]");

  elements.inputmask({
    alias: "numeric",
    groupSeparator: ",",
    autoGroup: true,
    digits: 3,
    digitsOptional: false,
    clearIncomplete: true,
    placeholder: "0.000",
    showMaskOnHover: false,
    max: 500.0,
    min: 1.0,
    step: 1.001,
    rightAlign: false,
    onblur: function () {
      const value = parseFloat($(this).val().replace(/,/g, ""));
      if (value > 100) {
        $(this).val("500.000");
      }
    },
  });
});

function appendModalHtml(data) {
  document.getElementById("modalContainer")?.remove();

  const contentDiv = document.createElement("div");
  const parser = new DOMParser();
  const doc = parser.parseFromString(data, "text/html");

  // Extract the body content and append it to the container
  const content = document.importNode(doc.body, true);
  contentDiv.appendChild(content);
  contentDiv.id = "modalContainer";

  document.querySelector("body").append(contentDiv);
}

// sortable list
const sortableList = document.getElementById("sortable-list");
let draggedRow = null;

// Enable drag on all table rows
const rows = sortableList.querySelectorAll("tr");
rows.forEach((row) => {
  row.addEventListener("dragstart", function (e) {
    draggedRow = row;
    setTimeout(function () {
      row.style.display = "none"; // Hide the row being dragged
    }, 0);
  });

  row.addEventListener("dragend", function () {
    setTimeout(function () {
      draggedRow.style.display = "table-row"; // Show the row again after drag
      draggedRow = null;
    }, 0);
  });

  row.addEventListener("dragover", function (e) {
    e.preventDefault(); // Allow dropping by preventing the default behavior
  });

  row.addEventListener("dragenter", function (e) {
    e.preventDefault(); // Same as above
    if (row !== draggedRow) {
      row.style.backgroundColor = "#e2e8f0"; // Highlight the row as a drop target
    }
  });

  row.addEventListener("dragleave", function () {
    row.style.backgroundColor = ""; // Reset highlight when the dragged item leaves
  });

  row.addEventListener("drop", function (e) {
    e.preventDefault();
    if (row !== draggedRow) {
      // Get the rows' parent to update the order
      const parent = row.parentNode;
      parent.insertBefore(draggedRow, row.nextSibling || row);

      // Re-select the rows after reordering and update display order
      updateDisplayOrder();
    }
    row.style.backgroundColor = ""; // Reset background color after drop
  });
});

function updateDisplayOrder() {
  const newOrder = Array.from(
    document.querySelectorAll("#sortable-list tr")
  ).map((row, index) => {
    const displayOrderInput = row.querySelector(
      'td input[id*="display_order"]'
    );
    if (displayOrderInput) {
      displayOrderInput.defaultValue = index + 1; // Update the value based on the new order
      displayOrderInput.classList.add("text-emerald-500"); // Show green color temporarily

      // Remove the green color after 300ms
      setTimeout(() => {
        displayOrderInput.classList.remove("text-emerald-500");
      }, 300);
    }
  });
}
