from flask import Flask, flash, render_template, request, redirect
import subprocess
import os
import time

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/wifi')
def wifi():
    wifi_ap_array = scan_wifi_networks()
    return render_template('wifi.html', wifi_ap_array = wifi_ap_array)

@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')

@app.route('/save_credentials', methods = ['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']
    create_wpa_supplicant(ssid, wifi_key)
    return redirect('/')

@app.route('/power')
def power():
    return render_template('power.html')

@app.route('/reboot', methods = ['GET', 'POST'])
def reboot():
    os.system('bash -c "sleep 1; reboot"&')
    return redirect('/')

@app.route('/poweroff', methods = ['GET', 'POST'])
def poweroff():
    os.system('bash -c "sleep 1; poweroff"&')
    return redirect('/')

######## FUNCTIONS ##########

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist','wlan0','scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []
    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)
    
    ap_array = list(set(ap_array))
    ap_array.sort()
    return ap_array

def create_wpa_supplicant(ssid, wifi_key):
        os.system('nmcli con add ifname wlan0 type wifi ssid ' + ssid + ' wifi-sec.key-mgmt wpa-psk wifi-sec.psk ' + wifi_key + ' --rescan no')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
