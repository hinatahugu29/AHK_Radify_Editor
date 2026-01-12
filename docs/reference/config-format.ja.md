# 設定ファイル形式

このページでは、Radify Menu Editorが使用する設定ファイルの形式を説明します。

## menu_config.json

メニューの構造とすべての設定を含むJSONファイルです。

### 基本構造

```json
{
  "image_dir": "images",
  "main_menu": [...],
  "submenus": {...},
  "menu_options": {...},
  "favorites": [...]
}
```

### トップレベルフィールド

#### image_dir

```json
"image_dir": "images"
```

アイコン画像が格納されるディレクトリのパス（相対パス）。

#### main_menu

```json
"main_menu": [
  {
    "ring": 1,
    "items": [...]
  },
  {
    "ring": 2,
    "items": [...]
  }
]
```

メインメニューのリング構造を定義する配列。

#### submenus

```json
"submenus": {
  "ツールメニュー": [...],
  "設定メニュー": [...]
}
```

サブメニューの定義。キーがサブメニュー名、値がリング配列。

#### menu_options

```json
"menu_options": {
  "skin": "Default",
  "EnableGlow": true,
  "itemSize": 60,
  "ringSpacing": 80,
  "menu_name": "myMainMenu",
  "gui_font_family": "",
  "gui_font_size": 12,
  "appearance_mode": "Dark"
}
```

メニュー全体の設定。

#### favorites

```json
"favorites": [
  {
    "name": "お気に入り1",
    "data": {...}
  }
]
```

お気に入りアイテムのリスト（将来の機能拡張用）。

## リング構造

### リングオブジェクト

```json
{
  "ring": 1,
  "items": [...]
}
```

- **ring**: リング番号（1から開始、内側から外側へ）
- **items**: このリングに配置されるアイテムの配列

## アイテム構造

### 基本アイテム

```json
{
  "label": "メモ帳",
  "icon": "images/notepad.png",
  "action": "Run \"notepad.exe\""
}
```

#### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `label` | String | Yes | アイテムに表示されるラベルテキスト |
| `icon` | String | No | アイコン画像のパス（相対または絶対） |
| `action` | String | No | クリック時に実行されるAutoHotkeyコード |

### サブメニューリンク

```json
{
  "label": "ツール",
  "icon": "images/tool-box.png",
  "submenu": "ツールメニュー"
}
```

- **submenu**: 遷移先のサブメニュー名（`submenus`のキーと一致）

### 空のアイテム

```json
{
  "label": "",
  "icon": "",
  "action": ""
}
```

空のスロットとして機能します。

## メニューオプション詳細

### skin

```json
"skin": "Default"
```

使用するスキン名。

利用可能な値:
- `"Default"`
- `"Dark"`
- `"Light"`
- `"Custom"`

### EnableGlow

```json
"EnableGlow": true
```

アイテムのグロー（発光）効果の有効/無効。

- `true`: 有効
- `false`: 無効

### itemSize

```json
"itemSize": 60
```

アイテムアイコンのサイズ（ピクセル単位）。

推奨範囲: 40 〜 100

### ringSpacing

```json
"ringSpacing": 80
```

リング間の距離（ピクセル単位）。

推奨範囲: 60 〜 120

### menu_name

```json
"menu_name": "myMainMenu"
```

AutoHotkeyスクリプト内で使用されるメニューオブジェクトの変数名。

命名規則: 英数字とアンダースコアのみ、数字で始まらない

### gui_font_family

```json
"gui_font_family": "Yu Gothic UI"
```

メニューで使用するフォントファミリー。

空文字列の場合はシステムデフォルト。

### gui_font_size

```json
"gui_font_size": 12
```

フォントサイズ（ポイント単位）。

推奨範囲: 8 〜 18

### appearance_mode

```json
"appearance_mode": "Dark"
```

エディタの外観モード。

利用可能な値:
- `"Light"`: ライトモード
- `"Dark"`: ダークモード
- `"System"`: システム設定に従う

## 完全な例

### シンプルなメニュー

```json
{
  "image_dir": "images",
  "main_menu": [
    {
      "ring": 1,
      "items": [
        {
          "label": "メモ帳",
          "icon": "images/notepad.png",
          "action": "Run \"notepad.exe\""
        },
        {
          "label": "電卓",
          "icon": "images/calculator.png",
          "action": "Run \"calc.exe\""
        },
        {
          "label": "Google",
          "icon": "images/google.png",
          "action": "Run \"https://www.google.com\""
        }
      ]
    }
  ],
  "submenus": {},
  "menu_options": {
    "skin": "Default",
    "EnableGlow": true,
    "itemSize": 60,
    "ringSpacing": 80,
    "menu_name": "myMainMenu",
    "gui_font_family": "",
    "gui_font_size": 12,
    "appearance_mode": "Dark"
  },
  "favorites": []
}
```

### 複雑なメニュー（サブメニュー付き）

```json
{
  "image_dir": "images",
  "main_menu": [
    {
      "ring": 1,
      "items": [
        {
          "label": "アプリ",
          "icon": "images/apps.png",
          "submenu": "アプリメニュー"
        },
        {
          "label": "Web",
          "icon": "images/web.png",
          "submenu": "Webメニュー"
        }
      ]
    }
  ],
  "submenus": {
    "アプリメニュー": [
      {
        "ring": 1,
        "items": [
          {
            "label": "メモ帳",
            "icon": "images/notepad.png",
            "action": "Run \"notepad.exe\""
          },
          {
            "label": "電卓",
            "icon": "images/calculator.png",
            "action": "Run \"calc.exe\""
          }
        ]
      }
    ],
    "Webメニュー": [
      {
        "ring": 1,
        "items": [
          {
            "label": "Google",
            "icon": "images/google.png",
            "action": "Run \"https://www.google.com\""
          },
          {
            "label": "GitHub",
            "icon": "images/github.png",
            "action": "Run \"https://github.com\""
          }
        ]
      }
    ]
  },
  "menu_options": {
    "skin": "Default",
    "EnableGlow": true,
    "itemSize": 60,
    "ringSpacing": 80,
    "menu_name": "myMainMenu",
    "gui_font_family": "Yu Gothic UI",
    "gui_font_size": 12,
    "appearance_mode": "Dark"
  },
  "favorites": []
}
```

## 手動編集

### バックアップの重要性

手動で編集する前に、必ずバックアップを取ってください。

```bash
copy menu_config.json menu_config.backup.json
```

### JSONの検証

編集後、JSONの構文が正しいことを確認してください。

オンラインツール:
- [JSONLint](https://jsonlint.com/)
- [JSON Formatter](https://jsonformatter.curiousconcept.com/)

### エディタでの再読み込み

手動編集後、エディタで「ファイル」→「設定を開く」から再読み込みしてください。

## トラブルシューティング

### 設定ファイルが読み込めない

- JSON構文エラーがないか確認
- フィールド名のスペルミスがないか確認
- 引用符が正しく閉じられているか確認

### アイコンが表示されない

- `image_dir` のパスが正しいか確認
- 各アイテムの `icon` パスが正しいか確認

### サブメニューに移動できない

- `submenu` フィールドの値が `submenus` のキーと一致しているか確認
- サブメニュー名の大文字小文字が一致しているか確認

## 次のステップ

- [テンプレート](templates.md)
- [モジュール構成](modules.md)
