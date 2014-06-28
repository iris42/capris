$(document).ready(function() {
    container = $('div#container');
    $.ajax({
        url: 'https://api.github.com/repos/eugene-eeo/capris/readme',
        success: function (data) {
            try {
                var markdown = marked(atob(data.content));
                container.html(markdown);
            } catch (err) {
                container.html("<img src='assets/error.png' align=left>"+
                               "<p>An error occured. Please try using a different browser "+
                               "if you are using <b>Safari</b> as the app is known to fail "+
                               "on <b>Safari</b>.</p>");
            }

            $('pre code').each(function(i, block) {
                console.log(block);
                hljs.highlightBlock(block);
            });
        },
        error: function() {
            container.html("<img src='assets/error.png' align=left>" +
                           "<p><b>An error occured.</b> Please try reloading the app. " +
                           "If the error persists perhaps you can try contacting the "  +
                           "maintainer at " +
                           "<a href='mailto:packwolf58@gmail.com'>packwolf58@gmail.com</a></p>");
        }
    });
});
