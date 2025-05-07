// scripts.js
// Function to get the value of a cookie by name
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if this cookie string starts with the name we want
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Define the global CSRF token variable
const csrftoken = getCookie("csrftoken");


// SweetAlert error popup
function showError(message = "Something went wrong") {
  Swal.fire({
    icon: "error",
    title: "Error",
    text: message,
  });
}

// SweetAlert success popup (optional helper)
function showSuccess(message = "Success", title = "Success") {
  Swal.fire({
    icon: "success",
    title: title,
    text: message,
    timer: 1500,
    showConfirmButton: false,
  });
}

