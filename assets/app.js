$(document).ready(function() {
    container = $('div#container');
    $.ajax({
        url: 'https://api.github.com/repos/eugene-eeo/commandeer/contents/README.md',
        success: function (data) {
            var content = data.content;
            container.html(marked(atob(content)));

            $('pre code').each(function(i, block) {
                console.log(block);
                hljs.highlightBlock(block);
            });
        }
    });
});
