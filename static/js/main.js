// Flexslider
$(window).load(function() {
    $('.flexslider').flexslider();
});

$(window).load(function() {
    // toggle delivery inputs based on selection
    $("form").change(function () {
        $(".delivery_addr").toggle($('input[name=delivery]:checked', 'form').val() == 'mail');
    });
});
