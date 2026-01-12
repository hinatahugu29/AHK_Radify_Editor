# 最小実行環境の構成

## ✅ アプリケーション実行に必要なファイル

### コアファイル（必須）
```
AHK_Radify_Editor_Modular/
├── main.py                    # エントリーポイント
├── requirements.txt           # Python依存パッケージ
├── menu_config.json           # メニュー設定
└── templates.json             # アクションテンプレート
```

### モジュール（必須）
```
modules/
├── __init__.py               # パッケージ初期化
├── core.py                   # メインクラス
├── ui_setup.py              # UI構築
├── preview.py               # プレビュー描画
├── file_io.py               # ファイル入出力
├── actions.py               # ユーザーアクション処理
├── dialogs.py               # ダイアログ管理
├── images.py                # 画像処理
└── utils.py                 # ユーティリティ
```

### リソース（推奨）
```
images/
└── (使用するアイコン画像)
```

## ❌ 実行に不要なファイル（ドキュメント・開発用）

```
docs/                         # ドキュメント全体（Read the Docs用）
README.md                     # GitHub用プロジェクト説明
LICENSE                       # ライセンスファイル
.gitignore                    # Git除外設定
.readthedocs.yaml            # Read the Docs設定
mkdocs.yml                   # ドキュメントビルド設定
GITHUB_SETUP.md              # セットアップガイド
HOWTO.html                   # HTMLドキュメント
TECH_SPEC.html               # 技術仕様HTML
Radify_Editor_Introduction.md # 紹介記事
```

## 🚀 最小環境のセットアップ手順

### 1. 新しいフォルダを作成
```bash
mkdir Radify_Editor_Minimal
cd Radify_Editor_Minimal
```

### 2. 必要なファイルをコピー
```powershell
# コアファイル
Copy-Item ..\main.py .
Copy-Item ..\requirements.txt .
Copy-Item ..\menu_config.json .
Copy-Item ..\templates.json .

# モジュール
Copy-Item ..\modules -Recurse .

# 画像（最小限）
New-Item -ItemType Directory -Name images
Copy-Item ..\images\radify-skin-editor.png .\images\
# 必要に応じて他のアイコンも
```

### 3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 4. 起動
```bash
python main.py
```

## 📊 ファイルサイズ比較

### フルバージョン
- 約30-50MB（ドキュメント、画像209個含む）

### 最小バージョン
- 約5-10MB（必須ファイルのみ）

## 💡 推奨する構成

実際の開発・使用では以下の構成をお勧めします：

```
AHK_Radify_Editor_Modular/
├── main.py              ✅ 必須
├── requirements.txt     ✅ 必須
├── modules/             ✅ 必須
├── menu_config.json     ✅ 必須
├── templates.json       ✅ 必須
├── images/              ✅ 必須（少なくとも使うアイコン）
├── README.md            📝 推奨（使い方の参照用）
└── HOWTO.html           📝 推奨（詳細なガイド）
```

## 🗂️ フォルダ整理のヒント

### オプション1: ドキュメントを別フォルダに
```
Radify_Editor/
├── app/                 # アプリ本体
│   ├── main.py
│   ├── modules/
│   └── ...
└── docs/                # ドキュメント
    └── ...
```

### オプション2: そのまま（推奨）
GitHubリポジトリとしてはそのままの構成が最適です。
- ユーザーはドキュメントをオンラインで読む
- 開発者は全ファイルにアクセス可能

## ⚡ クイックコマンド

最小実行環境を別フォルダに作成（PowerShell）:

```powershell
# 新しいフォルダ作成
New-Item -ItemType Directory -Name "Radify_Minimal"

# 必須ファイルをコピー
Copy-Item main.py Radify_Minimal\
Copy-Item requirements.txt Radify_Minimal\
Copy-Item menu_config.json Radify_Minimal\
Copy-Item templates.json Radify_Minimal\
Copy-Item modules -Recurse Radify_Minimal\

# 画像フォルダを作成し、最小限のアイコンをコピー
New-Item -ItemType Directory -Path Radify_Minimal\images
Copy-Item images\radify-skin-editor.png Radify_Minimal\images\
```
