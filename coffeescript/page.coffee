define ['jquery', 'pagelet','amplify.core'], ($, Pagelet) ->
    class Page
        constructor: (element) ->
            @element = $(element)
            @data = @element.data()
            @pagelets = null
	  
        load: (url) ->
            url = if url then url else @data.url
            if url
              url = '/page'+url
              $.get(url, @_load_html)
            @
	  
        load_pagelets: () ->
            @pagelets = {}
            pagelet_elements = @element.find('.pagelet')
            for pagelet_element in pagelet_elements
                pagelet = new Pagelet(pagelet_element, this)
                pagelet.load()
                @pagelets[pagelet.data.name]
            amplify.publish('ampcms.fullpageletload', this)
            @

        _load_html: (html) ->
            new_page = $(html)
            @element.replaceWith(new_page)
            @element = new_page
            @data = @element.data()
            amplify.publish('ampcms.pageload', this)
            @