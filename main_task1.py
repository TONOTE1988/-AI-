#!/usr/bin/env python3
"""
RAGエージェントシステム - 中間課題①用のメイン実行ファイル

このスクリプトはオンラインMTG議事録を外部参照するRAGシステムを実行します。
"""

import os
from pathlib import Path
from config.settings import MEETING_NOTES_DIR, OPENAI_API_KEY
from src.rag.rag_system import RAGSystem


def main():
    """メイン関数 - RAGシステムを実行"""
    
    # OpenAI APIキーのチェック
    if not OPENAI_API_KEY:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print("環境変数またはconfig/settings.pyで設定してください。")
        return
    
    print("=" * 60)
    print("RAGエージェントシステム - 中間課題①")
    print("=" * 60)
    
    # データディレクトリの確認
    if not MEETING_NOTES_DIR.exists():
        print(f"警告: データディレクトリが見つかりません: {MEETING_NOTES_DIR}")
        print("config/settings.pyのMEETING_NOTES_DIRパスを確認してください。")
        
        # サンプルデータディレクトリ構造を作成
        create_sample_data_structure()
    
    # RAGシステムの初期化
    rag_system = RAGSystem(MEETING_NOTES_DIR)
    theme_retriever = rag_system.initialize()
    
    print("\n" + "=" * 60)
    print("RAGシステムのテスト開始")
    print("=" * 60)
    
    # テストクエリの実行
    test_queries = [
        "多くの企業が力を入れているマーケティング施策は何ですか？",
        "もうちょい詳しく。",
        "100文字以内に要約して"
    ]
    
    for query in test_queries:
        print(f"\n質問: {query}")
        print("-" * 50)
        try:
            response = rag_system.query(query)
            print(f"回答: {response}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        print()


def create_sample_data_structure():
    """サンプルのデータディレクトリ構造を作成"""
    print("\nサンプルデータディレクトリ構造を作成しています...")
    
    # 基本ディレクトリの作成
    MEETING_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    
    # テーマディレクトリとサブディレクトリの作成
    themes = ["営業", "マーケティング", "採用", "開発", "教育", "全社", "顧客"]
    
    for theme in themes:
        theme_dir = MEETING_NOTES_DIR / theme
        theme_dir.mkdir(exist_ok=True)
        
        # サブディレクトリの作成
        (theme_dir / "データベース化前").mkdir(exist_ok=True)
        (theme_dir / "データベース化済み").mkdir(exist_ok=True)
    
    # .dbディレクトリの作成
    (MEETING_NOTES_DIR / ".db").mkdir(exist_ok=True)
    
    print(f"サンプルデータディレクトリ構造を作成しました: {MEETING_NOTES_DIR}")
    print("\n次の手順:")
    print("1. 議事録ファイル(.docx)を各テーマの「データベース化前」フォルダに配置してください")
    print("2. 再度このスクリプトを実行してください")


if __name__ == "__main__":
    main()
