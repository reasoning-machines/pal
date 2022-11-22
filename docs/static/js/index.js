window.HELP_IMPROVE_VIDEOJS = false;


$(document).ready(function() {
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");

    });

    var current_cmd_idxs = {
        "gsm": 1,
        "gsmhard": 1,
        "coloredobjects":1,
        "repeatcopy":1,
        "date":1
    }

    // examples
    $('select').on('change', function() {
        var sep_idx = this.value.indexOf('_');
        var domain_name = this.value.substring(0, sep_idx);
        var desired_cmd_idx = parseInt(this.value.substring(sep_idx + 1));
        var current_cmd_idx = current_cmd_idxs[domain_name];

        // hide current content
        var current_content = $('#content_' + domain_name + "_" + current_cmd_idx.toString());
        current_content.hide();

        // show desired content
        var desired_content = $('#content_' + domain_name + "_" + desired_cmd_idx.toString());
        desired_content.show();

        // set current to desired
        current_cmd_idxs[domain_name] = desired_cmd_idx;
    });
})



