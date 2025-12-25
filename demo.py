import streamlit as st
import json
from datetime import datetime

def demo_mode():
    """APIキー不要のデモモード"""
    st.title("🎬 RAGエージェントシステム - デモモード")
    
    st.info("📌 これはAPIキー不要のデモ版です。実際の機能を体験するにはOpenAI APIキーが必要です。")
    
    # サンプル議事録データ
    sample_meetings = {
        "開発": ["新機能の要件定義について討議", "UI/UXの改善案を検討"],
        "教育": ["研修プログラムの見直し", "スキルアップ計画の策定"],
        "全社": ["四半期業績レビュー", "来期戦略の方向性確認"]
    }
    
    # デモチャット履歴
    demo_chat = [
        {"role": "user", "content": "新機能について教えて"},
        {"role": "assistant", "content": "開発チームの議事録によると、新機能の要件定義では以下の点が重要視されています：\n\n1. ユーザビリティの向上\n2. パフォーマンスの最適化\n3. セキュリティ強化\n\n特にUI/UXの改善については、ユーザーフィードバックを基に具体的な改善案が検討されています。"},
        {"role": "user", "content": "研修について聞きたい"},
        {"role": "assistant", "content": "教育チームの議事録から、研修プログラムの見直しが進行中です：\n\n📚 主な改善点：\n- 実践的なスキルトレーニングの強化\n- オンライン学習コンテンツの充実\n- 個人の成長に合わせたカスタマイズ\n\nスキルアップ計画では、各メンバーの専門性向上を目指したロードマップが策定されています。"}
    ]
    
    # サイドバーでテーマ選択
    with st.sidebar:
        st.subheader("📂 利用可能テーマ")
        selected_theme = st.selectbox(
            "テーマを選択",
            list(sample_meetings.keys())
        )
        
        st.subheader("📋 議事録サンプル")
        for topic in sample_meetings[selected_theme]:
            st.write(f"• {topic}")
    
    # メインチャット画面
    st.subheader("💬 デモチャット")
    
    # 過去のチャット履歴を表示
    for chat in demo_chat:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])
    
    # ユーザー入力（デモ用）
    if prompt := st.chat_input("質問を入力してください（デモモード）"):
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            st.write("🎭 **デモモード**: 実際のRAGシステムでは、あなたの議事録ファイルから関連情報を検索して、より具体的で正確な回答を提供します。\n\n実機能を使用するには：\n1. OpenAI APIキーを設定\n2. 議事録ファイル(.docx)をアップロード\n3. システム初期化を実行")
    
    # 実機能への案内
    st.markdown("---")
    st.markdown("""
    ### 🚀 実際の機能を使用するには
    
    1. **APIキー設定**: `.env`ファイルにOpenAI APIキーを設定
    2. **ファイル配置**: `meeting_notes`フォルダに議事録(.docx)を配置  
    3. **初期化**: 「システム初期化」ボタンでRAGシステムを構築
    4. **AI対話**: 実際の議事録内容に基づいた高精度な回答を取得
    
    **リアルタイム機能:**
    - 📝 自動ベクトル化
    - 🔍 セマンティック検索
    - 🤖 文脈理解型AI応答
    - 📊 複数テーマ横断検索
    """)

if __name__ == "__main__":
    demo_mode()
