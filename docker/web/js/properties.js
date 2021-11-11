//サーバ名を環境変数から読み取る
const server = process.env.server;

//CSV名のリストを取得するAPI
function getCsvNameListApi(){
//    return server + ''
}

//問題取得API
function getQuestionApi(){
    return server + 'select'
}

//正解不正解登録API
function getCorrectRegisterApi(){
    return server + 'answer'
}

//問題登録API
function getAddQuizApi(){
//    return server + ''
}

//問題編集API
function getEditQuizApi(){
//    return server + ''
}
