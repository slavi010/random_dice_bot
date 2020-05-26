from pynput import mouse


class MyException(Exception): pass


def get_next_click_mouse():
    def on_click(x, y, button, pressed):
        if button == mouse.Button.left:
            raise MyException(x, y, button, pressed)

    # Collect events until released
    with mouse.Listener(
            on_click=on_click) as listener:
        try:
            listener.join()
        except MyException as e:
            return e.args[0], e.args[1], e.args[2], e.args[3]
    return None, None, None, None