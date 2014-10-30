Platforms = [
	['Windows',	'win'],
	['OS X',	'mac'],
]

NX_cameras = [
	['NX10',	'EV-NX10ZZBABGB',	''],
	['NX5',		'EV-NX5ZZZBABGB',	''],
	['NX100',	'EV-NX100ZBABGB',	''],
	['NX11',	'EV-NX11ZZBABGB',	''],
	['NX200',	'EV-NX200ZBABGB',	''],
	['NX20',	'EV-NX20ZZBSBGB',	''],
	['NX210',	'EV-NX210ZBSBGB',	''],
	['NX1000',	'EV-NX1000BABGB',	''],
	['NX300',	'EV-NX300ZBATGB',	'SAMSUNG NX300'],
	['NX1100',	'EV-NX1100BABGB',	''],
	['NX2000',	'EV-NX2000BABGB',	'SAMSUNG NX2000'],
	['NX300M',	'EV-NX300MBSTDE',	'SAMSUNG NX300M'],
	['NX30',	'EV-NX30ZZBZBGB',	'SAMSUNG NX30'],
	['NX3000',	'EV-NX3000BOHGB',	'SAMSUNG NX3000'],
	['NX1',		'EV-NX1ZZZBZBGB',	'SAMSUNG NX1'],
]

NX_lenses = [
	['10mm F3.5 Fisheye',					'EX-F10ANB',		'XL1302'],
	['16mm F2.4 Ultra Wide Pancake',		'EX-W16ANB',		'XL1102'],
	['20mm F2.8 Pancake',					'EX-W20NB',			'XL1016'],
	['30mm F2.0 Pancake',					'EX-S30NB',			'XL1012'],
	['45mm F1.8',							'EX-S45ANB',		'XL1201'],
	['45mm F1.8 2D/3D',						'EX-S45ADB',		'XL1202'],
	['60mm F2.8 Macro ED OIS SSA',			'EX-M60SB',			'XL1101'],
	['85mm F1.4 ED SSA',					'EX-T85NB',			'XL1103'],
	['12-24mm F4.0-5.6 ED',					'EX-W1224ANB',		'XL1203'],
	['16-50mm F2.0-2.8 S ED OIS',			'EX-S1650ASB',		'XL1301'],
	['16-50mm F3.5-5.6 Power Zoom ED OIS',	'EX-ZP1650ZABEP',	'XL1401'],
	['18-55mm F3.5-5.6 OIS',				'EX-S1855SB',		'XL1013'],
	['18-55mm F3.5-5.6 OIS II',				'EX-S1855IB',		'XL1013i'],
	['18-55mm F3.5-5.6 OIS III',			'EX-S1855CSB',		'XL1205'],
	['20-50mm F3.5-5.6 ED',					'EX-S2050NB',		'XL1015'],
	['20-50mm F3.5-5.6 ED II',				'EX-S2050BNB',		'XL1206'],
	['18-200mm F3.5-6.3 ED OIS',			'EX-L18200MB',		'XL1017'],
	['50-200mm F4.0-5.6 OIS ED',			'EX-T50200SB',		'XL1014'],
	['50-200mm F4.0-5.6 OIS ED II',			'EX-T50200IB',		'XL1014i'],
	['50-200mm F4.0-5.6 OIS ED III',		'EX-T50200CSB',		'XL1014i2'],
	['50-150mm F2.8 S ED OIS',				'EX-ZS50150ABEP',	''],
]

NX_M_cameras = [
	['NX Mini',	'EV-NXF1ZZB1IGB',	'SAMSUNG NXmini'],
]

NX_M_lenses = [
	['9mm F3.5 ED',				'EX-YN9ZZZZASEP',	'XM1404'],
	['17mm F1.8 OIS',			'EX-YN17ZZZASEP',	'XM1405'],
	['9-27mm F3.5-5.6 ED OIS',	'EX-YZ927ZZASEP',	'XM1403'],
]

