# VPS(Ubuntu)デプロイ手順書

## 1. はじめに

このドキュメントは、開発したTODOアプリケーションを、インターネット上のVPS（Virtual Private Server）にデプロイし、公開するための手順を解説します。

本番環境では、開発時とは異なり、アプリケーションを安定して稼働させ続けるための仕組み（プロセス管理、リバースプロキシなど）が必要になります。

## 2. 前提条件

- UbuntuがインストールされたVPSにSSHでアクセスできること。
- VPSのIPアドレスに紐づいたドメイン名を持っていること（推奨）。持っていない場合はIPアドレスでアクセスします。
- Linuxの基本的なコマンド操作に慣れていること。

## 3. デプロイ手順

### ステップ1: サーバーの初期設定と必要ソフトウェアのインストール

まず、サーバー環境を最新の状態にし、デプロイに必要なソフトウェアをインストールします。

```bash
# パッケージリストを更新し、システムをアップグレード
sudo apt update && sudo apt upgrade -y

# 必要なソフトウェアをインストール
sudo apt install python3-venv python3-pip nodejs npm nginx git -y
```

### ステップ2: プロジェクトの配置

Gitを使って、サーバーにプロジェクトのソースコードをクローンします。

```bash
# <your-repo-url> は実際のリポジトリURLに置き換えてください
git clone <your-repo-url> my-todo-app
cd my-todo-app
```

### ステップ3: バックエンドのセットアップとサービス化

APIサーバーを本番環境で安定稼働させるため、Gunicorn（WSGIサーバー）とSystemd（プロセス管理）を使用します。

```bash
# バックエンドのディレクトリに移動
cd backend-api

# Python仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# 依存ライブラリとGunicornのインストール
pip install -r requirements.txt
pip install gunicorn

# 仮想環境を抜ける
deactivate
```

次に、バックエンドをサービスとして自動起動するように設定します。

```bash
# Systemdのサービスファイルを作成
sudo nano /etc/systemd/system/todo-backend.service
```

エディタが開いたら、以下の内容を貼り付けます。`User`と`WorkingDirectory`はあなたの環境に合わせて修正してください。

```ini
[Unit]
Description=Todo App Backend Service
After=network.target

[Service]
User=ubuntu  # あなたのユーザー名
Group=www-data
WorkingDirectory=/home/ubuntu/my-todo-app/backend-api # プロジェクトのパス
ExecStart=/home/ubuntu/my-todo-app/backend-api/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

[Install]
WantedBy=multi-user.target
```

サービスを有効にして起動します。

```bash
# サービスを有効化
sudo systemctl enable todo-backend

# サービスを起動
sudo systemctl start todo-backend

# サービスの状態を確認 (エラーがないかチェック)
sudo systemctl status todo-backend
```

### ステップ4: フロントエンドのビルド

Vueアプリケーションを、静的なHTML/CSS/JSファイルに変換（ビルド）します。

```bash
# vue-test-appディレクトリに移動
cd ../vue-test-app

# 依存関係をインストール
npm install

# プロジェクトをビルド
npm run build
```

これにより、`vue-test-app/dist`ディレクトリに本番用のファイルが生成されます。

### ステップ5: Nginxの設定（リバースプロキシ）

Nginxをリバースプロキシとして設定し、ユーザーからのアクセスをフロントエンドとバックエンドに振り分けます。

```bash
# Nginxの設定ファイルを作成
sudo nano /etc/nginx/sites-available/todo-app
```

エディタに以下の内容を貼り付けます。`server_name`と`root`のパスは環境に合わせて修正してください。

```nginx
server {
    listen 80;
    server_name your_domain.com; # あなたのドメイン名 or VPSのIPアドレス

    # フロントエンドの静的ファイルを提供
    root /home/ubuntu/my-todo-app/vue-test-app/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # /todos/ へのアクセスをバックエンドAPIに転送
    location /todos/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

設定を有効にし、Nginxを再起動します。

```bash
# 設定ファイルのシンボリックリンクを作成
sudo ln -s /etc/nginx/sites-available/todo-app /etc/nginx/sites-enabled/

# Nginxの設定に文法エラーがないかテスト
sudo nginx -t

# Nginxを再起動
sudo systemctl restart nginx
```

### ステップ6: ファイアウォールの設定

最後に、HTTPトラフィックを許可するようにファイアウォールを設定します。

```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 4. 確認

Webブラウザであなたのドメイン名（またはIPアドレス）にアクセスし、TODOアプリケーションが表示され、正常に動作することを確認してください。

**次のステップ**: セキュリティ向上のため、[Let's Encrypt](https://letsencrypt.org/)を使って無料のSSL証明書を導入し、HTTPS通信を有効にすることを強くお勧めします。
