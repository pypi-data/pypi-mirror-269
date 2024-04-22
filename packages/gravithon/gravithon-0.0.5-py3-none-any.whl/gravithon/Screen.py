from gravithon.Space import Space
from gravithon.Body import Body
from gravithon.Sphere import Sphere
from tkinter import *
from multipledispatch import dispatch


class Screen:
    def __init__(self, space: Space,
                 start_x: float = None, end_x: float = None, start_y: float = None, end_y: float = None):
        if space.dimensions != 2:
            raise Exception('only 2d spaces are renderable!')

        self.space = space
        self.running = False

        self.master = Tk()
        self.master.title = 'Gravithon'
        # TODO: ICON

        # title frame
        self.title_frame = Frame(self.master)
        self.title_frame.pack(fill=X)

        self.play_pause_btn = Button(self.title_frame, command=self.toggle_play)
        self.play_pause_btn.pack(side=LEFT)

        self.step_btn = Button(self.title_frame, command=self.step2)
        self.step_btn.pack(side=LEFT)

        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

        self.canvas = Canvas(self.master, bg=self.space.background_color, bd=0)
        self.canvas.pack(fill=BOTH, expand=True)
        self.enable_drag()

    def draw_body(self, canvas: Canvas, body: Body):
        x = body.position[0]
        y = body.position[1]

        if isinstance(body, Sphere):
            # draw sphere
            coords = [(x - body.radius, y - body.radius), (x + body.radius, y + body.radius)]
            canvas.create_oval(self.space_to_px(coords, canvas), fill=body.color, width=0)

    def enable_drag(self):
        def scan_mark(event):
            self.canvas.scan_mark(event.x, event.y)

        def scan_dragto(event):
            self.canvas.scan_dragto(event.x, event.y, gain=1)

        self.canvas.bind('<ButtonPress-1>', scan_mark)
        self.canvas.bind("<B1-Motion>", scan_dragto)

    def render(self):
        self.canvas.delete(ALL)

        for body in self.space.bodies:
            self.draw_body(self.canvas, body)

        self.master.update()

    @dispatch(tuple, Canvas)
    def space_to_px(self, point: tuple, canvas: Canvas):
        """
        convert in meters to pixels according to space's size
        :param canvas: canvas
        :param point: x, y
        :return: value in pixels
        """
        x = point[0]
        y = point[1]
        a = 1 / 100000000
        a = 100
        x *= a
        y *= a
        self.master.update()
        y = canvas.winfo_height() - y

        return x, y

    @dispatch(list, Canvas)
    def space_to_px(self, points: list, canvas: Canvas):
        """
        convert meters to pixels according to space's size
        :param canvas: canvas
        :param points: list of points in meters
        :return: list of points in pixels
        """
        ret = []
        for value in points:
            ret.append(self.space_to_px(value, canvas))

        return ret

    def close(self):
        self.master.destroy()

    def step(self):
        if self.running:
            self.render()
            self.space.step()
            step_duration_ms = int(self.space.step_duration * 1000)  # convert seconds to ms
            self.master.after(step_duration_ms, self.step)

    def step2(self):
        self.render()
        self.space.step()

    def play(self):
        # TODO: stop condition
        self.master.bind("<space>", self.toggle_play)
        self.render()
        self.step()
        self.master.mainloop()

    def toggle_play(self, event=None):
        self.running = not self.running
        self.step()

    def stop(self):
        self.running = False
