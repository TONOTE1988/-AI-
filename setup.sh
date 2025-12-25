#!/bin/bash

echo "🚀 RAGエージェントシステムのセットアップを開始します..."

# Python仮想環境の作成
echo "📦 Python仮想環境を作成しています..."
python -m venv venv

# 仮想環境のアクティベート（macOS/Linux）
echo "🔧 仮想環境をアクティベートしています..."
source venv/bin/activate

# 依存パッケージのインストール
echo "📚 依存パッケージをインストールしています..."
pip install --upgrade pip
pip install -r requirements.txt

# .envファイルの作成
if [ ! -f .env ]; then
    echo "⚙️ .envファイルを作成しています..."
    cp .env.example .env
    echo "✅ .envファイルが作成されました"
    echo "⚠️  重要: .envファイルを編集してOpenAI APIキーを設定してください"
    echo "   OPENAI_API_KEY=your-actual-api-key-here"
else
    echo "ℹ️  .envファイルは既に存在します"
fi

# データディレクトリの作成
echo "📁 データディレクトリを作成しています..."
python -c "
from pathlib import Path
from config.settings import MEETING_NOTES_DIR, THEMES

# データディレクトリ作成
MEETING_NOTES_DIR.mkdir(parents=True, exist_ok=True)

# テーマディレクトリ作成
for theme in THEMES:
    theme_dir = MEETING_NOTES_DIR / theme
    theme_dir.mkdir(exist_ok=True)
    
    # サブディレクトリ作成
    (theme_dir / 'データベース化前').mkdir(exist_ok=True)
    (theme_dir / 'データベース化済み').mkdir(exist_ok=True)

print('✅ データディレクトリ構造が作成されました')
"

echo ""
echo "🎉 セットアップが完了しました！"
echo ""
echo "次のステップ："
echo "1. .envファイルを編集してAPIキーを設定"
echo "2. meeting_notesフォルダに議事録ファイル(.docx)を配置"
echo "3. Streamlitアプリを起動: streamlit run app.py"
echo ""
