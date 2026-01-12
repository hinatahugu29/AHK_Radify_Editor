import os
import json
import shutil
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import filedialog
from customtkinter import CTk, CTkLabel, CTkCheckBox, CTkButton

class FileIOMixin:
    def load_config(self):
        """設定ファイルを読み込む"""
        if not os.path.exists(self.config_file):
            if messagebox.askyesno("確認", "menu_config.jsonが見つかりません。新規作成しますか？"):
                default = {
                    "image_dir": "images",
                    "main_menu": [{"ring": 1, "items": []}],
                    "submenus": {},
                    "favorites": [], # お気に入り（新設）
                    "menu_options": {
                        "skin": "Default",
                        "EnableGlow": True,
                        "itemSize": 60,
                        "ringSpacing": 80,
                        "gui_font_family": "",
                        "gui_font_size": 12
                    }
                }
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(default, f, ensure_ascii=False, indent=4)
                return default
            else:
                exit()
        
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                # 既存の設定ファイルにfavoritesがない場合の対策
                if "favorites" not in config:
                    config["favorites"] = []
                return config
        except json.JSONDecodeError as e:
            messagebox.showerror("エラー", f"設定ファイルの読み込みに失敗しました:\\n{e}")
            exit()

    def load_templates(self):
        """テンプレートファイルを読み込む"""
        default_templates = [
            ("🚀 アプリ起動/切替 (基本)", 'LaunchOrActivate("ウィンドウタイトル", "C:\\\\Path\\\\To\\\\App.exe")'),
            ("🌐 Google検索", 'Run("https://www.google.com/search?q=検索ワード")'),
            ("💾 保存 (Ctrl+S)", 'Send("^s")'),
        ]
        
        if not os.path.exists(self.templates_file):
            return default_templates
        
        try:
            with open(self.templates_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # JSONは [{"name": "...", "code": "..."}] 形式を想定
                # タプルのリストに変換 [(name, code)]
                return [(item["name"], item["code"]) for item in data]
        except Exception as e:
            print(f"テンプレート読み込みエラー: {e}")
            return default_templates

    def save_config(self, backup=True):
        """設定を保存（バックアップオプション付き）"""
        if backup:
            self.create_backup()
        
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("エラー", f"設定の保存に失敗しました:\\n{e}")

    def create_backup(self):
        """設定ファイルのバックアップを作成"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.backup_dir, f"menu_config_{timestamp}.json")
        
        try:
            shutil.copy2(self.config_file, backup_path)
            # 古いバックアップを削除（最新10個を保持）
            backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("menu_config_")])
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    os.remove(os.path.join(self.backup_dir, old_backup))
        except Exception as e:
            print(f"バックアップ作成エラー: {e}")

    def restore_backup(self):
        """バックアップから復元"""
        if not os.path.exists(self.backup_dir):
            messagebox.showinfo("情報", "バックアップファイルが見つかりません")
            return
        
        backups = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("menu_config_")])
        if not backups:
            messagebox.showinfo("情報", "バックアップファイルが見つかりません")
            return
        
        # 最新のバックアップを表示
        backup_path = filedialog.askopenfilename(
            initialdir=self.backup_dir,
            title="復元するバックアップを選択",
            filetypes=[("JSON files", "*.json")]
        )
        
        if backup_path:
            try:
                shutil.copy2(backup_path, self.config_file)
                self.config = self.load_config()
                self.refresh_tree()
                self.refresh_image_list()
                messagebox.showinfo("完了", "バックアップから復元しました")
            except Exception as e:
                messagebox.showerror("エラー", f"復元に失敗しました:\\n{e}")

    def export_config(self):
        """設定をエクスポート"""
        export_path = filedialog.asksaveasfilename(
            title="設定をエクスポート",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"radify_menu_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        if export_path:
            try:
                # 設定と画像をまとめてエクスポートするか確認
                export_options = CTk()
                export_options.title("エクスポート設定")
                export_options.geometry("400x250")
                
                CTkLabel(export_options, text="📤 エクスポートオプション", font=self.get_font(14, "bold")).pack(pady=15)
                
                check_images = CTkCheckBox(export_options, text="画像フォルダを含める", font=self.get_font())
                check_images.select()
                check_images.pack(pady=5)
                
                check_libs = CTkCheckBox(export_options, text="Radifyライブラリを含める (Lib/*.ahk)", font=self.get_font())
                check_libs.select()
                check_libs.pack(pady=5)
                
                def do_export():
                    incl_img = check_images.get()
                    incl_lib = check_libs.get()
                    export_options.destroy()
                    
                    # 実際の処理
                    shutil.copy2(self.config_file, export_path)
                    export_dir = os.path.dirname(export_path)
                    
                    if incl_img and os.path.exists(self.image_dir):
                        export_image_dir = os.path.join(export_dir, "images")
                        if os.path.exists(export_image_dir): shutil.rmtree(export_image_dir)
                        shutil.copytree(self.image_dir, export_image_dir)
                    
                    if incl_lib:
                        # 自身のディレクトリからLibを探す
                        # Note: This relies on __file__ of main execution context or we assume CWD
                        # For modular approach, we must be careful. Assuming running from root.
                        lib_src = os.path.join(os.getcwd(), "Lib") 
                        # In the original code it used os.path.dirname(os.path.abspath(__file__))
                        # Here self is the instance. We assume CWD is correct or we use config paths.
                        
                        if not os.path.exists(lib_src):
                            # Try one level up if inside module folder? 
                            # But app runs from root.
                            pass
                            
                        if os.path.exists(lib_src):
                            lib_dest = os.path.join(export_dir, "Lib")
                            if os.path.exists(lib_dest): shutil.rmtree(lib_dest)
                            shutil.copytree(lib_src, lib_dest)

                    messagebox.showinfo("完了", "エクスポートが完了しました")

                CTkButton(export_options, text="実行", command=do_export, font=self.get_font()).pack(pady=20)
                export_options.mainloop()
                
            except Exception as e:
                messagebox.showerror("エラー", f"エクスポートに失敗しました:\\n{e}")

    def import_config(self):
        """設定をインポート"""
        import_path = filedialog.askopenfilename(
            title="設定をインポート",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if import_path:
            if messagebox.askyesno("確認", 
                "現在の設定を上書きしますか？\\n" +
                "（自動的にバックアップを作成します）"):
                try:
                    # 現在の設定をバックアップ
                    self.create_backup()
                    
                    # 新しい設定を読み込み
                    with open(import_path, "r", encoding="utf-8") as f:
                        imported_config = json.load(f)
                    
                    # 設定を適用
                    self.push_history()
                    self.config = imported_config
                    self.save_config(backup=False)
                    
                    # 画像フォルダもインポートするか確認
                    import_dir = os.path.dirname(import_path)
                    import_image_dir = os.path.join(import_dir, "images")
                    
                    if os.path.exists(import_image_dir):
                        if messagebox.askyesno("確認", "画像フォルダも見つかりました。インポートしますか？"):
                            if os.path.exists(self.image_dir):
                                shutil.rmtree(self.image_dir)
                            shutil.copytree(import_image_dir, self.image_dir)
                    
                    # UIを更新
                    self.refresh_all()
                    messagebox.showinfo("完了", "設定をインポートしました！")
                    
                except json.JSONDecodeError:
                    messagebox.showerror("エラー", "無効なJSONファイルです")
                except Exception as e:
                    messagebox.showerror("エラー", f"インポートに失敗しました:\\n{e}")

    def setup_autosave(self):
        """自動保存のスケジュール"""
        self.after(300000, self.autosave_loop) # 5分ごと

    def autosave_loop(self):
        """定期的なバックアップ保存"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup = os.path.join(self.backup_dir, f"autosave_{timestamp}.json")
            
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
                
            with open(temp_backup, "w", encoding="utf-8") as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
            
            # 5個以上あれば古いオートセーブを削除
            autosaves = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("autosave_")])
            if len(autosaves) > 5:
                for old in autosaves[:-5]:
                    os.remove(os.path.join(self.backup_dir, old))
            
            print(f"Autosaved: {temp_backup}")
        except Exception as e:
            print(f"Autosave error: {e}")
        
        self.after(300000, self.autosave_loop)

    def generate_ahk(self):
        """AHKコードを生成"""
        self.save_config(backup=False)
        
        # 保存先の選択
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ahk",
            filetypes=[("AutoHotkey Script", "*.ahk"), ("All Files", "*.*")],
            initialfile="generated_menu.ahk",
            title="AHKスクリプトを保存"
        )
        
        if not file_path:
            return

        # 内蔵コード生成機能を使用
        try:
            ahk_code = self.generate_ahk_code_internal()
            
            with open(file_path, "w", encoding="utf-8-sig") as f:
                f.write(ahk_code)
            
            messagebox.showinfo("完了", 
                f"AHKコード生成完了！\\n\\n" +
                f"{file_path} を確認してください\\n\\n" +
                f"({len(ahk_code)} 文字生成)")
            
            # ファイルを開くか確認
            if messagebox.askyesno("確認", "生成されたファイルを開きますか？"):
                os.startfile(file_path)
            
            # 単体パッケージ出力
            if self.standalone_check.get():
                self.export_standalone_resources(file_path)
                
        except Exception as e:
            messagebox.showerror("エラー", f"コード生成に失敗しました:\\n{e}")

    def export_standalone_resources(self, ahk_path):
        """単体パッケージ用のリソース出力"""
        try:
            dest_dir = os.path.dirname(ahk_path)
            
            # 画像フォルダ
            src_img = self.image_dir
            if os.path.exists(src_img):
                dest_img = os.path.join(dest_dir, "images")
                if not os.path.exists(dest_img):
                    os.makedirs(dest_img)
                for item in os.listdir(src_img):
                    s = os.path.join(src_img, item)
                    d = os.path.join(dest_img, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
            
            # Libフォルダ
            base_dir = os.getcwd() # Use CWD
            src_lib = os.path.join(base_dir, "Lib")
            
            if os.path.exists(src_lib):
                dest_lib = os.path.join(dest_dir, "Lib")
                if not os.path.exists(dest_lib):
                    shutil.copytree(src_lib, dest_lib)
                else:
                    for item in os.listdir(src_lib):
                        s = os.path.join(src_lib, item)
                        d = os.path.join(dest_lib, item)
                        if os.path.isfile(s):
                            shutil.copy2(s, d)
            
            # Radify.ahk
            src_radify = os.path.join(base_dir, "Radify.ahk")
            if os.path.exists(src_radify):
                shutil.copy2(src_radify, os.path.join(dest_dir, "Radify.ahk"))

            messagebox.showinfo("パッケージ出力", "関連ファイル（Lib, images, Radify.ahk）を\\n出力先にコピーしました。")
            
        except Exception as e:
            print(f"パッケージ出力エラー: {e}")
            messagebox.showwarning("警告", f"パッケージリソースのコピー中にエラーが発生しました:\\n{e}")
    
    def generate_ahk_code_internal(self):
        """内蔵AHKコード生成機能"""
        config = self.config
        
        # ヘッダー
        ahk_code = [
            "; ============================================",
            "; Radify Menu - Auto Generated",
            f"; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "; ============================================",
            "",
            "#Requires AutoHotkey v2.0",
            "#SingleInstance Force",
            "",
            "; ライブラリの読み込み",
            '#Include ".\\Lib\\Gdip_All.ahk"',
            '#Include "Radify.ahk"',
            "",
            "; GDI+の初期化",
            "if !(pToken := Gdip_Startup()) {",
            '    MsgBox("GDI+起動失敗。AHK v2とGDI+ライブラリを確認してください。",, "Icon!")',
            "    ExitApp",
            "}",
            "OnExit(*) => (Radify.DisposeResources(), Gdip_Shutdown(pToken))",
            "",
            "; メニュー構造を格納するオブジェクト",
            "global RadifyMenus := {}",
            "",
            "; グローバル変数",
            f'Radify.SetImageDir(A_ScriptDir . "\\\\{config.get("image_dir", "images")}")',
            f'global ItemSize := {config["menu_options"].get("itemSize", 60)}',
            f'global EnableGlow := {str(config["menu_options"].get("EnableGlow", True)).lower()}',
            f'global Skin := "{config["menu_options"].get("skin", "Default")}"',
            f'global MenuName := "{config["menu_options"].get("menu_name", "MainMenu")}"',
            "",
            "; === 汎用関数：ウィンドウ存在チェック＆起動/アクティブ化 ===",
            "LaunchOrActivate(title, exePath := \"\", options := \"\") {",
            "    SetTitleMatchMode(2)",
            "    if WinExist(title) {",
            "        WinActivate(title)",
            "        return true",
            "    } else if (exePath != \"\") {",
            "        Run(exePath, , options)",
            "        return true",
            "    } else {",
            "        return false",
            "    }",
            "}",
            "",
        ]
        
        # サブメニュー定義
        if config["submenus"]:
            ahk_code.append("; ============================================")
            ahk_code.append("; サブメニュー定義")
            ahk_code.append("; ============================================")
            ahk_code.append("")
            
            for submenu_name in config["submenus"].keys():
                var_name = self.sanitize_var_name(submenu_name)
                ahk_code.append(f'RadifyMenus.{var_name} := []')
            ahk_code.append("")

            for submenu_name, rings in config["submenus"].items():
                ahk_code.append(f'; サブメニュー定義: {submenu_name}')
                var_name = self.sanitize_var_name(submenu_name)
                submenu_literal = self.format_rings_literal(rings, indent_level=0)
                ahk_code.append(f'RadifyMenus.{var_name} := {submenu_literal}')
                ahk_code.append("")
        
        ahk_code.append("; ============================================")
        ahk_code.append("; メインメニュー作成")
        ahk_code.append("; ============================================")
        ahk_code.append("")
        
        main_menu_literal = self.format_rings_literal(config["main_menu"], indent_level=1)
        
        ahk_code.append(f'Radify.CreateMenu(MenuName, {main_menu_literal}, {{')
        ahk_code.append(f'    itemSize: ItemSize,')
        ahk_code.append(f'    enableGlow: EnableGlow,')
        ahk_code.append(f'    skin: Skin')
        ahk_code.append('})')
        ahk_code.append("")
        ahk_code.append("")
        
        t_type = config["menu_options"].get("trigger_type", "r_drag")
        t_key = config["menu_options"].get("trigger_key", "RButton")
        
        ahk_code.append("; ============================================")
        ahk_code.append(f"; 起動設定 (タイプ: {t_type}, キー: {t_key})")
        ahk_code.append("; ============================================")
        ahk_code.append("")
        
        if t_type == "r_drag":
            ahk_code.append(f"{t_key}::")
            ahk_code.append("{")
            ahk_code.append("    dist := 0")
            ahk_code.append("    MouseGetPos(&startX, &startY)")
            ahk_code.append(f"    while GetKeyState(\"{t_key}\", \"P\") {{")
            ahk_code.append("        MouseGetPos(&currentX, &currentY)")
            ahk_code.append("        dist := Sqrt((currentX - startX)**2 + (currentY - startY)**2)")
            ahk_code.append("        if (dist > 30) {")
            ahk_code.append(f'            Radify.Show(MenuName, true)')
            ahk_code.append("            return")
            ahk_code.append("        }")
            ahk_code.append("        Sleep(10)")
            ahk_code.append("    }")
            
            if t_key in ["RButton", "LButton", "MButton", "XButton1", "XButton2"]:
                btn_name = t_key.replace("Button", "")
                if btn_name == "R": btn_name = "Right"
                if btn_name == "L": btn_name = "Left"
                ahk_code.append(f"    Click(\"{btn_name} Down\")")
                ahk_code.append("    Sleep(1)")
                ahk_code.append(f"    Click(\"{btn_name} Up\")")
            else:
                ahk_code.append(f"    Send(\"{{{t_key}}}\")")
            ahk_code.append("}")

        elif t_type == "hold":
            ahk_code.append(f"{t_key}::")
            ahk_code.append("{")
            ahk_code.append(f"    if KeyWait(\"{t_key}\", \"T0.3\") {{")
            if t_key in ["RButton", "LButton", "MButton", "XButton1", "XButton2"]:
                btn_name = t_key.replace("Button", "")
                if btn_name == "R": btn_name = "Right"
                if btn_name == "L": btn_name = "Left"
                ahk_code.append(f"        Click(\"{btn_name} Down\")")
                ahk_code.append("        Sleep(1)")
                ahk_code.append(f"        Click(\"{btn_name} Up\")")
            else:
                ahk_code.append(f"        Send(\"{{{t_key}}}\")")
            ahk_code.append("    } else {")
            ahk_code.append(f'        Radify.Show(MenuName, true)')
            ahk_code.append(f"        KeyWait(\"{t_key}\")")
            ahk_code.append("    }")
            ahk_code.append("}")
            
        elif t_type == "alt_r":
            ahk_code.append(f"!{t_key}::")
            ahk_code.append("{")
            ahk_code.append(f'    Radify.Show(MenuName, true)')
            ahk_code.append("}")
            
        elif t_type == "ctrl_r":
            ahk_code.append(f"^{t_key}::")
            ahk_code.append("{")
            ahk_code.append(f'    Radify.Show(MenuName, true)')
            ahk_code.append("}")
            
        else: # hotkey
            ahk_code.append(f"{t_key}::")
            ahk_code.append("{")
            ahk_code.append(f'    Radify.Show(MenuName, true)')
            ahk_code.append("}")
            
        ahk_code.append("")
        ahk_code.append(f'#HotIf WinExist(MenuName)')
        ahk_code.append(f'Esc::Radify.Close(MenuName)')
        ahk_code.append(f'#HotIf')
        ahk_code.append("")
        ahk_code.append("")
        
        return "\n".join(ahk_code)
    
    def format_rings_literal(self, rings, indent_level=0):
        """リング配列の文字列表現を生成"""
        base_indent = "    " * indent_level
        has_items = any(ring.get("items") for ring in rings)
        if not has_items:
            return f"{base_indent}[\n{base_indent}    []\n{base_indent}]"
            
        lines = []
        lines.append("[")
        
        for i, ring in enumerate(rings):
            ring_label = ring.get("ring", f"ring_{i+1}")
            items = ring.get("items", [])
            ring_indent = base_indent + "    "
            
            if not items:
                lines.append(f'{ring_indent}[]  ; {ring_label}（空）')
            else:
                lines.append(f'{ring_indent}[  ; {ring_label}')
                item_strs = []
                for item in items:
                    item_str = self.format_menu_item(item, indent_level + 2)
                    item_strs.append(f'{ring_indent}    {item_str}')
                lines.append(",\n".join(item_strs))
                lines.append(f'{ring_indent}]')
            
            if i < len(rings) - 1:
                lines[-1] += ","
                
        lines.append(f"{base_indent}]")
        return "\n".join(lines)

    def format_menu_item(self, item, indent_level=0):
        """メニューアイテムをAHK形式にフォーマット"""
        parts = []
        text = item.get("text", "").replace('"', '""')
        parts.append(f'text: "{text}"')
        
        if item.get("image"):
            img = item["image"].replace('"', '""')
            parts.append(f'image: "{img}"')
        
        if item.get("submenu"):
            submenu_name = item["submenu"]
            if submenu_name in self.config["submenus"]:
                rings = self.config["submenus"][submenu_name]
                submenu_literal = self.format_rings_literal(rings, indent_level + 1)
                parts.append(f'submenu: {submenu_literal}')
                if item.get("submenuOptions"):
                    options_str = self.format_submenu_options(item["submenuOptions"])
                    parts.append(f'submenuOptions: {options_str}')
            else:
                parts.append(f'submenu: [[], []] ; Warning: {submenu_name} not found')
        
        elif item.get("click"):
            click = item["click"].strip()
            if "A_ScriptDir \"" in click and "A_ScriptDir . \"" not in click:
                click = click.replace("A_ScriptDir \"", "A_ScriptDir . \"")
            
            built_in_commands = ["CloseMenu", "BackMenu", "NextRing", "PrevRing"]
            
            if click in built_in_commands:
                parts.append(f'click: "{click}"')
            elif "\\n" in click or "{" in click or "}" in click or ";" in click:
                body_indent = "    " * (indent_level + 1)
                brace_indent = "    " * indent_level
                click_lines = click.split("\\n")
                formatted_lines = []
                for line in click_lines:
                    stripped = line.strip()
                    if stripped:
                        formatted_lines.append(f"{body_indent}{stripped}")
                    else:
                        formatted_lines.append("")
                click_formatted = "\n".join(formatted_lines)
                parts.append(f'click: (*) => {{\n{click_formatted}\n{brace_indent}}}')
            else:
                if not click.startswith("(*) =>") and not click.startswith('"'):
                    parts.append(f'click: (*) => {click}')
                else:
                    parts.append(f'click: {click}')
        
        if item.get("tooltip"):
            tooltip = item["tooltip"].replace('"', '""')
            parts.append(f'tooltip: "{tooltip}"')
        
        return "{" + ", ".join(parts) + "}"
    
    def format_submenu_options(self, options):
        """サブメニューオプションをフォーマット"""
        opts = []
        for key, value in options.items():
            if isinstance(value, bool):
                opts.append(f'{key}: {str(value).lower()}')
            elif isinstance(value, (int, float)):
                opts.append(f'{key}: {value}')
            else:
                opts.append(f'{key}: "{value}"')
        return "{" + ", ".join(opts) + "}"
    
    def sanitize_var_name(self, name):
        """変数名として使える形式に変換"""
        sanitized = name.replace(" ", "_").replace("-", "_")
        sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")
        if sanitized and sanitized[0].isdigit():
            sanitized = "m" + sanitized
        return sanitized if sanitized else "menu"
