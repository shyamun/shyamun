import os
import qrcode
from flask import Flask, request, redirect, render_template_string, send_file
from io import BytesIO
import base64
import zipfile

app = Flask(__name__)

# Your exact URLs
INSTAGRAM_URL = "https://www.instagram.com/spicmacaymangalore"
WHATSAPP_GROUP_URL = "https://chat.whatsapp.com/HaA9oFiRNqe2JgPK8BvLWD?mode=ac_t"

@app.route('/')
def auto_redirect():
    """
    PURE AUTO-REDIRECT - No landing page, direct decision
    """
    try:
        user_agent = request.headers.get('User-Agent', '').lower()
        
        # Device detection
        is_ios = any(device in user_agent for device in ['iphone', 'ipad', 'ipod'])
        is_android = 'android' in user_agent
        is_mobile = is_ios or is_android or 'mobile' in user_agent
        
        if not is_mobile:
            # Desktop → Instagram web
            return redirect(INSTAGRAM_URL)
        
        # Mobile device logic
        if is_android:
            # Android: Try Instagram app with intent
            instagram_intent = "intent://instagram.com/_u/spicmacaymangalore/#Intent;package=com.instagram.android;scheme=https;S.browser_fallback_url=" + WHATSAPP_GROUP_URL + ";end"
            return redirect(instagram_intent)
            
        elif is_ios:
            # iOS: Try Instagram app, but iOS doesn't have good fallback
            # So we use JavaScript detection
            return render_template_string(IOS_DETECTION_PAGE)
        else:
            # Other mobile → WhatsApp
            return redirect(WHATSAPP_GROUP_URL)
            
    except Exception as e:
        # Any error → WhatsApp
        return redirect(WHATSAPP_GROUP_URL)

