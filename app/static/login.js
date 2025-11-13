$(document).ready(function () {
    const $container = $('.container');
    const $loginLink = $('.SignInLink');
    const $registerLink = $('.SignUpLink');

    $registerLink.on('click', function () {
        $container.addClass('active');
    });

    $loginLink.on('click', function () {
        $container.removeClass('active');
    });

    //-----------------------
    // Password Eye Toggle
    //-----------------------

    const $password = $("#login-password-field"); 
    const $toggle = $("#toggle-password-eye"); 

    $toggle.on("click", function () {
      const type = $password.attr("type") === "password" ? "text" : "password";
      $password.attr("type", type);

      $(this).toggleClass("bx-eye bx-eye-closed"); 
    });

});