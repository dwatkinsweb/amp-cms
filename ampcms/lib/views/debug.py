from django.views.debug import ExceptionReporter as DjangoExceptionReporter
from django.template.base import Template
from django.template.context import Context
from django.conf import settings
from django.http import HttpResponseServerError

TECHNICAL_500_TEMPLATE = """
  <style type="text/css">
    #ampcms-debug-error table { border:1px solid #ccc; border-collapse: collapse; width:100%; background:white; }
    #ampcms-debug-error tbody td, tbody th { vertical-align:top; padding:2px 3px; }
    #ampcms-debug-error thead th { padding:1px 6px 1px 3px; background:#fefefe; text-align:left; font-weight:normal; font-size:11px; border:1px solid #ddd; }
    #ampcms-debug-error tbody th { width:12em; text-align:right; color:#666; padding-right:.5em; }
    #ampcms-debug-error table.vars { margin:5px 0 2px 40px; }
    #ampcms-debug-error table.vars td, table.req td { font-family:monospace; }
    #ampcms-debug-error table td.code { width:100%; }
    #ampcms-debug-error table td.code pre { overflow:hidden; }
    #ampcms-debug-error table.source th { color:#666; }
    #ampcms-debug-error table.source td { font-family:monospace; white-space:pre; border-bottom:1px solid #eee; }
    #ampcms-debug-error ul.traceback { list-style-type:none; color: #222; }
    #ampcms-debug-error ul.traceback li.frame { padding-bottom:1em; color:#666; }
    #ampcms-debug-error ul.traceback li.user { background-color:#e0e0e0; color:#000 }
    #ampcms-debug-error ul.traceback .frame .context .pre-context {display: none;}
    #ampcms-debug-error ul.traceback .frame .context .post-context {display: none;}
    #ampcms-debug-error ul.traceback .frame .vars {display: none;}
    #ampcms-debug-error div.context { padding:10px 0; overflow:hidden; }
    #ampcms-debug-error div.context ol { padding-left:30px; margin:0 10px; list-style-position: inside; }
    #ampcms-debug-error div.context ol li { font-family:monospace; white-space:pre; color:#777; cursor:pointer; }
    #ampcms-debug-error div.context ol li pre { display:inline; }
    #ampcms-debug-error div.context ol.context-line li { color:#505050; background-color:#dfdfdf; }
    #ampcms-debug-error div.context ol.context-line li span { position:absolute; right:32px; }
    #ampcms-debug-error .user div.context ol.context-line li { background-color:#bbb; color:#000; }
    #ampcms-debug-error .user div.context ol li { color:#666; }
    #ampcms-debug-error div.commands { margin-left: 40px; }
    #ampcms-debug-error div.commands a { color:#555; text-decoration:none; }
    #ampcms-debug-error .user div.commands a { color: black; }
    #ampcms-debug-error #summary { background: #ffc; }
    #ampcms-debug-error #summary h2 { font-weight: normal; color: #666; }
    #ampcms-debug-error #explanation { background:#eee; }
    #ampcms-debug-error #template, #template-not-exist { background:#f6f6f6; }
    #ampcms-debug-error #template-not-exist ul { margin: 0 0 0 20px; }
    #ampcms-debug-error #unicode-hint { background:#eee; }
    #ampcms-debug-error #traceback { background:#eee; }
    #ampcms-debug-error #requestinfo { background:#f6f6f6; padding-left:120px; }
    #ampcms-debug-error #summary table { border:none; background:transparent; }
    #ampcms-debug-error #requestinfo h2, #requestinfo h3 { position:relative; margin-left:-100px; }
    #ampcms-debug-error #requestinfo h3 { margin-bottom:-1em; }
    #ampcms-debug-error .error { background: #ffc; }
    #ampcms-debug-error .specific { color:#cc3300; font-weight:bold; }
    #ampcms-debug-error h2 span.commands { font-size:.7em;}
    #ampcms-debug-error span.commands a:link {color:#5E5694;}
    #ampcms-debug-error pre.exception_value { font-family: sans-serif; color: #666; font-size: 1.5em; margin: 10px 0 10px 0; }
  </style>
  {% if not is_email %}
  <script type="text/javascript">
  //<!--
    function getElementsByClassName(oElm, strTagName, strClassName){
        // Written by Jonathan Snook, http://www.snook.ca/jon; Add-ons by Robert Nyman, http://www.robertnyman.com
        var arrElements = (strTagName == "*" && document.all)? document.all :
        oElm.getElementsByTagName(strTagName);
        var arrReturnElements = new Array();
        strClassName = strClassName.replace(/\-/g, "\\-");
        var oRegExp = new RegExp("(^|\\s)" + strClassName + "(\\s|$)");
        var oElement;
        for(var i=0; i<arrElements.length; i++){
            oElement = arrElements[i];
            if(oRegExp.test(oElement.className)){
                arrReturnElements.push(oElement);
            }
        }
        return (arrReturnElements)
    }
    function hideAll(elems) {
      for (var e = 0; e < elems.length; e++) {
        elems[e].style.display = 'none';
      }
    }
    window.onload = function() {
      hideAll(getElementsByClassName(document, 'table', 'vars'));
      hideAll(getElementsByClassName(document, 'ol', 'pre-context'));
      hideAll(getElementsByClassName(document, 'ol', 'post-context'));
      hideAll(getElementsByClassName(document, 'div', 'pastebin'));
    }
    function toggle() {
      for (var i = 0; i < arguments.length; i++) {
        var e = document.getElementById(arguments[i]);
        if (e) {
          e.style.display = e.style.display == 'none' ? 'block' : 'none';
        }
      }
      return false;
    }
    function varToggle(link, id) {
      toggle('v' + id);
      var s = link.getElementsByTagName('span')[0];
      var uarr = String.fromCharCode(0x25b6);
      var darr = String.fromCharCode(0x25bc);
      s.innerHTML = s.innerHTML == uarr ? darr : uarr;
      return false;
    }
    function switchPastebinFriendly(link) {
      s1 = "Switch to copy-and-paste view";
      s2 = "Switch back to interactive view";
      link.innerHTML = link.innerHTML == s1 ? s2 : s1;
      toggle('browserTraceback', 'pastebinTraceback');
      return false;
    }
    //-->
  </script>
  {% endif %}
<div id="ampcms-debug-error">
<div id="summary">
  <h1>{% if exception_type %}{{ exception_type }}{% else %}Report{% endif %}{% if request %} at {{ request.path_info|escape }}{% endif %}</h1>
  <pre class="exception_value">{% if exception_value %}{{ exception_value|force_escape }}{% else %}No exception supplied{% endif %}</pre>
  <table class="meta">
{% if request %}
    <tr>
      <th>Request Method:</th>
      <td>{{ request.META.REQUEST_METHOD }}</td>
    </tr>
    <tr>
      <th>Request URL:</th>
      <td>{{ request.build_absolute_uri|escape }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Django Version:</th>
      <td>{{ django_version_info }}</td>
    </tr>
{% if exception_type %}
    <tr>
      <th>Exception Type:</th>
      <td>{{ exception_type }}</td>
    </tr>
{% endif %}
{% if exception_type and exception_value %}
    <tr>
      <th>Exception Value:</th>
      <td><pre>{{ exception_value|force_escape }}</pre></td>
    </tr>
{% endif %}
{% if lastframe %}
    <tr>
      <th>Exception Location:</th>
      <td>{{ lastframe.filename|escape }} in {{ lastframe.function|escape }}, line {{ lastframe.lineno }}</td>
    </tr>
{% endif %}
    <tr>
      <th>Python Executable:</th>
      <td>{{ sys_executable|escape }}</td>
    </tr>
    <tr>
      <th>Python Version:</th>
      <td>{{ sys_version_info }}</td>
    </tr>
    <tr>
      <th>Python Path:</th>
      <td><pre>{{ sys_path|pprint }}</pre></td>
    </tr>
    <tr>
      <th>Server time:</th>
      <td>{{server_time|date:"r"}}</td>
    </tr>
  </table>
</div>
{% if unicode_hint %}
<div id="unicode-hint">
    <h2>Unicode error hint</h2>
    <p>The string that could not be encoded/decoded was: <strong>{{ unicode_hint|force_escape }}</strong></p>
</div>
{% endif %}
{% if template_does_not_exist %}
<div id="template-not-exist">
    <h2>Template-loader postmortem</h2>
    {% if loader_debug_info %}
        <p>Django tried loading these templates, in this order:</p>
        <ul>
        {% for loader in loader_debug_info %}
            <li>Using loader <code>{{ loader.loader }}</code>:
                <ul>{% for t in loader.templates %}<li><code>{{ t.name }}</code> (File {% if t.exists %}exists{% else %}does not exist{% endif %})</li>{% endfor %}</ul>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Django couldn't find any templates because your <code>TEMPLATE_LOADERS</code> setting is empty!</p>
    {% endif %}
</div>
{% endif %}
{% if template_info %}
<div id="template">
   <h2>Error during template rendering</h2>
   <p>In template <code>{{ template_info.name }}</code>, error at line <strong>{{ template_info.line }}</strong></p>
   <h3>{{ template_info.message }}</h3>
   <table class="source{% if template_info.top %} cut-top{% endif %}{% ifnotequal template_info.bottom template_info.total %} cut-bottom{% endifnotequal %}">
   {% for source_line in template_info.source_lines %}
   {% ifequal source_line.0 template_info.line %}
       <tr class="error"><th>{{ source_line.0 }}</th>
       <td>{{ template_info.before }}<span class="specific">{{ template_info.during }}</span>{{ template_info.after }}</td></tr>
   {% else %}
      <tr><th>{{ source_line.0 }}</th>
      <td>{{ source_line.1 }}</td></tr>
   {% endifequal %}
   {% endfor %}
   </table>
</div>
{% endif %}
{% if frames %}
<div id="traceback">
  <h2>Traceback <span class="commands">{% if not is_email %}<a href="#" onclick="return switchPastebinFriendly(this);">Switch to copy-and-paste view</a></span>{% endif %}</h2>
  {% autoescape off %}
  <div id="browserTraceback">
    <ul class="traceback">
      {% for frame in frames %}
        <li class="frame {{ frame.type }}">
          <code>{{ frame.filename|escape }}</code> in <code>{{ frame.function|escape }}</code>

          {% if frame.context_line %}
            <div class="context" id="c{{ frame.id }}">
              {% if frame.pre_context and not is_email %}
                <ol start="{{ frame.pre_context_lineno }}" class="pre-context" id="pre{{ frame.id }}">{% for line in frame.pre_context %}<li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ line|escape }}</pre></li>{% endfor %}</ol>
              {% endif %}
              <ol start="{{ frame.lineno }}" class="context-line"><li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ frame.context_line|escape }}</pre>{% if not is_email %} <span>...</span>{% endif %}</li></ol>
              {% if frame.post_context and not is_email  %}
                <ol start='{{ frame.lineno|add:"1" }}' class="post-context" id="post{{ frame.id }}">{% for line in frame.post_context %}<li onclick="toggle('pre{{ frame.id }}', 'post{{ frame.id }}')"><pre>{{ line|escape }}</pre></li>{% endfor %}</ol>
              {% endif %}
            </div>
          {% endif %}

          {% if frame.vars %}
            <div class="commands">
                {% if is_email %}
                    <h2>Local Vars</h2>
                {% else %}
                    <a href="#" onclick="return varToggle(this, '{{ frame.id }}')"><span>&#x25b6;</span> Local vars</a>
                {% endif %}
            </div>
            <table class="vars" id="v{{ frame.id }}">
              <thead>
                <tr>
                  <th>Variable</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                {% for var in frame.vars|dictsort:"0" %}
                  <tr>
                    <td>{{ var.0|force_escape }}</td>
                    <td class="code"><pre>{{ var.1 }}</pre></td>
                  </tr>
                {% endfor %}
              </tbody>
            </table>
          {% endif %}
        </li>
      {% endfor %}
    </ul>
  </div>
  {% endautoescape %}
  <form action="http://dpaste.com/" name="pasteform" id="pasteform" method="post">
{% if not is_email %}
  <div id="pastebinTraceback" class="pastebin">
    <input type="hidden" name="language" value="PythonConsole">
    <input type="hidden" name="title" value="{{ exception_type|escape }}{% if request %} at {{ request.path_info|escape }}{% endif %}">
    <input type="hidden" name="source" value="Django Dpaste Agent">
    <input type="hidden" name="poster" value="Django">
    <textarea name="content" id="traceback_area" cols="140" rows="25">
Environment:

{% if request %}
Request Method: {{ request.META.REQUEST_METHOD }}
Request URL: {{ request.build_absolute_uri|escape }}
{% endif %}
Django Version: {{ django_version_info }}
Python Version: {{ sys_version_info }}
Installed Applications:
{{ settings.INSTALLED_APPS|pprint }}
Installed Middleware:
{{ settings.MIDDLEWARE_CLASSES|pprint }}

{% if template_does_not_exist %}Template Loader Error:
{% if loader_debug_info %}Django tried loading these templates, in this order:
{% for loader in loader_debug_info %}Using loader {{ loader.loader }}:
{% for t in loader.templates %}{{ t.name }} (File {% if t.exists %}exists{% else %}does not exist{% endif %})
{% endfor %}{% endfor %}
{% else %}Django couldn't find any templates because your TEMPLATE_LOADERS setting is empty!
{% endif %}
{% endif %}{% if template_info %}
Template error:
In template {{ template_info.name }}, error at line {{ template_info.line }}
   {{ template_info.message }}{% for source_line in template_info.source_lines %}{% ifequal source_line.0 template_info.line %}
   {{ source_line.0 }} : {{ template_info.before }} {{ template_info.during }} {{ template_info.after }}
{% else %}
   {{ source_line.0 }} : {{ source_line.1 }}
{% endifequal %}{% endfor %}{% endif %}
Traceback:
{% for frame in frames %}File "{{ frame.filename|escape }}" in {{ frame.function|escape }}
{% if frame.context_line %}  {{ frame.lineno }}. {{ frame.context_line|escape }}{% endif %}
{% endfor %}
Exception Type: {{ exception_type|escape }}{% if request %} at {{ request.path_info|escape }}{% endif %}
Exception Value: {{ exception_value|force_escape }}
</textarea>
  <br><br>
  <input type="submit" value="Share this traceback on a public Web site">
  </div>
</form>
</div>
{% endif %}
{% endif %}

<div id="requestinfo">
  <h2>Request information</h2>

{% if request %}
  <h3 id="get-info">GET</h3>
  {% if request.GET %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.GET.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No GET data</p>
  {% endif %}

  <h3 id="post-info">POST</h3>
  {% if filtered_POST %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in filtered_POST.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No POST data</p>
  {% endif %}
  <h3 id="files-info">FILES</h3>
  {% if request.FILES %}
    <table class="req">
        <thead>
            <tr>
                <th>Variable</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
            {% for var in request.FILES.items %}
                <tr>
                    <td>{{ var.0 }}</td>
                    <td class="code"><pre>{{ var.1|pprint }}</pre></td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
  {% else %}
    <p>No FILES data</p>
  {% endif %}


  <h3 id="cookie-info">COOKIES</h3>
  {% if request.COOKIES %}
    <table class="req">
      <thead>
        <tr>
          <th>Variable</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {% for var in request.COOKIES.items %}
          <tr>
            <td>{{ var.0 }}</td>
            <td class="code"><pre>{{ var.1|pprint }}</pre></td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No cookie data</p>
  {% endif %}

  <h3 id="meta-info">META</h3>
  <table class="req">
    <thead>
      <tr>
        <th>Variable</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in request.META.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% else %}
  <p>Request data not supplied</p>
{% endif %}

  <h3 id="settings-info">Settings</h3>
  <h4>Using settings module <code>{{ settings.SETTINGS_MODULE }}</code></h4>
  <table class="req">
    <thead>
      <tr>
        <th>Setting</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      {% for var in settings.items|dictsort:"0" %}
        <tr>
          <td>{{ var.0 }}</td>
          <td class="code"><pre>{{ var.1|pprint }}</pre></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>

</div>
{% if not is_email %}
  <div id="explanation">
    <p>
      You're seeing this error because you have <code>DEBUG = True</code> in your
      Django settings file. Change that to <code>False</code>, and Django will
      display a standard 500 page.
    </p>
  </div>
{% endif %}
</div>
"""

class ExceptionReporter(DjangoExceptionReporter):
    def get_traceback_ampcms_html(self):
        "Return HTML version of debug 500 HTTP error page."
        t = Template(TECHNICAL_500_TEMPLATE, name='Technical 500 template')
        c = Context(self.get_traceback_data())
        return t.render(c)

def technical_500_response(request, exc_type, exc_value, tb):
    """
    Create a technical server error response. The last three arguments are
    the values returned from sys.exc_info() and friends.
    """
    reporter = ExceptionReporter(request, exc_type, exc_value, tb)
    if request.is_ajax() and settings.AMPCMS_USE_AMPCMS_DEBUG:
        return HttpResponseServerError(reporter.get_traceback_ampcms_html(), mimetype='text/html')
    else:
        from django.views import debug as django_debug
        return django_debug.technical_500_response(request, exc_type, exc_value, tb)
