import unicodedata
from typing import Dict

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.tools import Tool
from langchain.agents import AgentType, initialize_agent
from langchain.schema import HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from config.settings import THEMES


class AIAgent:
    def __init__(self, theme_retriever: Dict, chat_history: list):
        if not theme_retriever:
            raise ValueError("theme_retrieverが空です。RAGシステムの初期化を確認してください。")
        
        self.theme_retriever = theme_retriever
        self.chat_history = chat_history
        
        try:
            self.llm = ChatOpenAI(
                model_name="gpt-4",
                temperature=0.0,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
            
            self.tools = self._create_tools()
            if not self.tools:
                raise ValueError("AIエージェント用のツールが作成されませんでした。")
            
            self.agent_executor = self._create_agent()
            
        except Exception as e:
            raise RuntimeError(f"AIエージェントの初期化に失敗しました: {str(e)}")
    
    def _create_rag_chain(self, retriever, llm):
        """テーマ別RAGチェーンを作成"""
        qgen_text = "会話履歴と最新の入力をもとに、履歴の内容を反映した独立した質問を日本語で生成してください。"
        qgen_prompt = ChatPromptTemplate.from_messages([
            ("system", qgen_text),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        history_aware_retriever = create_history_aware_retriever(
            llm=llm,
            retriever=retriever,
            prompt=qgen_prompt
        )
        
        qa_system = """あなたは優秀な質問応答アシスタント。{context}のみを根拠として、日本語で質問に回答する。
        わからない時はちゃんとわからないという。"""
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        qa_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)
        return create_retrieval_chain(history_aware_retriever, qa_chain)
    
    def _make_tool(self, theme_name: str):
        """テーマ別ツールを作成"""
        chain = self._create_rag_chain(self.theme_retriever[theme_name], self.llm)
        
        def _run(q: str):
            res = chain.invoke({"input": q, "chat_history": self.chat_history})
            answer = res.get("answer", "")
            self.chat_history.extend([
                HumanMessage(content=q),
                AIMessage(content=answer)
            ])
            return answer
        
        return Tool(
            name=f"{theme_name}RAG",
            func=_run,
            description=f"""{theme_name}に関する質問に日本語で回答してください。
            {theme_name}テーマのベクターストアのみを参照しなさい。"""
        )
    
    def _create_tools(self):
        """全テーマのツールを作成"""
        tools = []
        
        # 正規化のヘルパー関数
        def normalize(s: str) -> str:
            return unicodedata.normalize("NFKC", s)
        
        # 正規化キー -> 実キーのマッピング
        norm2real = {normalize(k): k for k in self.theme_retriever.keys()}
        
        for theme in THEMES:
            normalized_theme = normalize(theme)
            if normalized_theme in norm2real:
                real_theme = norm2real[normalized_theme]
                tool = self._make_tool(real_theme)
                tools.append(tool)
        
        return tools
    
    def _create_agent(self):
        """エージェントを作成"""
        return initialize_agent(
            llm=self.llm,
            tools=self.tools,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    def run(self, query: str) -> str:
        """クエリを実行"""
        return self.agent_executor.run(query)
