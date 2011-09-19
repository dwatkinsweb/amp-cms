class AMPCMSAjaxResponse(object):
    def __init__(self, response):
        self.response = response

class AMPCMSMedia(object):
    def __init__(self, css_files, js_files):
        self.css = css_files
        self.js = js_files