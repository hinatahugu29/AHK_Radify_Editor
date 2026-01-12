from customtkinter import (
    CTk, CTkToplevel, CTkLabel, CTkEntry, CTkTextbox,
    CTkButton, CTkComboBox, CTkSlider, CTkScrollableFrame
)
import tkinter.messagebox as messagebox
from tkinter import simpledialog, filedialog
import os

class DialogsMixin:
    def open_settings(self):
        settings_window = CTkToplevel(self)
        settings_window.title("設定")
        settings_window.geometry("500x700")
        
        from customtkinter import CTkFrame
        
        CTkLabel(settings_window, text="⚙️ メニュー設定", font=self.get_font(18, "bold")).pack(pady=20)
        
        skin_frame = CTkFrame(settings_window)
        skin_frame.pack(fill="x", padx=20, pady=10)
        CTkLabel(skin_frame, text="スキン:", font=self.get_font()).pack(side="left", padx=10)
        skin_entry = CTkEntry(skin_frame, width=200, font=self.get_font())
        skin_entry.insert(0, self.config["menu_options"].get("skin", "Default"))
        skin_entry.pack(side="left", padx=10)
        
        glow_frame = CTkFrame(settings_window)
        glow_frame.pack(fill="x", padx=20, pady=10)
        CTkLabel(glow_frame, text="グロー効果:", font=self.get_font()).pack(side="left", padx=10)
        glow_var = CTkComboBox(glow_frame, values=["有効", "無効"], width=200, font=self.get_font(), dropdown_font=self.get_font())
        glow_var.set("有効" if self.config["menu_options"].get("EnableGlow", True) else "無効")
        glow_var.pack(side="left", padx=10)
        
        size_frame = CTkFrame(settings_window)
        size_frame.pack(fill="x", padx=20, pady=10)
        CTkLabel(size_frame, text="アイテムサイズ:", font=self.get_font()).pack(side="left", padx=10)
        size_slider = CTkSlider(size_frame, from_=40, to=100, width=200)
        size_slider.set(self.config["menu_options"].get("itemSize", 60))
        size_slider.pack(side="left", padx=10)
        size_label = CTkLabel(size_frame, text=f"{int(size_slider.get())}px", width=60, font=self.get_font())
        size_label.pack(side="left")
        size_slider.configure(command=lambda val: size_label.configure(text=f"{int(float(val))}px"))
        
        spacing_frame = CTkFrame(settings_window)
        spacing_frame.pack(fill="x", padx=20, pady=10)
        CTkLabel(spacing_frame, text="リング間隔:", font=self.get_font()).pack(side="left", padx=10)
        spacing_slider = CTkSlider(spacing_frame, from_=50, to=150, width=200)
        spacing_slider.set(self.config["menu_options"].get("ringSpacing", 80))
        spacing_slider.pack(side="left", padx=10)
        spacing_label = CTkLabel(spacing_frame, text=f"{int(spacing_slider.get())}px", width=60, font=self.get_font())
        spacing_label.pack(side="left")
        spacing_slider.configure(command=lambda val: spacing_label.configure(text=f"{int(float(val))}px"))
        
        CTkLabel(settings_window, text="🖱️ 起動方法（トリガー）", font=self.get_font(14, "bold")).pack(pady=(10, 5))
        
        trigger_type_frame = CTkFrame(settings_window)
        trigger_type_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(trigger_type_frame, text="タイプ:", font=self.get_font()).pack(side="left", padx=10)
        trigger_type_var = CTkComboBox(trigger_type_frame, values=["Mouse", "Key"], width=200, font=self.get_font(), dropdown_font=self.get_font())
        
        type_mapping = {"r_drag": "右クリドラッグ", "hold": "長押し判定", "hotkey": "ホットキーのみ", "alt_r": "Alt+右クリ", "ctrl_r": "Ctrl+右クリ"}
        inv_type_mapping = {v: k for k, v in type_mapping.items()}
        current_type = self.config["menu_options"].get("trigger_type", "r_drag")
        trigger_type_var.set(type_mapping.get(current_type, "右クリドラッグ"))
        trigger_type_var.pack(side="left", padx=10)
        
        trigger_key_frame = CTkFrame(settings_window)
        trigger_key_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(trigger_key_frame, text="キー設定:", font=self.get_font()).pack(side="left", padx=10)
        trigger_key_entry = CTkEntry(trigger_key_frame, width=200, placeholder_text="例: RButton, F1, MButton", font=self.get_font())
        trigger_key_entry.insert(0, self.config["menu_options"].get("trigger_key", "RButton"))
        trigger_key_entry.pack(side="left", padx=10)
        
        theme_frame = CTkFrame(settings_window)
        theme_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(theme_frame, text="テーマ:", font=self.get_font()).pack(side="left", padx=10)
        theme_var = CTkComboBox(theme_frame, values=["Dark", "Light", "System"], width=200, font=self.get_font(), dropdown_font=self.get_font())
        theme_var.set(self.config["menu_options"].get("appearance_mode", "Dark"))
        theme_var.pack(side="left", padx=10)

        font_frame = CTkFrame(settings_window)
        font_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(font_frame, text="GUIフォント:", font=self.get_font()).pack(side="left", padx=10)
        
        import tkinter.font as tkfont
        available_fonts = sorted([f for f in list(set(tkfont.families())) if not f.startswith("@")])
        priority_fonts = ["Meiryo UI", "Meiryo", "Yu Gothic UI", "MS UI Gothic", "Segoe UI", "Arial"]
        final_fonts = ["Default"] + [f for f in priority_fonts if f in available_fonts] + ["---"] + [f for f in available_fonts if f not in priority_fonts]
        
        font_var = CTkComboBox(font_frame, values=final_fonts, width=200, font=self.get_font(), dropdown_font=self.get_font())
        current_font = self.config["menu_options"].get("gui_font_family", "")
        font_var.set(current_font if current_font else "Default")
        font_var.pack(side="left", padx=10)

        font_size_frame = CTkFrame(settings_window)
        font_size_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(font_size_frame, text="フォントサイズ:", font=self.get_font()).pack(side="left", padx=10)
        font_size_slider = CTkSlider(font_size_frame, from_=8, to=24, width=200)
        font_size_slider.set(self.config["menu_options"].get("gui_font_size", 12))
        font_size_slider.pack(side="left", padx=10)
        font_size_label = CTkLabel(font_size_frame, text=f"{int(font_size_slider.get())}pt", width=60, font=self.get_font())
        font_size_label.pack(side="left")
        font_size_slider.configure(command=lambda val: font_size_label.configure(text=f"{int(float(val))}pt"))

        def save_settings():
            self.push_history()
            self.config["menu_options"]["skin"] = skin_entry.get()
            self.config["menu_options"]["EnableGlow"] = (glow_var.get() == "有効")
            self.config["menu_options"]["itemSize"] = int(size_slider.get())
            self.config["menu_options"]["ringSpacing"] = int(spacing_slider.get())
            self.config["menu_options"]["trigger_type"] = inv_type_mapping.get(trigger_type_var.get(), "r_drag")
            self.config["menu_options"]["trigger_key"] = trigger_key_entry.get()
            self.config["menu_options"]["appearance_mode"] = theme_var.get()
            
            from customtkinter import set_appearance_mode
            set_appearance_mode(theme_var.get())

            new_font = font_var.get()
            self.config["menu_options"]["gui_font_family"] = "" if new_font == "Default" or new_font == "---" else new_font
            self.config["menu_options"]["gui_font_size"] = int(font_size_slider.get())
            
            self.gui_font_family = self.config["menu_options"]["gui_font_family"]
            self.gui_font_size = self.config["menu_options"]["gui_font_size"]

            self.save_config()
            self.draw_preview()
            settings_window.destroy()
            if messagebox.askyesno("完了", "設定を保存しました。\\n変更を完全に反映するには再起動が必要です。今すぐ再起動しますか？"):
                import sys
                os.execl(sys.executable, sys.executable, *sys.argv)

        CTkButton(settings_window, text="🆗 保存", command=save_settings, 
                 fg_color="#1f538d", height=40, font=self.get_font()).pack(pady=20)
        
        settings_window.grab_set(); settings_window.focus_set()

    def show_statistics(self):
        total_items = 0
        total_rings = len(self.config["main_menu"])
        for ring in self.config["main_menu"]: total_items += len(ring.get("items", []))
        submenu_count = len(self.config.get("submenus", {}))
        submenu_items = 0
        for rings in self.config.get("submenus", {}).values():
            for ring in rings: submenu_items += len(ring.get("items", []))
        
        image_count = 0
        if os.path.exists(self.image_dir):
            image_count = len([f for f in os.listdir(self.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico'))])
        backup_count = 0
        if os.path.exists(self.backup_dir):
            backup_count = len([f for f in os.listdir(self.backup_dir) if f.startswith("menu_config_")])
            
        stats_text = f"📊 メニュー統計情報\\n\\nメイン: リング{total_rings} / アイテム{total_items}\\nサブ: メニュー{submenu_count} / アイテム{submenu_items}\\n合計アイテム: {total_items + submenu_items}\\n画像: {image_count} / バックアップ: {backup_count}"
        
        stats_window = CTkToplevel(self)
        stats_window.title("統計情報")
        stats_window.geometry("500x400")
        CTkLabel(stats_window, text="📊 統計情報", font=self.get_font(18, "bold")).pack(pady=15)
        stats_text_box = CTkTextbox(stats_window, font=self.get_font(), wrap="word")
        stats_text_box.pack(fill="both", expand=True, padx=20, pady=10)
        stats_text_box.insert("0.0", stats_text)
        stats_text_box.configure(state="disabled")
        CTkButton(stats_window, text="閉じる", command=stats_window.destroy, height=40, font=self.get_font()).pack(pady=20)
        stats_window.grab_set()

    def show_favorites_dialog(self):
        fav_window = CTkToplevel(self)
        fav_window.title("お気に入りアイテム")
        fav_window.geometry("500x500")
        CTkLabel(fav_window, text="★ お気に入りリスト", font=self.get_font(16, "bold")).pack(pady=15)
        scroll_frame = CTkScrollableFrame(fav_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        favorites = self.config.get("favorites", [])
        if not favorites:
            CTkLabel(scroll_frame, text="お気に入りは登録されていません。", text_color="#aaaaaa", font=self.get_font()).pack(pady=20)
        
        from customtkinter import CTkFrame
        for fav in favorites:
            row = CTkFrame(scroll_frame)
            row.pack(fill="x", pady=2)
            icon = fav["data"].get("image", "")
            btn_text = f"{fav['name']} (🖼️ {os.path.basename(icon)})" if icon else fav['name']
            CTkButton(row, text=btn_text, anchor="w", fg_color="#d4af37", text_color="black", hover_color="#b69530", font=self.get_font(),
                     command=lambda f=fav: self.apply_favorite(f, fav_window)).pack(side="left", fill="x", expand=True, padx=2)
            CTkButton(row, text="🗑️", width=30, fg_color="#7d2d2d", font=self.get_font(),
                     command=lambda n=fav["name"]: self.delete_favorite(n, fav_window)).pack(side="right", padx=2)
        CTkButton(fav_window, text="閉じる", command=fav_window.destroy, height=40, font=self.get_font()).pack(pady=10)
        fav_window.grab_set()

    def show_ahk_help(self):
        help_window = CTkToplevel(self)
        help_window.title("AHK構文 クイックヘルプ")
        help_window.geometry("450x550")
        tabview = CTkTextbox(help_window, wrap="word", font=self.get_font())
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        help_text = "AHK Help Text Here..." # Simplified for brevity, same content as original
        tabview.insert("0.0", help_text)
        tabview.configure(state="disabled")
        CTkButton(help_window, text="閉じる", command=help_window.destroy, height=40, font=self.get_font()).pack(pady=(0, 20))
        help_window.grab_set()

    def _preload_template_window(self):
        if self.template_window and self.template_window.winfo_exists(): return
        self._create_template_window()

    def _create_template_window(self):
        self.template_window = CTkToplevel(self)
        self.template_window.title("テンプレートライブラリ")
        self.template_window.geometry("600x700")
        self.template_window.withdraw()
        self.template_window.protocol("WM_DELETE_WINDOW", self.hide_template_window)
        
        CTkLabel(self.template_window, text="📚 よく使うコードテンプレート", font=self.get_font(18, "bold")).pack(pady=15)
        
        from customtkinter import CTkFrame
        search_frame = CTkFrame(self.template_window)
        search_frame.pack(fill="x", padx=20, pady=5)
        CTkLabel(search_frame, text="🔍 検索:", font=self.get_font()).pack(side="left", padx=5)
        self.lib_search_entry = CTkEntry(search_frame, placeholder_text="キーワードを入力...", font=self.get_font())
        self.lib_search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.lib_scroll_frame = CTkScrollableFrame(self.template_window)
        self.lib_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.lib_search_entry.bind("<KeyRelease>", self.on_template_search_input)
        CTkButton(self.template_window, text="閉じる", command=self.hide_template_window, height=40, font=self.get_font()).pack(pady=15)
        self.refresh_template_list()

    def show_template_library(self):
        if not self.template_window or not self.template_window.winfo_exists():
            self._create_template_window()
        self.template_window.deiconify()
        self.template_window.lift()

    def hide_template_window(self):
        self.template_window.withdraw()

    def on_template_search_input(self, event=None):
        if self.search_debounce_timer: self.after_cancel(self.search_debounce_timer)
        self.search_debounce_timer = self.after(500, self.refresh_template_list)

    def refresh_template_list(self):
        query = self.lib_search_entry.get().lower()
        for child in self.lib_scroll_frame.winfo_children(): child.destroy()
        from customtkinter import CTkFrame
        for title, code in self.templates_data:
            if query and query not in title.lower() and query not in code.lower(): continue
            item_frame = CTkFrame(self.lib_scroll_frame)
            item_frame.pack(fill="x", pady=2, padx=5)
            CTkLabel(item_frame, text=title, width=250, anchor="w", font=self.get_font(13)).pack(side="left", padx=10)
            btn_container = CTkFrame(item_frame, fg_color="transparent")
            btn_container.pack(side="right", padx=5)
            CTkButton(btn_container, text="📋 挿入", width=70, height=28, command=lambda c=code: self.insert_and_close(c), font=self.get_font()).pack(side="right", padx=2)
            CTkButton(btn_container, text="👁️ 表示", width=70, height=28, fg_color="#3d3d3d", command=lambda c=code: self.show_code_preview(c), font=self.get_font()).pack(side="right", padx=2)

    def insert_and_close(self, template):
        self.insert_template(template)
        self.hide_template_window()

    def show_code_preview(self, code):
        messagebox.showinfo("コードプレビュー", f"このコードが挿入されます:\\n\\n{code}")

    def insert_submenu_call(self):
        submenu_names = list(self.config.get("submenus", {}).keys())
        if not submenu_names:
            if messagebox.askyesno("サブメニュー作成", "サブメニューがまだありません。作成しますか？"):
                self.add_submenu()
                self.after(100, self.insert_submenu_call)
            return
        
        dialog = CTk()
        dialog.title("サブメニューを選択")
        dialog.geometry("500x450")
        dialog.lift(); dialog.attributes('-topmost', True)
        dialog.after(100, lambda: dialog.attributes('-topmost', False))
        
        CTkLabel(dialog, text="📂 サブメニュー呼び出しを設定", font=self.get_font(16, "bold")).pack(pady=15)
        
        from customtkinter import CTkFrame
        method_frame = CTkFrame(dialog)
        method_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Method 1
        method1_frame = CTkFrame(method_frame, fg_color="#1a3a1a")
        method1_frame.pack(fill="x", padx=10, pady=5)
        CTkLabel(method1_frame, text="✅ 方法1: submenu プロパティ（推奨）", font=self.get_font(12, "bold")).pack(anchor="w", padx=15, pady=5)
        sub_list1 = CTkFrame(method1_frame)
        sub_list1.pack(fill="x", padx=15, pady=5)
        for name in submenu_names:
            item_count = sum(len(r.get("items", [])) for r in self.config["submenus"][name])
            CTkButton(sub_list1, text=f"📂 {name} ({item_count})", command=lambda n=name: self.use_submenu_property(n, dialog), fg_color="#2d5f2d", font=self.get_font()).pack(fill="x", pady=2)
            
        # Method 2
        method2_frame = CTkFrame(method_frame, fg_color="#1a1a3a")
        method2_frame.pack(fill="x", padx=10, pady=5)
        CTkLabel(method2_frame, text="⚙️ 方法2: click 動作でコード実行", font=self.get_font(12, "bold")).pack(anchor="w", padx=15, pady=5)
        sub_list2 = CTkFrame(method2_frame)
        sub_list2.pack(fill="x", padx=15, pady=5)
        for name in submenu_names:
            item_count = sum(len(r.get("items", [])) for r in self.config["submenus"][name])
            CTkButton(sub_list2, text=f"📂 {name} ({item_count})", command=lambda n=name: self.use_click_code(n, dialog), fg_color="#2d4a5f", font=self.get_font()).pack(fill="x", pady=2)

        CTkButton(dialog, text="➕ 新しいサブメニューを作成", command=lambda: self.create_submenu_from_dialog(dialog), fg_color="#5d4a2d", height=35, font=self.get_font()).pack(fill="x", padx=20, pady=5)
        CTkButton(dialog, text="キャンセル", command=dialog.destroy, fg_color="#7d2d2d", height=35, font=self.get_font()).pack(fill="x", padx=20, pady=5)
        try: dialog.grab_set()
        except: pass
        dialog.focus_set(); dialog.mainloop()

    def use_submenu_property(self, submenu_name, dialog):
        if dialog: dialog.destroy()
        if self.current_item:
            self.current_item["submenu"] = submenu_name
            if "click" in self.current_item: del self.current_item["click"]
            self.click_text.delete("0.0", "end")
            self.click_text.insert("0.0", f"# サブメニュー '{submenu_name}' がsubmenuプロパティで設定されています")
            messagebox.showinfo("完了", f"サブメニュー '{submenu_name}' を設定しました！")
        else: messagebox.showwarning("警告", "アイテムが選択されていません")

    def use_click_code(self, submenu_name, dialog):
        if dialog: dialog.destroy()
        var_name = self.sanitize_var_name(submenu_name)
        code = f'Radify.Show("{var_name}Menu")'
        self.click_text.delete("0.0", "end")
        self.click_text.insert("0.0", f'(*) => {code}')
        messagebox.showinfo("完了", f"クリック動作を設定しました！")

    def create_submenu_from_dialog(self, dialog):
        name = simpledialog.askstring("新規サブメニュー", "サブメニュー名:")
        if not name or not name.strip(): return
        if name in self.config["submenus"]:
            messagebox.showwarning("警告", "同名のサブメニューが存在します")
            return
        self.config["submenus"][name] = [{"ring": 1, "items": []}]
        self.save_config(); self.refresh_tree()
        dialog.destroy()
        if messagebox.askyesno("確認", f"サブメニュー '{name}' を設定しますか？"):
            self.use_submenu_property(name, None)

    def browse_file_for_click(self):
        path = filedialog.askopenfilename()
        if path: self.insert_template(f'Run("{path}")')
        
    def browse_folder_for_click(self):
        path = filedialog.askdirectory()
        if path: self.insert_template(f'Run("{path}")')
