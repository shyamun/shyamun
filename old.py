import qrcode
from flask import Flask, request, redirect, render_template_string
import os
from io import BytesIO
import base64

app = Flask(__name__)

# Your social media links - UPDATE THESE!
INSTAGRAM_URL = "https://www.instagram.com/spicmacaymangalore"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/HaA9oFiRNqe2JgPK8BvLWD?mode=ac_t"

# HTML Template (same as before, condensed for space)
LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPIC MACAY Mangalore</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               color: white; min-height: 100vh; margin: 0; }
        .container { max-width: 400px; margin: 0 auto; background: rgba(255, 255, 255, 0.1); 
                     padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
        .logo { width: 100px; height: 100px; margin: 0 auto 20px; background: white; 
                border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                font-weight: bold; color: #333; }
        .btn { display: inline-block; padding: 15px 30px; margin: 10px; text-decoration: none; 
               border-radius: 25px; font-weight: bold; transition: transform 0.3s; width: 200px; }
        .btn:hover { transform: translateY(-2px); }
        .instagram { background: linear-gradient(45deg, #f09433 0%,#e6683c 25%,#dc2743 50%,#cc2366 75%,#bc1888 100%); color: white; }
        .whatsapp { background: #25D366; color: white; }
        .description { margin: 20px 0; font-size: 16px; line-height: 1.5; }
    </style>
    <script>
        function detectInstagram() {
            const userAgent = navigator.userAgent || navigator.vendor || window.opera;
            const isIOS = /iPad|iPhone|iPod/.test(userAgent);
            
            if (isIOS) {
                window.location.href = "{{ instagram_url }}";
            } else {
                const appURL = "instagram://user?username=spicmacaymangalore";
                window.location.href = appURL;
                setTimeout(function() {
                    window.location.href = "{{ instagram_url }}";
                }, 1500);
            }
        }
        
        function openWhatsApp() {
            window.location.href = "{{ whatsapp_url }}";
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">SPIC MACAY</div>
        <h2>Connect with SPIC MACAY Mangalore</h2>
        <p class="description">Join our community for classical arts, cultural events, and performances!</p>
        
        <div><a href="javascript:detectInstagram()" class="btn instagram">📸 Follow on Instagram</a></div>
        <div><a href="javascript:openWhatsApp()" class="btn whatsapp">💬 Join WhatsApp Group</a></div>
        
        <p style="font-size: 14px; margin-top: 30px; opacity: 0.8;">Scan QR codes around campus to connect!</p>
    </div>
</body>
</html>
"""

@app.route('/')
def landing_page():
    html_content = LANDING_PAGE_HTML.replace('{{ instagram_url }}', INSTAGRAM_URL)
    html_content = html_content.replace('{{ whatsapp_url }}', WHATSAPP_GROUP_URL)
    return render_template_string(html_content)

@app.route('/qr-generator')
def generate_qr():
    """Generate QR code on demand"""
    url = request.args.get('url', request.url_root)
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{img_str}" alt="QR Code"><br><p>QR Code for: {url}</p>'

@app.route('/instagram')
def instagram_redirect():
    return redirect(INSTAGRAM_URL)

@app.route('/whatsapp') 
def whatsapp_redirect():
    return redirect(WHATSAPP_GROUP_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)