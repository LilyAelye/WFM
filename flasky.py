from flask_socketio import SocketIO as sio
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
from os import path as pathlib, listdir

from werkzeug.security import (generate_password_hash, check_password_hash)
from colorama import (Fore, Back, Style)
class Fileshare:
    def __init__(self, port, sharedir, title=None):
        self.port = port
        self.sharedirectory = sharedir

        self.title = title or "WFS"
        self.running = True
        self.app = Flask(__file__, static_folder='static/',template_folder='templates/')
    
    
    def run(self):
        rt = self.app.route

        @self.app.context_processor
        def contextproc():
            return {
                "title": self.title,
                "language": request.cookies.get('language','en')
            }

        def VerifyLogin(username, password):
            with open("config/WFMUSER.json", 'r') as f:
                import json
                data = json.load(f)
            print(data)
            if username in data and data[username]['password'] == password:
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
            print(extracted_path or "No path.")
            if item == 'New Folder':
                path :str = self.sharedirectory + "/" + extracted_path + "/" + name
                print(path)
                if path.find('/share'):
                    print("found")
                    path = path.replace('share//share',self.sharedirectory)

                os.mkdir(path)
                #return {'fail', 404}
            elif item == 'New File':

                path :str = self.sharedirectory + "/" + extracted_path + "/" + name
                print(path)
                if path.find('/share'):
                    print("found")
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

            print(scr)
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
        @rt('/')
        def index():
            if request.cookies.get('pwd') and request.cookies.get('usr'):
                pwd :str = request.cookies.get('pwd')
                usr :str = request.cookies.get('usr')

                with open("config/WFMUSER.json", 'r') as f:
                    import json
                    data = json.load(f)
                print(data)
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
                print(data)
                if username in data and data[username]['password'] == password:
                    resp = make_response(redirect('/'))
                    resp.set_cookie('usr', username)
                    resp.set_cookie('pwd', password)
                    return resp
                else:
                    return render_template('login.html', title=self.title, language=language)
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
            return redirect('/')

        print(f"{Back.BLUE + Fore.LIGHTGREEN_EX} Booting server on {self.port} {Style.RESET_ALL}")
        self.app.run('0.0.0.0',self.port, debug=True)