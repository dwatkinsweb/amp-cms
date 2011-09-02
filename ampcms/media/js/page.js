define(['jquery', 'pagelet', 'amplify.core'], function($, Pagelet) {
	var Page;
	return Page = (function() {
		function Page(element) {
			this.element = $(element);
			this.data = this.element.data();
			this.pagelets = null;
		}
		Page.prototype.load = function(url) {
			url = url ? url : this.data.url;
			if(url) {
				url = '/page' + url;
				$.get(url, this._load_html);
			}
			return this;
		};
		Page.prototype.load_pagelets = function() {
			var pagelet, pagelet_element, pagelet_elements, _i, _len;
			this.pagelets = {};
			pagelet_elements = this.element.find('.pagelet');
			for( _i = 0, _len = pagelet_elements.length; _i < _len; _i++) {
				pagelet_element = pagelet_elements[_i];
				pagelet = new Pagelet(pagelet_element, this);
				pagelet.load();
				this.pagelets[pagelet.data.name];
			}
			amplify.publish('ampcms.fullpageletload', this);
			return this;
		};
		Page.prototype._load_html = function(html) {
			var new_page;
			new_page = $(html);
			this.element.replaceWith(new_page);
			this.element = new_page;
			this.data = this.element.data();
			amplify.publish('ampcms.pageload', this);
			return this;
		};
		return Page;
	})();
});
