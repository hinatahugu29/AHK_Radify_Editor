# 複数メニューの管理

このページでは、複数のリングメニューを効率的に管理する方法を説明します。

## 複数メニューの必要性

### ユースケース

- **用途別メニュー**: 仕事用、プライベート用など
- **アプリ固有メニュー**: 特定のアプリケーションでのみ使用
- **階層的メニュー**: サブメニューで深い階層を構築
- **テーマ別メニュー**: 開発用、メディア編集用など

## サブメニューの活用

### サブメニューの作成

1. メインメニューのアイテムを選択
2. 「サブメニュー追加」ボタンをクリック
3. サブメニュー名を入力
4. サブメニューにリング・アイテムを追加

### サブメニューの構造

```json
{
  "main_menu": [
    {
      "ring": 1,
      "items": [
        {
          "label": "開発ツール",
          "submenu": "開発メニュー"
        }
      ]
    }
  ],
  "submenus": {
    "開発メニュー": [
      {
        "ring": 1,
        "items": [
          {"label": "VS Code", "action": "Run \"code\""},
          {"label": "Git Bash", "action": "Run \"git-bash.exe\""}
        ]
      }
    ]
  }
}
```

## 複数の設定ファイル

### 設定ファイルの分離

用途ごとに別々の設定ファイルを作成:

```
configs/
├── menu_work.json      # 仕事用
├── menu_personal.json  # プライベート用
└── menu_gaming.json    # ゲーム用
```

### 設定の切り替え

エディタで「ファイル」→「設定を開く」から、使用したい設定ファイルを選択します。

## 動的メニュー切り替え

### AutoHotkeyスクリプトでの切り替え

複数のメニューを1つのスクリプトに統合:

```ahk
#Include Radify.ahk

; メニュー1の定義
menu1 := RadifyMenu()
menu1.items := [...]

; メニュー2の定義
menu2 := RadifyMenu()
menu2.items := [...]

; ホットキーでメニューを切り替え
^Space::menu1.Show()
^!Space::menu2.Show()
```

### コンテキスト依存のメニュー

アクティブなウィンドウによってメニューを切り替え:

```ahk
^Space::
{
    if WinActive("ahk_exe code.exe")
        devMenu.Show()
    else if WinActive("ahk_exe chrome.exe")
        webMenu.Show()
    else
        mainMenu.Show()
}
```

## メニューの統合管理

### マスター設定ファイル

複数のメニュー設定を1つのファイルで管理:

```json
{
  "menus": {
    "main": {
      "hotkey": "^Space",
      "config": "menu_main.json"
    },
    "dev": {
      "hotkey": "^!d",
      "config": "menu_dev.json"
    },
    "media": {
      "hotkey": "^!m",
      "config": "menu_media.json"
    }
  }
}
```

### 起動スクリプトの生成

マスター設定から自動的にスクリプトを生成することも可能です（カスタムツールが必要）。

## メニューのインポート/エクスポート

### エクスポート

1. 「ファイル」→「AHKスクリプト出力」
2. メニューごとに別フォルダに出力

```
exports/
├── MainMenu/
│   ├── MainMenu.ahk
│   └── images/
├── DevMenu/
│   ├── DevMenu.ahk
│   └── images/
└── MediaMenu/
    ├── MediaMenu.ahk
    └── images/
```

### インポート

別のプロジェクトから設定をインポート:

1. `menu_config.json` をコピー
2. 「ファイル」→「設定を開く」で読み込み
3. 必要に応じて編集

## 共通リソースの管理

### アイコンの共有

複数のメニューで同じアイコンを使用する場合、共通フォルダに配置:

```
共有構造/
├── common_images/     # 共通アイコン
├── menu_main.json
├── menu_dev.json
└── menu_media.json
```

各設定ファイルで共通パスを参照:

```json
"image_dir": "../common_images"
```

### テンプレートの共有

`templates.json` を共通化して、すべてのメニューで同じテンプレートを使用できます。

## プロファイル管理

### プロファイルの概念

環境や状況に応じたメニューセット:

- **オフィスプロファイル**: 仕事関連のメニューのみ
- **ホームプロファイル**: プライベート用メニュー
- **ゲーミングプロファイル**: ゲーム特化メニュー

### プロファイル切り替えスクリプト

```ahk
; プロファイル管理スクリプト
currentProfile := "office"

SwitchProfile(profile) {
    global currentProfile
    currentProfile := profile
    
    switch profile {
        case "office":
            ; オフィス用メニューを読み込み
            Run "OfficeMenu.ahk"
        case "home":
            ; ホーム用メニューを読み込み
            Run "HomeMenu.ahk"
        case "gaming":
            ; ゲーム用メニューを読み込み
            Run "GamingMenu.ahk"
    }
}

; ホットキーで切り替え
^!1::SwitchProfile("office")
^!2::SwitchProfile("home")
^!3::SwitchProfile("gaming")
```

## バージョン管理

### Gitでの管理

複数の設定ファイルをGitで管理:

```bash
git init
git add *.json
git commit -m "Initial menu configurations"
```

### ブランチ戦略

- `main`: 安定版
- `dev`: 開発中の変更
- `experimental`: 実験的な機能

```bash
git checkout -b dev
# メニューを編集
git add menu_config.json
git commit -m "Add new development tools"
git checkout main
git merge dev
```

## 同期と配布

### クラウドストレージでの同期

Dropbox、OneDrive等を使用:

```
C:\Users\YourName\Dropbox\RadifyMenus\
├── menu_main.json
├── menu_dev.json
└── templates.json
```

複数のPCで同じ設定を共有できます。

### チームでの共有

GitHubやGitLabで設定を共有:

1. リポジトリに設定ファイルをプッシュ
2. チームメンバーがクローン
3. 各自がカスタマイズ

## ベストプラクティス

### 命名規則

わかりやすいファイル名とメニュー名:

```
menu_work_development.json
menu_personal_media.json
menu_gaming_shortcuts.json
```

### ドキュメント化

各メニューの目的をREADME.mdに記述:

```markdown
# メニュー構成

- **menu_main.json**: メインメニュー（全般）
- **menu_dev.json**: 開発ツール用
- **menu_media.json**: メディア編集用
```

### 定期的なバックアップ

重要な設定は定期的にバックアップ:

```bash
# バックアップスクリプト
$date = Get-Date -Format "yyyyMMdd"
Copy-Item "menu_*.json" "backups\backup_$date\"
```

## トラブルシューティング

### メニューが多すぎて管理しづらい

- メニューを統合する
- サブメニューを活用して階層化
- 使用頻度の低いメニューを削除

### 設定ファイルの競合

- バージョン管理システムを使用
- 変更前にバックアップ
- マージツールで競合を解決

### アイコンパスの不整合

- 相対パスを使用
- 共通アイコンフォルダを作成
- パスを一括置換

## 高度なテクニック

### メニューのホットリロード

スクリプトを再起動せずに設定を再読み込み:

```ahk
ReloadMenu() {
    ; 設定ファイルを再読み込み
    config := LoadConfig("menu_config.json")
    myMenu.UpdateFromConfig(config)
}

; ホットキーでリロード
^!r::ReloadMenu()
```

### 条件付きメニュー表示

特定の条件下でのみメニューを表示:

```ahk
ShowConditionalMenu() {
    hour := A_Hour
    if (hour >= 9 && hour < 17)
        workMenu.Show()
    else
        personalMenu.Show()
}
```

## 次のステップ

- [トラブルシューティング](troubleshooting.md)
- [カスタムアクション](custom-actions.md)
