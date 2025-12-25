import os
import unicodedata
from pathlib import Path
from typing import Dict, List

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from config.settings import *
from src.utils.file_manager import FileManager


class RAGSystem:
    def __init__(self, meeting_notes_dir: Path):
        self.meeting_notes_dir = Path(meeting_notes_dir)
        self.file_manager = FileManager(meeting_notes_dir)
        
        # LangChainコンポーネントを初期化
        self.text_splitter = CharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.0,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        self.theme_retriever = {}
        self.all_retriever = None
        self.rag_chain = None
        self.chat_history = []
    
    def reset_data(self):
        """データベース化済みフォルダと.dbフォルダを初期化"""
        self.file_manager.clear_complete_dir(self.meeting_notes_dir)
    
    def load_and_process_files(self) -> Dict[str, List]:
        """ファイルを読み込み、処理する"""
        theme_docs = {}
        self.file_manager.recursive_file_check(self.meeting_notes_dir, theme_docs)
        return theme_docs
    
    def get_theme_list(self) -> List[str]:
        """利用可能なテーマの一覧を取得"""
        if not self.meeting_notes_dir.exists():
            return []
        
        theme_list = []
        for item in self.meeting_notes_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                theme_list.append(item.name)
        return theme_list
    
    def create_vector_stores(self, theme_docs: Dict[str, List]):
        """ベクターストアを作成または更新"""
        theme_list = self.get_theme_list()
        all_combined_docs = []
        
        # 各テーマごとのベクターストアを作成（メモリ内で動作）
        for theme_name in theme_list:
            if theme_name in theme_docs:
                splitted_docs = self.text_splitter.split_documents(theme_docs[theme_name])
                
                # メモリ内ベクターストアを使用（永続化を避ける）
                try:
                    db = Chroma.from_documents(
                        splitted_docs,
                        self.embeddings,
                        # persist_directory を指定せずメモリ内で動作
                    )
                    print(f"✅ {theme_name}テーマのベクターストア作成完了")
                except Exception as e:
                    print(f"❌ {theme_name}テーマでエラー: {e}")
                    continue
                
                self.theme_retriever[theme_name] = db.as_retriever()
                all_combined_docs.extend(splitted_docs)
        
        # 全テーマ横断のベクターストアを処理（メモリ内）
        if all_combined_docs:
            try:
                all_db = Chroma.from_documents(
                    all_combined_docs,
                    self.embeddings
                    # persist_directory を指定せずメモリ内で動作
                )
                print("✅ 全テーマ横断ベクターストア作成完了")
            except Exception as e:
                print(f"❌ 全テーマ横断ベクターストアでエラー: {e}")
                # 空のリトリーバーを作成
                self.all_retriever = None
                return self.theme_retriever
            
            self.all_retriever = all_db.as_retriever(search_kwargs={"k": SEARCH_K})
    
    def setup_rag_chain(self):
        """RAGチェーンを設定"""
        if not self.all_retriever:
            raise ValueError("全テーマ横断のretrieverが設定されていません")
        
        # 履歴を考慮したクエリ生成
        question_generator = "会話履歴と最新の入力をもとに、会話履歴なしでも理解できる独立した入力テキストを生成してください。"
        question_generator_prompt = ChatPromptTemplate.from_messages([
            ("system", question_generator),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        all_history_retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self.all_retriever,
            prompt=question_generator_prompt
        )
        
        # 質問応答のプロンプト
        question_answer_template = """
        あなたは優秀な質問応答アシスタントです。以下のcontextを使用して質問に答えてください。
        また答えが分からない場合は、無理に答えようとせず「分からない」という旨を答えてください。
        {context}
        
        # 出力要件
        - ユーザーが「◯文字以内／◯字以内」と指定した場合は **厳密に** その文字数以下で出力する。
        - 文字数制約がある場合は **一文** で、箇条書き禁止・重複表現禁止・同義反復禁止。
        - 日本語で回答する。
        """
        
        question_answer_prompt = ChatPromptTemplate.from_messages([
            ("system", question_answer_template),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=question_answer_prompt
        )
        
        self.rag_chain = create_retrieval_chain(
            all_history_retriever,
            question_answer_chain
        )
    
    def query(self, user_input: str) -> str:
        """ユーザークエリに対して回答を生成"""
        if not self.rag_chain:
            raise ValueError("RAGチェーンが設定されていません")
        
        response = self.rag_chain.invoke({
            "input": user_input,
            "chat_history": self.chat_history
        })
        
        # 会話履歴を更新
        self.chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=response["answer"])
        ])
        
        return response["answer"]
    
    def initialize(self):
        """RAGシステムを初期化"""
        print("RAGシステムを初期化しています...")
        
        # リセット処理
        self.reset_data()
        
        # ファイルの読み込みと処理
        theme_docs = self.load_and_process_files()
        print(f"読み込んだテーマ: {list(theme_docs.keys())}")
        
        # ベクターストアの作成
        self.create_vector_stores(theme_docs)
        print(f"作成したリトリーバー: {list(self.theme_retriever.keys())}")
        
        # RAGチェーンの設定
        self.setup_rag_chain()
        print("RAGシステムの初期化が完了しました。")
        
        return self.theme_retriever
