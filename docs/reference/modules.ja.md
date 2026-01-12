# モジュール構成

このページでは、Radify Menu Editorのソースコード構成とモジュール設計について説明します。

## プロジェクト構造

```
AHK_Radify_Editor_Modular/
├── main.py                 # エントリーポイント
├── modules/                # コアモジュール
│   ├── __init__.py
│   ├── core.py            # メインクラス
│   ├── ui_setup.py        # UI構築
│   ├── preview.py         # プレビュー描画
│   ├── file_io.py         # ファイル入出力
│   ├── actions.py         # ユーザーアクション処理
│   ├── dialogs.py         # ダイアログ管理
│   ├── images.py          # 画像処理
│   └── utils.py           # ユーティリティ
├── menu_config.json        # メニュー設定
├── templates.json          # アクションテンプレート
└── images/                 # アイコンリソース
```

## モジュール詳細

### main.py

**役割**: アプリケーションのエントリーポイント

```python
from modules.core import RadifyMenuEditor

if __name__ == "__main__":
    app = RadifyMenuEditor()
    app.mainloop()
```

### modules/core.py

**役割**: メインアプリケーションクラス

**主要クラス**: `RadifyMenuEditor`

**継承**:
- `CTk` (CustomTkinter)
- `UISetupMixin`
- `PreviewMixin`
- `FileIOMixin`
- `ActionsMixin`
- `DialogsMixin`
- `ImageMixin`

**主要メソッド**:
- `__init__()`: 初期化
- `create_new_project()`: 新規プロジェクト作成
- `refresh_all()`: UI全体を更新
- `check_dependencies()`: 依存関係チェック
- `on_closing()`: 終了時の処理

### modules/ui_setup.py

**役割**: ユーザーインターフェースの構築

**主要クラス**: `UISetupMixin`

**主要メソッド**:
- `build_ui()`: メインUIの構築
- `create_menu_bar()`: メニューバーの作成
- `create_toolbar()`: ツールバーの作成
- `create_tree_panel()`: ツリービューパネル
- `create_preview_panel()`: プレビューパネル
- `create_properties_panel()`: プロパティパネル

**UIコンポーネント**:
- ツリービュー（Treeview）
- プレビューキャンバス（Canvas）
- プロパティエディタ（Entry, Text, Button等）

### modules/preview.py

**役割**: リングメニューのプレビュー描画

**主要クラス**: `PreviewMixin`

**主要メソッド**:
- `draw_preview()`: プレビュー全体を描画
- `draw_ring()`: 特定のリングを描画
- `draw_item()`: 個別アイテムを描画
- `calculate_item_position()`: アイテム座標を計算

**描画ロジック**:
- GDI+を模したCanvas描画
- 円形配置のための三角関数計算
- アイコンとラベルのレイアウト

### modules/file_io.py

**役割**: ファイルの読み書き

**主要クラス**: `FileIOMixin`

**主要メソッド**:
- `load_config()`: 設定ファイルの読み込み
- `save_config()`: 設定ファイルの保存
- `create_backup()`: バックアップの作成
- `export_ahk_script()`: AHKスクリプトの出力
- `load_templates()`: テンプレートの読み込み

**ファイル形式**:
- JSON形式での設定管理
- 自動バックアップ機能
- タイムスタンプ付きバックアップ

### modules/actions.py

**役割**: ユーザーアクションの処理

**主要クラス**: `ActionsMixin`

**主要メソッド**:
- `refresh_tree()`: ツリービューの更新
- `on_tree_select()`: ツリー選択時の処理
- `add_new_ring()`: 新規リングの追加
- `add_new_item()`: 新規アイテムの追加
- `delete_selected()`: 選択要素の削除
- `copy_item()` / `paste_item()`: コピー&ペースト
- `undo()` / `redo()`: 編集履歴の管理

**機能**:
- ドラッグ&ドロップ
- Undo/Redo履歴管理
- クリップボード機能

### modules/dialogs.py

**役割**: 各種ダイアログの管理

**主要クラス**: `DialogsMixin`

**主要メソッド**:
- `show_menu_options_dialog()`: メニューオプション設定
- `show_template_dialog()`: テンプレート検索ダイアログ
- `show_about_dialog()`: バージョン情報
- `show_export_dialog()`: エクスポート設定

