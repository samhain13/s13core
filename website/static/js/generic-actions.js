$(document).ready( function() {
    // Set up the site header.
    $('#site-header').css({
        'max-height': '100%',
        'overflow': 'auto',
        'position': 'fixed',
        'top': 0
    });
    $('#site-header').append($('<a id="site-tools-toggle" href="#">≋</a>'));
    $('#site-tools').hide();

    // Activate the site tools toggle link.
    $('#site-tools-toggle').data('toggle', 'show');
    $('#site-tools-toggle').click( function() {
        var d = $(this).data('toggle');
        if (d == 'show') $('#site-tools').stop(true, true).slideDown(400,
            function() {
                $('html').css('overflow', 'hidden');
                $('#site-tools-toggle').data('toggle', 'hide');
            });
        else $('#site-tools').stop(true, true).slideUp(400,
            function() {
                $('html').css('overflow', 'auto');
                $('#site-tools-toggle').data('toggle', 'show');
            });
    });
    
    // Adjust the site-content div height.
    function adjust_content_height() {
        var bd_hgt = $('body').height();
        var sc_hgt = $('#site-content').height();
        var ft_hgt = $('#site-footer').outerHeight();
        var top_pad = $('#site-header > h1').outerHeight() + 10;
        $('#site-content').css('padding-top', top_pad);

        if (bd_hgt > sc_hgt) $('#site-content').height(bd_hgt - (top_pad + ft_hgt));
    }

    $(window).resize( function() {
        adjust_content_height();
    });
    
    adjust_content_height();
});
