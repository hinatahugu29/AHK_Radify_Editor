# Radify Menu Editor

[![Documentation Status](https://readthedocs.org/projects/ahk-radify-editor/badge/?version=latest)](https://ahk-radify-editor.readthedocs.io/ja/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![AutoHotkey Version](https://img.shields.io/badge/AutoHotkey-v2-green.svg)](https://www.autohotkey.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> AutoHotkey v2製リングメニューを完全GUI化する統合開発環境

![Radify Menu Editor](images/radify-skin-editor.png)

## 📖 概要

**Radify Menu Editor** は、AutoHotkey v2のリングメニューライブラリ「Radify」を、1行のコードも書かずに、視覚的かつ直感的に構築できる統合開発環境（IDE）です。

### 🌟 主な特徴

- **完全GUI化**: テキストエディタ不要。すべての設定をビジュアルインターフェースで完結
- **リアルタイムプレビュー**: 編集内容が即座にキャンバスに反映（Live Sync）
- **柔軟なアクション定義**: テンプレートからの挿入と、AHKコードの直接記述の両立
- **画面キャプチャ統合**: デスクトップから直接アイコンを切り出して設定可能
- **ドラッグ&ドロップ**: ツリービューでの直感的なメニュー構造編集
- **Undo/Redo**: Ctrl+Z/Ctrl+Yによる編集履歴管理
- **自動バックアップ**: 保存時に自動的にバックアップを作成
- **ポータブル出力**: 作成したメニューを単体パッケージとして出力可能

## 🚀 クイックスタート

### 必要な環境

- **OS**: Windows 10/11
- **Python**: 3.8以上
- **AutoHotkey**: v2.0以上（生成されたスクリプトの実行用）

### インストール

1. リポジトリをクローン
```bash
git clone https://github.com/hinatahugu29/AHK_Radify_Editor.git
cd AHK_Radify_Editor
```

2. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

3. エディタを起動
```bash
python main.py
```

## 📚 ドキュメント

詳細なドキュメントは [Read the Docs](https://ahk-radify-editor.readthedocs.io/) で公開しています。

- [使い方ガイド (HOWTO)](HOWTO.html)
- [技術仕様 (TECH_SPEC)](TECH_SPEC.html)
- [紹介記事](Radify_Editor_Introduction.md)

## 💡 使い方

### 基本的なワークフロー

1. **新規リングを追加**: 左パネルの「新規リング追加」ボタン
2. **アイテムを追加**: リングを選択後、「新規アイテム追加」ボタン
3. **プロパティ編集**: 右パネルでアイコン、ラベル、アクションを設定
4. **プレビュー確認**: 中央のキャンバスでリアルタイム確認
5. **AHKスクリプト出力**: メニュー→「AHKスクリプト出力」

### スクリーンショット

*(実際の使用例のスクリーンショットを後ほど追加することをお勧めします)*

## 🛠️ プロジェクト構造

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
├── images/                 # アイコンリソース
├── menu_config.json        # サンプルメニュー設定
├── templates.json          # アクションテンプレート
├── HOWTO.html             # 使い方ガイド
├── TECH_SPEC.html         # 技術仕様
└── requirements.txt        # Python依存関係
```

## 🔧 技術スタック

- **GUI Framework**: CustomTkinter (モダンなダークテーマ対応Tkinter)
- **画像処理**: Pillow (PIL)
- **設定管理**: JSON
- **ターゲット言語**: AutoHotkey v2

## 🤝 コントリビューション

プルリクエストは大歓迎です！バグ報告や機能提案は [Issues](https://github.com/hinatahugu29/AHK_Radify_Editor/issues) にお願いします。

## 📝 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🙏 謝辞

- [AutoHotkey](https://www.autohotkey.com/) - 素晴らしいスクリプト言語
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - モダンなGUIライブラリ
- Radifyライブラリの開発者の皆様

## 🔗 関連リンク

- [AutoHotkey v2 ドキュメント](https://www.autohotkey.com/docs/v2/)
- [ディスカッション・質問](https://github.com/hinatahugu29/AHK_Radify_Editor/discussions)

---

Made with ❤️ for the AutoHotkey community
