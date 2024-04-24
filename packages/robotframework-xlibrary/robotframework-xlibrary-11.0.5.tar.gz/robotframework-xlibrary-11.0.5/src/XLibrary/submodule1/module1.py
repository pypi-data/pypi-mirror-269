# -*- coding: utf-8 -*-
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from .module2 import XDrint
from AppiumFlutterLibrary.finder import ElementFinder

class XPrint:
    def __init__(self):
        super().__init__()
        self._ne = XDrint()
        self._bi = BuiltIn()
        self.finder = ElementFinder()


    @keyword("XPrint Log")
    def XPrint_log(self):
        print("Hello, world! ,สวัสดีชาวโลก เทสภาษาไทย")

    def TestModule2(self):
        instance = XDrint()  
        instance.CDCDCD()   
        self._ne.CDCDCD() 

    def XQuit_App(self):
        """ปิดแอพปัจจุบันและปิดเซสชัน"""
        driver = self._current_application()
        driver.quit()

    @keyword('XSwitch Mode')
    def XSwitch_Mode(self, mode):
        """Switch Mode to NATIVE_APP OR FLUTTER."""
        driver = self._current_application()
        if mode == 'NATIVE':
            driver.switch_to.context('NATIVE_APP')
        elif mode == 'FLUTTER':
            driver.switch_to.context('FLUTTER')

    def _current_application(self):
        """คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน"""
        return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()
    

    @keyword("XSwipe")
    def swipe_on_screen(self, start_x, start_y, end_x, end_y, duration=800):
        """
        ***|    Description     |***
        |   *`XSwipe`*   |   ทำการเลื่อนหน้าจอจากจุดหนึ่งไปยังจุดหนึ่งในเวลาที่กำหนด และสลับคอนเทคซ์จาก NATIVE_APP กลับไปยัง FLUTTER  |

        
        ***|    Example     |***
        | *`XSwipe`* | *`start_x`* | *`start_y`* | *`end_x`* | *`end_y`* | *`duration`* |

        
        ***|    Parameters     |***
        - **`start_x`**  X-coordinate at start point.
        - **`start_y`**  Y-coordinate at start point.
        - **`end_x`**    X-coordinate at end point.
        - **`end_y`**    Y-coordinate at end point.
        - **`duration`** Duration of the swipe action in milliseconds.

        *`Create By Tassana Khrueawan`*
        """
        driver = self._current_application()
        original_context = driver.current_context  # Store the original context
        try:
            driver.switch_to.context('NATIVE_APP')  # Switch to native context
            driver.swipe(start_x, start_y, end_x, end_y, duration)
        finally:
            driver.switch_to.context('FLUTTER')  # Always switch back to Flutter context

    @keyword("XGet window height")
    def get_window_height(self):
        """
        ***|    Description     |***
        |   *`XGet window height`*   |   คืนค่าความสูงของหน้าต่างแอปพลิเคชันในคอนเทคซ์ native และสลับกลับไปยัง Flutter |

        
        ***|    Example     |***
        | *`${height}`* | *`XGet window height`* |
        | *`Log`* | *`Window height: ${height}`* |

        
        ***|    Parameters     |***
        - No parameters.

        *`Create By Tassana Khrueawan`*
        """
        driver = self._current_application()
        original_context = driver.current_context
        try:
            driver.switch_to.context('NATIVE_APP')  # Switch to native context
            height = driver.get_window_size()['height']
            return height
        finally:
            driver.switch_to.context('FLUTTER')  # Always switch back to Flutter context

    @keyword("XGet window width")
    def get_window_width(self):
        """
        ***|    Description     |***
        |   *`XGet window width`*   |   คืนค่าความกว้างของหน้าต่างแอปพลิเคชันในคอนเทคซ์ native และสลับกลับไปยัง Flutter |

        
        ***|    Example     |***
        | *`${width}`* | *`XGet window width`* |
        | *`Log`* | *`Window width: ${width}`* |

        
        ***|    Parameters     |***
        - No parameters.

        *`Create By Tassana Khrueawan`*
        """
        driver = self._current_application()
        original_context = driver.current_context
        try:
            driver.switch_to.context('NATIVE_APP')  # Switch to native context
            width = driver.get_window_size()['width']
            return width
        finally:
            driver.switch_to.context('FLUTTER')  # Always switch back to Flutter context



