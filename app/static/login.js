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

    $password.on("input", function () {
      if ($(this).val().length > 0) {
        $toggle.show();
      } else {
        $toggle.hide();
      }
    });

    $toggle.on("click", function () {
      const type = $password.attr("type") === "password" ? "text" : "password";
      $password.attr("type", type);

      $(this).toggleClass("bx-eye bx-eye-slash"); 
    });

    const $signupPassword = $("#signup-password-field"); 
    const $signupToggle = $("#signup-toggle-password-eye"); 

    $signupPassword.on("input", function () {
      if ($(this).val().length > 0) {
        $signupToggle.show();
      } else {
        $signupToggle.hide();
      }
    });

    $signupToggle.on("click", function () {
      const type = $signupPassword.attr("type") === "password" ? "text" : "password";
      $signupPassword.attr("type", type);

      $(this).toggleClass("bx-eye bx-eye-slash");
    });

});