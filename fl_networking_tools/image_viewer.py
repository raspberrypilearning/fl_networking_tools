from tkinter import Tk, Toplevel, Canvas, PhotoImage, Label, StringVar, BOTH, YES, X, TOP
from threading import Thread, Event
from queue import Queue, Empty

# the number of screen updates to do before forcing a .update()
UPDATE_THRESHOLD = 50

class ImageViewer():
    def __init__(self, width=640, height=480, bg="#000000", fg="#888888"):
        self._width = width
        self._height = height
        self._bg = bg
        self._fg = fg
        self._update_job = None
        self._get_data_thread = None

        # set the events and queues
        self._running = Event()
        self._update_queue = Queue()
        self._pixels = {}

    def _close(self):
        if self._update_job is not None:
            self._root.after_cancel(self._update_job)
            self._update_job = None
        self._running.clear()
        del self._img
        self._root.quit()
        self._root.destroy()
        
    # the display is updated in a separate thread from a Q,
    # this is so the calling application doesn't have to wait for the GUI to be updated before moving on
    def _update_display(self):
        updates = 0
        self._update_job = None
        # take any pixels which are on the Q off the Q and display them
        try:
            while self._running.is_set():
                # is there an update on the Q
                update_data = self._update_queue.get_nowait()

                # keep a track of the updates
                updates += 1
                
                # put a single pixel on the image
                if update_data[0] == "pixel":
                    pos = update_data[1]
                    color = update_data[2]
                    hash_color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                    self._img.put(hash_color, pos)
                
                # update the text
                elif update_data[0] == "text":
                    self._text_var.set(str(update_data[1]))
                
                # has the update threshold been reached, if so update the window
                if updates > UPDATE_THRESHOLD:
                    self._root.update()
                    updates = 0

        except Empty:
            # nothing left on the Q, wait and then try again
            self._update_job = self._root.after(250, self._update_display)

        # update the window, if there is nothing left on the Q
        if updates > 0:
            self._root.update()

    def _get_data(self):
        self._get_data_job = None
        if self._running.is_set():
            if self._get_data_func is not None:
                self._get_data_func()
            self._get_data_job = self._root.after(1, self._get_data)

    # put a single pixel on the image
    def put_pixel(self, pos, color):
        if pos[0] >= 0 and pos[1] >= 0:
            self._pixels[pos] = color
            self._update_queue.put(("pixel", pos, color))

    # get the value of single pixel
    def get_pixel(self, pos):
        if pos in self._pixels:
            return self._pixels[pos]
        else:
            return None

    def start(self, get_data_func=None):
        # setup user interface
        self._root = Tk()
        self._root.title("Image Viewer")
        self._root.geometry("{}x{}".format(self._width, self._height))
        self._root.protocol("WM_DELETE_WINDOW", self._close)

        # create the title
        self._text = ""
        self._text_var = StringVar()
        Label(self._root, textvariable=self._text_var, bg=self._bg, fg=self._fg).pack(side=TOP, fill=X)
        
        # create blank image
        self._canvas = Canvas(self._root, bg=self._bg, bd=0, highlightthickness=0)
        self._canvas.pack(fill=BOTH, expand=YES)
        self._img = PhotoImage(width=self._width, height=self._height)
        self._canvas.create_image((self._width/2, self._height/2), image=self._img, state="normal")

        # start the job to update the image after 250ms
        self._update_job = self._root.after(250, self._update_display)

        # set the _running status
        self._running.set()

        # the function to get the data is run in a separate thread
        # this is so the udp data can be read from the socket as quickly as possible
        if get_data_func is not None:
            self._get_data_thread = Thread(target=get_data_func)
            self._get_data_thread.start()
            
        # start up the app
        self._root.mainloop()

        print("finished")

    @property
    def running(self):
        return self._running

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self._update_queue.put(("text", self._text))

if __name__ == "__main__":
    from random import randint
    viewer = ImageViewer()
    
    def random_pixels():
        viewer.text = "Testing ImageViewer. You should see dots"
        for pixel_number in range(500):
            viewer.text = "Testing ImageViewer. You should {} dots".format(pixel_number + 1)
            pos = (randint(1,640), randint(1,480))
            color = (randint(0,255), randint(0,255), randint(0,255))
            viewer.put_pixel(pos, color)

    viewer.start(random_pixels)