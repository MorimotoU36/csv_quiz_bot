//サーバ名を環境変数から読み取る
//const server = process.env.server;
const server = 'http://localhost:5000/';

//CSV名のリストを取得するAPI
function getCsvNameListApi(){
    return server + 'namelist'
}

//問題取得API
function getQuestionApi(){
    return server + 'select'
}

//問題ランダム取得API
function getRandomQuestionApi(){
    return server + 'random'
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
