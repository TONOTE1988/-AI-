@echo off
echo 🚀 RAGエージェントシステムのセットアップを開始します...

REM Python仮想環境の作成
echo 📦 Python仮想環境を作成しています...
python -m venv venv

REM 仮想環境のアクティベート
echo 🔧 仮想環境をアクティベートしています...
call venv\Scripts\activate

REM 依存パッケージのインストール
echo 📚 依存パッケージをインストールしています...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM .envファイルの作成
if not exist .env (
    echo ⚙️ .envファイルを作成しています...
    copy .env.example .env
    echo ✅ .envファイルが作成されました
    echo ⚠️  重要: .envファイルを編集してOpenAI APIキーを設定してください
    echo    OPENAI_API_KEY=your-actual-api-key-here
) else (
    echo ℹ️  .envファイルは既に存在します
)

REM データディレクトリの作成
echo 📁 データディレクトリを作成しています...
python -c "from pathlib import Path; from config.settings import MEETING_NOTES_DIR, THEMES; MEETING_NOTES_DIR.mkdir(parents=True, exist_ok=True); [((theme_dir := MEETING_NOTES_DIR / theme).mkdir(exist_ok=True), (theme_dir / 'データベース化前').mkdir(exist_ok=True), (theme_dir / 'データベース化済み').mkdir(exist_ok=True)) for theme in THEMES]; print('✅ データディレクトリ構造が作成されました')"

echo.
echo 🎉 セットアップが完了しました！
echo.
echo 次のステップ：
echo 1. .envファイルを編集してAPIキーを設定
echo 2. meeting_notesフォルダに議事録ファイル(.docx)を配置
echo 3. Streamlitアプリを起動: streamlit run app.py
echo.
pause
