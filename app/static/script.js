
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

  // --------- DATA TABLE --------- //
  // Disable sorting in "Action" column
  // $("table").each(function () {
  //   var actionsIndex = $(this).find("thead th")
  //     .filter(function () { return $(this).text().trim() === "Action"; })
  //     .index();


  //   $(this).DataTable({
  //     columnDefs: [
  //       { orderable: false, targets: actionsIndex } // disable sorting
  //     ]
  //   });
  // });


  var table = $('#myDataTable').DataTable({
    columnDefs: [
      { orderable: false, targets: -1 } // disable sorting on last column
    ],
    "rowCallback": function (row, data, index) {
      if ($(row).hasClass('placeholder-row')) {
        $(row).addClass('dtr-disabled'); // optional styling
        $(row).attr('data-search', 'false'); // ignore search
        $(row).attr('data-order', 'false');  // ignore sort
      }
    },
    "drawCallback": function (settings) {
      // Always move placeholder-row back to the top after sorting or searching
      var placeholder = $('.placeholder-row').detach();
      $('#myDataTable tbody').prepend(placeholder);
    },
    "infoCallback": function (settings, start, end, max, total, pre) {
      // Count only real rows
      var realRows = $(settings.nTBody).find('tr:not(.placeholder-row)').length;

      if (realRows === 0) {
        start = 0;
        end = 0;
      } else {
        start = 1;          // first real row
        end = realRows;     // last real row
      }

      return 'Showing ' + start + ' to ' + end + ' of ' + realRows + ' entries';
    }
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
    $({ percent: 0 }).animate({ percent: value }, {
      duration: 1500,
      step: function (now) {
        let offset = circumference - (now / 100) * circumference;
        $progress.css("stroke-dashoffset", offset);
        $number.text(Math.floor(now) + "%");
      }
    });
  });

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


  //Edit College Popup
  $('#editCollege').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var collegeCode = button.data('collegeCode');
    var collegeName = button.data('collegeName');

    modal.find('#editCollegeCode').val(collegeCode);
    modal.find('#editCollegeName').val(collegeName);
    modal.find('#originalCode').val(collegeCode);
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
        if (response.success) {
          $("#editCollege").modal("hide");
          $("#editConfirmation").modal("show");
          $("#editCollegeForm")[0].reset();

          $("#editConfirmation").on("hidden.bs.modal", function () {
            location.reload();
          });
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
  $('#collegeDeletionModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var code = button.data('college-code'); // Extract code from data attribute
    $(this).find('#deleteCode').val(code); // Set value in hidden input
  });

  $('#deleteCollegeForm').submit(function (e) {
  e.preventDefault();

  $.ajax({
    url: "/colleges/delete",
    type: "POST",
    data: $(this).serialize(),
    success: function (response) {
      if (response.success) {
        // Hide delete confirmation prompt modal
        $('#collegeDeletionModal').modal('hide');

        // Show success message modal
        $('#deleteConfirmationModal').modal('show');

        // Reload after success modal closes
        $('#deleteConfirmationModal').on('hidden.bs.modal', function () {
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
    }
  });
});


  // --------- PROGRAM SCREEN --------- //
  //Add Program Popup
  $("#addProgramForm").submit(function (e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
      if (response.success) {
        $("#addProgram").modal("hide");
        $("#addConfirmation").modal("show");
        $("#addProgramForm")[0].reset();

        $("#addConfirmation").on("hidden.bs.modal", function () {
          location.reload();
        });
      } else {
        alert(response.message);
      }
    }).fail(function (xhr) {
      alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
  });

  //Edit Program Popup
  $('#editProgram').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var programCode = button.data('programCode');
    var programName = button.data('programName');
    var collegeCode = button.data('collegeCode');

    modal.find('#programCode').val(programCode);
    modal.find('#programName').val(programName);
    modal.find('#collegeCode').val(collegeCode);
    modal.find('#originalCode').val(programCode);

  });

  // Edit Confirmation Popup
  $("#editProgramForm").submit(function (e) {
    e.preventDefault();

    $.post("/programs/edit", $(this).serialize(), function (response) {
      if (response.success) {
        $("#editProgram").modal('hide');
        $("#editConfirmation").modal('show');
        $("#editProgramForm")[0].reset();


        $('#editConfirmation').on('hidden.bs.modal', function () {
          location.reload(); // reload table to show changes
        });

      } else {
        alert("Error: " + response.message);
      }
    }).fail(function (xhr) {
      alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
  });

  // Delete Program Popup
  $('#programDeletionModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var code = button.data('program-code'); // Extract code from data attribute
    $(this).find('#deleteCode').val(code); // Set value in hidden input
  });

  $('#deleteProgramForm').submit(function (e) {
    e.preventDefault();
    $.post("/programs/delete", $(this).serialize(), function (response) {
      if (response.success) {
        $('#programDeletionModal').modal('hide'); // hide the confirm modal
        $('#deleteConfirmationModal').modal('show'); // show "College Deleted" modal

        // optional: reload table or page when deletion modal closes
        $('#deleteConfirmationModal').on('hidden.bs.modal', function () {
          location.reload();
        });
      } else {
        alert(response.message);
      }
    });
  });

  // --------- STUDENT SCREEN --------- //
  //Add Student Popup
  $("#addStudentForm").submit(function (e) {
    e.preventDefault();

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
      if (response.success) {
        $("#addStudent").modal("hide");
        $("#addConfirmation").modal("show");
        $("#addStudentForm")[0].reset();

        $("#addConfirmation").on("hidden.bs.modal", function () {
          location.reload();
        });
      } else {
        alert(response.message);
      }
    }).fail(function (xhr) {
      alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
  });

  //Edit Student Popup
  $('#editStudent').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var studentID = button.data('student-id');
    var firstName = button.data('first-name');
    var lastName = button.data('last-name');
    var programCode = button.data('program-code');
    var yearLevel = button.data('year-level');
    var gender = button.data('gender');

    modal.find('#studentID').val(studentID);
    modal.find('#firstName').val(firstName);
    modal.find('#lastName').val(lastName);
    modal.find('#programCode').val(programCode);
    modal.find('#yearLevel').val(yearLevel);
    modal.find('#gender').val(gender);
    modal.find('#original_id').val(studentID);

  });

  // Edit Confirmation Popup
  $("#editStudentForm").submit(function (e) {
    e.preventDefault();

    $.post("/students/edit", $(this).serialize(), function (response) {
      if (response.success) {
        $("#editStudent").modal('hide');
        $("#editConfirmation").modal('show');
        $("#editStudentForm")[0].reset();


        $('#editConfirmation').on('hidden.bs.modal', function () {
          location.reload(); // reload table to show changes
        });

      } else {
        alert("Error: " + response.message);
      }
    }).fail(function (xhr) {
      alert("Error: " + (xhr.responseJSON?.message || "Something went wrong"));
    });
  });

  //Delete Student Popup
  $('#studentDeletionModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var id = button.data('student-id');
    $(this).find('#deleteStudentID').val(id); // Set value in hidden input
  });

  $('#deleteStudentForm').submit(function (e) {
    e.preventDefault();
    $.post("/students/delete", $(this).serialize(), function (response) {
      if (response.success) {
        $('#studentDeletionModal').modal('hide'); // hide the confirm modal
        $('#deleteConfirmationModal').modal('show'); // show "College Deleted" modal

        // optional: reload table or page when deletion modal closes
        $('#deleteConfirmationModal').on('hidden.bs.modal', function () {
          location.reload();
        });
      } else {
        alert(response.message);
      }
    });
  });
});



