define(["require", "jquery", "jquery.ba-bbq", "amplify.core"], function(require, $) {
	return function() {
		return {
			element: null,
			data: null,
			page: null,
			init: function(element, page) {
				this.element = $(element);
				this.page = page;
				this.data = this.element.data();
				return this;
			},
			load: function(pagelet_url) {
				var this_pagelet = this; // set THIS into a variable to use in the .get callback
				pagelet_url = this._get_pagelet_url(pagelet_url);
				if (pagelet_url != undefined && pagelet_url != this.data.location) {
					pagelet_url = '/pagelet'+this.page.data.url+'/'+this.data.name+pagelet_url;
					$.get(pagelet_url, function(response){
						response = $.parseJSON(response);
						if (response.css) {
							for (i in response.css) {
								if (document.createStylesheet) {
									document.createStylesheet(response.css[i]);
								} else {
									$("head").append($("<link rel='stylesheet' href='"+response.css[i]+"' type='text/css' />"));
								}
							}
						}
						if (response.js) {
							require(response.js, function() {
								this_pagelet._load_html(response.html);
							});
						}
					});
				}
				return this;
			},
			post: function(form) {
				var this_pagelet = this; // set THIS into a variable to use in the .ajax callback
				var form_data = $(form).serialize();
				var form_url = $(form).attr('action');
				var pagelet_url = this._get_pagelet_url(pagelet_url); 
				if (form_url == '' || form_url == undefined) {
					form_url = '/pagelet'+this.page.data.url+'/'+this.data.name+pagelet_url;
				} else {
					form_url = '/pagelet'+this.page.data.url+form_url;
				}
				$.ajax({
					type: 'POST',
					url: form_url,
					data: form_data,
					success: function(response){
						response = $.parseJSON(response);
						var new_element = $(response.html);
						var element_id = $('.pagelet', new_element).attr('id');
						var element_state = {};
						element_state[element_id] = response.location;
						$.bbq.pushState(element_state);
						this_pagelet._load_html(new_element);
					}
				});
				return this;
			},
			transform_links: function() {
				var this_pagelet = this; // set THIS into a variable to use in the .each callback
				$('a', this.element).each(function(idx, anchor) {
					var anchor_url = $(anchor).attr('href');
					anchor_url = anchor_url.replace(/.*\.com/, '');
					$(anchor).attr('href', '#'+anchor_url);
				});
				$(this_pagelet.element).delegate('a', 'click', function(event) {
					var anchor_url = $(this).attr('href').split('#')[1];
					var element_id = this_pagelet.element.attr('id');
					var element_state = {};
					element_state[element_id] = anchor_url;
					$.bbq.pushState(element_state);
					this_pagelet.data = this_pagelet.element.data();
					return false;
				});
				return this;
			},
			transform_forms: function() {
				var this_pagelet = this; // set THIS into a variable to use in the .each callback
				$(this_pagelet.element).delegate('form', 'submit', function(event){
					event.preventDefault();
					this_pagelet.post($(this));
				});
				return this;
			},
			_load_html: function(html) {
				var new_pagelet = $(html);
				this.element.parents('.pagelet-wrapper').replaceWith(new_pagelet);
				this.element = $('.pagelet', new_pagelet);
				this.data = this.element.data();
				amplify.publish('ampcms.pageletload', this, this.data.application);
				return this;
			},
			_get_pagelet_url: function(pagelet_url) {
				if (pagelet_url == undefined) {
					pagelet_url = $.bbq.getState(this.element.attr('id'));
					if (pagelet_url == undefined && this.data.application != undefined) {
						pagelet_url = this.data.starting_url;
					}
				}
				return pagelet_url;
			}
		};
	};
});