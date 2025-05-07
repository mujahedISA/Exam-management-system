function toggleUpload(button, type, courseId) {
  const card = button.closest('.card');
  const regularUpload = card.querySelector(`#regular-upload-${courseId}`);
  const resitGradesUpload = card.querySelector(`#resit-grades-upload-${courseId}`);
  const resitUpload = card.querySelector(`#resit-upload-${courseId}`);

  regularUpload.style.display = 'none';
  resitGradesUpload.style.display = 'none';
  resitUpload.style.display = 'none';

  if (type === 'resit') {
    resitUpload.style.display = 'block';
  } else if (type === 'resit_grades') {
    resitGradesUpload.style.display = 'block';
  } else if (type === 'regular') {
    regularUpload.style.display = 'block';
  }
}


  
function uploadExcel(courseId, isResit = false) {
    const fileInput = document.getElementById(isResit ? `inputGroupFileResit_${courseId}` : `inputGroupFile04_${courseId}`);
    if (!fileInput.files.length) {
      Swal.fire({
        icon: "warning",
        title: "No file selected",
        text: "Please select an Excel file before uploading.",
      });
      return;
    }
  
    const formData = new FormData();
    formData.append("grade_file", fileInput.files[0]);
    formData.append("upload_type", isResit ? "resit" : "regular"); // 👈 ensure this is added
  
    fetch(`/exams/upload_grades/${courseId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          Swal.fire({
            icon: "success",
            title: "Upload Successful",
            showConfirmButton: false,
            timer: 1500,
          });
          fileInput.value = "";
        } else {
          Swal.fire({
            icon: "error",
            title: "Upload Failed",
            text: data.message,
          });
        }
      })
      .catch((error) => {
        console.error("Upload error:", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "Something went wrong during upload.",
        });
      });
  }

// grades.js

function uploadResitExcel(courseId) {
    const fileInput = document.getElementById(`resitInputFile_${courseId}`);
    if (!fileInput || !fileInput.files.length) {
      Swal.fire({
        icon: "warning",
        title: "No file selected",
        text: "Please select an Excel file before uploading.",
      });
      return;
    }
  
    const formData = new FormData();
    formData.append("grade_file", fileInput.files[0]);
    formData.append("upload_type", "resit");
  
    fetch(`/exams/upload_grades/${courseId}/`, {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          showSuccess("Resit grades uploaded successfully!", "Upload Successful");
          fileInput.value = "";
        } else {
          showError(data.message || "Upload failed.");
        }
      })
      .catch((err) => {
        console.error(err);
        showError("Something went wrong uploading the resit grades.");
      });
  }
  function uploadResitExamDetails(courseId) {
    const form = document.querySelector(`#resit-upload-${courseId} form`);
    const formData = new FormData(form);

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value,
      },
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message || 'Upload completed!');
    })
    .catch(error => {
      console.error('Upload error:', error);
      alert('An error occurred during upload.');
    });
  }  



  
  



