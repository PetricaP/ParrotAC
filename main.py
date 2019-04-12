#!/bin/python

from pyparrot.Minidrone import Mambo
from DemoGUI import *


# mambo_addr = "d0:3a:a7:5a:e6:22"
# mambo_address = "d0:3a:a8:dd:e6:22"
mambo_address = "3c:a9:f4:08:54:80"


mambo = Mambo(mambo_address, use_wifi=True)

print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

if success:

    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    mambo.hover()

    root = tk.Tk()
    root.geometry("300x400")

    gui = DemoGUI(root, mambo)
    root.mainloop()

    print("disconnect")
    mambo.disconnect()



