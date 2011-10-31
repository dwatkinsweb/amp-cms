/*
* Copyright David Watkins 2011
* 
* AMP-CMS is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

var ampcms = function() {
	var require_config = {
		baseUrl: '/media/js',
		paths: {
			'ampcms' : '/media/ampcms/js/ampcms',
			'ampcms/ext' : '/media/js/ampcms',
			'libs/history' : '/media/ampcms/js/libs/history'
		}
	};
	
	// Create a basic extend function. Only works with basic objects and arrays.
	var extend = function(destination, source) {
		for (var k in source) {
			if (source.hasOwnProperty(k)) {
				if (typeof destination[k] === 'object' && typeof source[k] === 'object') {
					destination[k] = extend(destination[k], source[k]);
				} else {
					destination[k] = source[k];
				}
			}
		}
		return destination;
	};
	
	return {
		setup : function() {
			// If an ampcms_config object exists and it has a require attribute, use it to configure require.
			if (typeof ampcms_config !== 'undefined' && typeof ampcms_config.require !== 'undefined') {
				require_config = extend(require_config, ampcms_config.require);
			}
			require.config(require_config);
			return this;
		},
		run : function() {
			require(['ampcms/core'], function(core) {
				return require.ready(function() {
					// If a ampcms_config object exists and it has an ampcms, use it to configure ampcms
					if (typeof ampcms_config !== 'undefined' && typeof ampcms_config.ampcms !== 'undefined') {
						core.config(ampcms_config.ampcms);
					} else {
						core.config();
					}
				});
			});
			return this;
		}
	};
}();

ampcms.setup().run();
