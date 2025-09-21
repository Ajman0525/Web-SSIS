
$(document).ready(function () {
  const $body = $("body"),
        $sidebar = $(".sidebar"),
        $toggle = $(".toggle"),
        $modeSwitch = $(".toggle-switch"),
        $modeText = $(".mode-text");

  const savedSidebar = localStorage.getItem("sidebarState");
  if (savedSidebar === "open") {
    $sidebar.removeClass("close");
  } else {
    $sidebar.addClass("close"); // default collapsed
  }
  
  // Sidebar toggle
  // $toggle.on("click", () => $sidebar.toggleClass("close"));
  // $searchBtn.on("click", () => $sidebar.removeClass("close"));

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

  // Load saved theme
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

  $("table").each(function () {
    // find index of "Actions" column for this table
    var actionsIndex = $(this).find("thead th")
      .filter(function () { return $(this).text().trim() === "Actions"; })
      .index();

    // initialize DataTable
    $(this).DataTable({
      columnDefs: [
        { orderable: false, targets: actionsIndex } // disable sorting
      ]
    });
  });
});


  