# Minimal page for iOS detection only
IOS_DETECTION_PAGE = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <style>
        body {{ 
            font-family: Arial; text-align: center; padding: 50px;
            background: #667eea; color: white;
        }}
        .spinner {{ 
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%; width: 40px; height: 40px;
            animation: spin 1s linear infinite; margin: 20px auto;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="spinner"></div>
    <h2>🔄 Connecting...</h2>
    <p>Checking for Instagram app...</p>
    
    <script>
        let redirected = false;
        
        // Try Instagram app
        setTimeout(() => {{
            if (!redirected) {{
                window.location.href = "instagram://user?username=spicmacaymangalore";
            }}
        }}, 500);
        
        // Fallback to WhatsApp after 2 seconds
        setTimeout(() => {{
            if (!redirected) {{
                console.log('Instagram not found, going to WhatsApp app');
                // Try WhatsApp app first, then group link
                window.location.href = "whatsapp://send?text=Join%20SPIC%20MACAY:%20{WHATSAPP_GROUP_URL}";
                
                // Final fallback to group link after 2 more seconds
                setTimeout(() => {{
                    window.location.href = "{WHATSAPP_GROUP_URL}";
                }}, 1000);
            }}
        }}, 1000);
        
        // Listen for visibility change (Instagram opened)
        document.addEventListener('visibilitychange', () => {{
            if (document.hidden) {{
                redirected = true;
                console.log('Instagram app opened');
            }}
        }});
        
        // Listen for page blur (Instagram opened)
        window.addEventListener('blur', () => {{
            redirected = true;
            console.log('App opened via blur');
        }});
    </script>
</body>
</html>
"""

# WhatsApp Desktop Page Template
WHATSAPP_DESKTOP_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join SPIC MACAY WhatsApp Group</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
            color: white;
            min-height: 100vh;
            margin: 0;
        }}
        .container {{
            max-width: 500px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .whatsapp-logo {{
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }}
        .btn {{
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            color: white;
            font-size: 16px;
        }}
        .btn-primary {{
            background: #007bff;
        }}
        .btn-primary:hover {{
            background: #0056b3;
            transform: translateY(-2px);
        }}
        .btn-success {{
            background: #28a745;
        }}
        .btn-success:hover {{
            background: #1e7e34;
            transform: translateY(-2px);
        }}
        .step {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: left;
        }}
        .step-number {{
            background: white;
            color: #25D366;
            width: 25px;
            height: 25px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 10px;
        }}
    </style>
    <script>
        function openWhatsAppApp() {{
            // Try to open WhatsApp desktop app
            window.location.href = "whatsapp://send?text=Join%20SPIC%20MACAY%20Mangalore:%20{WHATSAPP_GROUP_URL}";
            
            // Fallback after 3 seconds
            setTimeout(function() {{
                // If still on page, show download options
                document.getElementById('download-section').style.display = 'block';
            }}, 3000);
        }}
        
        function openGroupLink() {{
            window.open("{WHATSAPP_GROUP_URL}", "_blank");
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="whatsapp-logo">💬</div>
        <h2>Join SPIC MACAY Mangalore</h2>
        <p>Connect with us on WhatsApp for cultural events, workshops, and updates!</p>
        
        <div>
            <a href="javascript:openWhatsAppApp()" class="btn btn-success">
                📱 Open WhatsApp App
            </a>
        </div>
        
        <div>
            <a href="javascript:openGroupLink()" class="btn btn-primary">
                🌐 Open in WhatsApp Web
            </a>
        </div>
        
        <div id="download-section" style="display: none; margin-top: 30px;">
            <h3>Don't have WhatsApp?</h3>
            <div class="step">
                <span class="step-number">1</span>
                Download WhatsApp for your device
            </div>
            <div class="step">
                <span class="step-number">2</span>
                Set up your account
            </div>
            <div class="step">
                <span class="step-number">3</span>
                <a href="{WHATSAPP_GROUP_URL}" style="color: white;">Click here to join our group</a>
            </div>
            
            <div style="margin-top: 20px;">
                <a href="https://www.whatsapp.com/download" class="btn btn-primary" target="_blank">
                    📲 Download WhatsApp
                </a>
            </div>
        </div>
        
        <div style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
            <p>🎭 Classical Arts • Dance • Music</p>
            <p>📱 Follow us: @spicmacaymangalore</p>
        </div>
    </div>
</body>
</html>
"""
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Redirecting...</title>
#     <style>
#         body {{ 
#             font-family: Arial; text-align: center; padding: 50px;
#             background: #667eea; color: white;
#         }}
#         .spinner {{ 
#             border: 4px solid rgba(255,255,255,0.3);
#             border-top: 4px solid white;
#             border-radius: 50%; width: 40px; height: 40px;
#             animation: spin 1s linear infinite; margin: 20px auto;
#         }}
#         @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
#     </style>
# </head>
# <body>
#     <div class="spinner"></div>
#     <h2>🔄 Connecting...</h2>
#     <p>Checking for Instagram app...</p>
    
#     <script>
#         let redirected = false;
        
#         // Try Instagram app
#         setTimeout(() => {{
#             if (!redirected) {{
#                 window.location.href = "instagram://user?username=spicmacaymangalore";
#             }}
#         }}, 500);
        
#         // Fallback to WhatsApp after 2 seconds
#         setTimeout(() => {
#             if (!redirected) {
#                 console.log('Instagram not found, going to WhatsApp app');
#                 // Try WhatsApp app first, then group link
#                 window.location.href = "whatsapp://send?text=Join%20SPIC%20MACAY:%20{WHATSAPP_GROUP_URL}";
                
#                 // Final fallback to group link after 2 more seconds
#                 setTimeout(() => {
#                     window.location.href = "{WHATSAPP_GROUP_URL}";
#                 }, 2000);
#             }
#         }, 2000);
        
#         // Listen for visibility change (Instagram opened)
#         document.addEventListener('visibilitychange', () => {{
#             if (document.hidden) {{
#                 redirected = true;
#                 console.log('Instagram app opened');
#             }}
#         }});
        
#         // Listen for page blur (Instagram opened)
#         window.addEventListener('blur', () => {{
#             redirected = true;
#             console.log('App opened via blur');
#         }});
#     </script>
# </body>
# </html>
# """

@app.route('/android-smart')
def android_smart():
    """
    Android-specific smart redirect with better Instagram detection
    """
    # Android Intent with WhatsApp fallback
    instagram_intent = f"intent://instagram.com/_u/spicmacaymangalore/#Intent;package=com.instagram.android;scheme=https;S.browser_fallback_url={WHATSAPP_GROUP_URL};end"
    return redirect(instagram_intent)

@app.route('/ios-smart')  
def ios_smart():
    """
    iOS-specific with fast detection
    """
    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redirecting...</title>
    </head>
    <body>
        <script>
            // Immediate Instagram attempt
            window.location.href = "instagram://user?username=spicmacaymangalore";
            
            // Quick fallback - 1.5 seconds max
            setTimeout(() => {{
                window.location.href = "{WHATSAPP_GROUP_URL}";
            }}, 500);
        </script>
    </body>
    </html>
    """)

@app.route('/whatsapp-direct')
def whatsapp_direct():
    """
    Smart WhatsApp redirect - tries app first, then web
    """
    try:
        user_agent = request.headers.get('User-Agent', '').lower()
        
        is_mobile = any(device in user_agent for device in [
            'android', 'iphone', 'ipad', 'ipod', 'mobile'
        ])
        
        is_android = 'android' in user_agent
        is_ios = any(device in user_agent for device in ['iphone', 'ipad', 'ipod'])
        
        if is_android:
            # Android - try WhatsApp app intent first
            whatsapp_intent = f"intent://send?phone=&text=#Intent;package=com.whatsapp;scheme=whatsapp;S.browser_fallback_url={WHATSAPP_GROUP_URL};end"
            return redirect(whatsapp_intent)
            
        elif is_ios:
            # iOS - try WhatsApp app scheme
            return redirect(f"whatsapp://send?text=Join%20SPIC%20MACAY%20group:%20{WHATSAPP_GROUP_URL}")
            
        elif is_mobile:
            # Other mobile - direct group link
            return redirect(WHATSAPP_GROUP_URL)
            
        else:
            # Desktop - show WhatsApp download page with group link
            return render_template_string(WHATSAPP_DESKTOP_PAGE)
            
    except Exception as e:
        return redirect(WHATSAPP_GROUP_URL)

@app.route('/whatsapp-app')
def whatsapp_app_redirect():
    """
    Force WhatsApp app redirect (mobile only)
    """
    try:
        user_agent = request.headers.get('User-Agent', '').lower()
        
        if 'android' in user_agent:
            # Android - WhatsApp app with group link
            return redirect(f"whatsapp://send?text=Join%20our%20group:%20{WHATSAPP_GROUP_URL}")
        elif any(device in user_agent for device in ['iphone', 'ipad', 'ipod']):
            # iOS - WhatsApp app scheme
            return redirect(f"whatsapp://send?text=Join%20SPIC%20MACAY:%20{WHATSAPP_GROUP_URL}")
        else:
            # Desktop fallback
            return redirect(WHATSAPP_GROUP_URL)
            
    except Exception as e:
        return redirect(WHATSAPP_GROUP_URL)

@app.route('/instagram-direct')
def instagram_direct():
    """
    Direct Instagram follow attempt
    """
    user_agent = request.headers.get('User-Agent', '').lower()
    
    if 'android' in user_agent:
        # Android: Try app first with web fallback
        return redirect(f"intent://instagram.com/_u/spicmacaymangalore/#Intent;package=com.instagram.android;scheme=https;S.browser_fallback_url={INSTAGRAM_URL};end")
    elif any(device in user_agent for device in ['iphone', 'ipad', 'ipod']):
        # iOS: Try app
        return redirect("instagram://user?username=spicmacaymangalore")
    else:
        # Desktop: Web version
        return redirect(INSTAGRAM_URL)

@app.route('/test-redirect')
def test_redirect():
    """
    Test page to check redirects
    """
    user_agent = request.headers.get('User-Agent', '')
    
    return f"""
    <html>
    <head><title>Redirect Test</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>🧪 Redirect Test Page</h2>
        
        <p><strong>Your Device:</strong> {user_agent}</p>
        
        <h3>Test Links:</h3>
        <p><a href="/">🎯 Main Auto-Redirect</a></p>
        <p><a href="/android-smart">🤖 Android Smart</a></p>
        <p><a href="/ios-smart">🍎 iOS Smart</a></p>
        <p><a href="/instagram-direct">📸 Instagram Direct</a></p>
        <p><a href="/whatsapp-direct">💬 WhatsApp Direct</a></p>
        
        <h3>Expected Behavior:</h3>
        <ul>
            <li><strong>Android with Instagram:</strong> Opens Instagram app to follow</li>
            <li><strong>Android without Instagram:</strong> Opens WhatsApp group</li>
            <li><strong>iOS with Instagram:</strong> Opens Instagram app to follow</li>
            <li><strong>iOS without Instagram:</strong> Opens WhatsApp group after 1.5s</li>
            <li><strong>Desktop:</strong> Opens Instagram web page</li>
        </ul>
        
        <h3>Your URLs:</h3>
        <p>Instagram: {INSTAGRAM_URL}</p>
        <p>WhatsApp: {WHATSAPP_GROUP_URL}</p>
    </body>
    </html>
    """

@app.route('/qr-generator')
def qr_generator_page():
    """
    QR Code Generator Interface
    """
    base_url = "https://spicmacay-qr-385957296840.asia-south1.run.app"
    
    qr_options = [
        {
            "name": "Smart Auto-Redirect (RECOMMENDED)",
            "url": f"{base_url}/",
            "description": "Detects Instagram app, falls back to WhatsApp automatically",
            "filename": "smart_auto_redirect_qr.png",
            "color": "#667eea"
        },
        {
            "name": "Android Optimized",
            "url": f"{base_url}/android-smart",
            "description": "Perfect for Android devices with Instagram intent fallback",
            "filename": "android_optimized_qr.png", 
            "color": "#25D366"
        },
        {
            "name": "iOS Optimized",
            "url": f"{base_url}/ios-smart",
            "description": "Optimized for iPhones with fast WhatsApp fallback",
            "filename": "ios_optimized_qr.png",
            "color": "#007AFF"
        },
        {
            "name": "Instagram Direct",
            "url": f"{base_url}/instagram-direct",
            "description": "Tries Instagram app, falls back to web version",
            "filename": "instagram_direct_qr.png",
            "color": "#E4405F"
        },
        {
            "name": "WhatsApp App Direct",
            "url": f"{base_url}/whatsapp-app",
            "description": "Tries WhatsApp app first, then group link",
            "filename": "whatsapp_app_direct_qr.png",
            "color": "#25D366"
        },
        {
            "name": "WhatsApp Group Direct",
            "url": f"{base_url}/whatsapp-direct", 
            "description": "Smart WhatsApp redirect with app detection",
            "filename": "whatsapp_group_direct_qr.png",
            "color": "#128C7E"
        },
        {
            "name": "Instagram Web Only",
            "url": INSTAGRAM_URL,
            "description": "Direct to Instagram web profile",
            "filename": "instagram_web_qr.png",
            "color": "#833AB4"
        }
    ]
    
    return render_template_string(QR_GENERATOR_TEMPLATE, qr_options=qr_options, base_url=base_url)

@app.route('/generate-qr')
def generate_single_qr():
    """
    Generate a single QR code
    """
    url = request.args.get('url', '')
    size = int(request.args.get('size', 300))
    filename = request.args.get('filename', 'qr_code.png')
    
    if not url:
        return "Error: No URL provided", 400
    
    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Resize if needed
        if size != 300:
            img = img.resize((size, size))
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return f"Error generating QR code: {str(e)}", 500

@app.route('/generate-all-qr')
def generate_all_qr():
    """
    Generate all QR codes as a ZIP file
    """
    try:
        base_url = "https://spicmacay-qr-385957296840.asia-south1.run.app"
        
        qr_configs = [
            {"url": f"{base_url}/", "filename": "1_smart_auto_redirect_QR.png", "name": "Smart Auto-Redirect"},
            {"url": f"{base_url}/android-smart", "filename": "2_android_optimized_QR.png", "name": "Android Optimized"},
            {"url": f"{base_url}/ios-smart", "filename": "3_ios_optimized_QR.png", "name": "iOS Optimized"},
            {"url": f"{base_url}/instagram-direct", "filename": "4_instagram_direct_QR.png", "name": "Instagram Direct"},
            {"url": f"{base_url}/whatsapp-app", "filename": "5_whatsapp_app_QR.png", "name": "WhatsApp App"},
            {"url": f"{base_url}/whatsapp-direct", "filename": "6_whatsapp_smart_QR.png", "name": "WhatsApp Smart"},
            {"url": INSTAGRAM_URL, "filename": "7_instagram_web_QR.png", "name": "Instagram Web"},
        ]
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add README file
            readme_content = f"""SPIC MACAY Mangalore QR Codes
=============================

Generated QR codes for social media connection:

1. smart_auto_redirect_QR.png (RECOMMENDED)
   - URL: {base_url}/
   - Best for: General campus posters
   - Function: Auto-detects Instagram, falls back to WhatsApp

2. android_optimized_QR.png
   - URL: {base_url}/android-smart
   - Best for: Android-heavy areas
   - Function: Optimized Instagram intent for Android

3. ios_optimized_QR.png  
   - URL: {base_url}/ios-smart
   - Best for: iPhone users
   - Function: Fast Instagram detection for iOS

4. instagram_direct_QR.png
   - URL: {base_url}/instagram-direct
   - Best for: Instagram-focused campaigns
   - Function: Tries Instagram app, falls back to web

5. whatsapp_app_QR.png
   - URL: {base_url}/whatsapp-app
   - Best for: Mobile WhatsApp users
   - Function: Forces WhatsApp app with join message

6. whatsapp_smart_QR.png
   - URL: {base_url}/whatsapp-direct
   - Best for: Mixed desktop/mobile
   - Function: Smart WhatsApp detection

7. instagram_web_QR.png
   - URL: {INSTAGRAM_URL}
   - Best for: Desktop users
   - Function: Instagram web profile

PRINTING TIPS:
- Print at least 2x2 inches (5x5 cm)
- Use high contrast black on white
- Test scanning from 2-3 feet away
- Laminate for weather protection

CONTACT:
Instagram: @spicmacaymangalore
WhatsApp: Group link in QR codes
"""
            zip_file.writestr("README.txt", readme_content)
            
            # Generate and add each QR code
            for config in qr_configs:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=12,  # Larger for better print quality
                    border=4,
                )
                qr.add_data(config["url"])
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save to BytesIO
                img_buffer = BytesIO()
                img.save(img_buffer, 'PNG')
                
                # Add to ZIP
                zip_file.writestr(config["filename"], img_buffer.getvalue())
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='SPICMACAY_QR_Codes.zip'
        )
        
    except Exception as e:
        return f"Error generating QR codes: {str(e)}", 500

@app.route('/qr-preview')
def qr_preview():
    """
    Preview QR codes without downloading
    """
    base_url = "https://spicmacay-qr-385957296840.asia-south1.run.app"
    
    qr_configs = [
        {"url": f"{base_url}/", "name": "Smart Auto-Redirect (MAIN)", "desc": "Auto-detects Instagram → WhatsApp fallback"},
        {"url": f"{base_url}/android-smart", "name": "Android Optimized", "desc": "Perfect for Android devices"},
        {"url": f"{base_url}/ios-smart", "name": "iOS Optimized", "desc": "iPhone-friendly detection"},
        {"url": f"{base_url}/instagram-direct", "name": "Instagram Direct", "desc": "Instagram app priority"},
        {"url": f"{base_url}/whatsapp-app", "name": "WhatsApp App", "desc": "Forces WhatsApp app open"},
        {"url": f"{base_url}/whatsapp-direct", "name": "WhatsApp Smart", "desc": "Smart WhatsApp redirect"},
        {"url": INSTAGRAM_URL, "name": "Instagram Web", "desc": "Web profile only"},
    ]
    
    qr_images = []
    for config in qr_configs:
        qr = qrcode.QRCode(version=1, box_size=8, border=3)
        qr.add_data(config["url"])
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        img_buffer = BytesIO()
        img.save(img_buffer, 'PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        qr_images.append({
            "name": config["name"],
            "desc": config["desc"],
            "url": config["url"],
            "image": f"data:image/png;base64,{img_str}"
        })
    
    return render_template_string(QR_PREVIEW_TEMPLATE, qr_images=qr_images)

# QR Generator Interface Template
QR_GENERATOR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SPIC MACAY QR Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .qr-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .qr-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .qr-card h3 { margin-top: 0; color: #333; }
        .qr-card p { color: #666; margin: 10px 0; }
        .url-box { background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; 
                  font-size: 12px; word-break: break-all; margin: 10px 0; }
        .btn { display: inline-block; padding: 10px 20px; background: #007bff; color: white; 
              text-decoration: none; border-radius: 5px; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #1e7e34; }
        .download-section { text-align: center; margin: 30px 0; padding: 20px; 
                           background: white; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎭 SPIC MACAY Mangalore</h1>
            <h2>QR Code Generator</h2>
            <p>Generate QR codes for smart social media redirection</p>
        </div>
        
        <div class="download-section">
            <h2>📦 Quick Download</h2>
            <p>Get all QR codes at once for your poster campaign</p>
            <a href="/generate-all-qr" class="btn btn-success" style="font-size: 18px; padding: 15px 30px;">
                📱 Download All QR Codes (ZIP)
            </a>
            <br><br>
            <a href="/qr-preview" class="btn">👀 Preview All QR Codes</a>
        </div>
        
        <h2>🎯 Individual QR Codes</h2>
        <div class="qr-grid">
            {% for qr in qr_options %}
            <div class="qr-card">
                <h3>{{ qr.name }}</h3>
                <p>{{ qr.description }}</p>
                <div class="url-box">{{ qr.url }}</div>
                <a href="/generate-qr?url={{ qr.url }}&filename={{ qr.filename }}" class="btn">
                    📱 Download QR Code
                </a>
                <a href="{{ qr.url }}" class="btn" target="_blank">🔗 Test Link</a>
            </div>
            {% endfor %}
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: white; border-radius: 10px;">
            <h2>📋 Usage Recommendations</h2>
            <ul>
                <li><strong>Smart Auto-Redirect:</strong> Use for main campus posters (works on all devices)</li>
                <li><strong>Android Optimized:</strong> Engineering hostels, Android-heavy areas</li>
                <li><strong>iOS Optimized:</strong> Management/MBA areas, iPhone users</li>
                <li><strong>Instagram Direct:</strong> Art/cultural events, Instagram-focused campaigns</li>
                <li><strong>WhatsApp Direct:</strong> Quick announcements, urgent communications</li>
                <li><strong>Instagram Web:</strong> Computer labs, desktop users</li>
            </ul>
        </div>
        
        <div style="margin-top: 20px; padding: 20px; background: #fff3cd; border-radius: 10px;">
            <h3>🖨️ Printing Tips</h3>
            <ul>
                <li>Print QR codes at least <strong>2x2 inches (5x5 cm)</strong></li>
                <li>Use <strong>high contrast</strong> - black QR on white background</li>
                <li>Test scanning from <strong>2-3 feet away</strong> before mass printing</li>
                <li><strong>Laminate outdoor posters</strong> for weather protection</li>
                <li>Include backup text: <strong>@spicmacaymangalore</strong></li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

# QR Preview Template
QR_PREVIEW_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Preview - SPIC MACAY</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .qr-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }
        .qr-item { background: white; padding: 20px; border-radius: 10px; text-align: center; 
                   box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .qr-item h3 { margin-top: 0; color: #333; }
        .qr-item img { max-width: 200px; margin: 15px 0; border: 1px solid #ddd; }
        .url-text { font-family: monospace; font-size: 11px; background: #f8f9fa; 
                   padding: 8px; border-radius: 5px; word-break: break-all; margin: 10px 0; }
        .btn { display: inline-block; padding: 8px 16px; background: #007bff; color: white; 
              text-decoration: none; border-radius: 5px; margin: 5px; font-size: 14px; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 QR Code Preview</h1>
            <p>SPIC MACAY Mangalore - All Generated QR Codes</p>
            <a href="/qr-generator" class="btn">← Back to Generator</a>
            <a href="/generate-all-qr" class="btn" style="background: #28a745;">📦 Download All</a>
        </div>
        
        <div class="qr-grid">
            {% for qr in qr_images %}
            <div class="qr-item">
                <h3>{{ qr.name }}</h3>
                <img src="{{ qr.image }}" alt="{{ qr.name }} QR Code">
                <p>{{ qr.desc }}</p>
                <div class="url-text">{{ qr.url }}</div>
                <a href="{{ qr.url }}" class="btn" target="_blank">🔗 Test Link</a>
            </div>
            {% endfor %}
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding: 20px; background: white; border-radius: 10px;">
            <h3>📋 Quick Test Checklist</h3>
            <p>Before printing, test these QR codes on:</p>
            <ul style="text-align: left; max-width: 500px; margin: 0 auto;">
                <li>✅ Android phone with Instagram app</li>
                <li>✅ Android phone without Instagram app</li>
                <li>✅ iPhone with Instagram app</li>
                <li>✅ iPhone without Instagram app</li>
                <li>✅ Desktop/laptop browser</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)