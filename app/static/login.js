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
});