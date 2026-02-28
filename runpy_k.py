
def run_now():
        from setup import setup_server
        setup_s = setup_server()
        setup_s.setup_now()
        from flasky import Fileshare
        from time import sleep
        import regex
        with open('config/FSConfig.conf') as file:
            reader = file.read()
            inf = reader.strip('port').split('=')[1]
            inf = regex.sub('\n.*','',inf)
            
            port = int(inf)
            dir_share = reader.strip("share_directory").split('=')[2]
            dir_share = regex.sub('\n.*', '', reader.split('share_directory=')[1])

        fsh = Fileshare(port,dir_share, 'Cloud')
        fsh.run()
run_now()