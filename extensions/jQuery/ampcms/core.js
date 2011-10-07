define(['jquery'], function() {
	return {
		// DOM Methods
		dom : {
			find : function(scope, selector) {
				var ret, thiz, jq_elements;
				thiz = this;
				if( typeof selector === 'undefined') {
					selector = scope;
					scope = null;
				}
				if(scope && scope.find) {
					jq_elements = jQuery(scope).find(selector);
				} else {
					jq_elements = jQuery(selector);
				}
				ret = jq_elements.get();
				ret.length = jq_elements.length;
				ret.find = function(sel) {
					return thiz.find(jq_elements, sel);
				};
				return ret;
			},
			filter : function(element, selector) {
				return jQuery(element).filter(selector).get();
			},
			attr : function(element, attr, value) {
				var ret;
				if( typeof value === 'undefined') {
					ret = jQuery(element).attr(attr);
				} else {
					ret = jQuery(element).attr(attr, value);
				}
				return ret;
			},
			html : function(element, html) {
				var ret;
				if( typeof html === 'undefined') {
					ret = jQuery(element).html();
				} else {
					ret = jQuery(element).html(html);
				}
				return ret;
			},
			append : function(element, html) {
				return jQuery(element).append(jQuery(html));
			},
			remove : function(selector) {
				jQuery(selector).remove();
			},
			replace : function(element, html) {
				return jQuery(element).replaceWith(html);
			},
			data : function(element, key, data) {
				var ret;
				if( typeof key === 'undefined') {
					ret = jQuery(element).data();
				} else if( typeof data === 'undefined') {
					ret = jQuery(element).data(key);
				} else {
					ret = jQuery(element).data(key, data);
				}
				return ret;
			},
			remove_data : function(element, key) {
				jQuery(element).removeData(key);
			},
			bind : function(element, event, callback) {
				if(element && event) {
					if( typeof event === 'function') {
						callback = event;
						event = 'click';
					}
					jQuery(element).bind(event, callback);
				} else {
					// log wrong arguments
				}
			},
			unbind : function(element, event, callback) {
				if(element && event) {
					if( typeof event === 'function') {
						callback = event;
						event = 'click';
					}
					jQuery(element).unbind(event, callback);
				} else {
					// log wrong arguments
				}
			},
			live : function(element, event, callback) {
				if(element && event) {
					if( typeof event === 'function') {
						callback = event;
						event = 'click';
					}
					jQuery(element).live(event, callback);
				} else {
					// log wrong arguments
				}
			},
			die : function(element, event, callback) {
				if(element && event) {
					if( typeof event === 'function') {
						callback = event;
						event = 'click';
					}
					jQuery(element).die(event, callback);
				} else {
					// log wrong arguments
				}
			},
			add_class : function(selector, css) {
				jQuery(selector).addClass(css);
			},
			remove_class : function(selector, css) {
				jQuery(selector).removeClass(css);
			},
			has_class : function(selector, css) {
				return jQuery(selector).hasClass(css);
			}
		},
		// Ajax Methods
		ajax : {
			ajax : function(url, config) {
				jQuery.ajax(url, config);
			},
			get : function(url, callback) {
				jQuery.get(url, function(response) {
					response = jQuery.parseJSON(response);
					callback(response);
				});
			},
			post : function(url, data, callback) {
				jQuery.post(url, data, function(response) {
					response = jQuery.parseJSON(response);
					callback(response);
				});
			},
			post_form : function(form, url, callback) {
				form = jQuery(form);
				var data = form.serialize();
				this.post(url, data, callback); 
			}
		},
		// Utility Methods
		utils : {
			is_array : function(arr) {
				return jQuery.isArray(arr);
			},
			is_object : function(obj) {
				return jQuery.isPlainObject(obj);
			},
			extend : function(object1, object2) {
				return jQuery.extend(object1, object2);
			},
			retract : function(object1, object2) {
				for(object in object2) {
					if(object1.hasOwnProperty(object)) {
						delete object1[object];
					}
				}
				return object1;
			},
			merge : function(first, second) {
				return jQuery.merge(first, second);
			}
		}
	};
});