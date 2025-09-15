FROM nginx:alpine

# ビルド済みファイルをコピー
COPY ./dist /usr/share/nginx/html

# Nginxのデフォルト設定を置き換える（後述）
COPY nginx.conf /etc/nginx/conf.d/default.conf
