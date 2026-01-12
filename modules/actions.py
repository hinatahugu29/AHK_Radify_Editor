import tkinter.messagebox as messagebox
from tkinter import simpledialog
import json
import copy

class ActionsMixin:
    def refresh_tree(self):
        """ツリービューを更新"""
        # 現在の選択と展開状態を保存
        selected = self.tree.selection()
        selected_path_values = []
        if selected:
            item = selected[0]
            while item:
                # テキストではなく値を保存
                val = self.tree.item(item, "values")
                tag = self.tree.item(item, "tags")
                selected_path_values.insert(0, (tag[0] if tag else None, val))
                item = self.tree.parent(item)
        
        # 展開されている項目の全パスを保存
        def get_all_open_value_paths(parent=""):
            paths = []
            for child in self.tree.get_children(parent):
                if self.tree.item(child, "open"):
                    path = []
                    curr = child
                    while curr:
                        val = self.tree.item(curr, "values")
                        tag = self.tree.item(curr, "tags")
                        path.insert(0, (tag[0] if tag else None, val))
                        curr = self.tree.parent(curr)
                    paths.append(path)
                    paths.extend(get_all_open_value_paths(child))
            return paths

        open_value_paths = get_all_open_value_paths()
        
        self.tree.delete(*self.tree.get_children())
        
        # メインリング
        main_iid = self.tree.insert("", "end", text="📊 メインメニュー", open=True, tags=("main_root",), values=("main_root",))
        for i, ring in enumerate(self.config["main_menu"]):
            ring_text = f"🔵 リング {ring['ring']} ({len(ring['items'])} アイテム)"
            ring_iid = self.tree.insert(main_iid, "end", text=ring_text, 
                                       values=("main_ring", i), tags=("ring",))
            for j, item in enumerate(ring["items"]):
                img = item.get("image", "")
                text = item.get("text", "（無題）")
                item_text = f"  🔹 {text}" + (f" [{img}]" if img else "")
                self.tree.insert(ring_iid, "end", text=item_text, 
                               values=("item", i, j), tags=("item",))

        # サブメニュー
        sub_iid = self.tree.insert("", "end", text="📑 サブメニュー", open=True, tags=("sub_root",), values=("sub_root",))
        for submenu_name, rings in self.config["submenus"].items():
            sub_menu_text = f"📂 {submenu_name} ({sum(len(r['items']) for r in rings)} アイテム)"
            sub_menu_iid = self.tree.insert(sub_iid, "end", text=sub_menu_text, 
                                           values=("submenu", submenu_name), tags=("submenu",))
            for i, ring in enumerate(rings):
                ring_label = ring.get("ring", "不明")
                ring_text = f"  🟢 {ring_label} ({len(ring['items'])} アイテム)"
                ring_iid = self.tree.insert(sub_menu_iid, "end", text=ring_text, 
                                           values=("sub_ring", submenu_name, i), tags=("ring",))
                for j, item in enumerate(ring["items"]):
                    img = item.get("image", "")
                    text = item.get("text", "（無題）")
                    item_text = f"    🔸 {text}" + (f" [{img}]" if img else "")
                    self.tree.insert(ring_iid, "end", text=item_text, 
                                   values=("item", submenu_name, i, j), tags=("item",))

        # 展開状態を復元
        def restore_expansion_state_by_values(paths):
            for path in paths:
                curr_parent = ""
                for tag, target_val in path:
                    found = False
                    for child in self.tree.get_children(curr_parent):
                        c_val = list(self.tree.item(child, "values"))
                        if list(map(str, c_val)) == list(map(str, target_val)):
                            self.tree.item(child, open=True)
                            curr_parent = child
                            found = True
                            break
                    if not found:
                        break

        restore_expansion_state_by_values(open_value_paths)

        if selected_path_values:
            self.restore_selection_by_values(selected_path_values)

        self.draw_preview()

    def restore_selection_by_values(self, path_values):
        """ツリーの選択を復元（値ベース）"""
        curr_parent = ""
        last_found = None
        
        for tag, target_val in path_values:
            found = False
            for child in self.tree.get_children(curr_parent):
                c_val = list(self.tree.item(child, "values"))
                if list(map(str, c_val)) == list(map(str, target_val)):
                    last_found = child
                    curr_parent = child
                    found = True
                    break
            if not found:
                break
        
        if last_found:
            self.tree.selection_set(last_found)
            self.tree.see(last_found)

    def on_tree_click(self, event):
        item_iid = self.tree.identify_row(event.y)
        if item_iid:
            self.drag_data["item"] = item_iid
            self.drag_data["index"] = self.tree.index(item_iid)

    def on_tree_drag(self, event):
        if not self.drag_data["item"]:
            return
        
        target_iid = self.tree.identify_row(event.y)
        if target_iid and target_iid != self.drag_data["item"]:
            source_vals = self.tree.item(self.drag_data["item"], "values")
            target_vals = self.tree.item(target_iid, "values")
            
            if source_vals and source_vals[0] == "item":
                if target_vals and target_vals[0] in ("item", "main_ring", "sub_ring"):
                    self.tree.configure(cursor="hand2")
                    return
            
        self.tree.configure(cursor="no")

    def on_tree_drop(self, event):
        self.tree.configure(cursor="")
        if not self.drag_data["item"]:
            return
        
        source_iid = self.drag_data["item"]
        target_iid = self.tree.identify_row(event.y)
        
        if not target_iid or source_iid == target_iid:
            self.drag_data = {"item": None, "index": None}
            return
        
        source_values = self.tree.item(source_iid, "values")
        target_values = self.tree.item(target_iid, "values")
        
        if not source_values or not target_values:
            self.drag_data = {"item": None, "index": None}
            return

        if source_values[0] == "item":
            self.push_history()
            self.move_item(source_values, target_values)
        
        self.drag_data = {"item": None, "index": None}

    def move_item(self, source_values, target_values):
        if len(source_values) == 3:
            src_ring_idx = int(source_values[1])
            src_idx = int(source_values[2])
            src_list = self.config["main_menu"][src_ring_idx]["items"]
        else:
            src_sub_name = source_values[1]
            src_ring_idx = int(source_values[2])
            src_idx = int(source_values[3])
            src_list = self.config["submenus"][src_sub_name][src_ring_idx]["items"]
            
        item = src_list[src_idx]
        
        t_type = target_values[0]
        
        if t_type == "item":
            if len(target_values) == 3:
                dest_ring_idx = int(target_values[1])
                dest_idx = int(target_values[2])
                dest_list = self.config["main_menu"][dest_ring_idx]["items"]
            else:
                dest_sub_name = target_values[1]
                dest_ring_idx = int(target_values[2])
                dest_idx = int(target_values[3])
                dest_list = self.config["submenus"][dest_sub_name][dest_ring_idx]["items"]
        elif t_type in ("main_ring", "sub_ring"):
            if t_type == "main_ring":
                dest_ring_idx = int(target_values[1])
                dest_list = self.config["main_menu"][dest_ring_idx]["items"]
                dest_idx = len(dest_list)
            else:
                dest_sub_name = target_values[1]
                dest_ring_idx = int(target_values[2])
                dest_list = self.config["submenus"][dest_sub_name][dest_ring_idx]["items"]
                dest_idx = len(dest_list)
        else:
            return

        if src_list is dest_list:
            src_list.pop(src_idx)
            if dest_idx > src_idx:
                dest_idx -= 1
            dest_list.insert(dest_idx, item)
        else:
            src_list.pop(src_idx)
            dest_list.insert(dest_idx, item)

        self.save_config()
        self.refresh_tree()
        self.draw_preview()

    def on_tree_double_click(self, event):
        item_iid = self.tree.identify_row(event.y)
        if not item_iid:
            return
        
        values = self.tree.item(item_iid, "values")
        if not values:
            return
        
        item_type = values[0]
        
        if item_type in ("main_ring", "sub_ring", "submenu"):
            self.edit_selected_ring_or_menu()

    def on_tree_select(self, event):
        if self.is_loading:
            return
        sel = self.tree.selection()
        if not sel:
            return
        self.is_loading = True
        try:
            self._perform_on_tree_select(sel[0])
        finally:
            self.is_loading = False

    def _perform_on_tree_select(self, item_iid):
        values = self.tree.item(item_iid, "values")
        if not values: return

        item_type = values[0]
        
        if item_type == "main_root" or item_type == "main_ring":
            self.current_menu = "main"
        elif item_type == "sub_root":
            self.current_menu = "main"
        elif item_type == "submenu":
            self.current_menu = values[1]
        elif item_type == "sub_ring":
            self.current_menu = values[1]
        elif item_type == "item":
            if len(values) == 3:
                self.current_menu = "main"
            elif len(values) == 4:
                self.current_menu = values[1]

        self.draw_preview()

        if item_type != "item":
            self.current_item = None
            self.current_ring = None
            self.clear_edit_fields()
            return

        if self.current_menu == "main":
            ring_idx = int(values[1])
            item_idx = int(values[2])
            self.current_parent = self.config["main_menu"][ring_idx]["items"]
            self.current_ring = self.config["main_menu"][ring_idx]
        else:
            submenu_name = self.current_menu
            ring_idx = int(values[2])
            item_idx = int(values[3])
            self.current_parent = self.config["submenus"][submenu_name][ring_idx]["items"]
            self.current_ring = self.config["submenus"][submenu_name][ring_idx]

        self.current_item = self.current_parent[item_idx]

        self.text_entry.delete(0, "end")
        self.text_entry.insert(0, self.current_item.get("text", ""))

        self.click_text.delete("1.0", "end")
        self.click_text.insert("1.0", self.current_item.get("click", ""))

        self.tooltip_entry.delete(0, "end")
        self.tooltip_entry.insert(0, self.current_item.get("tooltip", ""))

        img = self.current_item.get("image", "（なし）")
        self.image_combo.set(img if img else "（なし）")
        self.on_image_select(self.image_combo.get())

        self.refresh_submenu_combo()
        sub = self.current_item.get("submenu", "（なし）")
        self.submenu_combo.set(sub if sub else "（なし）")
        
        self.update_click_ui_state(sub)

    def add_new_ring(self):
        active_menu = getattr(self, "current_menu", "main")
        self.push_history()
        
        if active_menu == "main":
            new_ring_num = max([r["ring"] for r in self.config["main_menu"]], default=0) + 1
            self.config["main_menu"].append({"ring": new_ring_num, "items": []})
            msg = f"メイン リング {new_ring_num} を追加しました"
        else:
            if active_menu not in self.config["submenus"]:
                messagebox.showerror("エラー", f"サブメニュー '{active_menu}' が見つかりません")
                return
            rings = self.config["submenus"][active_menu]
            new_index = len(rings) + 1
            rings.append({"ring": f"Ring {new_index}", "items": []})
            msg = f"サブメニュー '{active_menu}' にリング {new_index} を追加しました"
            
        self.save_config()
        self.refresh_tree()
        self.draw_preview()
        messagebox.showinfo("完了", msg)

    def add_submenu(self):
        name = simpledialog.askstring("サブメニュー名", "新しいサブメニューの名前を入力してください")
        if not name or not name.strip(): return
        name = name.strip()
        if name in self.config["submenus"]:
            messagebox.showwarning("警告", "同名のサブメニューが既に存在します")
            return
            
        self.push_history()
        self.config["submenus"][name] = [{"ring": 1, "items": []}]
        self.save_config()
        self.refresh_tree()
        messagebox.showinfo("完了", f"サブメニュー '{name}' を追加しました")

    def add_new_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("情報", "アイテムを追加するリングを選択してください")
            return
        
        item_iid = sel[0]
        values = self.tree.item(item_iid, "values")
        
        if not values or values[0] not in ("main_ring", "sub_ring"):
            messagebox.showinfo("情報", 
                "アイテムを追加するリングを選択してください\\n" +
                "（ツリーで「リング」の行をクリック）")
            return

        self.push_history()
        new_item = {
            "text": "新規アイテム",
            "click": 'Run("https://example.com")',
            "tooltip": ""
        }
        
        if values[0] == "main_ring":
            ring_idx = int(values[1])
            self.config["main_menu"][ring_idx]["items"].append(new_item)
        else:
            submenu_name = values[1]
            ring_idx = int(values[2])
            self.config["submenus"][submenu_name][ring_idx]["items"].append(new_item)
            
        self.save_config()
        self.refresh_tree()
        self.draw_preview()

    def edit_selected_ring_or_menu(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("情報", "編集する項目を選択してください")
            return
        
        values = self.tree.item(sel[0], "values")
        if not values: return
        
        item_type = values[0]
        
        if item_type == "main_ring":
            ring_idx = int(values[1])
            current_ring = self.config["main_menu"][ring_idx]["ring"]
            new_ring = simpledialog.askinteger("リング番号変更", f"現在の値: {current_ring}", initialvalue=current_ring, minvalue=1)
            if new_ring and new_ring != current_ring:
                self.config["main_menu"][ring_idx]["ring"] = new_ring
                self.save_config(); self.refresh_tree()
        
        elif item_type == "sub_ring":
            submenu_name = values[1]
            ring_idx = int(values[2])
            current_label = self.config["submenus"][submenu_name][ring_idx]["ring"]
            new_label = simpledialog.askstring("リングラベル変更", f"現在の値: {current_label}", initialvalue=current_label)
            if new_label and new_label != current_label:
                self.config["submenus"][submenu_name][ring_idx]["ring"] = new_label
                self.save_config(); self.refresh_tree()
        
        elif item_type == "submenu":
            old_name = values[1]
            new_name = simpledialog.askstring("サブメニュー名変更", f"現在の値: {old_name}", initialvalue=old_name)
            if new_name and new_name != old_name and new_name.strip():
                new_name = new_name.strip()
                if new_name not in self.config["submenus"]:
                    self.config["submenus"][new_name] = self.config["submenus"].pop(old_name)
                    self.save_config(); self.refresh_tree()
                else:
                    messagebox.showwarning("警告", "同名のサブメニューが既に存在します")

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        
        if not messagebox.askyesno("確認", f"選択された {len(sel)} 件の項目を削除しますか？"): return
        self.push_history()
        
        to_delete = []
        for iid in sel:
            vals = self.tree.item(iid, "values")
            if vals: to_delete.append((vals[0], vals, iid))
        
        items_to_del = [x for x in to_delete if x[0] == "item"]
        main_items = [x for x in items_to_del if len(x[1]) == 3]
        main_items.sort(key=lambda x: (int(x[1][1]), int(x[1][2])), reverse=True)
        sub_items = [x for x in items_to_del if len(x[1]) == 4]
        sub_items.sort(key=lambda x: (x[1][1], int(x[1][2]), int(x[1][3])), reverse=True)

        for _, vals, _ in main_items:
            del self.config["main_menu"][int(vals[1])]["items"][int(vals[2])]
        for _, vals, _ in sub_items:
            del self.config["submenus"][vals[1]][int(vals[2])]["items"][int(vals[3])]

        others = [x for x in to_delete if x[0] in ("main_ring", "sub_ring", "submenu")]
        m_rings = [x for x in others if x[0] == "main_ring"]
        m_rings.sort(key=lambda x: int(x[1][1]), reverse=True)
        for _, vals, _ in m_rings:
            if len(self.config["main_menu"]) > 1: del self.config["main_menu"][int(vals[1])]
            
        s_rings = [x for x in others if x[0] == "sub_ring"]
        s_rings.sort(key=lambda x: (x[1][1], int(x[1][2])), reverse=True)
        for _, vals, _ in s_rings:
            if len(self.config["submenus"][vals[1]]) > 1: del self.config["submenus"][vals[1]][int(vals[2])]
            
        sub_menus = [x for x in others if x[0] == "submenu"]
        for _, vals, _ in sub_menus:
            if vals[1] in self.config["submenus"]: del self.config["submenus"][vals[1]]

        self.save_config()
        self.refresh_tree()
        self.draw_preview()
        self.current_item = None
        self.clear_edit_fields()

    def delete_item(self):
        if not self.current_item or not self.current_parent: return
        if not messagebox.askyesno("確認", "このアイテムを削除しますか？"): return
        self.push_history()
        self.current_parent.remove(self.current_item)
        self.save_config()
        self.refresh_tree()
        self.draw_preview()
        self.current_item = None
        self.clear_edit_fields()

    def apply_item(self, silent=False):
        if not self.current_item: return
        self.current_item["text"] = self.text_entry.get()
        
        img_val = self.image_combo.get()
        if img_val and img_val != "（なし）":
            self.current_item["image"] = img_val
        elif "image" in self.current_item:
            del self.current_item["image"]

        if self.submenu_combo.get() == "（なし）":
            self.current_item["click"] = self.click_text.get("1.0", "end").strip()
            if "submenu" in self.current_item: del self.current_item["submenu"]
        else:
            self.current_item["submenu"] = self.submenu_combo.get()
        self.current_item["tooltip"] = self.tooltip_entry.get()
        if not silent: self.save_config(); self.refresh_tree()
        self.draw_preview()

    def move_up(self): self._move_item_in_list(-1)
    def move_down(self): self._move_item_in_list(1)
    
    def _move_item_in_list(self, direction):
        if not self.current_item or not self.current_parent: return
        idx = self.current_parent.index(self.current_item)
        new_idx = idx + direction
        if 0 <= new_idx < len(self.current_parent):
            self.push_history()
            self.current_parent[idx], self.current_parent[new_idx] = self.current_parent[new_idx], self.current_parent[idx]
            self.save_config()
            self.refresh_tree()
            self.draw_preview()

    def copy_item(self):
        if self.current_item:
            self.clipboard = copy.deepcopy(self.current_item)
            messagebox.showinfo("コピー", "アイテムをコピーしました")

    def paste_item(self):
        if not self.clipboard: return
        if not self.current_parent:
            messagebox.showinfo("情報", "貼り付け先のリングを選択してください")
            return
        self.push_history()
        self.current_parent.append(copy.deepcopy(self.clipboard))
        self.save_config()
        self.refresh_tree()
        self.draw_preview()

    def push_history(self):
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        snapshot = json.dumps(self.config)
        if self.history and self.history[self.history_index] == snapshot: return
        self.history.append(snapshot)
        self.history_index += 1
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.config = json.loads(self.history[self.history_index])
            self.refresh_all()
    
    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.config = json.loads(self.history[self.history_index])
            self.refresh_all()

    def on_submenu_combo_select(self, choice):
        if not self.current_item: return
        if choice == "（なし）":
            if "submenu" in self.current_item: del self.current_item["submenu"]
        else:
            self.current_item["submenu"] = choice
            current_text = self.text_entry.get().strip()
            if not current_text or current_text == "新規アイテム":
                self.text_entry.delete(0, "end")
                self.text_entry.insert(0, choice)
        self.update_click_ui_state(choice)
        self.apply_item(silent=True)
        self.draw_preview()

    def insert_template(self, template):
        if self.submenu_combo.get() != "（なし）":
            self.submenu_combo.set("（なし）")
            self.on_submenu_combo_select("（なし）")
        self.click_text.configure(state="normal")
        current_pos = self.click_text.index("insert")
        self.click_text.insert(current_pos, template + "\\n")
        self.click_text.see(current_pos)

    def add_to_favorites(self):
        if not self.current_item:
            messagebox.showinfo("情報", "お気に入りに追加するアイテムを選択してください")
            return
        current_text = self.current_item.get("text", "新規アイテム")
        name = simpledialog.askstring("お気に入り追加", "お気に入りの名前を入力してください", initialvalue=current_text)
        if not name or not name.strip(): return
        
        name = name.strip()
        new_fav = {"name": name, "data": self.current_item}
        
        if any(f["name"] == name for f in self.config.get("favorites", [])):
            if not messagebox.askyesno("確認", f"'{name}' は既に存在します。上書きしますか？"): return
            self.config["favorites"] = [f for f in self.config["favorites"] if f["name"] != name]
            
        self.config["favorites"].append(new_fav)
        self.save_config()
        messagebox.showinfo("完了", f"'{name}' をお気に入りに追加しました！")

    def apply_favorite(self, fav_data, window):
        if not self.current_item:
            messagebox.showinfo("情報", "適用先のアイテムを選択してください")
            window.destroy()
            return
        if not messagebox.askyesno("確認", f"現在のアイテムを '{fav_data['name']}' の内容で上書きしますか？"): return
        new_data = copy.deepcopy(fav_data["data"])
        self.current_item.clear()
        self.current_item.update(new_data)
        self.save_config()
        self.refresh_tree()
        self.draw_preview()
        if self.tree.selection(): self.on_tree_select(None)
        window.destroy()
        messagebox.showinfo("完了", "適用しました！")

    def delete_favorite(self, name, window):
        if messagebox.askyesno("確認", f"'{name}' を削除しますか？"):
            self.config["favorites"] = [f for f in self.config["favorites"] if f["name"] != name]
            self.save_config()
            window.destroy()
            self.show_favorites_dialog()
