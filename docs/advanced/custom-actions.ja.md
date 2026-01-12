# カスタムアクション

このページでは、AutoHotkey v2の全機能を活用した高度なアクションの作成方法を説明します。

## AutoHotkey v2の基礎

### コードの直接記述

Radify Menu Editorでは、アクションフィールドに直接AutoHotkey v2のコードを記述できます。

エディタが自動的に無名関数としてラップするため、以下のように書くだけで動作します:

```ahk
MsgBox "Hello, World!"
```

実際にスクリプトで生成されるコード:

```ahk
item.action := (*) => {
    MsgBox "Hello, World!"
}
```

## 高度なアクション例

### 条件分岐

#### ウィンドウの状態によって動作を変更

```ahk
if WinExist("ahk_exe notepad.exe")
    WinActivate
else
    Run "notepad.exe"
```

#### 時間帯によって動作を変更

```ahk
hour := A_Hour
if (hour >= 9 && hour < 17)
    Run "work_app.exe"
else
    Run "personal_app.exe"
```

### ループ処理

#### 複数のウィンドウを順次操作

```ahk
windows := ["ahk_exe notepad.exe", "ahk_exe calc.exe"]
for exe in windows {
    if WinExist(exe)
        WinActivate
}
```

### 変数と配列

#### よく使うパスを変数化

```ahk
myDocs := A_MyDocuments
myWork := myDocs "\Work"
Run myWork
```

#### 配列からランダムに選択

```ahk
sites := ["https://www.google.com", "https://github.com", "https://stackoverflow.com"]
Random, index, 1, sites.Length
Run sites[index]
```

## 高度なウィンドウ操作

### ウィンドウの位置とサイズを調整

```ahk
if WinExist("ahk_exe notepad.exe") {
    WinActivate
    WinMove 0, 0, 800, 600  ; x, y, width, height
}
```

### ウィンドウを半分サイズに

```ahk
WinActivate "A"
WinGetPos &x, &y, &w, &h
screenW := A_ScreenWidth
WinMove 0, 0, screenW // 2, A_ScreenHeight
```

### 複数モニター環境での配置

```ahk
; 2番目のモニターに移動
MonitorGet 2, &Left, &Top, &Right, &Bottom
WinMove Left, Top, Right-Left, Bottom-Top, "A"
```

## ホットキーの動的制御

### 他のホットキーのON/OFF

```ahk
static enabled := true
enabled := !enabled
if enabled
    Hotkey "^!a", (*) => MsgBox("Enabled"), "On"
else
    Hotkey "^!a", "Off"
```

## クリップボードの高度な利用

### クリップボードの内容を加工

```ahk
old := A_Clipboard
A_Clipboard := StrUpper(old)  ; 大文字に変換
Sleep 100
Send "^v"
Sleep 100
A_Clipboard := old  ; 元に戻す
```

### クリップボード履歴

```ahk
static history := []
history.Push(A_Clipboard)
if history.Length > 10
    history.RemoveAt(1)
; 履歴を表示（実装は省略）
```

## ファイル操作

### テキストファイルの読み書き

```ahk
; 書き込み
FileAppend "ログ: " A_Now "`n", "C:\log.txt"

; 読み込み
content := FileRead("C:\data.txt")
MsgBox content
```

### ファイル存在チェック

```ahk
if FileExist("C:\important_file.txt")
    MsgBox "ファイルが存在します"
else
    MsgBox "ファイルが見つかりません"
```

### フォルダの作成

```ahk
myFolder := "C:\MyProjects\NewProject"
if !DirExist(myFolder)
    DirCreate myFolder
