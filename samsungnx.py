class SamsungSoftware:
	
	def reset(self):
		
		self.version = None
		self.url = None
		self.date = None
	
	def __init__(self, software, platform):
		
		self.reset()
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsungimaging.com/customer/data/' + software + '/' + platform + '/server_version.xml')
			import defusedxml
			from defusedxml.ElementTree import parse
			software = parse(response).getroot()
			self.version = software.find('version').text
			self.url = software.find('setupFile/url').text
			self.date = software.find('desc').text
			from urlparse import urlparse
			url = urlparse(self.url)
			if (url.scheme != 'http') and (url.scheme != 'https'):
				self.reset()
		except:
			self.reset()

class QueryiLauncher:
	
	def reset(self):
		
		self.version = None
		self.url = None
		self.changelog = None
	
	def __init__(self, product):
		
		self.reset()
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsungimaging.com/common/support/firmware/downloadUrlList.do?loc=global&prd_mdl_name=' + product)
			import defusedxml
			from defusedxml.ElementTree import parse
			firmware = parse(response).getroot()
			self.version = firmware.find('FWVersion').text
			if self.version == '-1':
				self.reset()
			else:
				self.url = firmware.find('DownloadURL').text
				self.changelog = firmware.find('Description').text
		except:
			self.reset()

class QueryUKWebsite:
	
	def reset(self):
		
		self.version = None
		self.url = None
		self.changelog = None
	
	def __init__(self, model):
		
		self.reset()
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsung.com/uk/api/support/download/' + model + '?mType=xml')
			import defusedxml
			from defusedxml.ElementTree import parse
			firmware = parse(response).getroot().find('fmDownloadFileList')
			for download in firmware.findall('downloadFile'):
				title = download.find('localDownloadFile/NMCTTType').text.lower()
				extension = download.find('fileExt').text.lower()
				description = download.find('localDownloadFile/description').text.lower()
				if ('firmware' in title or 'upgrade' in title) and 'zip' in extension and 'lens' not in description:
					self.url = download.find('downloadUrl').text
					self.version = download.find('localDownloadFile/CTTVersion').text
					self.changelog = download.find('localDownloadFile/descFileEng').text.replace('<br>', '\n').replace('&gt;','>').replace('&lt;','<')
					break
				elif ('firmware' in title or 'upgrade' in title) and 'zip' in extension:
					self.url = download.find('downloadUrl').text
					self.version = download.find('localDownloadFile/CTTVersion').text
					self.changelog = download.find('localDownloadFile/descFileEng').text.replace('<br>', '\n').replace('&gt;','>').replace('&lt;','<')
		except:
			self.reset()

def app(environ, start_response):
	
	body = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
<title>Samsung NX / NX Mini firmware check</title>
<link rel="icon" type="image/png" href="https://www.samsung.com/global/microsite/SAMSUNGCAMERA/mobile/img/feature/nx_icon.png">
<script type=\"text/javascript\">
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-55369806-1', 'auto');
  ga('send', 'pageview');

</script>
<style media=\"screen\" type=\"text/css\">
* {
	font-family: Arial, Helvetica, sans-serif;
	text-decoration: none;
}

body {
	margin-top: 2.5%;
	margin-bottom: 2.5%;
	margin-left: 12.5%;
	margin-right: 12.5%;
	font-size: 12pt;
	text-align: center;
}

h1 {
	font-size: 200%;
	font-weight: normal;
	margin-top: 1em;
	margin-bottom: 1em;
}

h2 {
	font-size: 150%;
	font-weight: normal;
	margin-top: 1em;
	margin-bottom: 1em;
}

h3 {
	font-size: 125%;
	font-weight: normal;
	margin-top: 1em;
	margin-bottom: 1em;
}

p {
	margin-top: 1em;
	margin-bottom: 1em;
}

p.footer {
	margin-top: 3em;
	margin-bottom: 3em;
}

p.copyright {
	margin-top: 6em;
	font-size: 50%;
}

