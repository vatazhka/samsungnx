nxCameras = {
	'SAMSUNG NX300': 'NX300',
	'SAMSUNG NX2000': 'NX2000',
	'SAMSUNG NX300M': 'NX300M',
	'SAMSUNG NX30': 'NX30',
	'SAMSUNG NX3000': 'NX3000'}

nxLenses = {
	'XL1302': '10mm fisheye',
	'XL1102': '16mm',
	'XL1016': '20mm',
	'XL1012': '30mm',
#	'': '45mm',
	'XL1202': '45mm 2D/3D',
#	'': '60mm macro',
	'XL1103': '85mm',
	'XL1203': '12-24mm',
	'XL1301': '16-50mm S',
	'XL1401': '16-50mm PZ',
	'XL1013': '18-55mm-I',
	'XL1013i': '18-55mm-II_iFn',
	'XL1205': '18-55mm-III_iFn',
	'XL1015': '20-50mm-I',
	'XL1206': '20-50mm-II',
	'XL1017': '18-200mm',
	'XL1014': '50-200mm-I',
	'XL1014i': '50-200mm-II_iFn'}

class iLauncher:
	
	def __init__(self):
		
		from urllib import urlopen
		samsung_response = urlopen('http://www.samsungimaging.com/customer/data/ilauncher/win/server_version.xml')
		
		import defusedxml
		from defusedxml.ElementTree import parse
		iLauncher = parse(samsung_response).getroot()
		self.version = iLauncher.find('version').text
		self.url = iLauncher.find('setupFile/url').text
		self.date = iLauncher.find('desc').text

class SamsungFirmware:
	
	def __init__(self, model):
		
		from urllib import urlencode
		samsung_parameters = urlencode([
			('prd_mdl_name', model),
			('loc', 'global')])
		from urllib import urlopen
		samsung_response = urlopen("http://www.samsungimaging.com/common/support/firmware/downloadUrlList.do?%s" % samsung_parameters)
		
		import defusedxml
		from defusedxml.ElementTree import parse
		firmware = parse(samsung_response).getroot()
		self.version = firmware.find('FWVersion').text
		self.url = firmware.find('DownloadURL').text
		self.changelog = firmware.find('Description').text

def app(environ, start_response):
	
	body = """<html><head><script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55369806-1', 'auto');
  ga('send', 'pageview');

</script></head><body>"""
	
	body += """<h1>Is your Samsung NX camera and lens up-to-date?</h1>"""
	
	if environ['PATH_INFO'] == '/check':
		
		# check route
		
		from cgi import parse_qs, escape;
		parameters = parse_qs(environ['QUERY_STRING'])
		product = escape(parameters.get('product', [''])[0])
		
		t = SamsungFirmware(product)
		if (t.version is None) or (t.url is None) or (t.changelog is None):
			body += """<p>No firmware file was available at this time. Please try again later - there's nothing I can do about it!</p>"""
		else:
			body += """<p>The current firmware version is <a href=\"""" + t.url + """\">""" + t.version + """</a>. """
			body += """Please download this file, unzip it and place the resulting BIN file in the topmost folder of your memory card.</p>"""
			body += """<p>Next, ensure that your camera has been fully charged, then choose relevant option from the menu to update your camera/lens firmware.</p>"""
			body += """<p>Please note that you won't be able to downgrade firmware of your camera/lens by following this procedure!</p>"""
			body += """<p><pre>""" + t.changelog + """</pre></p>"""
		del t
		
		body += """<p><a href=\"/\">Back</a></p>"""
		
		# end check route
		
	else:
		
		# default route
		
		t = iLauncher()
#		if (t.version is None) or (t.url is None) or (t.date is None):
		body += """<p>The current version of iLauncher for Windows is <a href=\"""" + str(t.url) + """\">""" + str(t.version) + """</a> released on """ + str(t.date)
		body += """, but the good news is that you don't need to use it anymore.</p>"""
		del t
		
		body += """<p><form action=\"/check\" method=\"get\">Choose a product: <select name=\"product\" required><optgroup label=\"NX Cameras\">"""
		for product, model in nxCameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup><optgroup label=\"NX Lenses\">"""
		for product, model in nxLenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body +="""</optgroup></select><input type=\"submit\" value=\"Check\"></form></p>"""
		
		# end default route
	
	body += """</body></html>"""
	
	body = body.encode('utf-8')
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
