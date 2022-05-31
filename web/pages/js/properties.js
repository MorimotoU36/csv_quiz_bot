//CSV名のリストを取得するAPI
function getCsvNameListApi(server){
    return server + 'namelist'
}

//問題取得API
function getQuestionApi(server){
    return server + 'select'
}

//問題ランダム取得API
function getRandomQuestionApi(server){
    return server + 'random'
}

//正解不正解登録API
function getAnswerRegisterApi(server){
    return server + 'answer'
}

//問題登録API
function getAddQuizApi(server){
    return server + 'add'
}

//問題編集API
function getEditQuizApi(server){
    return server + 'edit'
}

//問題検索API
function getSearchQuizApi(server){
    return server + 'search'
}

//カテゴリリスト取得API
function getCategoryListApi(server){
    return server + 'get_category'
}

//問題のカテゴリ更新API
function getEditCategoryOfQuestionApi(server){
    return server + 'edit_category_of_question'
}

//カテゴリ別正解率取得API
function getAccuracyRateByCategoryApi(server){
    return server + 'get_accuracy_rate_by_category'
}

//最低正解率問題取得API
function getWorstRateQuizApi(server){
    return server + 'worst_rate'
}

//最小正解数問題取得API
function getMinimumClearQuizApi(server){
    return server + 'minimum'
}

//カテゴリマスタ更新API
function getUpdateCategoryMasterApi(server){
    return server + 'update_category_master'
}

//問題のカテゴリ更新API
function getEditCheckedOfQuestionApi(server){
    return server + 'edit_checked_of_question'
}

//S3からファイルをダウンロードするAPI
function getDownloadFilefromS3Api(server){
    return server + 's3_file_download'
}

//問題削除API
function getDeleteQuizApi(server){
    return server + 'delete'
}

//問題統合API
function getIntegrateQuizApi(server){
    return server + 'integrate'
}