# 技術仕様

このページでは、Radify Menu Editorの技術的な仕様と実装の詳細を説明します。

## システム要件

### 最小要件

- **OS**: Windows 10 (64-bit)
- **Python**: 3.8以上
- **RAM**: 2GB以上
- **ディスク空き容量**: 100MB以上（設定ファイルと画像を除く）

### 推奨要件

- **OS**: Windows 11 (64-bit)
- **Python**: 3.10以上
- **RAM**: 4GB以上
- **ディスク空き容量**: 500MB以上

## 技術スタック

### フロントエンド（GUI）

- **CustomTkinter 5.2.0以上**: モダンなUI要素
- **Tkinter**: 標準GUIライブラリ（Python標準ライブラリ）

### 画像処理

- **Pillow (PIL) 10.0.0以上**: 画像の読み込み、リサイズ、変換

### データフォーマット

- **JSON**: 設定ファイルとテンプレートの保存形式

### 出力ターゲット

- **AutoHotkey v2**: 生成されるスクリプトの実行環境

## アーキテクチャ

### デザインパターン

#### Mixin パターン

メインクラス `RadifyMenuEditor` は複数のMixinクラスを継承:

```python
class RadifyMenuEditor(
    CTk,           # CustomTkinter基底クラス
    UISetupMixin,  # UI構築
    PreviewMixin,  # プレビュー描画
    FileIOMixin,   # ファイルI/O
    ActionsMixin,  # ユーザーアクション
    DialogsMixin,  # ダイアログ管理
    ImageMixin     # 画像処理
):
    pass
```

**利点**:
- モジュール性が高い
- 各機能を独立してテスト・修正可能
- コードの可読性向上

#### MVC パターン（部分的）

- **Model**: `menu_config.json`（データ）
- **View**: UIコンポーネント（Tkinter/CustomTkinter）
- **Controller**: ActionsMixin等のユーザーアクション処理

## データ構造

### 設定ファイル (menu_config.json)

```json
{
  "image_dir": String,      // 画像ディレクトリパス
  "main_menu": Array,       // メインメニュー構造
  "submenus": Object,       // サブメニュー定義
  "menu_options": Object,   // メニューオプション
  "favorites": Array        // お気に入りアイテム
}
```

### リング構造

```typescript
interface Ring {
  ring: number;           // リング番号（1から開始）
  items: MenuItem[];      // アイテムの配列
}
```

### メニューアイテム

```typescript
interface MenuItem {
  label: string;          // 表示ラベル
  icon?: string;          // アイコンパス（オプション）
  action?: string;        // AHKコード（オプション）
  submenu?: string;       // サブメニュー名（オプション）
}
```

## プレビュー描画アルゴリズム

### 円形配置の計算

アイテムの配置位置は以下の式で計算:

```python
# 極座標から直交座標への変換
angle = (index / total_items) * 2 * π + offset
x = center_x + radius * cos(angle)
y = center_y + radius * sin(angle)
```

### 複数リングの配置

```python
for ring_num, ring_data in enumerate(rings, start=1):
    radius = base_radius + (ring_num - 1) * ring_spacing
    # 各アイテムを配置
```

## ファイルI/O

### 読み込みフロー

```
load_config()
  → ファイル存在確認
  → JSON読み込み
  → バリデーション
  → Pythonオブジェクトに変換
  → メモリに格納
```

### 保存フロー

```
save_config()
  → データ検証
  → JSON文字列に変換
  → バックアップ作成（オプション）
  → ファイル書き込み
```

### バックアップ戦略

- **自動保存**: 5分ごと（設定可能）
- **バックアップフォルダ**: `backups/`
- **ファイル名形式**: `autosave_YYYYMMDD_HHMMSS.json`
- **保持期間**: 最新10ファイル

## AHKスクリプト生成

### コード生成フロー

```
export_ahk_script()
  → テンプレート読み込み
  → メニュー構造をAHKコードに変換
  → 依存ライブラリを識別
  → 出力フォルダ作成
  → スクリプトファイル書き込み
  → ライブラリファイルコピー
  → 画像リソースコピー
```

### 生成されるコードの構造

```ahk
#Requires AutoHotkey v2.0

; ライブラリのインクルード
#Include Radify.ahk

; メニューオブジェクトの作成
myMenu := RadifyMenu()

; メニュー構造の定義
myMenu.rings := [
    {
        ring: 1,
        items: [
            {label: "Item1", icon: "images/icon1.png", action: (*) => Run("app.exe")}
        ]
    }
]

; ホットキーの設定
^Space::myMenu.Show()
```

## パフォーマンス最適化

### 画像キャッシュ

ロード済みの画像をメモリにキャッシュ:

```python
self.image_cache = {}

def load_image(self, path):
    if path in self.image_cache:
        return self.image_cache[path]
    
    image = Image.open(path)
    self.image_cache[path] = image
    return image
```

