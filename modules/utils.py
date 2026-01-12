import tkinter as tk
from customtkinter import CTkToplevel, CTkLabel, CTkImage
from tkinter import Canvas
import ctypes
from PIL import Image

class ScreenCaptureOverlay(CTkToplevel):
    def __init__(self, on_complete, font=None):
        super().__init__()
        self.on_complete = on_complete
        self.font = font if font else ("", 16, "bold")
        
        # マルチモニター対応のジオメトリ取得 (Windows)
        user32 = ctypes.windll.user32
        self.v_x = user32.GetSystemMetrics(76) # SM_XVIRTUALSCREEN
        self.v_y = user32.GetSystemMetrics(77) # SM_YVIRTUALSCREEN
        self.v_w = user32.GetSystemMetrics(78) # SM_CXVIRTUALSCREEN
        self.v_h = user32.GetSystemMetrics(79) # SM_CYVIRTUALSCREEN
        
        # フルスクリーン設定 (仮想スクリーン全体をカバー)
        self.geometry(f"{self.v_w}x{self.v_h}+{self.v_x}+{self.v_y}")
        self.overrideredirect(True)
        self.attributes("-alpha", 0.4) # 少し濃くして見やすく
        self.attributes("-topmost", True)
        self.configure(fg_color="black")
        
        # キャンバス
        self.canvas = Canvas(self, cursor="crosshair", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # 変数
        self.rect_id = None
        self.drag_mode = None # "create", "move", "resize"
        self.resize_edge = None # "nw", "ne", "sw", "se"
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.handle_size = 10 # リサイズ判定の余白
        
        # バインディング
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.update_cursor) # カーソル形状の更新
        self.canvas.bind("<Double-Button-1>", self.confirm_selection)
        self.bind("<Return>", self.confirm_selection)
        self.bind("<Escape>", self.cancel)
        
        # 説明ラベル
        self.label = CTkLabel(self, text="ドラッグで選択 / 枠内ドラッグで移動 / 四隅ドラッグでリサイズ / Enterで決定", 
                              text_color="white", font=self.font)
        self.label.place(relx=0.5, rely=0.1, anchor="center")

    def get_selection_coords(self):
        if not self.rect_id: return None
        coords = self.canvas.coords(self.rect_id)
        if not coords: return None
        x1, y1, x2, y2 = coords
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

    def update_cursor(self, event):
        if self.drag_mode: return
        
        coords = self.get_selection_coords()
        if not coords:
            self.canvas.configure(cursor="crosshair")
            return
            
        x1, y1, x2, y2 = coords
        h = self.handle_size
        
        # 四隅の判定
        if abs(event.x - x1) < h and abs(event.y - y1) < h: self.canvas.configure(cursor="size_nw_se")
        elif abs(event.x - x2) < h and abs(event.y - y1) < h: self.canvas.configure(cursor="size_ne_sw")
        elif abs(event.x - x1) < h and abs(event.y - y2) < h: self.canvas.configure(cursor="size_ne_sw")
        elif abs(event.x - x2) < h and abs(event.y - y2) < h: self.canvas.configure(cursor="size_nw_se")
        elif x1 < event.x < x2 and y1 < event.y < y2: self.canvas.configure(cursor="fleur")
        else: self.canvas.configure(cursor="crosshair")

    def on_mouse_down(self, event):
        coords = self.get_selection_coords()
        
        if coords:
            x1, y1, x2, y2 = coords
            h = self.handle_size
            
            # リサイズ開始判定
            if abs(event.x - x1) < h and abs(event.y - y1) < h:
                self.drag_mode = "resize"; self.resize_edge = "nw"
            elif abs(event.x - x2) < h and abs(event.y - y1) < h:
                self.drag_mode = "resize"; self.resize_edge = "ne"
            elif abs(event.x - x1) < h and abs(event.y - y2) < h:
                self.drag_mode = "resize"; self.resize_edge = "sw"
            elif abs(event.x - x2) < h and abs(event.y - y2) < h:
                self.drag_mode = "resize"; self.resize_edge = "se"
            elif x1 < event.x < x2 and y1 < event.y < y2:
                self.drag_mode = "move"
            else:
                self.drag_mode = "create"
        else:
            self.drag_mode = "create"

        if self.drag_mode == "create":
            self.canvas.delete("all")
            self.rect_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="white", width=2)
            self.start_x, self.start_y = event.x, event.y
        
        self.last_mouse_x, self.last_mouse_y = event.x, event.y

    def on_mouse_drag(self, event):
        if not self.rect_id: return
        
        if self.drag_mode == "create":
            # 正方形で新規作成
            size = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            sx = 1 if event.x >= self.start_x else -1
            sy = 1 if event.y >= self.start_y else -1
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.start_x + size*sx, self.start_y + size*sy)
            
        elif self.drag_mode == "move":
            dx, dy = event.x - self.last_mouse_x, event.y - self.last_mouse_y
            self.canvas.move(self.rect_id, dx, dy)
            self.last_mouse_x, self.last_mouse_y = event.x, event.y
            
        elif self.drag_mode == "resize":
            x1, y1, x2, y2 = self.canvas.coords(self.rect_id)
            if self.resize_edge == "se":
                # 南東角ドラッグ: 正方形を維持しつつリサイズ
                size = min(abs(event.x - x1), abs(event.y - y1))
                self.canvas.coords(self.rect_id, x1, y1, x1 + size, y1 + size)
            elif self.resize_edge == "nw":
                size = min(abs(x2 - event.x), abs(y2 - event.y))
                self.canvas.coords(self.rect_id, x2 - size, y2 - size, x2, y2)
            elif self.resize_edge == "ne":
                size = min(abs(event.x - x1), abs(y2 - event.y))
                self.canvas.coords(self.rect_id, x1, y2 - size, x1 + size, y2)
            elif self.resize_edge == "sw":
                size = min(abs(x2 - event.x), abs(event.y - y1))
                self.canvas.coords(self.rect_id, x2 - size, y1, x2, y1 + size)

    def on_mouse_up(self, event):
        self.drag_mode = None
        self.update_cursor(event)

    def confirm_selection(self, event=None):
        coords = self.get_selection_coords()
        if not coords: return
        x1, y1, x2, y2 = coords
        
        if (x2 - x1) < 10: return
        
        self.withdraw()
        final_bbox = (self.v_x + int(x1), self.v_y + int(y1), self.v_x + int(x2), self.v_y + int(y2))
        self.on_complete(final_bbox)
        self.destroy()

    def cancel(self, event=None):
        self.destroy()
        self.on_complete(None)
