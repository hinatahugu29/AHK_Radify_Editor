from customtkinter import (
    CTk, CTkToplevel, CTkLabel, CTkButton, CTkTabview, 
    CTkScrollableFrame, CTkImage
)
import tkinter.messagebox as messagebox
from tkinter import simpledialog, filedialog
import os
import shutil
from PIL import Image, ImageGrab
from .utils import ScreenCaptureOverlay

class ImageMixin:
    def add_image_file(self):
        """画像ファイルを追加"""
        file_path = filedialog.askopenfilename(
            title="画像を選択",
            filetypes=[("画像ファイル", "*.png *.jpg *.jpeg *.gif *.bmp *.ico")]
        )
        if file_path:
            if not os.path.exists(self.image_dir): os.makedirs(self.image_dir)
            filename = os.path.basename(file_path)
            dest_path = os.path.join(self.image_dir, filename)
            if os.path.exists(dest_path):
                if not messagebox.askyesno("確認", f"{filename} は既に存在します。上書きしますか？"): return
            try:
                shutil.copy2(file_path, dest_path)
                self.refresh_image_list()
                self.image_combo.set(filename)
                self.on_image_select(filename)
                messagebox.showinfo("完了", f"画像を追加しました: {filename}")
            except Exception as e: messagebox.showerror("エラー", f"画像の追加に失敗しました: {e}")

    def refresh_image_list(self):
        """画像リストを更新"""
        if not os.path.exists(self.image_dir): os.makedirs(self.image_dir)
        images = ["（なし）"] + sorted([f for f in os.listdir(self.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])
        self.image_combo.configure(values=images)

    def on_image_select(self, choice):
        """画像選択時の処理"""
        if choice == "（なし）" or not choice:
            empty = CTkImage(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), size=(1, 1))
            self.image_preview.configure(image=empty, text="画像なし")
            self.image_preview.image = empty
            if not self.is_loading: self.apply_item(silent=True)
            return
        
        if not self.is_loading:
            current_text = self.text_entry.get().strip()
            if not current_text or current_text == "新規アイテム":
                name_no_ext = os.path.splitext(choice)[0]
                self.text_entry.delete(0, "end")
                self.text_entry.insert(0, name_no_ext)
        
        path = os.path.join(self.image_dir, choice)
        if not os.path.exists(path):
            self.image_preview.configure(image=None, text="見つかりません")
            return
        
        if choice in self.image_cache:
            photo = self.image_cache[choice]
        else:
            try:
                img = Image.open(path).resize((100, 100), Image.Resampling.LANCZOS)
                photo = CTkImage(img, size=(100, 100))
                self.image_cache[choice] = photo
            except Exception as e:
                self.image_preview.configure(image=None, text="読込エラー")
                return
        
        self.image_preview.configure(image=photo, text="")
        self.image_preview.image = photo
        self.apply_item(silent=True)

    def on_image_combo_scroll(self, event):
        values = self.image_combo.cget("values")
        if not values: return
        try:
            current_idx = values.index(self.image_combo.get())
        except ValueError: current_idx = 0
        
        if event.delta > 0: new_idx = max(0, current_idx - 1)
        else: new_idx = min(len(values) - 1, current_idx + 1)
        
        if new_idx != current_idx:
            new_val = values[new_idx]
            self.image_combo.set(new_val)
            self.on_image_select(new_val)

    def start_screen_capture(self):
        self.iconify()
        self.after(500, lambda: ScreenCaptureOverlay(self.on_capture_complete, font=self.get_font(16, "bold")))

    def on_capture_complete(self, bbox):
        self.deiconify()
        if not bbox: return
        if bbox[2] - bbox[0] < 5 or bbox[3] - bbox[1] < 5: return
        try:
            img = ImageGrab.grab(bbox, all_screens=True, include_layered_windows=True)
        except Exception as e:
            messagebox.showerror("エラー", f"キャプチャ失敗: {e}"); return
        
        name = simpledialog.askstring("アイコン保存", "アイコンの名前を入力:")
        if not name: return
        filename = f"{name}.png"
        save_path = os.path.join(self.image_dir, filename)
        try:
            img.save(save_path, "PNG")
            messagebox.showinfo("完了", f"保存しました: {filename}")
            self.refresh_image_list()
            self.image_combo.set(filename)
            self.on_image_select(filename)
        except Exception as e: messagebox.showerror("エラー", f"保存失敗: {e}")

    def show_image_manager(self):
        manager = CTk()
        manager.title("画像マネージャー")
        manager.geometry("600x500")
        CTkLabel(manager, text="🖼️ 画像リソース管理", font=self.get_font(18, "bold")).pack(pady=15)
        
        tabview = CTkTabview(manager)
        tabview.pack(fill="both", expand=True, padx=10, pady=5)
        tabview._segmented_button.configure(font=self.get_font())
        tabview.add("画像一覧"); tabview.add("未使用画像")
        
        self.img_mgr_scroll = CTkScrollableFrame(tabview.tab("画像一覧"))
        self.img_mgr_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.img_mgr_unused_scroll = CTkScrollableFrame(tabview.tab("未使用画像"))
        self.img_mgr_unused_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh_image_manager_lists()
        
        CTkButton(manager, text="閉じる", command=manager.destroy, font=self.get_font()).pack(pady=10)
        manager.mainloop()

    def refresh_image_manager_lists(self):
        for child in self.img_mgr_scroll.winfo_children(): child.destroy()
        for child in self.img_mgr_unused_scroll.winfo_children(): child.destroy()
        if not os.path.exists(self.image_dir): return
        
        all_images = sorted([f for f in os.listdir(self.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))])
        used_images = set()
        
        def collect_used(items):
            for item in items:
                if "image" in item: used_images.add(item["image"])
        
        for ring in self.config["main_menu"]: collect_used(ring.get("items", []))
        for rings in self.config["submenus"].values():
            for ring in rings: collect_used(ring.get("items", []))
            
        from customtkinter import CTkFrame
        for img in all_images:
            is_used = img in used_images
            target = self.img_mgr_scroll if is_used else self.img_mgr_unused_scroll
            row = CTkFrame(target)
            row.pack(fill="x", pady=1, padx=2)
            CTkLabel(row, text=img, anchor="w", width=250, font=self.get_font()).pack(side="left", padx=5)
            
            if is_used:
                CTkButton(row, text="✏️ 変更", width=60, height=24, font=self.get_font(),
                         command=lambda n=img: self.rename_image_dialog(n)).pack(side="right", padx=2)
            else:
                CTkButton(row, text="🗑️ 削除", width=60, height=24, fg_color="#7d2d2d", font=self.get_font(),
                         command=lambda n=img: self.delete_image_file(n)).pack(side="right", padx=2)
                CTkButton(row, text="✏️ 変更", width=60, height=24, font=self.get_font(),
                         command=lambda n=img: self.rename_image_dialog(n)).pack(side="right", padx=2)

    def delete_image_file(self, filename):
        if messagebox.askyesno("確認", f"画像 '{filename}' を削除しますか？"):
            try:
                os.remove(os.path.join(self.image_dir, filename))
                self.refresh_image_list()
                self.refresh_image_manager_lists()
            except Exception as e: messagebox.showerror("エラー", f"削除失敗: {e}")

    def rename_image_dialog(self, old_name):
        new_name = simpledialog.askstring("リネーム", f"'{old_name}' の新しい名前を入力:", initialvalue=old_name)
        if new_name and new_name != old_name:
            if not new_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                new_name += os.path.splitext(old_name)[1]
            old_path = os.path.join(self.image_dir, old_name)
            new_path = os.path.join(self.image_dir, new_name)
            if os.path.exists(new_path):
                messagebox.showwarning("警告", "同名のファイルが存在します"); return
            try:
                os.rename(old_path, new_path)
                def update_ref(items):
                    for item in items:
                        if item.get("image") == old_name: item["image"] = new_name
                for ring in self.config["main_menu"]: update_ref(ring.get("items", []))
                for rings in self.config["submenus"].values():
                    for ring in rings: update_ref(ring.get("items", []))
                self.save_config(backup=False)
                self.refresh_all()
                self.refresh_image_manager_lists()
            except Exception as e: messagebox.showerror("エラー", f"リネーム失敗: {e}")
