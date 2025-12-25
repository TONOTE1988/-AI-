# RAGエージェントシステム

DMM AICAMP中間課題で開発したRAGエージェントシステムをVS Code環境用に再構築したプロジェクトです。

**🔥 特徴:**
- 📝 **議事録を自動でRAG化** - Wordファイルをドラッグ&ドロップするだけ
- 🤖 **AIエージェント機能** - テーマ別に最適な回答を自動選択
- 💬 **WebUI搭載** - ブラウザで簡単操作
- 🎯 **会話履歴対応** - 文脈を理解した自然な対話

## 📱 デモ画面

### 💡 主要機能の紹介

**🎯 メイン画面**
- RAGモード/AIエージェントモードの選択
- デモモード切り替え（APIキー不要）
- リアルタイムシステム状態表示

**💬 チャット画面**  
- ストリーミング応答でリアルタイム表示
- 会話履歴の自動保存
- テーマ別検索結果のハイライト

**⚡ システム初期化**
- 議事録ファイルの自動読み込み
- ベクターストア作成の進捗表示
- エラーハンドリングと詳細ログ

> **📌 実際の画面を確認するには**: `streamlit run demo.py` でデモモードを起動してください

## プロジェクト構造

```
├── config/
│   ├── __init__.py
│   └── settings.py           # 設定ファイル
├── src/
│   ├── __init__.py
│   ├── rag/
│   │   ├── __init__.py
│   │   └── rag_system.py     # RAGシステムのメインロジック
│   ├── agent/
│   │   ├── __init__.py
│   │   └── ai_agent.py       # AIエージェント機能
│   └── utils/
│       ├── __init__.py
│       └── file_manager.py   # ファイル操作ユーティリティ
├── data/                     # データディレクトリ（自動作成）
├── venv/                     # 仮想環境
├── requirements.txt          # 依存パッケージ
├── main_task1.py            # 中間課題①実行ファイル
├── main_task2.py            # 中間課題②実行ファイル
└── README.md
```

## 🎬 クイック体験（APIキー不要）

**📺 今すぐ画面を確認したい方:**

```bash
git clone https://github.com/TONOTE1988/-AI-.git
cd -AI-
pip install streamlit
streamlit run demo.py
```

**🌐 ブラウザで確認**: `http://localhost:8501`

または、メインアプリ（`streamlit run app.py`）で「🎬 デモモード」をチェックしてください。

---

## セットアップ

### 🚀 簡単セットアップ（推奨）

**macOS/Linux:**
```bash
git clone <このリポジトリのURL>
cd DMM-AICAMP中間課題（RAGエージェントシステム0
./setup.sh
```

**Windows:**
```cmd
git clone <このリポジトリのURL>
cd DMM-AICAMP中間課題（RAGエージェントシステム0
setup.bat
```

### 📋 手動セットアップ

#### 1. リポジトリのクローン

```bash
git clone <このリポジトリのURL>
cd DMM-AICAMP中間課題（RAGエージェントシステム0
```

### 2. Python仮想環境の作成とアクティベート

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定

**重要**: OpenAI APIキーを設定してください。

1. `.env.example`ファイルを`.env`にコピー：
```bash
cp .env.example .env
```

2. `.env`ファイルを編集してAPIキーを設定：
```bash
# .env ファイル内
OPENAI_API_KEY=your-actual-openai-api-key-here
```

### 5. データの準備

初回実行時に、プログラムが自動的にデータディレクトリ構造を作成します：

```
data/オンラインMTG議事録/
├── 営業/
│   ├── データベース化前/     # ここに.docxファイルを配置
│   └── データベース化済み/   # 処理済みファイルが保存される
├── マーケティング/
├── 採用/
├── 開発/
├── 教育/
├── 全社/
├── 顧客/
└── .db/                     # ベクターストアが保存される
```

各テーマの「データベース化前」フォルダに議事録ファイル（.docx形式）を配置してください。

## 使い方

### WebUI版（推奨）- Streamlitアプリの起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` にアクセスして、以下の機能を利用できます：

- **RAG（中間課題①）モード**: 基本的なRAGシステム
- **AIエージェント（中間課題②）モード**: 高度なエージェント機能
- **リアルタイムチャット**: ストリーミング応答対応
- **テーマ選択**: 複数のテーマから選択可能

### コマンドライン版

#### 中間課題① - RAGシステムの実行

```bash
python main_task1.py
```

#### 中間課題② - AIエージェント機能搭載版の実行

```bash
python main_task2.py
```

## 主な機能

### RAGSystem クラス
- ファイルの自動読み込み
- ベクターストアの作成・更新
- 会話履歴を考慮した回答生成
- 文字数制限への対応

### AIAgent クラス
- テーマ別ツールの自動作成
- エージェントによる適切なツール選択
- 複数ターンの会話対応

### FileManager クラス
- 再帰的ファイル検索
- 自動的な重複処理防止
- エラーハンドリング

## 設定のカスタマイズ

`config/settings.py`で以下の設定を変更できます：

- `MEETING_NOTES_DIR`: データディレクトリのパス
- `CHUNK_SIZE`: テキスト分割のサイズ
- `CHUNK_OVERLAP`: チャンクのオーバーラップ
- `SEARCH_K`: 検索で取得するドキュメント数
- `THEMES`: 対応テーマの一覧

## トラブルシューティング

### よくある問題

1. **APIキーが設定されていない**
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **データディレクトリが見つからない**
   - `main_task1.py`を実行してディレクトリ構造を作成
   - 議事録ファイルを正しいフォルダに配置

3. **パッケージが見つからない**
   ```bash
   pip install -r requirements.txt
   ```

4. **仮想環境がアクティブでない**
   ```bash
   source venv/bin/activate
   ```

## 注意事項

- 元のGoogle Colabコードの機能は変更していませんが、ファイル構造を整理しました
- データディレクトリのパスは実際の環境に合わせて調整してください
- 大量のファイル処理時はメモリ使用量にご注意ください

## 開発者向け

各モジュールは独立しているため、必要に応じて個別にカスタマイズできます：

- RAGシステムのロジック: `src/rag/rag_system.py`
- AIエージェントの動作: `src/agent/ai_agent.py`
- ファイル操作: `src/utils/file_manager.py`
- 設定: `config/settings.py`
