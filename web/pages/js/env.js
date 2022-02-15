// 環境により値が違う設定を記載するファイル

// サーバー名を返す
function getServerName(){
    return 'http://localhost:5000/';
}

// S3からダウンロードしたファイルを置くディレクトリを返す
function getImgDirfromS3(){
    return '/pages/img/';
}

// 静的ファイルを置くディレクトリを返す
function getStaticDir(){
    return '/pages/static/';
}
