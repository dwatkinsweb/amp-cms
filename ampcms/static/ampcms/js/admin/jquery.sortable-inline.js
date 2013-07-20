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

(function($) {
	$.fn.extend({
		inline_sort: function() {
			return this.each(function() {
				_enhance_inline($(this));
				_initialize_inline($(this));
			});
		}
	});
	
	var _enhance_inline = function(ele) {
		ele.find('fieldset.module > table > tbody > tr')
			.prepend('<td class="inline-mover">&nbsp;</td>');
		ele.find('fieldset.module > table > thead > tr')
			.prepend('<th class="inline-mover">&nbsp;</th>');
	};
	
	var _initialize_inline = function(ele) {
		var _update_inline = function() {
		    $(this).find('.inline-related .row1:visible, .inline-related .row2:visible').each(function(i) {
		    	var order_field = $(this).find('input[id$=order]')
		    	if (order_field.attr('value') > 0)
		    	{
		    		order_field.attr('value', i+1);
		    	}
		    	$(this).removeClass('row1 row2').addClass('row'+((i%2)+1));
		    });
		};
		
		ele.sortable({
			axis: 'y',
			handle: '.inline-mover',
	        placeholder: 'ui-state-highlight', 
	        forcePlaceholderSize: 'true', 
	        items: '.row1:visible, .row2:visible', 
	        update: _update_inline
	    });
		ele.disableSelection();
	}
})(jQuery);
