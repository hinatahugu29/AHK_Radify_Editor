# アクションの設定

このページでは、メニューアイテムをクリックしたときに実行されるアクションの設定方法を説明します。

## アクションの種類

Radify Menu Editorでは、以下のような様々なアクションを設定できます:

- **アプリケーション起動**: プログラムやファイルを開く
- **キー送信**: キーボード操作を自動化
- **ウィンドウ操作**: ウィンドウの最小化、最大化など
- **システムコマンド**: シャットダウン、再起動など
- **スクリプト実行**: AutoHotkeyコードの実行
- **サブメニュー表示**: 別のメニューへ遷移

## テンプレートを使用したアクション設定

### テンプレートの検索

1. アイテムを選択
2. 右パネルの「テンプレート検索」をクリック
3. カテゴリまたはキーワードで検索
4. 目的のテンプレートをクリック

### よく使うテンプレート

#### アプリケーション起動

```ahk
Run "notepad.exe"
```

パラメータ付きで起動:

```ahk
Run "notepad.exe C:\memo.txt"
```

#### Webページを開く

```ahk
Run "https://www.google.com"
```

#### フォルダを開く

```ahk
Run "C:\Users\YourName\Documents"
```

#### キー送信

```ahk
Send "^c"  ; Ctrl+C
```

```ahk
Send "^v"  ; Ctrl+V
```

#### ウィンドウの最小化

```ahk
WinMinimize "A"
```

## 直接コードを記述

### 基本的な記述方法

アクションフィールドに直接AutoHotkey v2のコードを記述できます。

```ahk
MsgBox "Hello, World!"
```

!!! note "自動ラップ"
    エディタが自動的に無名関数 `(*) => { ... }` としてラップするため、直接コードを書くだけで動作します。

### 複数行のコード

複数の処理を順次実行:

```ahk
WinActivate "ahk_exe notepad.exe"
Send "Hello from Radify!"
```

### 条件分岐

ウィンドウの状態によって動作を変える:

```ahk
if WinExist("ahk_exe notepad.exe")
    WinActivate
else
    Run "notepad.exe"
```

### 変数の使用

```ahk
myPath := "C:\MyFolder"
Run myPath
```

## 高度なアクション

### ホットキーのトグル

```ahk
static toggle := false
toggle := !toggle
if toggle
    MsgBox "ON"
else
    MsgBox "OFF"
```

### クリップボード操作

```ahk
A_Clipboard := "コピーされたテキスト"
MsgBox "クリップボードにコピーしました"
```

### ファイルの読み書き

```ahk
FileAppend "ログ: " A_Now "`n", "C:\log.txt"
```

### COM操作（Excel等）

```ahk
xl := ComObject("Excel.Application")
xl.Visible := true
xl.Workbooks.Add
```

## サブメニューへのリンク

### 手動設定

```ahk
ShowSubmenu("サブメニュー名")
```

### ドロップダウンから選択

1. 右パネルの「サブメニュー」ドロップダウン
2. 遷移先のサブメニューを選択
3. アクションが自動設定される

## エラー処理

### Try-Catch

```ahk
try {
    Run "存在しないファイル.exe"
} catch as err {
    MsgBox "エラー: " err.Message
}
```

## アクションのデバッグ

### MsgBoxでの確認

```ahk
MsgBox "この位置まで実行されました"
Run "notepad.exe"
```

### ToolTipでの通知

```ahk
ToolTip "処理中..."
Sleep 2000
ToolTip  ; ToolTipを消す
```

## ベストプラクティス

### わかりやすいコード

- コメントを活用
- 変数名は説明的に
- 複雑な処理は分割

```ahk
; メモ帳を開いて特定のファイルを読み込む
notePath := "C:\memo.txt"
if FileExist(notePath)
    Run "notepad.exe " notePath
else
    MsgBox "ファイルが見つかりません"
```

### パスの取り扱い

#### 絶対パスを使用

```ahk
Run "C:\Program Files\MyApp\app.exe"
```

#### 相対パスを使用（スクリプトからの相対）

```ahk
Run A_ScriptDir "\tools\mytool.exe"
```

#### 環境変数を活用

```ahk
Run A_ProgramFiles "\Microsoft Office\Office16\EXCEL.EXE"
```

### エラーに強いコード

存在確認をしてから実行:

```ahk
if FileExist("C:\myapp.exe")
    Run "C:\myapp.exe"
else
    MsgBox "アプリが見つかりません"
```

## テンプレートのカスタマイズ

### 自分用テンプレートの作成

`templates.json` ファイルを編集することで、独自のテンプレートを追加できます。

```json
{
  "category": "カスタム",
  "templates": [
    {
      "name": "My Custom Action",
      "code": "Run \"myapp.exe\"",
      "description": "私のカスタムアクション"
    }
  ]
}
```

## トラブルシューティング

### アクションが実行されない

1. コードに構文エラーがないか確認
2. パスが正しいか確認
3. 管理者権限が必要な場合は、スクリプトを管理者として実行

### パスが見つからない

- 絶対パスを使用してみる
- ファイルが実際に存在するか確認
- `FileExist()` で事前確認

### ウィンドウが見つからない

- ウィンドウタイトルが正しいか確認
- `ahk_exe` または `ahk_class` を使用
- Window Spyツールで正確な情報を取得

## サンプル集

### よく使うアクション

#### Googleで検索

```ahk
query := "検索キーワード"
Run "https://www.google.com/search?q=" query
```

#### 音量調整

```ahk
SoundSetVolume "+10"  ; 音量を10%上げる
```

```ahk
SoundSetVolume "-10"  ; 音量を10%下げる
```

#### スクリーンショット

```ahk
Send "#{PrintScreen}"  ; Win+PrintScreen
```

#### タスクマネージャーを開く

```ahk
Run "taskmgr.exe"
```

## 次のステップ

アクションの設定方法を理解したら、次はビジュアルを整えましょう:

- [アイコンとビジュアル](icons-visuals.md)
- [スクリプト出力](export.md)

より高度な使い方については:

- [カスタムアクション](../advanced/custom-actions.md)
