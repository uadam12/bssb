const requestIndicator = document.getElementById('request-indicator');
const toastContainer = htmx.find("[data-toast-container]");
const toastTemplate = htmx.find("[data-toast-template]");
const toastOptions = { delay: 2000 }

function createToast(message) {
    // Clone the template
    const element = toastTemplate.cloneNode(true)

    // Remove the data-toast-template attribute
    delete element.dataset.toastTemplate;

    // Set the CSS class
    element.className += " " + message.tags;

    // Set the text
    htmx.find(element, "[data-toast-body]").innerText = message.message;

    // Add the new element to the container
    toastContainer.appendChild(element);

    // Show the toast using Bootstrap's API
    const toast = new bootstrap.Toast(element, toastOptions);
    toast.show();
}

htmx.on("messages", (event) => {
    toastContainer.innerHTML = '';
    event.detail.value.forEach(createToast);
})

document.addEventListener("htmx:beforeRequest", () => {
    requestIndicator.classList.add('show');
});

document.addEventListener("htmx:afterRequest", () => {
    requestIndicator.classList.remove('show');
});