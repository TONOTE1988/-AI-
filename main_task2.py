#!/usr/bin/env python3
"""
RAGエージェントシステム - 中間課題②用のメイン実行ファイル

このスクリプトはRAGシステムにAIエージェント機能を搭載したバージョンを実行します。
"""

import os
from pathlib import Path
from config.settings import MEETING_NOTES_DIR, OPENAI_API_KEY
from src.rag.rag_system import RAGSystem
from src.agent.ai_agent import AIAgent


def main():
    """メイン関数 - AIエージェント搭載RAGシステムを実行"""
    
    # OpenAI APIキーのチェック
    if not OPENAI_API_KEY:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        print("環境変数またはconfig/settings.pyで設定してください。")
        return
    
    print("=" * 60)
    print("RAGエージェントシステム - 中間課題②")
    print("AIエージェント機能搭載版")
    print("=" * 60)
    
    # データディレクトリの確認
    if not MEETING_NOTES_DIR.exists():
        print(f"警告: データディレクトリが見つかりません: {MEETING_NOTES_DIR}")
        print("まず main_task1.py を実行してデータ構造を作成してください。")
        return
    
    # RAGシステムの初期化
    print("RAGシステムを初期化しています...")
    rag_system = RAGSystem(MEETING_NOTES_DIR)
    theme_retriever = rag_system.initialize()
    
    if not theme_retriever:
        print("エラー: テーマ別リトリーバーが作成されませんでした。")
        print("議事録ファイルが正しく配置されているか確認してください。")
        return
    
    # AIエージェントの初期化
    print("\nAIエージェントを初期化しています...")
    ai_agent = AIAgent(theme_retriever, rag_system.chat_history)
    
    print("\n" + "=" * 60)
    print("AIエージェント搭載RAGシステムのテスト開始")
    print("=" * 60)
    
    # テストクエリの実行
    test_queries = [
        "自社メンバーの育成に関する具体的なアクションプランを教えて",
        "教育の観点って言ってるけどもうちょい詳しく説明できる？",
        "前回の質問に対する回答の最後の部分がよくわからない。平易な言葉に言い換えて"
    ]
    
    for query in test_queries:
        print(f"\n質問: {query}")
        print("-" * 50)
        try:
            response = ai_agent.run(query)
            print(f"回答: {response}")
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        print()


if __name__ == "__main__":
    main()
