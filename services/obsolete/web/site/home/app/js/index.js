$(document).ready(function () {

//the reason for the odd-looking selector is to listen for the click event
// on links that don't even exist yet - i.e. are loaded from the server.
    // JvdB; This gave the trigger to use this:
    // https://coderwall.com/p/1lnxba/load-bootstrap-tabs-dynamically
    // This simple construct allows us to load main content dynamically in a SPA
    // See index.html for setup.
    $('#tabs').on('click', '.tablink,#navtabs a', function (e) {
        e.preventDefault();
        var url = $(this).attr("data-url");

        if (typeof url !== "undefined") {
            var pane = $(this), href = '#page'; // this.hash;

            // ajax load from data-url
            $(href).load(url, function (result) {
                pane.tab('show');
            });
        } else {
            $(this).tab('show');
        }
    });

    // Start with home page
    $('#page').load('home/pages/home.html')
});