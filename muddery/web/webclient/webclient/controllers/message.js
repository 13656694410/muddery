
var controller = {

    // close popup box
    doClosePopupBox: function() {
        parent.controller.doClosePopupBox();
    },

	setPopup: function(header, content, commands) {
	    try {
	        header = text2html.parseHtml(header);
	    	$("#popup_header").html(header);
	    }
	    catch(error) {
            console.error(error.message);
        }

        try {
	        content = text2html.parseHtml(content);
		    $("#popup_body").html(content);
	    }
	    catch(error) {
            console.error(error.message);
        }

        this.clearButtons();
		if (!commands) {
            commands = [{"name": _("OK"),
                         "cmd": "",
                         "args": ""}];
        }
		this.addButtons(commands);
	},

	clearButtons: function() {
    	// remove buttons that are not template..
    	$("#button_content").children().not(".template").remove();
    },

	addButtons: function(data) {
    	var content = $("#button_content");
		var item_template = content.find("button.template");

		var has_button = false;
		if (data) {
            for (var i in data) {
                var cmd = data[i];

                try {
                    var name = text2html.parseHtml(cmd["name"]);
                    item_template.clone()
                        .removeClass("template")
                        .data("cmd_name", cmd["cmd"])
                        .data("cmd_args", cmd["args"])
                        .html(name)
                        .appendTo(content);

                    has_button = true;
                }
                catch(error) {
                    console.error(error.message);
                }
            }
        }
    },

    doCommandLink: function(caller) {
        this.doClosePopupBox();

        var cmd = $(caller).data("cmd_name");
        var args = $(caller).data("cmd_args");
        if (cmd) {
            parent.commands.doCommandLink(cmd, args);
        }
    },
};
