from customtkinter import (
    CTkFrame, CTkLabel, CTkEntry, CTkTextbox,
    CTkButton, CTkComboBox, CTkSlider,
    CTkScrollableFrame, CTkCheckBox
)
from tkinter import Canvas, ttk
import re

class UISetupMixin:
    def get_font(self, size=None, weight="normal"):
        """設定に基づいたフォントを取得"""
        f_size = size if size else self.gui_font_size
        f_family = self.gui_font_family if self.gui_font_family else ""
        return (f_family, int(f_size), weight)
    
    def build_ui(self):
        """UIを構築"""
        # トップメニューバー
        top_menu = CTkFrame(self, height=50)
        top_menu.pack(side="top", fill="x", padx=10, pady=5)
        
        CTkButton(top_menu, text="💾 保存", command=lambda: self.save_config(backup=True), width=100, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="🆕 新規作成", command=self.create_new_project, width=120, fg_color="#2d5f2d", font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="📂 バックアップ復元", command=self.restore_backup, width=150, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="🔄 更新", command=self.refresh_all, width=100, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="⚙️ 設定", command=self.open_settings, width=100, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="📊 統計", command=self.show_statistics, width=100, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="📤 エクスポート", command=self.export_config, width=120, font=self.get_font()).pack(side="left", padx=5)
        CTkButton(top_menu, text="📥 インポート", command=self.import_config, width=120, font=self.get_font()).pack(side="left", padx=5)

        # メメインコンテナ
        main_container = CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)

        # 左側：ツリー + ボタン
        left_frame = CTkFrame(main_container, width=400)
        left_frame.pack(side="left", fill="y", padx=5)

        CTkLabel(left_frame, text="📋 メニュー構造", font=self.get_font(16, "bold")).pack(pady=10)
        
        # ツリービュー
        tree_frame = CTkFrame(left_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeviewスタイル
        style = ttk.Style()
        style.configure("Treeview", font=self.get_font(11))
        style.configure("Treeview.Heading", font=self.get_font(11, "bold"))
        
        self.tree = ttk.Treeview(tree_frame, columns=("type",), show="tree", selectmode="extended")
        self.tree.column("#0", width=350)
        
        # スクロールバー
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # ツリーイベント
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<B1-Motion>", self.on_tree_drag)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_drop)
        self.tree.bind("<Double-Button-1>", self.on_tree_double_click)

        # 操作ボタン
        btn_frame = CTkFrame(left_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        CTkButton(btn_frame, text="➕ リング追加", 
                 command=self.add_new_ring, fg_color="#2d5f2d", font=self.get_font()).pack(fill="x", pady=2)
        CTkButton(btn_frame, text="➕ サブメニュー追加", 
                 command=self.add_submenu, fg_color="#2d5f2d", font=self.get_font()).pack(fill="x", pady=2)
        CTkButton(btn_frame, text="➕ アイテム追加", 
                 command=self.add_new_item, fg_color="#1f538d", font=self.get_font()).pack(fill="x", pady=2)
        CTkButton(btn_frame, text="✏️ 選択項目を編集", 
                 command=self.edit_selected_ring_or_menu, fg_color="#5d4a2d", font=self.get_font()).pack(fill="x", pady=2)
        CTkButton(btn_frame, text="🗑️ 選択項目を削除", 
                 command=self.delete_selected, fg_color="#7d2d2d", font=self.get_font()).pack(fill="x", pady=2)
        
        undo_redo_frame = CTkFrame(left_frame)
        undo_redo_frame.pack(fill="x", padx=10, pady=5)
        CTkButton(undo_redo_frame, text="↩️ 戻す", command=self.undo, width=150, font=self.get_font()).pack(side="left", padx=5, expand=True)
        CTkButton(undo_redo_frame, text="↪️ やり直し", command=self.redo, width=150, font=self.get_font()).pack(side="left", padx=5, expand=True)

        # 中央：プレビュー
        preview_frame = CTkFrame(main_container)
        preview_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        preview_header = CTkFrame(preview_frame)
        preview_header.pack(fill="x", pady=5)
        
        CTkLabel(preview_header, text="🔍 プレビュー", font=self.get_font(16, "bold")).pack(side="left", padx=10)
        
        # ズームコントロール
        zoom_frame = CTkFrame(preview_header)
        zoom_frame.pack(side="right", padx=10)
        CTkLabel(zoom_frame, text="ズーム:", font=self.get_font()).pack(side="left", padx=5)
        self.zoom_slider = CTkSlider(zoom_frame, from_=0.5, to=2.0, 
                                     command=self.on_zoom_change, width=150)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(side="left", padx=5)
        self.zoom_label = CTkLabel(zoom_frame, text="100%", width=50, font=self.get_font())
        self.zoom_label.pack(side="left")
        
        # プレビューキャンバス
        canvas_container = CTkFrame(preview_frame)
        canvas_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.preview_canvas = Canvas(canvas_container, bg="#1a1a1a", 
                                     highlightthickness=0)
        self.preview_canvas.pack(fill="both", expand=True)
        self.preview_canvas.bind("<Configure>", lambda e: self.draw_preview())
        self.preview_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.preview_canvas.bind("<Button-1>", self.on_preview_click)
        self.preview_canvas.bind("<Motion>", self.on_preview_hover)
        self.preview_canvas.bind("<Leave>", lambda e: self.on_hover_leave())

        # ショートカットキー
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())
        self.bind("<Control-S>", lambda e: self.save_config(backup=True))
        self.bind("<Control-s>", lambda e: self.save_config(backup=True))

        # 右側：編集エリア
        right_frame = CTkFrame(main_container, width=450)
        right_frame.pack(side="right", fill="y", padx=5)

        edit_header = CTkFrame(right_frame, fg_color="transparent")
        edit_header.pack(fill="x", pady=10)
        CTkLabel(edit_header, text="✏️ アイテム編集", font=self.get_font(16, "bold")).pack(side="left", padx=10)
        self.live_label = CTkLabel(edit_header, text="● Live Sync", font=self.get_font(10), text_color="#50fa7b")
        self.live_label.pack(side="right", padx=20)

        # スクロール可能なフレーム
        edit_scroll = CTkFrame(right_frame)
        edit_scroll.pack(fill="both", expand=True, padx=10)

        # 画像選択
        img_frame = CTkFrame(edit_scroll)
        img_frame.pack(fill="x", pady=10)
        CTkLabel(img_frame, text="🖼️ アイコン:", font=self.get_font(12, "bold")).pack(anchor="w", padx=10)
        
        img_select_frame = CTkFrame(img_frame)
        img_select_frame.pack(fill="x", padx=10, pady=5)
        
        self.image_preview = CTkLabel(img_select_frame, text="画像なし", 
                                      width=100, height=100, 
                                      fg_color="#2b2b2b", corner_radius=8, font=self.get_font())
        self.image_preview.pack(side="left", padx=10)
        
        img_btn_frame = CTkFrame(img_select_frame)
        img_btn_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        self.image_combo = CTkComboBox(img_btn_frame, values=["（なし）"], 
                                       command=self.on_image_select, font=self.get_font(), dropdown_font=self.get_font())
        self.image_combo.pack(fill="x", pady=2)
        self.image_combo.bind("<MouseWheel>", self.on_image_combo_scroll)
        
        img_manage_btns = CTkFrame(img_btn_frame)
        img_manage_btns.pack(fill="x", pady=2)
        
        CTkButton(img_manage_btns, text="📁 追加", width=80,
                 command=self.add_image_file, font=self.get_font()).pack(side="left", padx=2, expand=True, fill="x")
        CTkButton(img_manage_btns, text="📷 取り込み", width=80, 
                 command=self.start_screen_capture, font=self.get_font()).pack(side="left", padx=2, expand=True, fill="x")
        CTkButton(img_manage_btns, text="⚙️ 管理", width=80, 
                 command=self.show_image_manager, font=self.get_font()).pack(side="left", padx=2, expand=True, fill="x")

        # テキスト入力
        text_frame = CTkFrame(edit_scroll)
        text_frame.pack(fill="x", pady=10)
        CTkLabel(text_frame, text="📝 表示テキスト:", font=self.get_font(12, "bold")).pack(anchor="w", padx=10)
        self.text_entry = CTkEntry(text_frame, placeholder_text="アイテムの表示名", font=self.get_font())
        self.text_entry.pack(fill="x", padx=10, pady=5)

        # サブメニュー設定セクション (新設)
        self.submenu_section = CTkFrame(edit_scroll)
        self.submenu_section.pack(fill="x", pady=10)
        CTkLabel(self.submenu_section, text="📂 サブメニュー設定:", font=self.get_font(12, "bold")).pack(anchor="w", padx=10)
        
        submenu_sel_frame = CTkFrame(self.submenu_section)
        submenu_sel_frame.pack(fill="x", padx=10, pady=5)
        
        self.submenu_combo = CTkComboBox(submenu_sel_frame, values=["（なし）"], 
                                         command=self.on_submenu_combo_select, font=self.get_font(), dropdown_font=self.get_font())
        self.submenu_combo.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        CTkButton(submenu_sel_frame, text="➕", width=30, 
                 command=self.add_submenu, font=self.get_font()).pack(side="left")

        # クリック動作
        click_frame = CTkFrame(edit_scroll)
        click_frame.pack(fill="x", pady=10)
        
        click_label_frame = CTkFrame(click_frame, fg_color="transparent")
        click_label_frame.pack(fill="x", padx=10)
        CTkLabel(click_label_frame, text="🖱️ クリック動作 (AHKコード):", font=self.get_font(12, "bold")).pack(side="left")
        CTkButton(click_label_frame, text="❓", width=25, height=25, 
                 fg_color="#444444", hover_color="#666666",
                 command=self.show_ahk_help, font=self.get_font()).pack(side="right", pady=2)
        
        self.click_text = CTkTextbox(click_frame, height=120, font=self.get_font())
        self.click_text.pack(fill="x", padx=10, pady=5)
        
        # よく使う動作のボタン
        click_btn_frame = CTkFrame(click_frame)
        click_btn_frame.pack(fill="x", padx=10, pady=2)
        CTkButton(click_btn_frame, text="🌐 URL", width=70,
                 command=lambda: self.insert_template('Run("https://example.com")'), font=self.get_font()).pack(side="left", padx=2)
        CTkButton(click_btn_frame, text="📁 アプリ", width=70,
                 command=lambda: self.insert_template('Run("C:\\\\Program Files\\\\app.exe")'), font=self.get_font()).pack(side="left", padx=2)
        CTkButton(click_btn_frame, text="⌨️ キー", width=70,
                 command=lambda: self.insert_template('Send("^c")'), font=self.get_font()).pack(side="left", padx=2)
        CTkButton(click_btn_frame, text="📂 サブメニュー", width=90,
                 command=lambda: self.safe_call(self.insert_submenu_call), font=self.get_font()).pack(side="left", padx=2)
        
        # よく使う動作の追加行
        click_btn_frame2 = CTkFrame(click_frame)
        click_btn_frame2.pack(fill="x", padx=10, pady=2)
        CTkButton(click_btn_frame2, text="📄 ファイル", width=70,
                 command=self.browse_file_for_click, font=self.get_font()).pack(side="left", padx=2)
        CTkButton(click_btn_frame2, text="📁 フォルダ", width=70,
                 command=self.browse_folder_for_click, font=self.get_font()).pack(side="left", padx=2)

        CTkButton(click_btn_frame2, text="🔧 カスタム", width=70,
                 command=self.show_template_library, font=self.get_font()).pack(side="left", padx=2)
        CTkButton(click_btn_frame2, text="★ お気に入り", width=70, fg_color="#d4af37", text_color="black",
                 command=self.show_favorites_dialog, font=self.get_font()).pack(side="left", padx=2)

        # ツールチップ
        tooltip_frame = CTkFrame(edit_scroll)
        tooltip_frame.pack(fill="x", pady=10)
        CTkLabel(tooltip_frame, text="💬 ツールチップ:", font=self.get_font(12, "bold")).pack(anchor="w", padx=10)
        self.tooltip_entry = CTkEntry(tooltip_frame, placeholder_text="マウスオーバー時の説明", font=self.get_font())
        self.tooltip_entry.pack(fill="x", padx=10, pady=5)
        
        # リアルタイム更新のバインド
        self.text_entry.bind("<KeyRelease>", lambda e: self.apply_item(silent=True))
        self.tooltip_entry.bind("<KeyRelease>", lambda e: self.apply_item(silent=True))
        self.click_text.bind("<KeyRelease>", self.on_click_text_key)

        # 編集ボタン
        btn_frame2 = CTkFrame(edit_scroll)
        btn_frame2.pack(fill="x", pady=20, padx=10)
        
        CTkButton(btn_frame2, text="✅ 適用", command=self.apply_item, 
                 fg_color="#2d5f2d", height=40, font=self.get_font()).pack(fill="x", pady=2)
        CTkButton(btn_frame2, text="🗑️ 削除", command=self.delete_item, 
                 fg_color="#7d2d2d", height=40, font=self.get_font()).pack(fill="x", pady=2)
        
        move_frame = CTkFrame(btn_frame2)
        move_frame.pack(fill="x", pady=5)
        CTkButton(move_frame, text="⬆️", command=self.move_up, width=40, font=self.get_font()).pack(side="left", padx=2)
        CTkButton(move_frame, text="⬇️", command=self.move_down, width=40, font=self.get_font()).pack(side="left", padx=2)
        CTkButton(move_frame, text="★", width=30, fg_color="#d4af37", text_color="black", command=self.add_to_favorites, font=self.get_font()).pack(side="left", padx=2)
        CTkButton(move_frame, text="📋 コピー", command=self.copy_item, font=self.get_font()).pack(side="left", expand=True, fill="x", padx=2)
        CTkButton(move_frame, text="📥 貼り付け", command=self.paste_item, font=self.get_font()).pack(side="left", expand=True, fill="x", padx=2)

        # 下部ボタン
        bottom_frame = CTkFrame(self)
        bottom_frame.pack(side="bottom", fill="x", pady=10, padx=10)
        
        self.standalone_check = CTkCheckBox(bottom_frame, text="📦 単体パッケージとして出力 (Libフォルダと画像を含める)", font=self.get_font())
        self.standalone_check.pack(side="top", pady=5)
        
        CTkButton(bottom_frame, text="💾 保存＆AHKコード生成", 
                 command=self.generate_ahk, fg_color="#1f538d", 
                 height=50, font=self.get_font(14, "bold")).pack(side="left", expand=True, fill="x", padx=5)

    def refresh_submenu_combo(self):
        """サブメニューリストを更新"""
        submenus = ["（なし）"] + sorted(list(self.config.get("submenus", {}).keys()))
        self.submenu_combo.configure(values=submenus)

    def update_click_ui_state(self, sub_choice):
        """サブメニュー選択状態に基づいてクリックテキストのUIを更新"""
        self.click_text.configure(state="normal") # 一旦編集可能にして書き換え
        self.click_text.delete("1.0", "end")
        
        if sub_choice and sub_choice != "（なし）":
            self.click_text.insert("1.0", f'radifyMenu.ShowSubmenu("{sub_choice}")')
            self.click_text.configure(state="disabled", fg_color="#333333")
        else:
            # 既存のクリックコードを表示
            self.click_text.insert("1.0", self.current_item.get("click", ""))
            self.click_text.configure(state="normal", fg_color="#1d1d1d")

    def clear_edit_fields(self):
        """編集フィールドをクリア"""
        self.text_entry.delete(0, "end")
        self.click_text.delete("0.0", "end")
        self.tooltip_entry.delete(0, "end")
        self.image_combo.set("（なし）")
        self.on_image_select("（なし）")

    def setup_syntax_highlighting(self):
        """シンタックスハイライトの設定"""
        self.click_text.tag_config("keyword", foreground="#ff79c6") # ピンク
        self.click_text.tag_config("function", foreground="#50fa7b") # 緑
        self.click_text.tag_config("string", foreground="#f1fa8c") # 黄色
        self.click_text.tag_config("comment", foreground="#6272a4") # 青味のある灰色
        self.click_text.tag_config("parameter", foreground="#ffb86c") # オレンジ

    def on_click_text_key(self, event):
        """キー入力時にハイライトと適用を行う"""
        self.apply_syntax_highlighting()
        self.apply_item(silent=True)

    def apply_syntax_highlighting(self):
        """簡易シンタックスハイライトの実行"""
        if self.submenu_combo.get() != "（なし）":
            return # サブメニュー時はスキップ
            
        content = self.click_text.get("1.0", "end")
        self.click_text.tag_remove("keyword", "1.0", "end")
        self.click_text.tag_remove("function", "1.0", "end")
        self.click_text.tag_remove("string", "1.0", "end")
        self.click_text.tag_remove("comment", "1.0", "end")
        
        # コメント
        for match in re.finditer(r';.*', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.click_text.tag_add("comment", start, end)
            
        # 文字列
        for match in re.finditer(r'"[^"]*"', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.click_text.tag_add("string", start, end)
            
        # キーワード
        keywords = ["if", "else", "return", "global", "local", "static", "for", "while", "loop"]
        for kw in keywords:
            for match in re.finditer(rf'\\b{kw}\\b', content):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.click_text.tag_add("keyword", start, end)
                
        # 関数 (単純なパターン)
        for match in re.finditer(r'\\b[A-Za-z0-9_]+(?=\()', content):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            self.click_text.tag_add("function", start, end)
