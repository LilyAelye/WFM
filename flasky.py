from flask_socketio import (SocketIO as sio, emit, join_room, disconnect, close_room, leave_room)
import logging
from flask import (
    Flask,
    make_response,
    send_file,
    send_from_directory,
    url_for,
    render_template,
    request,
    redirect
)
from flask.logging import default_handler
from os import path as pathlib, listdir
from waitress import serve
from werkzeug.security import (generate_password_hash, check_password_hash)
from consolemenu import clear_terminal
from threading import Thread
from time import sleep
from colorama import (Fore, Back, Style)
import psutil


class Fileshare:
    def __init__(self, port, sharedir, title=None):
        self.port = port
        self.sharedirectory = sharedir

        self.title = title or "WFS"
        self.running = True
        self.app = Flask(__file__, static_folder='static/',template_folder='templates/')
        self.socketio = sio(self.app, cors_allowed_origins="*", async_mode='threading')
        self.runningdisk = psutil.disk_usage(self.sharedirectory)
        self.cpuinfo = psutil.cpu_percent
        self.vram = psutil.virtual_memory()

        

    def get_internetinfo(self):
        def is_internet_connected():
            # Retrieve the network interfaces
            interfaces = psutil.net_if_stats()

            # Check each interface
            for interface, stats in interfaces.items():
                # Check if the interface is up (running)
                if stats.isup:
                    # Additionally, you might want to check IP addresses linked with this interface
                    addrs = psutil.net_if_addrs()[interface]
                    for addr in addrs:
                        # Generally, looking for an IPv4 address
                        if addr.family == psutil.AF_LINK:

                            return True
            return False
        def get_local_ips():
            ip = None
            addrs = psutil.net_if_addrs()
            for interface, addr_list in addrs.items():
                for addr in addr_list:
                    if addr.address.startswith('192.168'):  # Check for IPv4 addresses
                        ip = addr
            return ip or '0.0.0.0'
        
        return get_local_ips() != '0.0.0.0', get_local_ips()
    
    def fetch_info(self):
        diskinfo = f"{(self.runningdisk.free / self.runningdisk.total) * 100:.1f}%"
        cpuinfo = self.cpuinfo(None)

        vram_perc = self.vram.percent
        vram_max = 100
        internet_isup, ip = self.get_internetinfo()
        return diskinfo, cpuinfo, vram_perc, vram_max, internet_isup
    
    def run(self):
        rt = self.app.route

        @self.app.context_processor
        def contextproc():
            # foramt disk usage of free (%) in 0.[xxx] (three dots fot the deciamls)
            formatted, cpu, vram_perc, vram_max, isup = self.fetch_info()
            return {
                "title": self.title,
                "language": request.cookies.get('language','en'),
                "diskusage":formatted,
                "cpuusage": cpu,
                "vrp":vram_perc,
                "vrm":vram_max,
                "isup": isup
            }

        def VerifyLogin(username, password):
            with open("config/WFMUSER.json", 'r') as f:
                import json
                data = json.load(f)
            #print(data)
            if username in data and data[username]['password'] == password and data[username]['login_enabled'] is True:
                return True
            else:
                return False

        @rt('/create/<item>', methods=['POST'])
        def create(item):
            pwd = request.cookies.get('pwd')
            usr = request.cookies.get('usr')
            if not VerifyLogin(usr, pwd):
                return redirect('/log')

            name = request.form['name']
            import os
            extracted_path = request.form.get('path')
            #print(extracted_path or "No path.")
            if item == 'New Folder':
                path :str = self.sharedirectory + "/" + extracted_path + "/" + name
                #print(path)
                if path.find('/share'):
                    #print("found")
                    path = path.replace('share//share',self.sharedirectory)

                os.mkdir(path)
                #return {'fail', 404}
            elif item == 'New File':

                path :str = self.sharedirectory + "/" + extracted_path + "/" + name
                #print(path)
                if path.find('/share'):
                    #print("found")
                    path = path.replace('share//share',self.sharedirectory)

                open(path, 'a').close()
                
            return redirect(request.referrer)

        @rt('/js/<path:scr>')
        def js(scr):
            return send_from_directory('JS', scr)

        @rt('/editor')
        def editor():
            base = self.sharedirectory
            scr :str = request.args.get('path', 'share/')
            if not base in scr:
                scr = base + (scr.strip('/'))
            pwd = request.cookies.get('pwd')
            usr = request.cookies.get('usr')
            if not VerifyLogin(usr, pwd):
                return redirect('/log')

            #print(scr)
            if pathlib.exists(scr):
                content = ""
            
                with open(scr,'r') as f:
                    content= f.read()
                    name = f.name
                return render_template('editor.html',content=content, file=name, path=request.referrer)
            else:
                return redirect(request.referrer)
        #[[
        @rt('/share')
        def share():
            pwd = request.cookies.get('pwd')
            usr = request.cookies.get('usr')
            if not VerifyLogin(usr, pwd):
                return redirect('/log')

            base = self.sharedirectory
            rel = request.args.get('path', '').lstrip('/')
            if rel == 'share':
                rel = ''

            if rel.startswith(base + '/'):
                rel = rel[len(base) + 1:]
            if rel.startswith('share/share/'):
                rel = rel.replace('share/share/', 'share/')
            

            fs_path = pathlib.join(base, rel)
            if fs_path.startswith('share/share/'):
                fs_path = fs_path.replace('share/share/','share/')

            language = request.cookies.get('language', 'en')
            files = []

            for f in listdir(fs_path):
                files.append({
                    "name": f,
                    "is_dir": pathlib.isdir(pathlib.join(fs_path, f))
                })

            if pathlib.isfile(fs_path):
                return send_file(fs_path, as_attachment=True)

            return render_template(
                'share.html',
                title=self.title,
                path=rel,      # RELATIVE ONLY
                files=files,
                language=language
            )

        #

        def errorasync(msg):
            print(f"{Fore.RED + Back.BLACK} [ERROR] {msg} {Style.RESET_ALL}")

        def warnasync(msg):
            print(f"{Fore.YELLOW + Back.BLACK} [WARNING] {msg} {Style.RESET_ALL}")
        
        def successasync(msg):
            print(f"{Fore.GREEN + Back.CYAN} [SUCCESS] {msg} {Style.RESET_ALL}")

        @rt('/')
        def index():
            if request.cookies.get('pwd') and request.cookies.get('usr'):
                pwd :str = request.cookies.get('pwd')
                usr :str = request.cookies.get('usr')

                with open("config/WFMUSER.json", 'r') as f:
                    import json
                    data = json.load(f)
               #print(data)
                if usr in data and data[usr]['password'] == pwd:
                    return redirect('/share')
                else:
                    return redirect('/log')
            else:
                return redirect('/log')
        
        @rt('/log', methods=['GET','POST'])
        def login():
            language = request.cookies.get('language', 'en')
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                with open("config/WFMUSER.json", 'r') as f:
                    import json
                    data = json.load(f)
                #print(data)
                if username in data and data[username]['password'] == password and data[username]['login_enabled'] is True:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('usr', username)
                    resp.set_cookie('pwd', password)
                    successasync('user '+ username + " has logged in.")
                    return resp
                else:
                    if data[username]['login_enabled'] is False:
                        warnasync('A account that is disabled was tried to be logged into. Please go to WFMUSER.json to re-enable the account or use the web interface of the administrator.')
                        return render_template('login.html', error="account is disabled. Please contact the administrator or go to WFMUSER.json.")
                    return render_template('login.html', title=self.title, language=language, error="Invalid Credentials")
            else:
                return render_template('login.html', title=self.title, language=language)
        
        @rt('/sl', methods=['POST'])
        def set_language():
            language = request.form['language']
            resp = make_response(redirect(request.referrer))
            resp.set_cookie('language', language)
            return resp
        
        @self.app.errorhandler(404)
        def page_not_found(err):
            return redirect('/', code=404)
        
        @rt('/download/')
        def download():
            pwd :str = request.cookies.get('pwd')
            usr :str = request.cookies.get('usr')
            path = request.args.get('path')
            print(path)
            path = path.strip('"')
            print(path)
            if not VerifyLogin(usr, pwd):
                return redirect('/log')
            else:
                #print(path)
                import regex
                name = regex.sub(r'.*\.', '', path)
                print(name)
                return send_file(path,download_name='Downloaded.'+name, as_attachment=True)
        
        @rt('/save/')
        def save():
            pwd :str = request.cookies.get('pwd')
            usr :str = request.cookies.get('usr')
            path = request.args.get('path')
            newcontent = request.args.get('content')

            path = path.strip('"')
            newcontent = newcontent.strip('"')

            if not VerifyLogin(usr, pwd):
                return redirect('/log')
            else:
                if pathlib.exists(path):
                    newcontent = newcontent.replace('scnl','\n')
                    with open(path, 'w+') as writter:
                        writter.write(newcontent)
                        writter.close()
                    return redirect(request.referrer)
                return redirect(request.referrer)
        @self.socketio.on('update')
        def update_info():
            disk, cpu, vram_perf, vram_max, isup = self.fetch_info()
            emit('update',{
                'diskusage':disk,
                'cpuusage':cpu,
                'vrp':vram_perf,
                'vrm':vram_max,
                'isup':isup or False
            })

        ip = "[??]"
        def is_internet_connected():
            # Retrieve the network interfaces
            interfaces = psutil.net_if_stats()

            # Check each interface
            for interface, stats in interfaces.items():
                # Check if the interface is up (running)
                if stats.isup:
                    # Additionally, you might want to check IP addresses linked with this interface
                    addrs = psutil.net_if_addrs()[interface]
                    for addr in addrs:
                        # Generally, looking for an IPv4 address
                        if addr.family == psutil.AF_LINK:

                            return True
            return False
        def get_local_ips():
            ip = None
            addrs = psutil.net_if_addrs()
            for interface, addr_list in addrs.items():
                for addr in addr_list:
                    if addr.address.startswith('192.168'):  # Check for IPv4 addresses
                        ip = addr.address
            return ip or '0.0.0.0'
        
        


        if not is_internet_connected():
            print(f"{Fore.YELLOW} [WARNING!] The server is running with no internet connection. Only this machine can access it via localhost:"+str(self.port))
        else:
            ip = get_local_ips()
            print(f"{Back.BLACK + Fore.WHITE} WIFI/ETERNET is connected. Server will be accessible on your IP of the server: {Fore.GREEN}", ip+":"+str(self.port)+f"{Style.RESET_ALL}\n\n")
        log = logging.getLogger('werkzeug')
        log.disabled = True
        print(f"{Back.BLUE + Fore.LIGHTGREEN_EX} Booting server on {self.port} {Style.RESET_ALL}")
        self.app.run(port=self.port,host='0.0.0.0', threaded=True, debug=True)
        
        #server_thr = Thread(target=run_now,daemon=True)
        #server_thr.start()
        clear_terminal()
        print(f"{Back.GREEN + Fore.BLACK} Server is started. {Style.RESET_ALL}")
        print(f"{Back.BLUE + Fore.LIGHTGREEN_EX} Booted server on {self.port} {Style.RESET_ALL}")
        