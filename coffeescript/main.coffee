require ['jquery', 'page', 'pagelet', 'jquery.ba-bbq', 'amplify.core'], ($, Page, Pagelet) ->
    require.ready () ->
        page = new Page('#page')
        
        amplify.subscribe 'ampcms.pageletload', (pagelet) ->
            pagelet.transform_links().transform_forms()
        
        amplify.subscribe 'ampcms.pageload', (page) ->
            $(window).trigger('hashchange')
        
        $(window).bind 'hashchange', (event) ->
            page.load_pagelets()
        
        page.load_pagelets()
