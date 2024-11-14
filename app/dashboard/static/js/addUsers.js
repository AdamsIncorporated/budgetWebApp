function filterTable() {
  // Get the input value and convert it to lower case
  const filter = document.getElementById("filterInput").value.toLowerCase();
  const table = document.getElementById("businessUnitsTable");
  const rows = table.getElementsByTagName("tr");

  // Loop through all table rows (except the first, which is the header)
  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName("td");
    let rowVisible = false;

    // Loop through the cells in the current row
    for (let j = 0; j < cells.length; j++) {
      // Check if the cell contains the filter text
      if (cells[j].textContent.toLowerCase().includes(filter)) {
        rowVisible = true; // Mark the row as visible if a match is found
        break; // Exit the inner loop if a match is found
      }
    }

    // Show or hide the row based on whether it matched the filter
    rows[i].style.display = rowVisible ? "" : "none";
  }
}

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

  document.querySelectorAll("[edit]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("rowId");
      fetchData(`/dashboard/add-users/edit?id=${id}`);
    });
  });

  document.querySelectorAll("[delete]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("rowId");
      fetchData(`/dashboard/add-users/delete?id=${id}`);
    });
  });

  document.querySelector("[create]").addEventListener("click", () => {
    fetchData("/dashboard/add-users/create");
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

  $("#userTable").DataTable({
    paging: true,
    searching: true,
    ordering: true,
    info: true,
    lengthMenu: [5, 10, 15, 25],
    language: {
      search: "Search:",
    },
    search: {
      smart: true,
    },
  });
});
