define(["jquery", "jquery.pagelet", "amplify.core"], function($, Pagelet) {
	return function() {
		return {
			element: null,
			data: null,
			pagelets: null,
			init: function(element) {
				// Initialize the element and data for the page
				this.element = $(element);
				this.data = this.element.data();
				return this;
			},
			load: function(page_url) {
				// Load the page with either the given url or the default url if no url is given
				var this_page = this; // set THIS into a variable to use in the .get callback
				page_url = page_url != undefined ? page_url : this.data.url;
				if (page_url != undefined) {
					page_url = '/page'+page_url;
					$.get(page_url, function(html){
						this_page._load_html(html);
					});
				}
				return this;
			},
			load_pagelets: function() {
				// Load all hte pagelets into an array
				var page_object = this; // put THIS into a variable so it can be passed to the pagelet
				var pagelet_list = new Array;
				$('.pagelet', this.element).each(function(idx, element){
					var data = $(this).data();
					pagelet = Pagelet();
					pagelet_list[data.name] = pagelet.init(element, page_object).load();
				});
				this.pagelets = pagelet_list;
				amplify.publish('ampcms.fullpageletload', this);
				return this;
			},
			_load_html: function(html) {
				// Load the given html into the page
				var new_page = $(html);
				this.element.replaceWith(new_page);
				this.element = new_page;
				this.data = this.element.data();
				amplify.publish('ampcms.pageload', this);
				return this;
			}
		};
	};
});
