from flask import Flask, render_template_string, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    vpn_status = "running" if is_vpn_running() else "stopped"
    current_ip = get_current_ip()
    return render_template_string('''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>VPN Control</title>
          </head>
          <body>
            <div class="container">
              <h1>VPN Control</h1>
              <p>VPN Status: {{ vpn_status }}</p>
              <p>Current IP: {{ current_ip }}</p>
              <form action="/start" method="post">
                <button type="submit">Start VPN</button>
              </form>
              <form action="/stop" method="post">
                <button type="submit">Stop VPN</button>
              </form>
            </div>
          </body>
        </html>
    ''', vpn_status=vpn_status, current_ip=current_ip)

def is_vpn_running():
    result = subprocess.run(['service', 'openvpn', 'status'], capture_output=True, text=True)
    return 'active (running)' in result.stdout

def get_current_ip():
    result = subprocess.run(['/bin/bash', 'scripts/get_ip.sh'], capture_output=True, text=True)
    return result.stdout.strip()

@app.route('/start', methods=['POST'])
def start_vpn():
    subprocess.run(["/bin/bash", "scripts/start_vpn.sh"])
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_vpn():
    subprocess.run(["/bin/bash", "scripts/stop_vpn.sh"])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