class SamsungSoftware:
	
	def __init__(self, software, platform):
		
		try:
			from urllib import urlopen
			response = urlopen('http://www.samsungimaging.com/customer/data/' + software + '/' + platform + '/server_version.xml')
			
			import defusedxml
			from defusedxml.ElementTree import parse
			software = parse(response).getroot()
			self.version = software.find('version').text
			self.url = software.find('setupFile/url').text
			self.date = software.find('desc').text
		except:
			pass

class SamsungFirmware:
	
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

class SamsungDownloads:
	
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
				title = download.find('localDownloadFile/NMCTTType').text;
				extension = download.find('fileExt').text
				description = download.find('localDownloadFile/description').text;
				if ('firmware' in title.lower() or 'upgrade' in title.lower()) and 'zip' in extension.lower() and 'lens' not in description.lower():
					self.url = download.find('downloadUrl').text
					self.version = download.find('localDownloadFile/CTTVersion').text
					self.changelog = download.find('localDownloadFile/descFileEng').text.replace('<br>', '\n')
					break
				elif ('firmware' in title.lower() or 'upgrade' in title.lower()) and 'zip' in extension.lower():
					self.url = download.find('downloadUrl').text
					self.version = download.find('localDownloadFile/CTTVersion').text
					self.changelog = download.find('localDownloadFile/descFileEng').text.replace('<br>', '\n')
		except:
			self.reset()

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
	text-align: center;
}

body {
	margin-top: 2.5%;
	margin-bottom: 2.5%;
	margin-left: 12.5%;
	margin-right: 12.5%;
}

p {
	margin-top: 1em;
	margin-bottom: 1em;
}

a {
	text-decoration: none;
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
			body += """<p>Please note that you won't be able to downgrade firmware of your camera/lens by following this procedure!</p>\n"""
			body += """<h2>Changelog</h2>\n"""
			body += """<pre>""" + escape(t.changelog.encode('utf-8')) + """</pre>\n"""
		except:
			body += """<h2>No firmware file is available at this time.</h2>\n"""
			body += """<p>There's nothing I can do about it, please try again later.</p>\n"""
		
		body += """<p><a href=\"/\">Go back to the product selection page</a></p>\n"""
		
		# end check route
		
	else:
		
		# default route
		
		from cgi import escape;
		body += """<h2>Samsung wants you to use the i-Launcher software...</h2>\n"""
		for i in Platforms:
			t = SamsungSoftware('ilauncher', i[1])
			if (t.version is not None) or (t.url is not None) or (t.date is not None):
				body += """<p><a href=\"""" + escape(t.url.encode('utf-8')) + """\">i-Launcher for """ + i[0] + """ """ + escape(t.version.encode('utf-8')) + """</a>"""
				body += """ was released on """ + escape(t.date.encode('utf-8')) + """.</p>\n"""
			del t
		
		body += """<h2>... but why not update your camera and/or lens manually?</h2>\n"""
		
		body += """<h3>The i-Launcher method</h3>\n"""
		body += """<p>This method queries the web service which i-Launcher and Tizen-based cameras use.</p>\n"""
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"product\">"""
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
		
		body += """<h3>The Samsung web page method</h3>\n"""
		body += """<p>This method queries the web service which sits behind the Samsung web page.</p>\n"""
		body += """<form action=\"/check\" method=\"get\"><p><select name=\"model\">"""
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
		
		body += """<h2>By the way, if you insist on using the PC Auto Backup software...</h2>\n"""
		for i in Platforms:
			t = SamsungSoftware('autobackup', i[1])
			if (t.version is not None) or (t.url is not None) or (t.date is not None):
				body += """<p><a href=\"""" + escape(t.url.encode('utf-8')) + """\">PC Auto Backup for """ + i[0] + """ """ + escape(t.version.encode('utf-8')) + """</a>"""
				body += """ was released on """ + escape(t.date.encode('utf-8')) + """.</p>\n"""
			del t
		
		# end default route
		
	body += """</body>
</html>"""
	
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'), ('Content-Length', str(len(body)))])
	return [body]
