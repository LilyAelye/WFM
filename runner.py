from setup import setup_server
setup_s = setup_server()
setup_s.setup_now()
from flasky import Fileshare
fsh = Fileshare(2704,'share/', 'Cloud')
fsh.run()