$(document).ready(function () {
  const $body = $("body"),
    $sidebar = $(".sidebar"),
    $toggle = $(".toggle"),
    $modeSwitch = $(".toggle-switch"),
    $modeText = $(".mode-text");

  // --------- SIDEBAR --------- //
  const savedSidebar = localStorage.getItem("sidebarState");
  if (savedSidebar === "open") {
    $sidebar.removeClass("close");
  } else {
    $sidebar.addClass("close");
  }

  $(window).on("load", function () {
    $("html").addClass("ready");
  });

  $toggle.on("click", () => {
    $sidebar.toggleClass("close");
    localStorage.setItem(
      "sidebarState",
      $sidebar.hasClass("close") ? "close" : "open"
    );
  });

  // --------- DARK/LIGHT MODE TOGGLE --------- //
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    $body.addClass("dark");
    $modeText.text("Dark Mode");
  } else {
    $modeText.text("Light Mode"); // default
  }

  // Dark/Light toggle
  $modeSwitch.on("click", () => {
    $body.toggleClass("dark");
    if ($body.hasClass("dark")) {
      $modeText.text("Dark Mode");
      localStorage.setItem("theme", "dark");
    } else {
      $modeText.text("Light Mode");
      localStorage.setItem("theme", "light");
    }
  });

  // --------- DATA TABLE INITIALIZATION --------- //
  var table = $("#myDataTable").DataTable({
    columnDefs: [
      { orderable: false, targets: -1 }, // disable sorting on last column
    ],
    rowCallback: function (row, data, index) {
      if ($(row).hasClass("placeholder-row")) {
        $(row).addClass("dtr-disabled"); // optional styling
        $(row).attr("data-search", "false"); // ignore search
        $(row).attr("data-order", "false"); // ignore sort
      }
    },
    drawCallback: function (settings) {
      // Always move placeholder-row back to the top after sorting or searching
      var placeholder = $(".placeholder-row").detach();
      $("#myDataTable tbody").prepend(placeholder);
    },
    infoCallback: function (settings, start, end, max, total, pre) {
      // Count only real rows
      var realRows = $(settings.nTBody).find("tr:not(.placeholder-row)").length;

      if (realRows === 0) {
        start = 0;
        end = 0;
      } else {
        start = 1; // first real row
        end = realRows; // last real row
      }

      return "Showing " + start + " to " + end + " of " + realRows + " entries";
    },
  });

  $(".progress-circle").each(function () {
    let $circle = $(this);
    let value = $circle.data("value"); // percentage
    let $progress = $circle.find(".progress");
    let $number = $circle.find(".progress-number");

    let radius = 52;
    let circumference = 2 * Math.PI * radius;

    // start at 0
    $progress.css("stroke-dasharray", circumference);
    $progress.css("stroke-dashoffset", circumference);

    // animate stroke
    $({ percent: 0 }).animate(
      { percent: value },
      {
        duration: 1500,
        step: function (now) {
          let offset = circumference - (now / 100) * circumference;
          $progress.css("stroke-dashoffset", offset);
          $number.text(Math.floor(now) + "%");
        },
      }
    );
  });

  // --------- INPUT RESTRICTIONS --------- //
  $("#collegeName, #editCollegeName, #programName, #editProgramName").on(
    "input",
    function () {
      this.value = this.value.replace(/[^a-zA-Z\s,]/g, "");
    }
  );

  $("#collegeCode, #editCollegeCode, #programCode, #editProgramCode").on(
    "input",
    function () {
      this.value = this.value.replace(/[^A-Za-z]/g, "");
    }
  );

  $("#addStudentID, #editStudentID").on("input", function () {
    let cleaned = $(this)
      .val()
      .replace(/[^0-9\-]/g, "");
    $(this).val(cleaned);
  });

  $("#firstName, #lastName, #gender").on("input", function () {
    let cleaned = $(this)
      .val()
      .replace(/[^a-zA-Z\s]/g, "");
    $(this).val(cleaned);
  });

  // --------- COLLEGE MODALS --------- //
  // Add College Popup
  $("#addCollegeForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#addCodeError").text("");
    $("#addNameError").text("");
    $("#collegeCode, #collegeName").removeClass("is-invalid");

    $.ajax({
      url: $(this).attr("action"),
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          $("#addCollege").modal("hide");
          $("#addConfirmation").modal("show");
          $("#addCollegeForm")[0].reset();

          $("#addConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (msg.includes("code")) {
          $("#addCodeError").text(response.message);
          $("#collegeCode").addClass("is-invalid");
        } else if (msg.includes("name")) {
          $("#addNameError").text(response.message);
          $("#collegeName").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#addCollege").on("hidden.bs.modal", function () {
    $("#addCollegeForm")[0].reset(); // clear inputs
    $("#collegeCode, #collegeName").removeClass("is-invalid");
    $("#addCodeError").text("");
    $("#addNameError").text("");
  });

  //Edit College Popup
  $("#editCollege").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var collegeCode = button.data("collegeCode");
    var collegeName = button.data("collegeName");

    modal.find("#editCollegeCode").val(collegeCode);
    modal.find("#editCollegeName").val(collegeName);
    modal.find("#originalCode").val(collegeCode);
  });

  // Edit College jQuery
  $("#editCollegeForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#editCodeError").text("");
    $("#editNameError").text("");
    $("#editCollegeCode, #editCollegeName").removeClass("is-invalid");

    $.ajax({
      url: "/colleges/edit", // Your Flask route for editing
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success === true) {
          $("#editCollege").modal("hide");
          $("#editConfirmation").modal("show");
          $("#editCollegeForm")[0].reset();

          $("#editConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
        } else if (response.no_change) {
          $("#editCollege").modal("hide");
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (response?.field === "code" || msg.includes("code")) {
          $("#editCodeError").text(response.message);
          $("#editCollegeCode").addClass("is-invalid");
        } else if (response?.field === "name" || msg.includes("name")) {
          $("#editNameError").text(response.message);
          $("#editCollegeName").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#editCollege").on("hidden.bs.modal", function () {
    $("#editCollegeForm")[0].reset(); // clear inputs
    $("#editCollegeCode, #editCollegeName").removeClass("is-invalid");
    $("#editCodeError").text("");
    $("#editNameError").text("");
  });

  // Delete Popup
  // When opening the delete modal, set the college code
  $("#collegeDeletionModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var code = button.data("college-code"); // Extract code from data attribute
    $(this).find("#deleteCode").val(code); // Set value in hidden input
  });

  $("#deleteCollegeForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
      url: "/colleges/delete",
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          // Hide delete confirmation prompt modal
          $("#collegeDeletionModal").modal("hide");

          // Show success message modal
          $("#deleteConfirmationModal").modal("show");

          // Reload after success modal closes
          $("#deleteConfirmationModal").on("hidden.bs.modal", function () {
            location.reload();
          });
        } else {
          // If the backend returns an error message (like non-existent code)
          alert(response.message || "Failed to delete college.");
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        alert(response?.message || "An error occurred while deleting.");
      },
    });
  });

  // --------- PROGRAM MODALS --------- //
  //Add Program Popup
  $("#addProgramForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#addProgramCodeError").text("");
    $("#addProgramNameError").text("");
    $("#programCode, #programName").removeClass("is-invalid");

    $.ajax({
      url: $(this).attr("action"),
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          $("#addProgram").modal("hide");
          $("#addConfirmation").modal("show");
          $("#addProgramForm")[0].reset();

          $("#addConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (msg.includes("code")) {
          $("#addProgramCodeError").text(response.message);
          $("#programCode").addClass("is-invalid");
        } else if (msg.includes("name")) {
          $("#addProgramNameError").text(response.message);
          $("#programName").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#addProgram").on("hidden.bs.modal", function () {
    $("#addProgramForm")[0].reset(); // clear inputs
    $("#programCode, #programName").removeClass("is-invalid");
    $("#addProgramCodeError").text("");
    $("#addProgramNameError").text("");
  });

  //Edit Program Popup
  $("#editProgram").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var programCode = button.data("programCode");
    var programName = button.data("programName");
    var collegeCode = button.data("collegeCode");

    modal.find("#editProgramCode").val(programCode);
    modal.find("#editProgramName").val(programName);
    modal.find("#collegeCode").val(collegeCode);
    modal.find("#originalCode").val(programCode);
  });

  // Edit Confirmation Popup
  $("#editProgramForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#editProgramCodeError").text("");
    $("#editProgramNameError").text("");
    $("#editProgramCode, #editProgramName").removeClass("is-invalid");

    $.ajax({
      url: "/programs/edit",
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success == true) {
          $("#editProgram").modal("hide");
          $("#editConfirmation").modal("show");
          $("#editProgramForm")[0].reset();

          $("#editConfirmation").on("hidden.bs.modal", function () {
            location.reload(); // reload table to show changes
          });
        } else if (response.no_change) {
          $("#editProgram").modal("hide");
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (response?.field === "code" || msg.includes("code")) {
          $("#editProgramCodeError").text(response.message);
          $("#editProgramCode").addClass("is-invalid");
        } else if (response?.field === "name" || msg.includes("name")) {
          $("#editProgramNameError").text(response.message);
          $("#editProgramName").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#editProgram").on("hidden.bs.modal", function () {
    $("#editProgramForm")[0].reset(); // clear inputs
    $("#editProgramCode, #editProgramName").removeClass("is-invalid");
    $("#editProgramCodeError").text("");
    $("#editProgramNameError").text("");
  });

  // Delete Program Popup
  $("#programDeletionModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var code = button.data("program-code"); // Extract code from data attribute
    $(this).find("#deleteCode").val(code); // Set value in hidden input
  });

  $("#deleteProgramForm").submit(function (e) {
    e.preventDefault();

    $.ajax({
      url: "/programs/delete",
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          $("#programDeletionModal").modal("hide"); // hide the confirm modal

          $("#deleteConfirmationModal").modal("show"); // show "College Deleted" modal

          // optional: reload table or page when deletion modal closes
          $("#deleteConfirmationModal").on("hidden.bs.modal", function () {
            location.reload();
          });
        } else {
          alert(response.message || "Failed to delete program.");
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        alert(response?.message || "An error occurred while deleting.");
      },
    });
  });

  // --------- STUDENT MODALS --------- //
  function previewAddPhoto(event) {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert("File size must be less than 5MB");
        event.target.value = "";
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        $("#addPhotoPreview")
          .attr("src", e.target.result)
          .css("display", "inline-block");
        $("#addPhotoPlaceholder").css("display", "none");
      };
      reader.readAsDataURL(file);
    }
  }

  function previewEditPhoto(event) {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert("File size must be less than 5MB");
        event.target.value = "";
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        $("#editPhotoPreview")
          .attr("src", e.target.result)
          .css("display", "inline-block");
        $("#editPhotoPlaceholder").css("display", "none");
      };
      reader.readAsDataURL(file);
    }
    $("#removePhoto").val("false");
  }

  function removeEditPhoto() {
    $("#editPhotoPreview").css("display", "none");
    $("#editPhotoPlaceholder").css("display", "inline-flex");
    $("#editStudentPhoto").val("");
    $("#removePhoto").val("true");
  }
  // Add Student Modal
  $(document).ready(function () {
    $("#addStudentPhoto").on("change", previewAddPhoto);
    $("#editStudentPhoto").on("change", previewEditPhoto);
    $("#removePhotoBtn").on("click", removeEditPhoto);
  });

  $("#addStudentForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#addStudentIDError").text("");
    $("#addStudentID").removeClass("is-invalid");

    var formData = new FormData(this);

    $.ajax({
      url: $(this).attr("action"),
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.success) {
          $("#addStudent").modal("hide");
          $("#addConfirmation").modal("show");
          $("#addStudentForm")[0].reset();

          // Reset photo preview
          $("#addPhotoPreview").css("display", "none").attr("src", "");
          $("#addPhotoPlaceholder").css("display", "inline-flex");

          $("#addConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (msg.includes("id")) {
          $("#addStudentIDError").text(response.message);
          $("#addStudentID").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#addStudent").on("hidden.bs.modal", function () {
    $("#addStudentForm")[0].reset();
    $("#addStudentID").removeClass("is-invalid");
    $("#addStudentIDError").text("");

    // Reset photo preview
    $("#addPhotoPreview").css("display", "none").attr("src", "");
    $("#addPhotoPlaceholder").css("display", "inline-flex");
  });

  // Edit Student Modal
  $("#editStudent").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var studentID = button.data("student-id");
    var firstName = button.data("first-name");
    var lastName = button.data("last-name");
    var programCode = button.data("program-code");
    var yearLevel = button.data("year-level");
    var gender = button.data("gender");
    var photo = button.data("photo");

    modal.find("#editStudentID").val(studentID);
    modal.find("#firstName").val(firstName);
    modal.find("#lastName").val(lastName);
    modal.find("#programCode").val(programCode);
    modal.find("#yearLevel").val(yearLevel);
    modal.find("#gender").val(gender);
    modal.find("#original_id").val(studentID);
    modal.find("#current_photo").val(photo || "");
    modal.find("#removePhoto").val("false");

    // Handle photo preview
    if (photo && photo !== "None" && photo !== "" && photo !== "null") {
      $("#editPhotoPreview").attr("src", photo).css("display", "inline-block");
      $("#editPhotoPlaceholder").css("display", "none");
    } else {
      $("#editPhotoPreview").css("display", "none");
      $("#editPhotoPlaceholder").css("display", "inline-flex");
    }
  });

  // Edit Student Form Submit with File Upload
  $("#editStudentForm").submit(function (e) {
    e.preventDefault();

    // Clear previous errors
    $("#editStudentIDError").text("");
    $("#editStudentID").removeClass("is-invalid");

    // Create FormData to handle file upload
    var formData = new FormData(this);

    $.ajax({
      url: "/students/edit",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        if (response.success == true) {
          $("#editStudent").modal("hide");
          $("#editConfirmation").modal("show");
          $("#editStudentForm")[0].reset();

          $("#editConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
        } else if (response.no_change) {
          $("#editStudent").modal("hide");
        }
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const msg = response?.message?.toLowerCase() || "Something went wrong.";

        if (response?.field === "id" || msg.includes("id")) {
          $("#editStudentIDError").text(response.message);
          $("#editStudentID").addClass("is-invalid");
        } else {
          alert(response?.message || "An unexpected error occurred.");
        }
      },
    });
  });

  $("#editStudent").on("hidden.bs.modal", function () {
    $("#editStudentForm")[0].reset();
    $("#editStudentID").removeClass("is-invalid");
    $("#editStudentIDError").text("");

    // Reset photo preview
    $("#editPhotoPreview").css("display", "none").attr("src", "");
    $("#editPhotoPlaceholder").css("display", "none");
  });

  // Delete Student Modal
  $("#studentDeletionModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var id = button.data("student-id");
    $(this).find("#deleteStudentID").val(id);
  });

  $("#deleteStudentForm").submit(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/students/delete",
      type: "POST",
      data: $(this).serialize(),
      success: function (response) {
        if (response.success) {
          $("#studentDeletionModal").modal("hide");
          $("#deleteConfirmationModal").modal("show");

          $("#deleteConfirmationModal").on("hidden.bs.modal", function () {
            location.reload();
          });
        } else {
          alert(response.message || "Failed to delete student record.");
        }
      },
    });
  });

  // --------- STUDENT PROFILE CARD --------- //
  let hoverDisplayDelay = null;

  $(".student-row").on("mouseenter", function (e) {
    const $row = $(this);
    const $card = $row.find(".student-profile-card");

    // Clear any existing timer
    clearTimeout(hoverDisplayDelay);

    // Set a timer to show the card after 0.75 seconds
    hoverDisplayDelay = setTimeout(function () {
      const viewportHeight = window.innerHeight;
      const viewportWidth = window.innerWidth;

      const cardWidth = 400;
      const cardHeight = 250;
      const spacing = 15;

      // Use mouse position from the event
      let cardLeft = e.pageX + spacing;
      let cardTop = e.pageY - cardHeight / 2;

      // If card would go off right edge, show on left of cursor
      if (cardLeft + cardWidth > viewportWidth) {
        cardLeft = e.pageX - cardWidth - spacing;
      }

      // If card would go off left edge
      if (cardLeft < 20) {
        cardLeft = 20;
      }

      // If card would go off bottom
      if (cardTop + cardHeight > viewportHeight - 20) {
        cardTop = viewportHeight - cardHeight - 20;
      }

      // If card would go off top
      if (cardTop < 20) {
        cardTop = 20;
      }

      // Position the card
      $card.css({
        left: cardLeft + "px",
        top: cardTop + "px",
        transform: "none",
      });

      $card.addClass("show-card");
    }, 750);
  });

  $(".student-row").on("mouseleave", function () {
    const $card = $(this).find(".student-profile-card");

    // Clear the timer if user leaves before delay completes
    clearTimeout(hoverDisplayDelay);

    // Hide the card immediately
    $card.removeClass("show-card");
  });
});
