NX_www_cameras = {
	'EV-NX5ZZZBABGB': 'NX5',
	'EV-NX10ZZBABGB': 'NX10',
	'EV-NX11ZZBABGB': 'NX11',
	'EV-NX100ZBABGB': 'NX100',
	'EV-NX20ZZBSBGB': 'NX20',
	'EV-NX200ZBABGB': 'NX200',
	'EV-NX210ZBSBGB': 'NX210',
	'EV-NX1000BABGB': 'NX1000',
	'EV-NX1100BABGB': 'NX1100',
	'EV-NX2000BABGB': 'NX2000',
	'EV-NX300ZBATGB': 'NX300',
	'EV-NX30ZZBZBGB': 'NX30',
	'EV-NX300MBSTDE': 'NX300M',
	'EV-NX3000BOHGB': 'NX3000',
}

NX_www_lenses = {
	'EX-F10ANB': '10mm F3.5 Fisheye',
	'EX-W16ANB': '16mm F2.4 Ultra Wide Pancake',
	'EX-W20NB': '20mm F2.8 Pancake',
	'EX-S30NB': '30mm F2.0 Pancake',
	'EX-S45ANB': '45mm F1.8',
	'EX-S45ADB': '45mm F1.8 2D/3D',
	'EX-M60SB': '60mm F2.8 Macro ED OIS SSA',
	'EX-T85NB': '85mm F1.4 ED SSA',
	'EX-W1224ANB': '12-24mm F4.0-5.6 ED',
	'EX-S1650ASB': '16-50mm F2.0-2.8 S ED OIS',
	'EX-ZP1650ZABEP': '16-50mm F3.5-5.6 Power Zoom ED OIS',
	'EX-S1855SB': '18-55mm F3.5-5.6 OIS',
	'EX-S1855IB': '18-55mm F3.5-5.6 OIS II',
	'EX-S1855CSB': '18-55mm F3.5-5.6 OIS III',
	'EX-S2050NB': '20-50mm F3.5-5.6 ED',
	'EX-S2050BNB': '20-50mm F3.5-5.6 ED II',
	'EX-L18200MB': '18-200mm F3.5-6.3 ED OIS',
	'EX-T50200SB': '50-200mm F4.0-5.6 OIS ED',
	'EX-T50200IB': '50-200mm F4.0-5.6 OIS ED II',
	'EX-T50200CSB': '50-200mm F4.0-5.6 OIS ED III',
#	'': '50-150mm F2.8 S ED OIS',
}

NX_M_www_cameras = {
	'EV-NXF1ZZB1IGB': 'NX Mini',
}

NX_M_www_lenses = {
	'EX-YZ927ZZASEP': '9-27mm F3.5-5.6 ED OIS',
	'EX-YN9ZZZZASEP': '9mm F3.5 ED',
	'EX-YN17ZZZASEP': '17mm F1.8 OIS',
}

NX_iLauncher_cameras = {
	'SAMSUNG NX300': 'NX300',
	'SAMSUNG NX2000': 'NX2000',
	'SAMSUNG NX300M': 'NX300M',
	'SAMSUNG NX30': 'NX30',
	'SAMSUNG NX3000': 'NX3000',
	'SAMSUNG NX1': 'NX1',
}

