
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
  $("table").each(function () {
    var actionsIndex = $(this).find("thead th")
      .filter(function () { return $(this).text().trim() === "Actions"; })
      .index();


    $(this).DataTable({
      columnDefs: [
        { orderable: false, targets: actionsIndex } // disable sorting
      ]
    });
  });

  $("#addForm").submit(function (e) {
    e.preventDefault();
    $("#addCollege").modal('hide');
    $("#addConfirmation").modal('show');

    $.post($(this).attr("action"), $(this).serialize(), function (response) {
      if (response.success) {
        $("#addCollege").modal("hide");
        $("#addConfirmation").modal("show");
        $("#addForm")[0].reset();

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

  //Edit College Popup
  $('#editCollege').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var collegeCode = button.data('collegeCode');
    var collegeName = button.data('collegeName');

    modal.find('#collegeCode').val(collegeCode);
    modal.find('#collegeName').val(collegeName);
  });

  // Edit Confirmation Popup
  $("#editForm").submit(function (e) {
    e.preventDefault();
    $("#editCollege").modal('hide');
    $("#editConfirmation").modal('show');
  });

  // Delete Popup
  // When opening the delete modal, set the college code
  $('#deleteConfirmationModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var code = button.data('college-code'); // Extract code from data attribute
    $(this).find('#deleteCode').val(code); // Set value in hidden input
  });

  $('#deleteForm').submit(function (e) {
    e.preventDefault();
    $.post("/colleges/delete", $(this).serialize(), function (response) {
      if (response.success) {
        $('#deleteConfirmationModal').modal('hide'); // hide the confirm modal
        $('#deletionModal').modal('show'); // show "College Deleted" modal

        // optional: reload table or page when deletion modal closes
        $('#deletionModal').on('hidden.bs.modal', function () {
          location.reload();
        });
      } else {
        alert(response.message);
      }
    });
  });


  // --------- PROGRAM SCREEN --------- //
  //Add Program Popup
  $("#addForm").submit(function (e) {
    e.preventDefault();
    $("#addProgram").modal('hide');
    $("#addConfirmation").modal('show');
  });

  //Edit Program Popup
  $('#editCollege').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var modal = $(this);

    var programCode = button.data('program-code');
    var programName = button.data('program-name');
    var collegeCode = button.data('college-code');

    modal.find('#programCode').val(programCode);
    modal.find('#programName').val(programName);
    modal.find('#collegeCode').val(collegeCode);

  });

  // Edit Confirmation Popup
  $("#editForm").submit(function (e) {
    e.preventDefault();
    $("#editProgram").modal('hide');
    $("#editConfirmation").modal('show');
  });

  //Delete Program Popup
  $("#deleteForm").submit(function (e) {
    e.preventDefault();
    $("#deleteConfirmationModal").modal('hide');
    $("#deletionModal").modal('show');
  });

  // --------- STUDENT SCREEN --------- //
  //Add Student Popup
  $("#addForm").submit(function (e) {
    e.preventDefault();
    $("#addStudent").modal('hide');
    $("#addConfirmation").modal('show');
  });

  //Edit Student Popup
  $('#editCollege').on('show.bs.modal', function (event) {
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

  });

  // Edit Confirmation Popup
  $("#editForm").submit(function (e) {
    e.preventDefault();
    $("#editStudent").modal('hide');
    $("#editConfirmation").modal('show');
  });

  //Delete Student Popup
  $("#deleteForm").submit(function (e) {
    e.preventDefault();
    $("#deleteConfirmationModal").modal('hide');
    $("#deletionModal").modal('show');
  });
});



