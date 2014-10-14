NX_cameras = {
	'SAMSUNG NX300': 'NX300',
	'SAMSUNG NX2000': 'NX2000',
	'SAMSUNG NX300M': 'NX300M',
	'SAMSUNG NX30': 'NX30',
	'SAMSUNG NX3000': 'NX3000',
	'SAMSUNG NX1': 'NX1',
}

NX_lenses = {
	'XL1302': '10mm F3.5 Fisheye',
	'XL1102': '16mm F2.4 Ultra Wide Pancake',
	'XL1016': '20mm F2.8 Pancake',
	'XL1012': '30mm F2.0 Pancake',
	'XL1201': '45mm F1.8',
	'XL1202': '45mm F1.8 2D/3D',
	'XL1101': '60mm F2.8 Macro ED OIS SSA',
	'XL1103': '85mm F1.4 ED SSA',
	'XL1203': '12-24mm F4.0-5.6 ED',
	'XL1301': '16-50mm F2.0-2.8 S ED OIS',
	'XL1401': '16-50mm F3.5-5.6 Power Zoom ED OIS',
	'XL1013': '18-55mm F3.5-5.6 OIS',
	'XL1013i': '18-55mm F3.5-5.6 OIS II',
	'XL1205': '18-55mm F3.5-5.6 OIS III',
	'XL1015': '20-50mm F3.5-5.6 ED',
	'XL1206': '20-50mm F3.5-5.6 ED II',
	'XL1017': '18-200mm F3.5-6.3 ED OIS',
	'XL1014': '50-200mm F4.0-5.6 OIS ED',
	'XL1014i': '50-200mm F4.0-5.6 OIS ED II',
	'XL1014i2': '50-200mm F4.0-5.6 OIS ED III',
#	'': '50-150mm F2.8 S ED OIS',
}

NX_M_cameras = {
	'SAMSUNG NXmini': 'NX mini',
}

NX_M_lenses = {
	'XM1403': '9-27mm F3.5-5.6 ED OIS',
	'XM1404': '9mm F3.5 ED',
	'XM1405': '17mm F1.8 OIS',
}

class iLauncher:
	
	def __init__(self, platform):
		
		from urllib import urlopen
		samsung_response = urlopen("http://www.samsungimaging.com/customer/data/ilauncher/%s/server_version.xml" % platform)
		
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
			('loc', 'global'),
		])
		from urllib import urlopen
		samsung_response = urlopen("http://www.samsungimaging.com/common/support/firmware/downloadUrlList.do?%s" % samsung_parameters)
		
		import defusedxml
		from defusedxml.ElementTree import parse
		firmware = parse(samsung_response).getroot()
		self.version = firmware.find('FWVersion').text
		self.url = firmware.find('DownloadURL').text
		self.changelog = firmware.find('Description').text

def app(environ, start_response):
	
	body = """<html><head>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55369806-1', 'auto');
  ga('send', 'pageview');

</script>
<style media="screen" type="text/css">
* {
	font-size: 12pt;
	font-family: Arial, Helvetica, sans-serif;
	line-height: 150%;
	text-align: center;
}

body {
	margin-top: 2.5%;
	margin-bottom: 2.5%;
	margin-left: 12.5%;
	margin-right: 12.5%;
}

a {
	text-decoration: none;
}

h1 {
	font-size: 250%;
	font-weight: normal;
}

h2 {
	font-size: 150%;
	font-weight: normal;
}

pre {
	margin-left: 25%;
	margin-right: 25%;
	overflow: auto;
	white-space: pre-wrap;
	font-size: 75%;
	text-align: left;
}
</style>
</head><body>"""
	
	body += """<h1>Is your Samsung NX / NX mini camera and lens up-to-date?</h1>"""
	
	if environ['PATH_INFO'] == '/check':
		
		# check route
		
		from cgi import parse_qs, escape;
		parameters = parse_qs(environ['QUERY_STRING'])
		product = escape(parameters.get('product', [''])[0])
		
		t = SamsungFirmware(product)
		if (t.version is None) or (t.url is None) or (t.changelog is None):
			body += """<h2>No firmware file is available at this time.</h2>"""
			body += """<p>There's nothing I can do about it, please try again later.</p>"""
		else:
			body += """<h2>The current firmware version is """ + t.version + """.</h2>"""
			body += """<p>Manual upgrade is very easy to perform! First, download <a href=\"""" + t.url + """\">this</a> file. """
			body += """Unzip it and place the resulting <em>.bin</em> file in the topmost folder of your memory card. """
			body += """Next, ensure that your camera has been fully charged, then choose relevant option from the menu to update your camera/lens firmware.</p>"""
			body += """<p>Please note that you won't be able to downgrade firmware of your camera/lens by following this procedure!</p>"""
			body += """<h2>Changelog</h2>"""
			body += """<pre>""" + t.changelog + """</pre>"""
		del t
		
		body += """<p><a href=\"/\">Go back to the product selection page</a></p>"""
		
		# end check route
		
	else:
		
		# default route
		
		body += """<h2>Samsung wants you to use the iLauncher software...</h2>"""
		t = iLauncher('win')
		if (t.version is not None) or (t.url is not None) or (t.date is not None):
			body += """<p>The current version of iLauncher for Windows is <a href=\"""" + str(t.url) + """\">""" + str(t.version) + """</a> released on """ + str(t.date) + """.</p>"""
		del t
		t = iLauncher('mac')
		if (t.version is not None) or (t.url is not None) or (t.date is not None):
			body += """<p>The current version of iLauncher for OS X is <a href=\"""" + str(t.url) + """\">""" + str(t.version) + """</a> released on """ + str(t.date) + """.</p>"""
		del t
		
		body += """<h2>... but why not update your camera and/or lens manually?</h2>"""
		body += """<p><form action=\"/check\" method=\"get\">Choose a product: <select name=\"product\" required>"""
		body += """<optgroup label=\"NX Cameras\">"""
		for product, model in NX_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup><optgroup label=\"NX Lenses\">"""
		for product, model in NX_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup><optgroup label=\"NX-M Cameras\">"""
		for product, model in NX_M_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup><optgroup label=\"NX-M Lenses\">"""
		for product, model in NX_M_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body +="""</optgroup></select><input type=\"submit\" value=\"Check\"></form></p>"""
		
		# end default route
		
	body += """</body></html>"""
	
	body = body.encode('utf-8')
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
