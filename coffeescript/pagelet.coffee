define ["jquery", "jquery.ba-bbq", "amplify.core"], ($) ->
    class Pagelet
        constructor: (element, page) ->
            @element = $(element)
            @page = page
            @data = @element.data()

        transform_links: () ->
            anchors = @element.find('a')
            for anchor in anchors
                anchor = $(anchor)
                url = anchor.attr('href')
                url.replace(/// .*\.com ///, '')
                anchor.attr('href', '#'+url)
            
            $(@element).delegate('a', 'click', (event) =>
                event.preventDefault()
                url = $(this).attr('href').split('#')[1]
                @push_url(url)
                @data = this_pagelet.element.data()
                false
            )
            @

        transform_forms: () ->
            $(@element).delegate('form', 'submit', (event) =>
                event.preventDefault()
                @post(event.target)
            )
            @

        push_url: (url) ->
            id = @element.attr('id')
            state = {}
            state[id] = url
            $.bbq.pushState(state)
            @

        load: (url) ->
            url = @_get_pagelet_url(url)
            if (url?) and url != @data.location
                url = @_build_url(url)
                $.get(url, (response) =>
                    response = $.parseJSON(response)
                    if response.css?
                        for css in response.css
                            if css?
                                if document.createStylesheet
                                    document.createStylesheet(css)
                                else
                                    $('head').append($("<link rel='stylesheet' href='"+css+"' type='text/css' />"))
                    if response.js?
                        require(response.js, () =>
                            @push_url(response.location)
                            @_load_html(response.html)
                        )
                    else
                        @push_url(response.location)
                        @_load_html(response.html)
                )
            @

        post: (form) ->
            form_data = $(form).serialize()
            form_url = $(form).attr('action')
            if !form_url
                form_url = @_build_url(@_get_pagelet_url())
            else
                form_url = '/pagelet'+@page.data.url+form_url
            $.ajax(form_url, {
                type: 'POST',
                data: form_data,
                success: (response) =>
                    response = $.parseJSON(response)
                    new_element = $(response.html)
                    @push_url(response.location)
                    @_load_html(new_element)
            })
            @

        _build_url: (url) ->
            '/pagelet'+@page.data.url+'/'+@data.name+url

        _load_html: (html) ->
            new_pagelet = $(html)
            @element.parents('.pagelet-wrapper').replaceWith(new_pagelet)
            @element = new_pagelet.find('.pagelet')
            @data = @element.data()
            amplify.publish('ampcms.pageletload', this, @data.application)
            @

        _get_pagelet_url: (url) ->
            if not url?
                url = $.bbq.getState(@element.attr('id'))
                if @data.application? and not url?
                    url = @data.starting_url
            url
