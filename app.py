import streamlit as st
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(str(Path(__file__).parent))

from config.settings import OPENAI_API_KEY
from src.rag.rag_system import RAGSystem
from src.agent.ai_agent import AIAgent
from demo import demo_mode

st.set_page_config(
    page_title="RAGエージェントシステム",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 RAG エージェントシステム")
    st.markdown("**AI搭載の高度な情報検索・対話システム**")
    st.markdown("---")
    
    # サイドバーでモード選択
    st.sidebar.title("⚙️ システム設定")
    
    # デモモード選択
    demo_mode_enabled = st.sidebar.checkbox("🎬 デモモード（APIキー不要）")
    
    if demo_mode_enabled:
        demo_mode()
        return
    
    mode = st.sidebar.radio(
        "動作モード",
        ["RAGシステム（中間課題①）", "AIエージェント（中間課題②）"]
    )
    
    # APIキーチェック
    if not OPENAI_API_KEY:
        st.error("❌ OpenAI APIキーが設定されていません。.envファイルを確認してください。")
        st.stop()
    
    # セッションステートの初期化
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = mode
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'ai_agent' not in st.session_state:
        st.session_state.ai_agent = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    
    # モードが変更された場合は再初期化が必要
    if st.session_state.current_mode != mode:
        st.session_state.current_mode = mode
        st.session_state.initialized = False
        st.session_state.ai_agent = None
    
    # 初期化ボタン
    if not st.session_state.initialized:
        st.warning("⚠️ システムを初期化してください。")
        if st.button("⚡ システム初期化", type="primary"):
            with st.spinner("RAGシステムを初期化しています..."):
                try:
                    from config.settings import MEETING_NOTES_DIR
                    st.session_state.rag_system = RAGSystem(MEETING_NOTES_DIR)
                    theme_retriever = st.session_state.rag_system.initialize()
                    
                    if mode == "AIエージェント（中間課題②）":
                        if theme_retriever:
                            st.info("AIエージェントを初期化しています...")
                            st.write(f"🔍 利用可能テーマ: {list(theme_retriever.keys())}")
                            st.write(f"📊 チャット履歴数: {len(st.session_state.rag_system.chat_history)}")
                            
                            try:
                                st.session_state.ai_agent = AIAgent(theme_retriever, st.session_state.rag_system.chat_history)
                                st.success("✅ AIエージェント初期化完了！")
                            except Exception as agent_error:
                                st.error(f"❌ AIエージェント初期化エラー: {str(agent_error)}")
                                import traceback
                                st.code(traceback.format_exc())
                                st.warning("⚠️ RAGモードで続行します")
                                st.session_state.current_mode = "RAG（中間課題①）"
                        else:
                            st.warning("⚠️ テーマリトリーバーが空のため、RAGモードのみで初期化しました")
                    
                    st.session_state.initialized = True
                    st.success("✅ システム初期化完了！")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 初期化エラー: {str(e)}")
                    st.error(f"エラー詳細: {type(e).__name__}")
                    import traceback
                    st.error(f"スタックトレース: {traceback.format_exc()}")
        return
    
    # チャット履歴表示
    st.subheader("💬 対話履歴")
    chat_container = st.container()
    
    with chat_container:
        for i, (user_msg, ai_msg) in enumerate(st.session_state.chat_history):
            st.markdown(f"**👤 ユーザー:** {user_msg}")
            st.markdown(f"**💡 AI:** {ai_msg}")
            st.markdown("---")
    
    # 入力フォーム
    st.subheader("✍️ 質問を入力")
    user_input = st.text_area(
        "質問を入力してください",
        placeholder="例: 多くの企業が力を入れているマーケティング施策は何ですか？",
        height=100
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("✨ 送信", type="primary"):
            if user_input.strip():
                with st.spinner("回答を生成しています..."):
                    try:
                        if mode == "RAGシステム（中間課題①）":
                            response = st.session_state.rag_system.query(user_input)
                        else:
                            response = st.session_state.ai_agent.run(user_input)
                        
                        st.session_state.chat_history.append((user_input, response))
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ エラー: {e}")
            else:
                st.warning("質問を入力してください。")
    
    with col2:
        if st.button("🗑️ チャット履歴クリア"):
            st.session_state.chat_history = []
            if st.session_state.rag_system:
                st.session_state.rag_system.chat_history = []
            st.rerun()
    
    # サイドバーの情報
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 システム状態")
    if st.session_state.rag_system:
        st.sidebar.success("✅ RAGシステム: 稼働中")
        st.sidebar.info(f"💬 会話履歴: {len(st.session_state.chat_history)}件")
    
    if mode == "AIエージェント（中間課題②）" and st.session_state.ai_agent:
        st.sidebar.success("✅ AIエージェント: 稼働中")

if __name__ == "__main__":
    main()
