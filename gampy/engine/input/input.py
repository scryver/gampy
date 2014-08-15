#!/usr/bin/env python
__author__ = 'michiel'

import os
import gampy.engine.objects.vectors as vectors


# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-types.html
# name          keysym_num  Description
KEY_0           =    48     # The 0 key
KEY_1           =    49     # The 1 key
KEY_2           =    50     # The 2 key
KEY_3           =    51     # The 3 key
KEY_4           =    52     # The 4 key
KEY_5           =    53     # The 5 key
KEY_6           =    54     # The 6 key
KEY_7           =    55     # The 7 key
KEY_8           =    56     # The 8 key
KEY_9           =    57     # The 9 key
KEY_A           =    97     # The letter A
KEY_SHIFT_A     =    65     # The capital A
KEY_B           =    98     # The letter B
KEY_SHIFT_B     =    66     # The capital B
KEY_C           =    99     # The letter C
KEY_SHIFT_C     =    67     # The capital C
KEY_D           =   100     # The letter D
KEY_SHIFT_D     =    68     # The capital D
KEY_E           =   101     # The letter E
KEY_SHIFT_E     =    69     # The capital E
KEY_F           =   102     # The letter F
KEY_SHIFT_F     =    70     # The capital F
KEY_G           =   103     # The letter G
KEY_SHIFT_G     =    71     # The capital G
KEY_H           =   104     # The letter H
KEY_SHIFT_H     =    72     # The capital H
KEY_I           =   105     # The letter I
KEY_SHIFT_I     =    73     # The capital I
KEY_J           =   106     # The letter J
KEY_SHIFT_J     =    74     # The capital J
KEY_K           =   107     # The letter K
KEY_SHIFT_K     =    75     # The capital K
KEY_L           =   108     # The letter L
KEY_SHIFT_L     =    76     # The capital L
KEY_M           =   109     # The letter M
KEY_SHIFT_M     =    77     # The capital M
KEY_N           =   110     # The letter N
KEY_SHIFT_N     =    78     # The capital N
KEY_O           =   111     # The letter O
KEY_SHIFT_O     =    79     # The capital O
KEY_P           =   112     # The letter P
KEY_SHIFT_P     =    80     # The capital P
KEY_Q           =   113     # The letter Q
KEY_SHIFT_Q     =    81     # The capital Q
KEY_R           =   114     # The letter R
KEY_SHIFT_R     =    82     # The capital R
KEY_S           =   115     # The letter S
KEY_SHIFT_S     =    83     # The capital S
KEY_T           =   116     # The letter T
KEY_SHIFT_T     =    84     # The capital T
KEY_U           =   117     # The letter U
KEY_SHIFT_U     =    85     # The capital U
KEY_V           =   118     # The letter V
KEY_SHIFT_V     =    86     # The capital V
KEY_W           =   119     # The letter W
KEY_SHIFT_W     =    87     # The capital W
KEY_X           =   120     # The letter X
KEY_SHIFT_X     =    88     # The capital X
KEY_Y           =   121     # The letter Y
KEY_SHIFT_Y     =    89     # The capital Y
KEY_Z           =   122     # The letter Z
KEY_SHIFT_Z     =    90     # The capital Z
KEY_ALT_L       = 65513     # The left-hand alt key
KEY_ALT_R       = 65514     # The right-hand alt key
KEY_BACKSPACE   = 65288     # backspace
KEY_CANCEL      = 65387     # break
KEY_CAPS_LOCK   = 65549     # CapsLock
KEY_CTRL_L      = 65507     # The left-hand control key
KEY_CTRL_R      = 65508     # The right-hand control key
KEY_DELETE      = 65535     # Delete
KEY_DOWN        = 65364     # Down (↓)
KEY_END         = 65367     # end
KEY_ESCAPE      = 65307     # Escape
KEY_EXECUTE     = 65378     # SysReq
KEY_F1          = 65470     # Function key F1
KEY_F2          = 65471     # Function key F2
KEY_F3          = 65472     # Function key F3
KEY_F4          = 65473     # Function key F4
KEY_F5          = 65474     # Function key F5
KEY_F6          = 65475     # Function key F6
KEY_F7          = 65476     # Function key F7
KEY_F8          = 65477     # Function key F8
KEY_F9          = 65478     # Function key F9
KEY_F10         = 65479     # Function key F10
KEY_F11         = 65480     # Function key F11
KEY_F12         = 65481     # Function key F12
KEY_HOME        = 65360     # home
KEY_INSERT      = 65379     # insert
KEY_LEFT        = 65361     # Left (←)
KEY_KP_0        = 65438	    # 0 on the keypad
KEY_KP_1        = 65436	    # 1 on the keypad
KEY_KP_2        = 65433	    # 2 on the keypad
KEY_KP_3        = 65435	    # 3 on the keypad
KEY_KP_4        = 65430	    # 4 on the keypad
KEY_KP_5        = 65437	    # 5 on the keypad
KEY_KP_6        = 65432	    # 6 on the keypad
KEY_KP_7        = 65429	    # 7 on the keypad
KEY_KP_8        = 65431	    # 8 on the keypad
KEY_KP_9        = 65434	    # 9 on the keypad
KEY_KP_BEGIN    = 65437     # The center key (same key as 5) on the keypad
KEY_KP_DECIMAL  = 65439     # Decimal (.) on the keypad
KEY_KP_DELETE   = 65439     # KP_Delete	    91	65439	delete on the keypad
KEY_KP_DIVIDE   = 65455     # / on the keypad
KEY_KP_DOWN     = 65433     # ↓ on the keypad
KEY_KP_END      = 65436     #end on the keypad
KEY_KP_ENTER	= 65421	    # enter on the keypad
KEY_KP_HOME		= 65429	    # home on the keypad
KEY_KP_INSERT	= 65438	    # insert on the keypad
KEY_KP_LEFT		= 65430	    # ← on the keypad
KEY_KP_MULTIPLY = 65450	    # × on the keypad
KEY_KP_NEXT		= 65435	    # PageDown on the keypad
KEY_KP_PRIOR	= 65434	    # PageUp on the keypad
KEY_KP_RIGHT	= 65432	    # → on the keypad
KEY_KP_SUBTRACT = 65453	    # - on the keypad
KEY_KP_UP		= 65431	    # ↑ on the keypad
KEY_NEXT        = 65366     # PageDown
KEY_NUM_LOCK    = 65407     # NumLock
KEY_PAUSE       = 65299     # pause
KEY_PRINT       = 65377     # PrintScrn
KEY_PRIOR       = 65365     # PageUp
KEY_RETURN      = 65293     # Return	    36	65293	The enter key (control-M). The name Enter refers to a mouse-related event, not a keypress; see Section 54, “Events”
KEY_RIGHT       = 65363     # Right (→)
KEY_SCROLL_LOCK = 65300     # ScrollLock
KEY_SHIFT_LEFT  = 65505     # The left-hand shift key
KEY_SHIFT_RIGHT = 65506     # The right-hand shift key
KEY_TAB         = 65289     # The tab key
KEY_UP          = 65362     # Up (↑)