NX_iLauncher_lenses = {
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

NX_M_iLauncher_cameras = {
	'SAMSUNG NXmini': 'NX Mini',
}

NX_M_iLauncher_lenses = {
	'XM1403': '9-27mm F3.5-5.6 ED OIS',
	'XM1404': '9mm F3.5 ED',
	'XM1405': '17mm F1.8 OIS',
}

class iLauncher:
	
	def __init__(self, platform):
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsungimaging.com/customer/data/ilauncher/' + platform + '/server_version.xml')
			
			import defusedxml
			from defusedxml.ElementTree import parse
			iLauncher = parse(response).getroot()
			self.version = iLauncher.find('version').text
			self.url = iLauncher.find('setupFile/url').text
			self.date = iLauncher.find('desc').text
		except:
			pass

class SamsungFirmware:
	
	def __init__(self, product):
		
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsungimaging.com/common/support/firmware/downloadUrlList.do?loc=global&prd_mdl_name=' + product)
			import defusedxml
			from defusedxml.ElementTree import parse
			firmware = parse(response).getroot()
			self.version = firmware.find('FWVersion').text
			self.url = firmware.find('DownloadURL').text
			self.changelog = firmware.find('Description').text
		except:
			pass

class SamsungDownloads:
	
	def __init__(self, model):
		
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsung.com/uk/api/support/download/' + model + '?mType=xml')
			import defusedxml
			from defusedxml.ElementTree import parse
			firmware = parse(response).getroot().find('fmDownloadFileList')
			for download in firmware.findall('downloadFile'):
#				if 'Firmware File' in download.find('localDownloadFile/description').text or 'Upgrade File' in download.find('localDownloadFile/description').text:
				if 'Firmware' in download.find('localDownloadFile/NMCTTType').text:
					self.url = download.find('downloadUrl').text
					self.version = download.find('localDownloadFile/CTTVersion').text
					self.changelog = download.find('localDownloadFile/descFileEng').text
					break
		except:
			pass

def app(environ, start_response):
	
	body = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
<title>Samsung NX / NX Mini firmware check</title>
<script type="text/javascript">
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

h3 {
	font-size: 100%;
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

select {
	width: 37.5%;
}
</style>
</head>
<body>"""
	
	body += """<h1>Is your Samsung NX / NX Mini camera and lens up-to-date?</h1>"""
	
	if environ['PATH_INFO'] == '/check':
		
		# check route
		
		from cgi import parse_qs, escape;
		parameters = parse_qs(environ['QUERY_STRING'])
		product = escape(parameters.get('product', [''])[0])
		model = escape(parameters.get('model', [''])[0])
		
		if len(product) > 0:
			t = SamsungFirmware(product)
		elif len(model) > 0:
			t = SamsungDownloads(model)
		
		try:
			body += """<h2>The current firmware version is """ + escape(t.version.encode('utf-8')) + """.</h2>"""
			body += """<p>Manual upgrade is very easy to perform! First, download <a href=\"""" + escape(t.url.encode('utf-8')) + """\">this</a> file. """
			body += """Unzip it and place the resulting <em>.bin</em> file in the topmost folder of your memory card. """
			body += """Next, ensure that your camera has been fully charged, then choose relevant option from the menu to update your camera/lens firmware.</p>"""
			body += """<p>Please note that you won't be able to downgrade firmware of your camera/lens by following this procedure!</p>"""
			body += """<h2>Changelog</h2>"""
			body += """<pre>""" + t.changelog.encode('utf-8') + """</pre>""" # There's deliberately no quoting! It's not safe!!!
		except:
			body += """<h2>No firmware file is available at this time.</h2>"""
			body += """<p>There's nothing I can do about it, please try again later.</p>"""
		
		body += """<p><a href=\"/\">Go back to the product selection page</a></p>"""
		
		# end check route
		
	else:
		
		# default route
		
		from cgi import escape;
		body += """<h2>Samsung wants you to use the iLauncher software...</h2>"""
		t = iLauncher('win')
		if (t.version is not None) or (t.url is not None) or (t.date is not None):
			body += """<p>The current version of iLauncher for Windows is <a href=\"""" + escape(t.url.encode('utf-8')) + """\">""" + escape(t.version.encode('utf-8')) + """</a>"""
			body += """ released on """ + escape(t.date.encode('utf-8')) + """.</p>"""
		del t
		t = iLauncher('mac')
		if (t.version is not None) or (t.url is not None) or (t.date is not None):
			body += """<p>The current version of iLauncher for OS X is <a href=\"""" + escape(t.url.encode('utf-8')) + """\">""" + escape(t.version.encode('utf-8')) + """</a>"""
			body += """ released on """ + escape(t.date.encode('utf-8')) + """.</p>"""
		del t
		
		body += """<h2>... but why not update your camera and/or lens manually?</h2>"""
		
		body += """<h3>Primary method</h3>"""
		body += """<p>This method uses the iLauncher backend.</p>"""
		
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"product\">"""
		body += """<optgroup label=\"NX Cameras\">"""
		for product, model in NX_iLauncher_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX Lenses\">"""
		for product, model in NX_iLauncher_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Cameras\">"""
		for product, model in NX_M_iLauncher_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Lenses\">"""
		for product, model in NX_M_iLauncher_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """</select>&nbsp;<input type=\"submit\" value=\"Check\"></p></form>"""
		
		body += """<h3>Alternative method</h3>"""
		body += """<p>This method uses the Samsung web page backend.</p>"""
		
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"model\">"""
		body += """<optgroup label=\"NX Cameras\">"""
		for product, model in NX_www_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX Lenses\">"""
		for product, model in NX_www_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Cameras\">"""
		for product, model in NX_M_www_cameras.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Lenses\">"""
		for product, model in NX_M_www_lenses.iteritems():
			body += """<option value=\"""" + product + """\">""" + model + """</option>"""
		body += """</optgroup>"""
		body += """</select>&nbsp;<input type=\"submit\" value=\"Check\"></p></form>"""

		
		# end default route
		
	body += """</body>
</html>"""
	
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
