class iLauncher:
    
    def __init__(self):
	
	import urllib
	samsung_response = urllib.urlopen('http://www.samsungimaging.com/customer/data/ilauncher/win/server_version.xml')
	
	import defusedxml
	from defusedxml.ElementTree import parse
	iLauncher = parse(samsung_response).getroot()
	self.version = iLauncher.find('version').text
	self.url = iLauncher.find('setupFile/url').text
	self.date = iLauncher.find('desc').text

class CameraFirmware:
    
    def __init__(self, model):
	
	import urllib
	samsung_parameters = urllib.urlencode([
	    ('prd_mdl_name', model),
	    ('loc', 'global')
	    ])
	samsung_response = urllib.urlopen("http://www.samsungimaging.com/common/support/firmware/downloadUrlList.do?%s" % samsung_parameters)
	
	import defusedxml
	from defusedxml.ElementTree import parse
	firmware = parse(samsung_response).getroot()
	self.version = firmware.find('FWVersion').text
	self.url = firmware.find('DownloadURL').text
	self.changelog = firmware.find('Description').text

def app(environ, start_response):
    
    data = '<html><body>'
    
    data += """<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55369806-1', 'auto');
  ga('send', 'pageview');

</script>"""
    
    t = iLauncher()
    data += 'The current version of iLauncher is <a href="' + t.url + '">' + t.version + '</a> released on ' + t.date + '.<hr>'
    
    product_models = [
    'SAMSUNG NX300',
    'SAMSUNG NX2000',
    'SAMSUNG NX300M',
    'SAMSUNG NX30',
    'SAMSUNG NX3000'
    ]
    
    for model in product_models:
	t = CameraFirmware(model)
	data += '<p>The current firmware version of '+ model + ' is <a href="' + t.url + '">' + t.version + '</a>:<pre>' + t.changelog + '</pre></p><hr>'
    
    data += '</body></html>'
    
    start_response('200 OK', [
	('Content-Type', 'text/html'),
	('Content-Length', str(len(data)))
	])
    
    return iter([data])
