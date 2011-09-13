var __bind = function(fn, me) {
	return function() {
		return fn.apply(me, arguments);
	};
};
define(["jquery", "jquery.ba-bbq", "amplify.core"], function($) {
	var Pagelet;
	return Pagelet = (function() {
		function Pagelet(element, page) {
			this.element = $(element);
			this.page = page;
			this.data = this.element.data();
		}


		Pagelet.prototype.transform_links = function() {
			var anchor, anchors, url, _i, _len;
			console.log('transforming anchors');
			anchors = this.element.find('a');
			for( _i = 0, _len = anchors.length; _i < _len; _i++) {
				anchor = anchors[_i];
				anchor = $(anchor);
				url = anchor.attr('href');
				url.replace(/.*\.com/, '');
				anchor.attr('href', '#' + url);
			}
			$(this.element).delegate('a', 'click', __bind(function(event) {
				console.log('a.click triggered');
				event.preventDefault();
				url = $(event.target).attr('href').split('#')[1];
				this.push_url(url);
				this.data = this.element.data();
				return false;
			}, this));
			return this;
		};
		Pagelet.prototype.transform_forms = function() {
			console.log('transforming forms');
			$(this.element).delegate('form', 'submit', __bind(function(event) {
				event.preventDefault();
				return this.post(event.target);
			}, this));
			return this;
		};
		Pagelet.prototype.push_url = function(url) {
			var id, state;
			id = this.element.attr('id');
			console.log('pagelet.push - url: ' + url + '; id: ' + id);
			state = {};
			state[id] = url;
			$.bbq.pushState(state);
			return this;
		};
		Pagelet.prototype.load = function(url) {
			console.log('pagelet.load - url: ' + url);
			url = this._get_pagelet_url(url);
			if((url != null) && url !== this.data.location) {
				url = this._build_url(url);
				$.get(url, __bind(function(response) {
					var css, _i, _len, _ref;
					response = $.parseJSON(response);
					if(response.css != null) {
						_ref = response.css;
						for( _i = 0, _len = _ref.length; _i < _len; _i++) {
							css = _ref[_i];
							if(css != null) {
								if(document.createStylesheet) {
									document.createStylesheet(css);
								} else {
									$('head').append($("<link rel='stylesheet' href='" + css + "' type='text/css' />"));
								}
							}
						}
					}
					if(response.js != null) {
						return require(response.js, __bind(function() {
							this.push_url(response.location);
							return this._load_html(response.html);
						}, this));
					} else {
						this.push_url(response.location);
						return this._load_html(response.html);
					}
				}, this));
			}
			return this;
		};
		Pagelet.prototype.post = function(form) {
			var form_data, form_url;
			form_data = $(form).serialize();
			form_url = $(form).attr('action');
			if(!form_url) {
				form_url = this._build_url(this._get_pagelet_url());
			} else {
				form_url = '/pagelet' + this.page.data.url + form_url;
			}
			$.ajax(form_url, {
				type : 'POST',
				data : form_data,
				success : __bind(function(response) {
					var new_element;
					response = $.parseJSON(response);
					new_element = $(response.html);
					this.push_url(response.location);
					return this._load_html(new_element);
				}, this)
			});
			return this;
		};
		Pagelet.prototype._build_url = function(url) {
			return '/pagelet' + this.page.data.url + '/' + this.data.name + url;
		};
		Pagelet.prototype._load_html = function(html) {
			var new_pagelet;
			new_pagelet = $(html);
			this.element.parents('.pagelet-wrapper').replaceWith(new_pagelet);
			this.element = new_pagelet.find('.pagelet');
			this.data = this.element.data();
			console.log('pagelet publishing ampcms.pageletload');
			amplify.publish('ampcms.pageletload', this, this.data.application);
			return this;
		};
		Pagelet.prototype._get_pagelet_url = function(url) {
			if(!(url != null)) {
				url = $.bbq.getState(this.element.attr('id'));
				if((this.data.application != null) && !(url != null)) {
					url = this.data.starting_url;
				}
			}
			return url;
		};
		return Pagelet;
	})();
});
