# インストール

このページでは、Radify Menu Editorのインストール方法を説明します。

## 必要な環境

### システム要件

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8以上
- **AutoHotkey**: v2.0以上（生成されたスクリプトの実行用）

!!! note "Pythonのバージョンについて"
    Python 3.8以上が必要です。`python --version`コマンドで確認できます。

## インストール手順

### 1. Pythonのインストール

Pythonがインストールされていない場合は、[公式サイト](https://www.python.org/downloads/)からダウンロードしてインストールしてください。

!!! warning "重要"
    インストール時に「Add Python to PATH」にチェックを入れてください。

### 2. AutoHotkey v2のインストール

AutoHotkey v2は[公式サイト](https://www.autohotkey.com/)からダウンロードできます。

!!! info "AutoHotkey v1との違い"
    このエディタはAutoHotkey **v2専用**です。v1では動作しません。

### 3. プロジェクトのダウンロード

GitHubリポジトリからプロジェクトをクローンまたはダウンロードします。

#### Gitを使う場合

```bash
git clone https://github.com/hinatahugu29/AHK_Radify_Editor.git
cd AHK_Radify_Editor
```

#### ZIPでダウンロードする場合

1. [GitHubリポジトリ](https://github.com/hinatahugu29/AHK_Radify_Editor)にアクセス
2. 「Code」→「Download ZIP」をクリック
3. ダウンロードしたZIPファイルを解凍

### 4. Pythonパッケージのインストール

プロジェクトフォルダで以下のコマンドを実行します。

```bash
pip install -r requirements.txt
```

インストールされるパッケージ:

- **CustomTkinter**: モダンなGUIフレームワーク
- **Pillow**: 画像処理ライブラリ

## 起動方法

インストールが完了したら、以下のコマンドでエディタを起動できます。

```bash
python main.py
```

!!! success "起動成功"
    ウィンドウが表示されたらインストール成功です！

## トラブルシューティング

### Pythonが認識されない

`python`コマンドが認識されない場合は、以下を試してください:

1. `python3`コマンドを試す
2. Pythonを環境変数PATHに追加する
3. Pythonを再インストールする（「Add to PATH」にチェック）

### パッケージのインストールエラー

管理者権限で実行してみてください:

```bash
pip install --user -r requirements.txt
```

### モジュールが見つからないエラー

必要なファイルが揃っているか確認してください:

- `main.py`
- `modules/`フォルダ
- `requirements.txt`

## 次のステップ

インストールが完了したら、[クイックスタートガイド](quickstart.md)で最初のメニューを作成してみましょう！
