
/*
 * Derive from the base class.
 */
function MudderyHonours() {
	BaseController.call(this);

	this.min_honour_level = 1;
	this.paginator = new Paginator("#honours_wrapper");
}

MudderyHonours.prototype = prototype(BaseController.prototype);
MudderyHonours.prototype.constructor = MudderyHonours;

/*
 * Reset the view's language.
 */
MudderyHonours.prototype.resetLanguage = function() {
    this.select("#honours_view_ranking").text($$("RANKING"));
    this.select("#honours_view_name").text($$("NAME"));
    this.select("#honours_view_honour").text($$("HONOUR"));
    this.select("#honours_button_queue").text($$("QUEUE UP"));
    this.select("#honours_button_quit").text($$("QUIT QUEUE"));
}

/*
 * Bind events.
 */
MudderyHonours.prototype.bindEvents = function() {
    this.onClick("#honours_button_queue", this.onQueueUpCombat);
    this.onClick("#honours_button_quit", this.onQuitCombatQueue);
	this.on(window, "resize", this.onResize);
}

/*
 * Event when clicks the queue up button.
 */
MudderyHonours.prototype.onQueueUpCombat = function(element) {
    if ($$.data_handler.character_level < this.min_honour_level) {
        $$.controller.showAlert($$("You need to reach level ") + this.min_honour_level + $$("."));
        return;
    }

    this.queueUpCombat();
    $$.commands.queueUpCombat();
}

/*
 * Event when clicks the quit queue button.
 */
MudderyHonours.prototype.onQuitCombatQueue = function(element) {
	this.quitCombatQueue();
    $$.commands.quitCombatQueue();
}

/*
 * Event then the window resizes.
 */
MudderyHonours.prototype.onResize = function(element) {
	var height = $(window).innerHeight() - this.select("#honours_wrapper").offset().top - 16;
	this.paginator.tableHeight(height);
}

/*
 * Set the minimum level that a player can attend the honour combat.
 */
MudderyHonours.prototype.setMinHonourLevel = function(level) {
	this.min_honour_level = level;
}

/*
 * Set top characters.
 */
MudderyHonours.prototype.setRankings = function(rankings) {
    this.clearElements("#honours_character_items");
    var template = this.select("#honours_character_items>tr.template");

    for (var i in rankings) {
        var data = rankings[i];
        var item = this.cloneTemplate(template);

        item.find(".character_ranking")
            .text(data["ranking"]);

        item.find(".character_name")
            .text(data["name"]);

        item.find(".character_honour")
            .text(data["honour"]);
    }
    
    var height = $(window).innerHeight() - this.select("#honours_wrapper").offset().top - 16;
	this.paginator.refresh(height);
}

/*
 * Set the queue up state.
 */
MudderyHonours.prototype.queueUpCombat = function() {
    this.select("#honours_button_queue").hide();
    this.select("#honours_button_quit").show();
}

/*
 * Set the quit queue state.
 */
MudderyHonours.prototype.quitCombatQueue = function() {
    this.select("#honours_button_queue").show();
    this.select("#honours_button_quit").hide();
}