MOUSE_LEFT      = 1
MOUSE_RIGHT     = 3
MOUSE_MIDDLE    = 2
MOUSE_UP        = 4
MOUSE_DOWN      = 5

class Input:
    NUM_KEY_CODES = 256
    NUM_MOUSE_BUTTONS = 5

    def __init__(self):
        # HACK FOR REPEATING KEYS
        # os.system('xset r off')

        self._event_keys = {}
        self._last_keys = {}
        self._event_mouse = {}
        self._last_mouse = {}
        self._mouse_position = vectors.Vector2(0, 0)

    def _key_press_event(self, event):
        """
        event.char = A single-character string that is the key's code
        event.keysym = A string that is the key's symbolic name
        event.keycode = An integer that identifies which key was pressed, but the code does not reflect the state of
                        various modifiers like the shift and control keys and the NumLock key.
                        So, for example, both a and A have the same key code.
        event.keysym_num = A numeric code equivalent to the key symbol. Unlike .keycode, these codes are different
                           for different modifiers. For example, the digit 2 on the numeric keypad (key symbol KP_2)
                           and the down arrow on the numeric keypad (key symbol KP_Down) have the same key code (88),
                           but different .keysym_num values (65433 and 65458, respectively)
        event.widget = The widget in which the event has occurred
        """
        if not self._event_keys.get(event.keysym_num, False):
            self._event_keys[event.keysym_num] = True

    def _key_release_event(self, event):
        if self._event_keys.get(event.keysym_num, False):
            self._event_keys[event.keysym_num] = False

    def _mouse_event(self, event):
        self._mouse_position_event(event)

    def _mouse_click_event(self, event):
        """
        event.num = Button number
        event.x, event.y = Mouse position, in pixels, relative to the upper left corner of the widget
        event.x_root, event.y_root = Mouse position, in pixels, relative to the upper left corner of the screen
        event.widget = The widget in which the event has occurred
        """
        if not self._event_mouse.get(event.num, False):
            self._event_mouse[event.num] = True

    def _mouse_release_event(self, event):
        if self._event_mouse.get(event.num, False):
            self._event_mouse[event.num] = False

    def _mouse_position_event(self, event):
        self._mouse_position.x = event.x
        self._mouse_position.y = event.y

    def get_key(self, key_code):
        return self._event_keys.get(key_code, False)

    def get_key_down(self, key_code):
        return self.get_key(key_code) and not self._last_keys.get(key_code, False)

    def get_key_up(self, key_code):
        return not self.get_key(key_code) and self._last_keys.get(key_code, False)

    def get_mouse(self, mouse_button):
        return self._event_mouse.get(mouse_button, False)

    def get_mouse_down(self, mouse_button):
        return self.get_mouse(mouse_button) and not self._last_mouse.get(mouse_button, False)

    def get_mouse_up(self, mouse_button):
        return not self.get_mouse(mouse_button) and self._last_mouse.get(mouse_button, False)

    def update(self, delta):
        self._last_keys = self._event_keys.copy()
        self._last_mouse = self._event_mouse.copy()

    def bind_window(self, window):
        window.display.bind_all('<Key>', self._key_press_event)
        window.display.bind_all('<KeyRelease>', self._key_release_event)

        for i in range(1, Input.NUM_MOUSE_BUTTONS + 1):
            window.display.bind_all('<Button-{button}>'.format(button=i), self._mouse_click_event)
            window.display.bind_all('<ButtonRelease-{button}>'.format(button=i), self._mouse_release_event)
            window.display.bind_all('<Double-Button-{button}>'.format(button=i), self._mouse_event)
            window.display.bind_all('<Triple-Button-{button}>'.format(button=i), self._mouse_event)
            window.display.bind_all('<Motion>'.format(button=i), self._mouse_position_event)

    @property
    def mouse_position(self):
        return self._mouse_position

    def set_mouse_position(self, widget, x, y):
        try:
            widget.event_generate('<Motion>', warp=True, x=x, y=y)
        except Exception as err:
            print(err.with_traceback(None))

    def set_cursor(self, widget, enabled=True, type='target'):
        types = ['arrow', 'circle', 'clock', 'cross', 'dotbox', 'exchange', 'fleur', 'heart', 'heart',
                 'man', 'mouse', 'pirate', 'plus', 'shuttle', 'sizing', 'spider', 'spraycan', 'star',
                 'target', 'tcross', 'trek', 'watch']
        if enabled and type in types:
            cursor = type
        else:
            cursor = 'none'
        widget.config(cursor=cursor)

    def destroy(self):
        # HACK FOR REPEATING KEYS
        # os.system('xset r on')
        pass