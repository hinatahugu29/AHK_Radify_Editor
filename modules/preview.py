from PIL import Image, ImageTk
import math
import os

class PreviewMixin:
    def draw_preview(self):
        """プレビューを描画（デバウンス処理）"""
        if self.preview_update_pending:
            return
            
        self.preview_update_pending = True
        self.after(20, self._perform_draw_preview) # 20ms後に実行

    def _perform_draw_preview(self):
        """実際のプレビュー描画処理"""
        self.preview_update_pending = False
        
        # 非表示時は描画スキップ
        try:
            if not self.preview_canvas.winfo_ismapped():
                return
        except:
            return

        self.preview_canvas.delete("all")
        self.preview_click_areas = [] # クリア
        w = self.preview_canvas.winfo_width()
        h = self.preview_canvas.winfo_height()
        
        if w < 100 or h < 100:
            return

        center_x, center_y = w // 2, h // 2
        item_size = int(self.config["menu_options"].get("itemSize", 60) * self.preview_scale)
        glow = self.config["menu_options"].get("EnableGlow", True)
        ring_spacing = int(self.config["menu_options"].get("ringSpacing", 80) * self.preview_scale)

        # 表示対象のリングを抽出
        active_menu = getattr(self, "current_menu", "main")
        all_rings = []
        
        if active_menu == "main":
            menu_title = "メインメニュー"
            for i, ring in enumerate(self.config["main_menu"]):
                all_rings.append(("main", i, ring))
        else:
            menu_title = f"サブメニュー: {active_menu}"
            if active_menu in self.config["submenus"]:
                for i, ring in enumerate(self.config["submenus"][active_menu]):
                    all_rings.append(("sub", active_menu, i, ring))

        # プレビューのタイトル表示
        preview_title_font = self.get_font(12, "bold")
        self.preview_canvas.create_text(
            15, 15, text=f"👁️ Preview: {menu_title}", fill="#ffffff", 
            font=preview_title_font, anchor="nw"
        )

        base_radius = int(100 * self.preview_scale)

        for ring_idx, ring_data in enumerate(all_rings):
            radius = base_radius + ring_idx * ring_spacing
            
            if len(ring_data) == 3:
                ring_type, idx, ring = ring_data
                ring_label = f"リング {ring['ring']}"
            else:
                ring_type, submenu_name, idx, ring = ring_data
                ring_label = f"リング {ring.get('ring', idx+1)}"
            
            items = ring.get("items", [])
            
            # リング円を描画
            self.preview_canvas.create_oval(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                outline="#444444", width=1, dash=(3, 3)
            )
            
            # リングラベル
            ring_label_font = self.get_font(9)
            self.preview_canvas.create_text(
                center_x + radius + 10, center_y,
                text=ring_label, fill="#888888", font=ring_label_font,
                anchor="w"
            )
            
            if not items:
                continue
            
            angle_step = 360 / len(items)
            
            for i, item in enumerate(items):
                angle = math.radians(i * angle_step - 90)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                # 選択中・ホバー中のアイテムをハイライト
                is_selected = (self.current_item == item)
                is_hovered = (self.hovered_item and self.hovered_item[-1][1] == ["item", idx, i]) if ring_type == "main" else \
                             (self.hovered_item and self.hovered_item[-1][1] == ["item", submenu_name, idx, i])
                
                # グロー効果
                if glow:
                    if is_selected:
                        glow_size = item_size // 2 + 15
                        self.preview_canvas.create_oval(
                            x - glow_size, y - glow_size,
                            x + glow_size, y + glow_size,
                            fill="#ffcc00", outline="", stipple="gray50"
                        )
                    elif is_hovered:
                        glow_size = item_size // 2 + 10
                        self.preview_canvas.create_oval(
                            x - glow_size, y - glow_size,
                            x + glow_size, y + glow_size,
                            fill="#ffffff", outline="", stipple="gray50"
                        )
                    else:
                        glow_size = item_size // 2 + 8
                        self.preview_canvas.create_oval(
                            x - glow_size, y - glow_size,
                            x + glow_size, y + glow_size,
                            fill="#666666", outline="", stipple="gray75"
                        )

                # アイテム本体
                rect_color = "#ff6600" if is_selected else ("#8888ff" if is_hovered else "#5555ff")
                outline_color = "white" if (is_selected or is_hovered) else "#aaaaaa"
                
                # アイコン表示の試行
                img_name = item.get("image")
                photo = self.get_cached_image(img_name, item_size - 4) if img_name else None
                
                if photo:
                    # 背景
                    self.preview_canvas.create_rectangle(
                        x - item_size//2, y - item_size//2,
                        x + item_size//2, y + item_size//2,
                        fill="#222222", outline=outline_color, width=2
                    )
                    # 画像
                    self.preview_canvas.create_image(x, y, image=photo)
                else:
                    # 四角形のみ
                    self.preview_canvas.create_rectangle(
                        x - item_size//2, y - item_size//2,
                        x + item_size//2, y + item_size//2,
                        fill=rect_color, outline=outline_color, width=2
                    )

                # クリック判定用座標を保存
                if ring_type == "main":
                    item_path = [("main_root", ["main_root"]), ("ring", ["main_ring", idx]), ("item", ["item", idx, i])]
                else:
                    item_path = [("sub_root", ["sub_root"]), ("submenu", ["submenu", submenu_name]), ("ring", ["sub_ring", submenu_name, idx]), ("item", ["item", submenu_name, idx, i])]
                
                self.preview_click_areas.append((
                    x - item_size//2, y - item_size//2,
                    x + item_size//2, y + item_size//2,
                    item_path
                ))

                # テキスト
                text = item.get("text", "NoText")
                text_color = "white" if (is_selected or is_hovered) else "#cccccc"
                item_text_font = self.get_font(int(10 * self.preview_scale), "bold" if is_selected else "normal")
                self.preview_canvas.create_text(
                    x, y + item_size//2 + 15 * self.preview_scale,
                    text=text, fill=text_color,
                    font=item_text_font
                )
                
                # ツールチップ（ホバー時のみ簡易表示）
                if is_hovered and item.get("tooltip"):
                    tt_text = item["tooltip"]
                    tooltip_font = self.get_font(int(9 * self.preview_scale))
                    self.preview_canvas.create_text(
                        x, y - item_size//2 - 15 * self.preview_scale,
                        text=f"💬 {tt_text}", fill="#ffff00",
                        font=tooltip_font,
                        anchor="s"
                    )

    def on_preview_click(self, event):
        """プレビューキャンバスクリック時の処理"""
        for x1, y1, x2, y2, item_path in self.preview_click_areas:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                # アイテムを選択
                self.restore_selection_by_values(item_path)
                return

    def on_zoom_change(self, value):
        """ズーム変更時の処理"""
        self.preview_scale = float(value)
        self.zoom_label.configure(text=f"{int(self.preview_scale * 100)}%")
        self.draw_preview()

    def on_mouse_wheel(self, event):
        """マウスホイールでズーム"""
        if event.delta > 0:
            new_scale = min(2.0, self.preview_scale + 0.1)
        else:
            new_scale = max(0.5, self.preview_scale - 0.1)
        
        self.zoom_slider.set(new_scale)
        self.on_zoom_change(new_scale)

    def on_preview_hover(self, event):
        """ポインタがプレビュー上を移動した時の処理"""
        old_hovered = self.hovered_item
        self.hovered_item = None
        
        for x1, y1, x2, y2, item_path in self.preview_click_areas:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.hovered_item = item_path
                break
        
        if old_hovered != self.hovered_item:
            self.draw_preview()

    def on_hover_leave(self, event=None):
        """ポインタがキャンバスを離れた時の処理"""
        if self.hovered_item:
            self.hovered_item = None
            self.draw_preview()

    def get_cached_image(self, img_name, size):
        """画像をキャッシュして返す（リサイズ込み）"""
        if not img_name:
            return None
            
        cache_key = f"{img_name}_{size}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
            
        img_path = os.path.join(self.image_dir, img_name)
        if not os.path.exists(img_path):
            return None
            
        try:
            with Image.open(img_path) as img:
                img = img.convert("RGBA")
                
                # High quality resize
                # PIL.Image.Resampling.LANCZOS logic from origin code
                img.thumbnail((size, size), Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(img) # create photo image
                self.image_cache[cache_key] = photo
                return photo
        except Exception as e:
            print(f"画像読み込みエラー ({img_name}): {e}")
            return None