### プレビュー更新の遅延

ユーザー入力中はプレビュー更新を遅延:

```python
def schedule_preview_update(self):
    if self.preview_update_timer:
        self.after_cancel(self.preview_update_timer)
    
    self.preview_update_timer = self.after(300, self.draw_preview)
```

### 編集履歴の制限

Undo/Redo履歴を最大50ステップに制限:

```python
MAX_HISTORY = 50

def push_history(self):
    if len(self.history) > MAX_HISTORY:
        self.history.pop(0)
    self.history.append(copy.deepcopy(self.config))
```

## セキュリティ

### ファイルパス検証

ユーザー入力のパスを検証:

```python
def is_safe_path(self, path):
    # 絶対パスに変換
    abs_path = os.path.abspath(path)
    # プロジェクトディレクトリ内かチェック
    return abs_path.startswith(self.project_dir)
```

### コードインジェクション対策

AutoHotkeyコードは直接出力されるため、エディタ側でのサニタイズは限定的。
ユーザーの責任において安全なコードを記述する必要があります。

!!! warning "重要"
    生成されるAHKスクリプトには、ユーザーが入力したコードがそのまま含まれます。信頼できるコードのみを使用してください。

## エラーハンドリング

### Try-Catch の使用

主要な操作をtry-catchで囲む:

```python
def safe_call(self, func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error in {func.__name__}: {e}")
        messagebox.showerror("エラー", f"処理中にエラーが発生しました:\n{e}")
```

## 拡張性

### プラグインシステム（将来的な拡張）

現在は実装されていませんが、将来的にプラグインシステムを追加する可能性があります:

```python
# 将来的な実装例
class PluginManager:
    def __init__(self):
        self.plugins = []
    
    def load_plugin(self, plugin_path):
        # プラグインの動的ロード
        pass
    
    def execute_hook(self, hook_name, *args):
        for plugin in self.plugins:
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)(*args)
```

## ライセンス

### Radify Menu Editor

- **ライセンス**: MIT License
- **著作権**: © 2026 hinatahugu29

### 依存ライブラリ

- **CustomTkinter**: MIT License
- **Pillow**: HPND License
- **Tkinter**: PSF License（Python標準ライブラリ）

## バージョニング

### セマンティックバージョニング

**形式**: `MAJOR.MINOR.PATCH`

- **MAJOR**: 互換性のない変更
- **MINOR**: 後方互換性のある機能追加
- **PATCH**: 後方互換性のあるバグ修正

**現在のバージョン**: 1.3.0

## API（内部）

### 主要なPublicメソッド

#### RadifyMenuEditor

```python
class RadifyMenuEditor:
    def __init__(self)
    def create_new_project(self)
    def refresh_all(self)
    def load_config(self) -> dict
    def save_config(self, backup=True)
    def export_ahk_script(self, output_dir)
```

#### FileIOMixin

```python
class FileIOMixin:
    def load_config(self) -> dict
    def save_config(self, backup=True)
    def create_backup(self)
    def export_ahk_script(self, output_dir)
```

#### PreviewMixin

```python
class PreviewMixin:
    def draw_preview(self)
    def calculate_item_position(self, index, total, radius, center)
```

## 制限事項

### 技術的制限

1. **最大アイテム数**: 1リングあたり推奨12アイテムまで（技術的制限はないが、UI上の理由）
2. **最大リング数**: 推奨5リングまで
3. **画像サイズ**: 最大2048x2048px（メモリ使用量削減のため）
4. **Undo履歴**: 最大50ステップ

### プラットフォーム制限

- **Windows専用**: Tkinterの実装がPlatform依存
- **AutoHotkey v2専用**: v1とは互換性なし

## パフォーマンス指標

### 起動時間

- **初回起動**: 約2-3秒
- **2回目以降**: 約1-2秒（キャッシュあり）

### メモリ使用量

- **アイドル時**: 約50-80MB
- **編集中**: 約100-150MB
- **画像多数読み込み時**: 約200-300MB

### スクリプト生成時間

- **小規模メニュー**（10アイテム未満）: 約0.5秒
- **中規模メニュー**（50アイテム）: 約1-2秒
- **大規模メニュー**（100アイテム以上）: 約3-5秒

## 今後の展望

### 計画中の機能

- プラグインシステム
- テーマカスタマイズ
- クラウド同期機能
- 多言語対応（英語、中国語等）
- アニメーション効果のプレビュー

### コミュニティへの期待

- フィードバックとバグ報告
- 新機能のアイデア提案
- ドキュメントの改善
- テンプレートの共有

## 参考資料

- [AutoHotkey v2 Documentation](https://www.autohotkey.com/docs/v2/)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Python Official Documentation](https://docs.python.org/3/)

---

**最終更新**: 2026年1月  
**ドキュメントバージョン**: 1.0
