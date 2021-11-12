//英語問題のデータの個数
let question_total_num = 0;

//問題番号
let question_num = -1;
//問題文
let sentense = ""
//答え
let quiz_answer = ""

//問題番号の変更を反映する
function update_question_num(event){
    question_num = Number(document.getElementById("question_number").value)
}

//エラーメッセージの設定・表示
function set_error_message(msg){
    err = document.getElementById("error")
    err.innerText = msg
}

//エラーメッセージのクリア
function clear_error_message(){
    err = document.getElementsByClassName("error")
    for(i=0;i<err.length;i++){
        err[i].innerText = ""
    }
}

//表示されているメッセージのクリア
function clear_all_message(){
    msg = document.getElementsByClassName("message")
    for(i=0;i<msg.length;i++){
        msg[i].innerText = ""
    }
}

//エラーチェック①,入力した問題番号がcsvにある問題番号の範囲内か調べる
function check_input_question_num(){
    if(question_num < 1 || question_total_num < question_num ){
        return true
    }else{
        return false
    }
}

//min以上max未満の数値をランダムに取得
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

//min以上max以下の数値をランダムに取得
function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min); //The maximum is inclusive and the minimum is inclusive
}

//問題の総数を取得する
function get_total_question_num(){
    //メッセージをクリア
    clear_all_message();

    //外部APIへCSVリストを取得しにいく
    post_data(getCsvNameListApi(),{"text" : 'E'},function(resp){
        if(resp['statusCode'] == 200){    
            // 問題の総数が帰ってくるので変数を設定
            question_total_num = resp['text']
        }else{
            //内部エラー時
            set_error_message("statusCode："+resp['statusCode']
                                +" "+resp['error_log']);
        }
    })
}

//英語問題取得
function get_english_question(){
    //メッセージをクリア
    clear_all_message();

    //問題番号入力されてなかったらエラー
    //入力値エラーチェック
    if(question_num == -1 || document.getElementById("question_number").value == ""){
        set_error_message("問題番号を入力して下さい");
        return false;
    }

    //JSONデータ作成
    var data = {
        "text" : 'E-'+String(question_num)
    }
    //外部APIへPOST通信、問題を取得しにいく
    post_data(getQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            sentense = resp.sentense === undefined ? "" : resp.sentense
            quiz_answer =  resp.answer === undefined ? "" : resp.question_answer

            question.textContent = sentense
            answer.textContent = ""

            //カテゴリエリア
            let category = resp.question_category
            set_category_box(category)
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
    })
}

//ランダムに問題を選んで出題する
function random_select_question(){
    //メッセージをクリア
    clear_all_message();

    //問題番号をランダムに選ぶ
    question_num = getRandomIntInclusive(1,question_total_num)

    //JSONデータ作成
    var data = {
        "text" : 'E-'+String(question_num)
    }
    //外部APIへPOST通信、問題を取得しにいく
    post_data(getQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            sentense = resp.sentense === undefined ? "" : resp.sentense
            quiz_answer =  resp.answer === undefined ? "" : resp.answer

            question.textContent = sentense
            answer.textContent = ""

            //カテゴリエリア
            let category = resp.question_category
            set_category_box(category)
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
    })
}

//問題に正解したときに正解データ登録
function correct_register(){
    //メッセージをクリア
    clear_all_message();

    //JSONデータ作成
    var data = {
        "text" : 'E-'+String(question_num)
    }
    //外部APIに指定した問題の正解数を登録しに行く
    post_data(getCorrectRegisterApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            //問題と答えは削除
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            sentense = ""
            quiz_answer = ""

            question.textContent = ""
            answer.textContent = ""

            //正解登録完了メッセージ
            let result = document.getElementById("result")
            result.textContent = resp['message']

            //カテゴリ欄のクリア
            let category_area = document.getElementById("category_area")
            //子要素(以前のカテゴリ)削除
            category_area.innerHTML = ""
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
    })
}

