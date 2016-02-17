import ctypes as cy
from ctypes.wintypes import MSG
def handle_win_f10 ():
    print "hallo world"

def set_mouse_key():
        byref = cy.byref
        user32 = cy.windll.user32
        WM_HOTKEY   = 0x0312
        HOTKEYS = {
                1 : (121, 0x0001),    #alt + F10  
                #1 : (0x020A, 0x0001),    #alt + MWU
        }

        HOTKEY_ACTIONS = {
                1 : handle_win_f10,
        }
        
        for id, (vk, modifiers) in HOTKEYS.items ():
                if not user32.RegisterHotKey (None, id, modifiers, vk):
                        print "system key confliction,unable to register :", id, "\n"
        try:
                msg = MSG ()
                while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
                        if msg.message == WM_HOTKEY:              
                                action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
                                if action_to_take:
                                        action_to_take ()
                        user32.TranslateMessage (byref (msg))                     
                        user32.DispatchMessageA (byref (msg))
               
        finally:
                for id in HOTKEYS.keys ():
                        user32.UnregisterHotKey (None, id)
set_mouse_key()