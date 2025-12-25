# Streamlit Cloud デプロイ手順

## 無料でオンラインデモを公開する方法

### 1. Streamlit Cloudアカウント作成
- https://share.streamlit.io/ にアクセス
- GitHubアカウントでログイン

### 2. デプロイ設定
- 「New app」をクリック
- Repository: `TONOTE1988/-AI-`
- Branch: `main`  
- Main file path: `app.py`

### 3. 環境変数設定（Secrets）
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-api-key-here"
```

### 4. 自動デプロイ
- GitHubにプッシュすると自動で更新

### 5. 公開URL取得
- `https://あなたのアプリ名.streamlit.app/`

## 注意点
- ⚠️ 無料プランは月50時間の制限あり
- 🔒 APIキーはStreamlitのSecretsで安全に管理
- 🌍 世界中からアクセス可能