**ダイアログ種類**:
- 設定ダイアログ
- テンプレート検索ウィンドウ
- ファイル選択ダイアログ
- 確認ダイアログ

### modules/images.py

**役割**: 画像処理

**主要クラス**: `ImageMixin`

**主要メソッド**:
- `load_image()`: 画像の読み込み
- `resize_image()`: 画像のリサイズ
- `capture_screen()`: 画面キャプチャ
- `refresh_image_list()`: 画像リストの更新

**画像処理**:
- PIL (Pillow) を使用
- 自動リサイズ
- キャッシュ管理
- 画面キャプチャ機能

### modules/utils.py

**役割**: ユーティリティ関数

**主要関数**:
- `sanitize_var_name()`: 変数名の正規化
- `escape_ahk_string()`: AHK文字列のエスケープ
- `validate_json()`: JSON検証
- `generate_unique_name()`: 一意な名前の生成

## データフロー

### 設定の読み込み

```
load_config() 
  → JSON解析 
  → self.config に格納 
  → refresh_tree() 
  → ツリービューに表示
```

### アイテムの編集

```
on_tree_select()
  → 選択アイテムのデータ取得
  → プロパティパネルに表示
  → ユーザーが編集
  → apply_item()
  → self.config を更新
  → draw_preview() で即座に反映
```

### スクリプト出力

```
export_ahk_script()
  → self.config から読み取り
  → AHKコードを生成
  → ファイルに書き出し
  → 依存ライブラリをコピー
  → 使用画像をコピー
```

## Mixin設計の理由

### メリット

1. **関心の分離**: 各機能を独立したモジュールに分割
2. **保守性**: 特定の機能を修正する際に該当モジュールのみ編集
3. **再利用性**: 他のプロジェクトでも部分的に再利用可能
4. **可読性**: ファイルサイズが適切に分割され読みやすい

### デメリットと対策

- **複雑性**: 複数のMixinを継承するため、メソッドの所在がわかりにくい
  - 対策: 明確な命名規則と適切なコメント

## 拡張方法

### 新しい機能を追加

1. 適切なMixinに新しいメソッドを追加、または
2. 新しいMixinを作成して `core.py` で継承

例: 新しい機能用のMixin

```python
# modules/new_feature.py
class NewFeatureMixin:
    def new_feature_method(self):
        # 新機能の実装
        pass
```

```python
# modules/core.py
from .new_feature import NewFeatureMixin

class RadifyMenuEditor(CTk, UISetupMixin, ..., NewFeatureMixin):
    ...
```

### カスタムテンプレートの追加

`templates.json` を編集して新しいテンプレートを追加するだけです。

### UI要素の追加

`ui_setup.py` の該当メソッドを編集してコンポーネントを追加します。

## デバッグ

### ログ出力

プリント文を使った簡易デバッグ:

```python
print(f"Debug: {variable_name}")
```

### エラーハンドリング

`core.py` の `safe_call()` メソッドを使用:

```python
self.safe_call(self.some_method, arg1, arg2)
```

## パフォーマンス最適化

### 画像キャッシュ

`images.py` でロード済み画像をキャッシュ:

```python
self.image_cache = {}
```

### プレビューの遅延更新

ユーザー入力中はプレビュー更新を遅延させることで、スムーズな操作感を実現:

```python
self.preview_update_pending = False
```

## セキュリティ考慮事項

### ファイルパスの検証

ユーザー入力のパスを使用する際は、必ず検証:

```python
if os.path.exists(path):
    # 安全に処理
```

### コードインジェクション対策

ユーザーが入力したAHKコードは、そのまま出力されるため、エディタ側でのサニタイズは限定的です。使用者の責任において安全なコードを記述してください。

## テスト

現在、自動テストは実装されていませんが、以下のような手動テストを推奨:

1. 設定ファイルの読み書き
2. アイテムの追加・削除・編集
3. プレビューの正確性
4. AHKスクリプト出力の動作確認

## 次のステップ

- [カスタムアクション](../advanced/custom-actions.md)
- [トラブルシューティング](../advanced/troubleshooting.md)
