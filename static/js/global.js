
function postAnnouncement() {
    const title = document.getElementById("announcementTitle").value;
    const text = document.getElementById("announcementText").value;

    const formData = new FormData();
    formData.append("title", title);
    formData.append("text", text);

    fetch("/courses/post_announcement/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Server error: " + res.status);
        }
        return res.json();
    })
    .then(data => {
        if (data.status === "success") {
            alert("Announcement posted!");
            document.getElementById("announcementTitle").value = "";
            document.getElementById("announcementText").value = "";
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(error => {
        alert("Something went wrong: " + error.message);
    });
}

document.querySelector(".publish").addEventListener("click", postAnnouncement);


function uploadFile() {
    const fileInput = document.getElementById('scheduleFile');
    const filePreview = document.getElementById('filePreview');
    const confirmationMsg = document.getElementById('confirmationMsg');
    const file = fileInput.files[0];
  
    if (!file) {
      confirmationMsg.innerHTML = '<span style="color: red;">Please select a file to upload.</span>';
      return;
    }
  
    filePreview.textContent = `Selected file: ${file.name}`;
    confirmationMsg.textContent = 'Uploading...';
  
    const formData = new FormData();
    formData.append('excel_file', file);
  
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const uploadUrl = document.querySelector('main').dataset.uploadUrl;
  
    fetch(uploadUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        confirmationMsg.innerHTML = '<span style="color: green;">File uploaded and processed successfully!</span>';
        fileInput.value = '';
        filePreview.textContent = '';
      } else {
        confirmationMsg.innerHTML = `<span style="color: red;">Error: ${data.message}</span>`;
      }
    })
    .catch(err => {
      confirmationMsg.innerHTML = `<span style="color: red;">Upload failed. Please try again.</span>`;
    });
  }

  

function deleteStudent(studentId, button) {
    console.log("Deleting student ID:", studentId);
  
    if (!confirm('Are you sure you want to delete this student?')) return;
  
    const formData = new FormData();
    formData.append("id", studentId);
  
    fetch('/exams/delete_grade/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken   // 👈 ADD this line
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        button.closest('tr').remove();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error deleting student:', error);
      alert('Something went wrong.');
    });
  }
 
   
 
  function resetAllStudentsTable() {
    document.getElementById("allStudentsCourseSelect").value = "";
    const rows = document.querySelectorAll("#allStudentsTable tbody tr");
    rows.forEach(row => row.style.display = "");
  }
