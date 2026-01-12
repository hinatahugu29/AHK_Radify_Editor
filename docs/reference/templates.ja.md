# テンプレート

このページでは、Radify Menu Editorのアクションテンプレートシステムについて説明します。

## templates.json

テンプレートは `templates.json` ファイルで管理されています。

### 基本構造

```json
{
  "categories": [
    {
      "category": "カテゴリ名",
      "templates": [...]
    }
  ]
}
```

## テンプレートの形式

### テンプレートオブジェクト

```json
{
  "name": "テンプレート名",
  "code": "AutoHotkeyコード",
  "description": "説明",
  "keywords": ["キーワード1", "キーワード2"]
}
```

#### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|---|---|---|---|
| `name` | String | Yes | テンプレートの表示名 |
| `code` | String | Yes | 挿入されるAutoHotkeyコード |
| `description` | String | No | テンプレートの説明 |
| `keywords` | Array | No | 検索用キーワード |

## 組み込みテンプレート

### アプリケーション起動

```json
{
  "name": "アプリケーション起動",
  "code": "Run \"notepad.exe\"",
  "description": "プログラムを起動します",
  "keywords": ["run", "起動", "実行"]
}
```

### Webページを開く

```json
{
  "name": "Webページを開く",
  "code": "Run \"https://www.google.com\"",
  "description": "ブラウザでURLを開きます",
  "keywords": ["web", "url", "browser"]
}
```

### フォルダを開く

```json
{
  "name": "フォルダを開く",
  "code": "Run \"C:\\\\Users\"",
  "description": "エクスプローラーでフォルダを開きます",
  "keywords": ["folder", "explorer", "フォルダ"]
}
```

### キー送信

```json
{
  "name": "キーを送信",
  "code": "Send \"^c\"",
  "description": "キーボード操作を送信します",
  "keywords": ["send", "キー", "shortcut"]
}
```

### ウィンドウ操作

```json
{
  "name": "ウィンドウを最小化",
  "code": "WinMinimize \"A\"",
  "description": "アクティブウィンドウを最小化します",
  "keywords": ["window", "minimize", "最小化"]
}
```

## カスタムテンプレートの追加

### 手順

1. `templates.json` をテキストエディタで開く
2. 適切なカテゴリに新しいテンプレートを追加
3. ファイルを保存
4. エディタを再起動

### 例: 新しいテンプレートを追加

```json
{
  "category": "カスタム",
  "templates": [
    {
      "name": "スクリーンショット",
      "code": "Send \"#{PrintScreen}\"",
      "description": "Win+PrintScreenでスクリーンショットを撮る",
      "keywords": ["screenshot", "capture", "スクショ"]
    }
  ]
}
```

## テンプレートカテゴリ

### 標準カテゴリ

- **基本**: よく使う基本的なアクション
- **アプリ**: アプリケーション起動関連
- **Web**: Web関連の操作
- **システム**: システム操作
- **ウィンドウ**: ウィンドウ操作
- **メディア**: 音量調整など
- **カスタム**: ユーザー定義テンプレート

## テンプレート変数

### プレースホルダーの使用

将来的には、テンプレート内でプレースホルダーを使用できるようになる予定です。

```json
{
  "name": "アプリ起動（パラメータ付き）",
  "code": "Run \"{APP_PATH}\"",
  "description": "指定したパスのアプリを起動",
  "parameters": [
    {
      "name": "APP_PATH",
      "description": "アプリケーションのパス",
      "default": "notepad.exe"
    }
  ]
}
```

## ベストプラクティス

### 明確な命名

テンプレート名は、そのテンプレートが何をするのかが一目でわかるようにしましょう。

```json
// Good
"name": "メモ帳を起動"

// Bad
"name": "テンプレート1"
```

### わかりやすい説明

`description`フィールドに具体的な説明を記述しましょう。

```json
"description": "メモ帳を起動します。既に起動している場合はアクティブにします。"
```

### キーワードの活用

検索しやすいように、関連するキーワードを追加しましょう。

```json
"keywords": ["notepad", "メモ帳", "テキスト", "エディタ", "text"]
```

## サンプルテンプレート集

### システム操作

```json
{
  "category": "システム",
  "templates": [
    {
      "name": "シャットダウン",
      "code": "Shutdown 1",
      "description": "PCをシャットダウンします",
      "keywords": ["shutdown", "シャットダウン", "電源"]
    },
    {
      "name": "再起動",
      "code": "Shutdown 2",
      "description": "PCを再起動します",
      "keywords": ["restart", "再起動", "reboot"]
    },
    {
      "name": "スリープ",
      "code": "DllCall(\"PowrProf\\\\SetSuspendState\", \"Int\", 0, \"Int\", 0, \"Int\", 0)",
      "description": "PCをスリープ状態にします",
      "keywords": ["sleep", "スリープ", "suspend"]
    }
  ]
}
```

### メディア操作

```json
{
  "category": "メディア",
  "templates": [
    {
      "name": "音量を上げる",
      "code": "SoundSetVolume \"+10\"",
      "description": "音量を10%上げます",
      "keywords": ["volume", "音量", "up"]
    },
    {
      "name": "音量を下げる",
      "code": "SoundSetVolume \"-10\"",
      "description": "音量を10%下げます",
      "keywords": ["volume", "音量", "down"]
    },
    {
      "name": "ミュート切り替え",
      "code": "SoundSetMute -1",
      "description": "ミュートのON/OFFを切り替えます",
      "keywords": ["mute", "ミュート", "消音"]
    }
  ]
}
```

### クリップボード操作

```json
{
  "category": "クリップボード",
  "templates": [
    {
      "name": "クリップボードにコピー",
      "code": "A_Clipboard := \"コピーするテキスト\"",
      "description": "指定したテキストをクリップボードにコピーします",
      "keywords": ["clipboard", "copy", "コピー"]
    },
    {
      "name": "クリップボードを貼り付け",
      "code": "Send \"^v\"",
      "description": "Ctrl+Vでクリップボードの内容を貼り付けます",
      "keywords": ["clipboard", "paste", "貼り付け"]
    }
  ]
}
```

## トラブルシューティング

### テンプレートが表示されない

- `templates.json` の構文エラーがないか確認
- エディタを再起動してみる

### テンプレートが動作しない

- コード内の構文エラーを確認
- AutoHotkey v2の構文に準拠しているか確認

## 次のステップ

- [モジュール構成](modules.md)
- [カスタムアクション](../advanced/custom-actions.md)
