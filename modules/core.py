import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import simpledialog
from customtkinter import CTk, set_appearance_mode, set_default_color_theme
import os

from .ui_setup import UISetupMixin
from .preview import PreviewMixin
from .file_io import FileIOMixin
from .actions import ActionsMixin
from .dialogs import DialogsMixin
from .images import ImageMixin

class RadifyMenuEditor(CTk, UISetupMixin, PreviewMixin, FileIOMixin, ActionsMixin, DialogsMixin, ImageMixin):
    def __init__(self):
        super().__init__()

        # 設定
        self.title("Radify Menu Editor (Modular Version)")
        self.geometry("1400x900")
        
        # テーマ設定
        set_appearance_mode("Dark")
        set_default_color_theme("blue")
        
        self.config_file = "menu_config.json"
        self.backup_dir = "backups"
        self.templates_file = "templates.json"
        
        # 設定読み込み
        self.config = self.load_config()
        self.templates_data = self.load_templates()
        
        # フォント設定（キャッシュ）
        self.gui_font_family = self.config["menu_options"].get("gui_font_family", "")
        self.gui_font_size = self.config["menu_options"].get("gui_font_size", 12)
        
        set_appearance_mode(self.config["menu_options"].get("appearance_mode", "Dark"))
        
        # 変数初期化
        self.image_dir = self.config.get("image_dir", "images")
        self.current_menu = "main" # "main" or submenu_name
        self.current_ring = None
        self.current_item = None
        self.current_parent = None # リストへの参照
        self.preview_scale = 1.0
        self.preview_click_areas = []
        self.drag_data = {"item": None, "index": None}
        self.clipboard = None
        self.history = []
        self.history_index = -1
        self.template_window = None
        self.search_debounce_timer = None
        self.image_cache = {}
        self.hovered_item = None
        self.preview_update_pending = False
        self.is_loading = False

        # 画像ディレクトリ確保
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)

        # UI構築
        self.build_ui()
        
        # 初期描画
        self.refresh_tree()
        self.refresh_image_list()
        self.draw_preview()
        
        # バインディング
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 依存関係チェック
        self.check_dependencies()
        
        # テンプレートウィンドウのプリロード
        self.after(2000, self._preload_template_window)
        
        # 自動保存開始
        self.setup_autosave()

    def create_new_project(self):
        """既存プロジェクトを破棄して新規作成"""
        if not messagebox.askyesno("確認", "現在の設定を破棄して新規作成しますか？\\n(現在のファイルはバックアップされます)"):
            return
        
        name = simpledialog.askstring("新規プロジェクト", "メインメニューの変数名（AHK用）を入力してください", initialvalue="myMainMenu")
        if not name: return
        name = self.sanitize_var_name(name)
        
        self.push_history()
        self.create_backup()
        
        self.config = {
            "image_dir": "images",
            "main_menu": [{"ring": 1, "items": []}],
            "submenus": {},
            "menu_options": {
                "skin": "Default",
                "EnableGlow": True,
                "itemSize": 60,
                "ringSpacing": 80,
                "menu_name": name,
                "gui_font_family": "",
                "gui_font_size": 12
            },
            "favorites": []
        }
        
        self.save_config(backup=False)
        self.refresh_all()
        messagebox.showinfo("完了", f"新規プロジェクト '{name}' を作成しました")

    def refresh_all(self):
        """UI全体を更新"""
        self.is_loading = True
        try:
            self.refresh_tree()
            self.refresh_image_list()
            self.clear_edit_fields()
            self.draw_preview()
            self.refresh_submenu_combo()
            
            # フォント設定の更新反映
            self.gui_font_family = self.config["menu_options"].get("gui_font_family", "")
            self.gui_font_size = self.config["menu_options"].get("gui_font_size", 12)
            
            # スキン設定の反映
            set_appearance_mode(self.config["menu_options"].get("appearance_mode", "Dark"))
            
        finally:
            self.is_loading = False

    def check_dependencies(self):
        """必要なファイルが存在するか確認"""
        missing = []
        if not os.path.exists("Lib/Gdip_All.ahk"): missing.append("Lib/Gdip_All.ahk")
        if not os.path.exists("Radify.ahk"): missing.append("Radify.ahk")
        
        if missing:
            msg = "以下の必須ファイルが見つかりません。\\nAHKスクリプトの実行に支障が出る可能性があります。\\n\\n" + "\\n".join(missing)
            messagebox.showwarning("依存関係の警告", msg)

    def on_closing(self):
        """終了時の処理"""
        if messagebox.askokcancel("終了", "アプリケーションを終了しますか？"):
            self.save_config(backup=False)
            self.quit()

    def safe_call(self, func, *args, **kwargs):
        """エラーハンドリング付きの関数呼び出し"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            messagebox.showerror("エラー", f"処理中にエラーが発生しました:\\n{e}")
