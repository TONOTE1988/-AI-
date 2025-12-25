import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# プロジェクトのルートディレクトリ
ROOT_DIR = Path(__file__).parent.parent.absolute()

# データディレクトリ
DATA_DIR = ROOT_DIR / "data"

# 会議議事録のディレクトリ（環境変数で上書き可能）
MEETING_NOTES_DIR = Path(os.getenv("MEETING_NOTES_DIR", DATA_DIR / "オンラインMTG議事録"))

# OpenAI API設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# チャンク分割設定
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# 埋め込み検索設定
SEARCH_K = 2

# 対応テーマ
THEMES = ["営業", "マーケティング", "採用", "開発", "教育", "全社", "顧客"]
