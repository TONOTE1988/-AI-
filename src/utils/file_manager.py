import os
import shutil
from pathlib import Path
from docx import Document
from langchain_community.document_loaders import Docx2txtLoader

class FileManager:
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
    
    def clear_complete_dir(self, dir_path: Path):
        """データベース化済みフォルダと.dbフォルダ内のファイルを削除する処理"""
        print(f"Checking directory: {dir_path}")
        
        if dir_path.is_dir():
            if dir_path.name == ".db":
                shutil.rmtree(dir_path)
                dir_path.mkdir()
                print("作成済みの全てのベクターストアを削除しました。")
                return
            
            if dir_path.name == "データベース化済み":
                for file in dir_path.iterdir():
                    if file.is_file():
                        file.unlink()
                print(f"対象テーマの「データベース化済み」フォルダを空にしました: {dir_path}")
                return
            
            # 再帰的に処理
            for item in dir_path.iterdir():
                if item.is_dir():
                    self.clear_complete_dir(item)
    
    def recursive_file_check(self, path: Path, theme_docs: dict):
        """階層の深いフォルダ内のファイルを再帰的にチェックして読み込む"""
        if path.is_dir():
            # データベース化済みフォルダや.dbフォルダはスキップ
            if path.name in ["データベース化済み", ".db"]:
                return
            
            # フォルダ内を再帰的に処理
            for item in path.iterdir():
                self.recursive_file_check(item, theme_docs)
        else:
            # ファイルの場合は読み込み処理
            self.file_load(path, theme_docs)
    
    def file_load(self, file_path: Path, theme_docs: dict):
        """ファイルを読み込み、データベース化済みフォルダにコピーする"""
        # パスからテーマ名を取得
        theme_name = self._extract_theme_name(file_path)
        if not theme_name:
            return
        
        # データベース化済みファイルのパスを構築
        save_filepath = self._get_save_filepath(file_path)
        
        # まだデータベース化されていない場合のみ処理
        if not save_filepath.exists():
            try:
                # docxファイルを読み込み
                loader = Docx2txtLoader(str(file_path))
                doc = loader.load()
                
                # データベース化済みフォルダに保存
                self._save_to_processed_folder(doc[0].page_content, save_filepath)
                
                # theme_docsに追加
                if theme_name in theme_docs:
                    theme_docs[theme_name] += doc
                else:
                    theme_docs[theme_name] = doc
                    
                print(f"ファイルを処理しました: {file_path}")
                
            except Exception as e:
                print(f"ファイル処理でエラーが発生しました {file_path}: {e}")
    
    def _extract_theme_name(self, file_path: Path) -> str:
        """ファイルパスからテーマ名を抽出"""
        path_parts = file_path.parts
        
        # base_dirからの相対パスでテーマを判定
        try:
            relative_path = file_path.relative_to(self.base_dir)
            theme_name = relative_path.parts[0]
            
            # データディレクトリ内の既存テーマをチェック
            theme_dir = self.base_dir / theme_name
            if theme_dir.is_dir():
                return theme_name
        except ValueError:
            pass
        
        return None
    
    def _get_save_filepath(self, file_path: Path) -> Path:
        """データベース化済みフォルダのファイルパスを取得"""
        # 親ディレクトリの2つ上まで移動して、データベース化済みフォルダに保存
        parent_dir = file_path.parent.parent
        save_dir = parent_dir / "データベース化済み"
        save_dir.mkdir(exist_ok=True)
        return save_dir / file_path.name
    
    def _save_to_processed_folder(self, content: str, save_path: Path):
        """コンテンツをデータベース化済みフォルダに保存"""
        new_doc = Document()
        new_doc.add_paragraph(content)
        new_doc.save(str(save_path))