//問題に不正解のときに正解データ登録
function incorrect_register(){
    //メッセージをクリア
    clear_all_message();

    //JSONデータ作成
    var data = {
        "text" : 'E-'+String(question_num)
    }
    //外部APIに指定した問題の正解数を登録しに行く
    post_data(getIncorrectRegisterApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            //問題と答えは削除
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            sentense = ""
            quiz_answer = ""

            question.textContent = ""
            answer.textContent = ""

            //正解登録完了メッセージ
            let result = document.getElementById("result")
            result.textContent = resp['message']

            //カテゴリ欄のクリア
            let category_area = document.getElementById("category_area")
            //子要素(以前のカテゴリ)削除
            category_area.innerHTML = ""
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
    })
}

//答えの文を表示
function display_answer(){
    //メッセージをクリア
    clear_all_message();

    if(sentense == ""){
        set_error_message("問題文がありません。")
    }else{
        let answer = document.getElementById("answer")
        answer.textContent = quiz_answer
    }
}

//Ajaxで指定したurlにPOST通信を送る、受け取った後の処理関数も定義して引数に入力
function post_data(url,jsondata,responsed_func){
    //XMLHttpRequest用意
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader('content-type', 'application/json;charset=UTF-8');

    //送信
    xhr.send( JSON.stringify(jsondata) );

    //受信して結果を表示
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            const jsonObj = JSON.parse(xhr.responseText);
            //受信したデータを処理する      
            responsed_func(jsonObj);
        }
    }
}


//(クイズ追加画面)入力したCSVデータを送信して追加する
function add_quiz(){
    //メッセージをクリア
    clear_all_message();

    let input_data = document.getElementById("input_data").value

    //JSONデータ作成
    var data = {
        "file" : "E",
        "data" : input_data
    }

    post_data(getAddQuizApi(),data,function(resp){
        //正解登録完了メッセージ
        let log = document.getElementById("add_log")
        log.innerHTML = resp['log'].join('<br>')
    })

    //入力データをクリア
    document.getElementById("input_data").value = ""
}

//(問題編集画面での)問題取得
function get_question_for_edit(){
    //メッセージをクリア
    clear_all_message();

    //JSONデータ作成
    var data = {
        "text" : 'E-'+String(question_num)
    }

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            document.getElementById("question_num").innerText = question_num
            document.getElementById("question_sentense").value = resp.question_sentense === undefined ? "" : resp.question_sentense
            document.getElementById("question_answer").value = resp.question_answer === undefined ? "" : resp.question_answer
            document.getElementById("question_category").value = resp.question_category === undefined ? "" : resp.question_category
            document.getElementById("question_img_file_name").value = resp.question_img_file_name === undefined ? "" : resp.question_img_file_name
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
        console.log(document.getElementById("question_of_file_num").innerText)
    })
}

//問題を編集
function edit_question(){
    //メッセージをクリア
    clear_all_message();

    //JSONデータ作成
    var data = {
        "file_num": "E",
        "number": document.getElementById("question_num").innerText,
        "sentense": document.getElementById("question_sentense").value,
        "answer": document.getElementById("question_answer").value,
        "category": document.getElementById("question_category").value,
        "img_file_name": document.getElementById("question_img_file_name").value
    }

    //外部APIに指定した問題を更新する
    post_data(getEditQuizApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            //編集完了メッセージ
            let result = document.getElementById("result")
            result.textContent = resp['message']
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error_log']);
        }
    })
}

//取得した問題のカテゴリを表示
function set_category_box(category){
    let categories = category.split(':');

    let category_area = document.getElementById("category_area")
    //子要素(以前のカテゴリ)削除
    category_area.innerHTML = ""

    //カテゴリを一個一個表示させる
    for(let i=0;i<categories.length;i++){
        //カテゴリ１要素を作成
        var newCategoryElement = document.createElement("span");
        var newCategoryContent = document.createTextNode(categories[i]);
        newCategoryElement.appendChild(newCategoryContent);
        newCategoryElement.setAttribute("class","category-elements");

        //カテゴリエリアの子要素にappend
        category_area.appendChild(newCategoryElement);
    }
}