Run myFolder
```

## レジストリ操作

!!! warning "注意"
    レジストリの編集は慎重に行ってください。誤った操作はシステムに影響を与える可能性があります。

### レジストリ値の読み取り

```ahk
value := RegRead("HKEY_CURRENT_USER\Software\MyApp", "Setting")
MsgBox "現在の値: " value
```

### レジストリ値の書き込み

```ahk
RegWrite "MyValue", "REG_SZ", "HKEY_CURRENT_USER\Software\MyApp", "Setting"
```

## COM操作

### Excelの操作

```ahk
xl := ComObject("Excel.Application")
xl.Visible := true
wb := xl.Workbooks.Add()
wb.Sheets(1).Range("A1").Value := "Hello from AHK!"
```

### Internet Explorerの操作

```ahk
ie := ComObject("InternetExplorer.Application")
ie.Visible := true
ie.Navigate("https://www.google.com")
```

## HTTP リクエスト

### Webページの内容を取得

```ahk
whr := ComObject("WinHttp.WinHttpRequest.5.1")
whr.Open("GET", "https://api.example.com/data", true)
whr.Send()
whr.WaitForResponse()
MsgBox whr.ResponseText
```

## GUI の表示

### カスタム入力ダイアログ

```ahk
myGui := Gui()
myGui.Add("Text", , "名前を入力してください:")
edit := myGui.Add("Edit", "w200")
myGui.Add("Button", "Default", "OK").OnEvent("Click", (*) => myGui.Submit())
myGui.Show()
```

## タイマーとスケジュール

### 一定時間後に実行

```ahk
SetTimer () => MsgBox("5秒経過しました"), -5000  ; 5秒後に1回だけ
```

### 定期的に実行

```ahk
SetTimer () => ToolTip(A_Now), 1000  ; 1秒ごとに時刻を表示
```

## エラーハンドリング

### Try-Catch

```ahk
try {
    Run "存在しないファイル.exe"
} catch as err {
    MsgBox "エラー: " err.Message
}
```

### より詳細なエラー情報

```ahk
try {
    ; 危険な操作
    RegDelete "HKEY_CURRENT_USER\Software\Test"
} catch as err {
    MsgBox "エラーが発生しました`n"
         . "メッセージ: " err.Message "`n"
         . "What: " err.What "`n"
         . "Extra: " err.Extra
}
```

## マルチスレッド処理

### 並行処理

```ahk
; スレッド1: 画像処理
SetTimer ImageProcess, 100

; スレッド2: ログ記録
SetTimer LogData, 1000

ImageProcess() {
    ; 重い処理
}

LogData() {
    ; ログ記録
}
```

## デバッグテクニック

### ToolTipでのデバッグ

```ahk
ToolTip "変数の値: " myVar
Sleep 2000
ToolTip  ; 消す
```

### ログファイル出力

```ahk
FileAppend "Debug: " A_Now " - 処理開始`n", "debug.log"
; 処理
FileAppend "Debug: " A_Now " - 処理完了`n", "debug.log"
```

### MsgBoxでの確認

```ahk
MsgBox "この位置まで到達しました"
```

## パフォーマンス最適化

### 無駄な処理を避ける

```ahk
; Bad
Loop 1000 {
    if WinExist("ahk_exe notepad.exe")
        count++
}

; Good
if WinExist("ahk_exe notepad.exe")
    count := 1000
```

### キャッシュの活用

```ahk
static cachedValue := ""
if !cachedValue
    cachedValue := ExpensiveFunction()
return cachedValue
```

## セキュリティ

### 入力検証

```ahk
userInput := InputBox("ファイル名を入力してください").Value
; 危険な文字を除去
userInput := RegExReplace(userInput, "[<>:\"/\\|?*]", "")
Run "notepad.exe " userInput ".txt"
```

## 実践例

### プロジェクトランチャー

```ahk
projects := Map(
    "Web", "C:\Projects\WebApp",
    "Desktop", "C:\Projects\DesktopApp",
    "Mobile", "C:\Projects\MobileApp"
)

myGui := Gui()
for name, path in projects {
    myGui.Add("Button", "w200", name).OnEvent("Click", (*) => Run(path))
}
myGui.Show()
```

### スクリーンショット→保存

```ahk
; スクリーンショットを撮って保存
Send "#{PrintScreen}"
Sleep 500
path := A_MyDocuments "\Screenshots\" A_Now ".png"
; スクリーンショットは Pictures\Screenshots に自動保存される
MsgBox "スクリーンショットを撮りました"
```

### Webページの特定要素を開く

```ahk
; Google検索
query := InputBox("検索キーワードを入力してください").Value
if query
    Run "https://www.google.com/search?q=" UrlEncode(query)

UrlEncode(str) {
    ; URLエンコード処理（簡易版）
    return StrReplace(str, " ", "+")
}
```

## 次のステップ

- [複数メニューの管理](multiple-menus.md)
- [トラブルシューティング](troubleshooting.md)

## 参考リソース

- [AutoHotkey v2 公式ドキュメント](https://www.autohotkey.com/docs/v2/)
- [AutoHotkey v2 チュートリアル](https://www.autohotkey.com/docs/v2/Tutorial.htm)
- [AutoHotkey v2 コマンドリファレンス](https://www.autohotkey.com/docs/v2/lib/)