pre {
	margin-left: 25%;
	margin-right: 25%;
	margin-top: 1em;
	margin-bottom: 1em;
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
<body>
"""
	
	body += """<h1>Is your Samsung NX / NX Mini camera and lens up-to-date?</h1>\n"""
	
	if environ['PATH_INFO'] == '/check':
		
		# check route
		
		from cgi import parse_qs, escape
		parameters = parse_qs(environ['QUERY_STRING'])
		product = escape(parameters.get('product', [''])[0])
		model = escape(parameters.get('model', [''])[0])
		
		if len(product) > 0:
			t = QueryiLauncher(product)
		elif len(model) > 0:
			t = QueryUKWebsite(model)
		
		try:
			body += """<h2>The current firmware version is """ + escape(t.version.encode('utf-8')) + """.</h2>"""
			body += """<p>Manual upgrade is very easy to perform! First, download <a href=\"""" + escape(t.url.encode('utf-8')) + """\">this</a> file. """
			body += """If it's a <em>.zip</em> file, unzip it. Then, place the resulting <em>.bin</em> file in the topmost folder of your memory card. """
			body += """Next, ensure that your camera has been fully charged, then choose relevant option from the menu to update your camera/lens firmware.</p>"""
			body += """<p>Please note that you won't be able to downgrade firmware of your camera/lens by following this procedure!</p>\n"""
			body += """<p>Please also note that the firmware file has been directly provided by Samsung - I do not host any firmware files!</p>\n"""
			body += """<h2>Changelog</h2>\n"""
			body += """<pre>""" + escape(t.changelog.encode('utf-8')) + """</pre>\n"""
		except:
			body += """<h2>No firmware file is available at this time.</h2>\n"""
			body += """<p>There's nothing I can do about it, please try again later.</p>\n"""
		
		body += """<p class=\"footer\"><a href=\"/\">Go back to the product selection page</a></p>\n"""
		
		# end check route
		
	elif environ['PATH_INFO'] == '/software':
		
		# software route
		
		body += """<h2>Download software directly from Samsung</h2>\n"""
		body += """<p>Please note that the links below have been directly provided by Samsung - I do not host any software downloads!</p>\n"""
		
		Software = [
			['i-Launcher', 'ilauncher'],
			['DNG Converter', 'dngconverter'],
			['Movie Converter', 'movieconverter'],
			['PC Auto Backup', 'autobackup'],
			['Remote Studio', 'remotestudio']
		]
		
		Platforms = [
			['Windows', 'win'],
			['OS X', 'mac']
		]
		
		from cgi import escape
		for j in Software:
			body += """<h3>""" + j[0] + """</h3>\n"""
			for i in Platforms:
				t = SamsungSoftware(j[1], i[1])
				if (t.version is not None) or (t.url is not None) or (t.date is not None):
					body += """<p><a href=\"""" + escape(t.url.encode('utf-8')) + """\">""" + j[0] + """ for """ + i[0] + """ """ + escape(t.version.encode('utf-8')) + """</a>"""
					body += """ was released on """ + escape(t.date.encode('utf-8')) + """.</p>\n"""
				else:
					body += """<p>""" + j[0] + """ for """ + i[0] + """ was not released (yet).</p>\n"""
				del t
		
		body += """<p class=\"footer\"><a href=\"/\">Go back to the main page</a></p>\n"""
		
		# end software route
		
	else:
		
		# default route
		
		body += """<h2>Firmware updates</h2>\n"""
		body += """<p>The methods appear in order of preference.  The results may differ between methods.</p>\n"""
		
		NX_cameras = [
			['NX10', '', 'EV-NX10ZZBABGB'],
			['NX5', '', 'EV-NX5ZZZBABGB'],
			['NX100', '', 'EV-NX100ZBABGB'],
			['NX11', '', 'EV-NX11ZZBABGB'],
			['NX200', '', 'EV-NX200ZBABGB'],
			['NX20', '', 'EV-NX20ZZBSBGB'],
			['NX210', '', 'EV-NX210ZBSBGB'],
			['NX1000', '', 'EV-NX1000BABGB'],
			['NX300', 'SAMSUNG NX300', 'EV-NX300ZBATGB'],
			['NX1100', '', 'EV-NX1100BABGB'],
			['NX2000', 'SAMSUNG NX2000', 'EV-NX2000BABGB'],
			['NX300M', 'SAMSUNG NX300M', 'EV-NX300MBSTDE'],
			['NX30', 'SAMSUNG NX30', 'EV-NX30ZZBZBGB'],
			['NX3000', 'SAMSUNG NX3000', 'EV-NX3000BOHGB'],
			['NX1', 'SAMSUNG NX1', 'EV-NX1ZZZBZBGB'],
			['NX500', 'SAMSUNG NX500', 'EV-NX500ZBMIGB'],
			['NX3300', 'SAMSUNG NX3300', 'EV-NX3300BOBGB']
		]
		
		NX_lenses = [
			['10mm F3.5 Fisheye', 'XL1302', 'EX-F10ANB'],
			['16mm F2.4 Ultra-Wide Pancake', 'XL1102', 'EX-W16ANB'],
			['20mm F2.8 Wide Pancake', 'XL1016', 'EX-W20NB'],
			['30mm F2.0 Standard Pancake', 'XL1012', 'EX-S30NB'],
			['45mm F1.8 Mid-Telephoto', 'XL1201', 'EX-S45ANB'],
			['45mm F1.8 2D/3D Mid-Telephoto', 'XL1202', 'EX-S45ADB'],
			['60mm F2.8 ED OIS SSA Tele Macro', 'XL1101', 'EX-M60SB'],
			['85mm F1.4 ED SSA Premium Portrait', 'XL1103', 'EX-T85NB'],
			['12-24mm F4.0-5.6 ED Compact Wide Zoom', 'XL1203', 'EX-W1224ANB'],
			['16-50mm F2.0-2.8 S ED OIS Professional Standard Zoom', 'XL1301', 'EX-S1650ASB'],
			['16-50mm F3.5-5.6 ED OIS Standard Power Zoom', 'XL1401', 'EX-ZP1650ZABEP'],
			['20-50mm F3.5-5.6 ED Compact Standard Zoom', 'XL1015', 'EX-S2050NB'],
			['20-50mm F3.5-5.6 ED II Compact Standard Zoom', 'XL1206', 'EX-S2050BNB'],
			['18-55mm F3.5-5.6 OIS Standard Zoom', 'XL1013', 'EX-S1855SB'],
			['18-55mm F3.5-5.6 OIS II Standard Zoom', 'XL1013i', 'EX-S1855IB'],
			['18-55mm F3.5-5.6 OIS III Standard Zoom', 'XL1205', 'EX-S1855CSB'],
			['50-150mm F2.8 S ED OIS Professional Tele Zoom', 'XL1406', 'EX-ZS50150ABEP'],
			['50-200mm F4.0-5.6 OIS ED Tele Zoom', 'XL1014', 'EX-T50200SB'],
			['50-200mm F4.0-5.6 OIS ED II Tele Zoom', 'XL1014i', 'EX-T50200IB'],
			['50-200mm F4.0-5.6 OIS ED III Tele Zoom', 'XL1014i2', 'EX-T50200CSB'],
			['18-200mm F3.5-6.3 ED OIS Long Zoom', 'XL1017', 'EX-L18200MB']
		]
		
		NX_M_cameras = [
			['NX Mini', 'SAMSUNG NXmini', 'EV-NXF1ZZB1IGB']
		]
		
		NX_M_lenses = [
			['9mm F3.5 ED Wide Prime', 'XM1404', 'EX-YN9ZZZZASEP'],
			['17mm F1.8 OIS Large Aperture Prime', 'XM1405', 'EX-YN17ZZZASEP'],
			['9-27mm F3.5-5.6 ED OIS Standard Zoom', 'XM1403', 'EX-YZ927ZZASEP']
		]
		
		body += """<h3>The i-Launcher method</h3>\n"""
		body += """<p>Queries data feed which i-Launcher and newer cameras use.  Does not support older (pre-NX300) cameras.</p>\n"""
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"product\">"""
		body += """<optgroup label=\"NX Cameras\">"""
		for i in NX_cameras:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX Lenses\">"""
		for i in NX_lenses:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Cameras\">"""
		for i in NX_M_cameras:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Lenses\">"""
		for i in NX_M_lenses:
			if len(i[1]) > 0:
				body += """<option value=\"""" + i[1] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """</select>&nbsp;<input type=\"submit\" value=\"Check\"></p></form>\n"""
		
		body += """<h3>The UK Samsung web page method</h3>\n"""
		body += """<p>Queries data feed which the UK Samsung web page uses.  Recommended if the i-Launcher method does not support your gear.</p>\n"""
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"model\">"""
		body += """<optgroup label=\"NX Cameras\">"""
		for i in NX_cameras:
			if len(i[2]) > 0:
				body += """<option value=\"""" + i[2] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX Lenses\">"""
		for i in NX_lenses:
			if len(i[2]) > 0:
				body += """<option value=\"""" + i[2] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Cameras\">"""
		for i in NX_M_cameras:
			if len(i[2]) > 0:
				body += """<option value=\"""" + i[2] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """<optgroup label=\"NX-M Lenses\">"""
		for i in NX_M_lenses:
			if len(i[2]) > 0:
				body += """<option value=\"""" + i[2] + """\">""" + i[0] + """</option>"""
		body += """</optgroup>"""
		body += """</select>&nbsp;<input type=\"submit\" value=\"Check\"></p></form>\n"""
		
		body += """<h2>Software updates</h2>\n"""
		body += """<p>If you insist on using Samsung software, you can download it <a href=\"/software\">here</a>.</p>\n"""
		
		# end default route
		
	body += """<p class=\"copyright\">Copyright &copy; 2014 and 2015 by <a href=\"http://www.dpreview.com/members/4380410987\">vatazhka</a> &reg;</p>\n"""
	body += """</body>
</html>"""
	
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
