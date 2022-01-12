//各csvのデータの個数
var csv_item_list = [];

//ファイル名
let file_name = "";
//ファイル番号
let file_num = -1;
//問題番号
let question_num = -1;
//問題文
let sentense = ""
//答え
let quiz_answer = ""

//問題検索をしたファイルの番号
let searched_file_num = -1;

//ファイル名、ファイル番号の変更を反映する。カテゴリリストも変更する
function update_file_num(event){
    fl = document.getElementById("file_list")
    file_num = Number(fl.options[fl.selectedIndex].value)
    file_name = fl.options[fl.selectedIndex].innerText

    //カテゴリリスト反映
    if(document.getElementById("category_list") != null){
        get_category_list(file_num)
    }
}

//現在選択されているファイルの番号を取得
function get_file_num(){
    fl = document.getElementById("file_list")
    return Number(fl.options[fl.selectedIndex].value)
}

//問題番号の変更を反映する
function update_question_num(event){
    question_num = Number(document.getElementById("question_number").value)
}

//入力されている問題番号を取得する
function get_question_num(){
    return Number(document.getElementById("question_number").value)
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
function check_input_question_num(file_index){
    if(question_num < 1 || csv_item_list[file_index] < question_num ){
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

//問題csvのリストを取得する
function get_csv_name_list(){
    //メッセージをクリア
    clear_all_message();

    //外部APIへCSVリストを取得しにいく
    post_data(getCsvNameListApi(),{"text" : ''},function(resp){
        if(resp['statusCode'] == 200){    
            // ドロップダウンリストにCSVファイルのリストを定義する
            let file_list = document.getElementById("file_list");
            for(var i=0;i<resp['table'].length;i++){
                var target = document.createElement('option');
                target.innerText = resp['table'][i]['nickname'];
                target.setAttribute('value',i);
                file_list.appendChild(target);
            }
        }else{
            //内部エラー時
            set_error_message("statusCode："+resp['statusCode']
                                +" "+resp['error']);
        }
    })
}

//問題取得
function get_question(){
    //メッセージをクリア
    clear_all_message();

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }
    else if(isNaN(get_question_num())){
        set_error_message("エラー：問題番号には数値を入力して下さい");
        return false;
    }
    else if(document.getElementById("question_number").value == ""){
        set_error_message("エラー：問題番号を入力して下さい");
        return false;
    }

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "quiz_num": get_question_num(),
        "image_flag": true 
    }
    //外部APIへPOST通信、問題を取得しにいく
    post_data(getQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            let response = resp.response
            sentense = response.quiz_sentense === undefined ? "" : response.quiz_sentense
            quiz_answer =  response.answer === undefined ? "" : response.answer
            question_num = get_question_num()

            question.textContent = sentense
            answer.textContent = ""

            //カテゴリエリア
            let category = response.category
            set_category_box(category)
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })
}

//ランダムに問題を選んで出題する
function random_select_question(){
    //メッセージをクリア
    clear_all_message();

    //ファイル番号を取得、「指定なし」の時はランダムに選ぶ
    if(get_file_num() == -1){
        file_num = getRandomInt(0,csv_item_list.length);
    }else{
        file_num = get_file_num();
    }

    //選択されたカテゴリ取得
    cl = document.getElementById("category_list")
    selected_category = cl.options[cl.selectedIndex].value

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "category": selected_category == -1 ? "" : selected_category
    }
    //外部APIへPOST通信、問題を取得しにいく
    post_data(getRandomQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            let response = resp.response
            sentense = response.quiz_sentense === undefined ? "" : response.quiz_sentense
            quiz_answer =  response.answer === undefined ? "" : response.answer
            question_num = Number(response.quiz_num)

            question.textContent = sentense
            answer.textContent = ""

            //カテゴリエリア
            let category = response.category
            set_category_box(category)
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })
}

//正解率最低の問題を出題する
function worst_rate_question(){
    //メッセージをクリア
    clear_all_message();

    //ファイル番号を取得、「指定なし」の時はランダムに選ぶ
    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }else{
        file_num = get_file_num();
    }

    //選択されたカテゴリ取得
    cl = document.getElementById("category_list")
    selected_category = cl.options[cl.selectedIndex].value

    //JSONデータ作成
    var data = {
        "file_num": file_num
    }
    if(selected_category != -1){
        data.category = selected_category
    }
    console.log(data)

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getWorstRateQuizApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let question = document.getElementById("question")
            let answer = document.getElementById("answer")
            let response = resp.response
            sentense = response.quiz_sentense === undefined ? "" : response.quiz_sentense
            quiz_answer =  response.answer === undefined ? "" : response.answer
            question_num = Number(response.quiz_num)

            question.textContent = sentense
            answer.textContent = ""

            //カテゴリエリア
            let category = response.category
            set_category_box(category)
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })
}

//問題に正解したときに正解データ登録
function correct_register(){
    //メッセージをクリア
    clear_all_message();

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "quiz_num": question_num,
        "clear": true
    }
    //外部APIに指定した問題の正解数を登録しに行く
    post_data(getAnswerRegisterApi(),data,function(resp){
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
            result.textContent = resp['result']

            //カテゴリ欄のクリア
            let category_area = document.getElementById("category_area")
            //子要素(以前のカテゴリ)削除
            category_area.innerHTML = ""
            //問題番号のクリア
            question_num = -1
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
        "file_num": file_num,
        "quiz_num": question_num,
        "clear": false
    }
    //外部APIに指定した問題の正解数を登録しに行く
    post_data(getAnswerRegisterApi(),data,function(resp){
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
            result.textContent = resp['result']

            //カテゴリ欄のクリア
            let category_area = document.getElementById("category_area")
            //子要素(以前のカテゴリ)削除
            category_area.innerHTML = ""
            //問題番号のクリア
            question_num = -1
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

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }

    let input_data = document.getElementById("input_data").value

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "data" : input_data
    }

    post_data(getAddQuizApi(),data,function(resp){
        //正解登録完了メッセージ
        let log = document.getElementById("add_log")
        log.innerHTML = resp['result'].join('<br>')
    })

    //入力データをクリア
    document.getElementById("input_data").value = ""
}

//(問題編集画面での)問題取得
function get_question_for_edit(){
    //メッセージをクリア
    clear_all_message();

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }else if(check_input_question_num(file_num)){
        set_error_message("エラー：問題("+file_name
                            +")の問題番号は1〜"+csv_item_list[file_num]
                            +"の範囲内で入力して下さい");
        return false;
    }

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "quiz_num": question_num,
        "image_flag": true 
    }

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){  
            document.getElementById("question_of_file").innerText = file_name
            document.getElementById("question_num").innerText = question_num
            document.getElementById("question_of_file_num").innerText = get_file_num()
            document.getElementById("question_sentense").value = resp.response.quiz_sentense === undefined ? "" : resp.response.quiz_sentense
            document.getElementById("question_answer").value = resp.response.answer === undefined ? "" : resp.response.answer
            document.getElementById("question_category").value = resp.response.category === undefined ? "" : resp.response.category
            document.getElementById("question_img_file_name").value = resp.response.img_file === undefined ? "" : resp.response.img_file
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
        "file_num": document.getElementById("question_of_file_num").innerText,
        "quiz_num": document.getElementById("question_num").innerText,
        "question": document.getElementById("question_sentense").value,
        "answer": document.getElementById("question_answer").value,
        "category": document.getElementById("question_category").value,
        "img_file": document.getElementById("question_img_file_name").value
    }

    //外部APIに指定した問題の正解数を登録しに行く
    post_data(getEditQuizApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            //編集完了メッセージ
            let result = document.getElementById("result")
            result.textContent = resp['message']
        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
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

//問題検索
function search_question(){
    //メッセージをクリア
    clear_all_message();

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }

    //入力された検索語句
    let query = document.getElementById("query").value

    //選択されたカテゴリ取得
    cl = document.getElementById("category_list")
    selected_category = cl.options[cl.selectedIndex].value

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "query": query,
        "condition" : {
            "question": document.getElementById('check_question').checked,
            "answer": document.getElementById('check_answer').checked
        },
        "category": selected_category == -1 ? "" : selected_category
    }

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getSearchQuizApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let result = resp.result

            let result_table = ""
            result_table += "<table id='search_result_table'>"
            result_table += "<thead><tr><th class='table_id'>番号</th><th class='table_sentense'>問題</th><th class='table_answer'>答え</th><th>カテゴリ</th></tr></thead>"

            for(let i=0;i<result.length;i++){
                let sentense = result[i].quiz_sentense.replace(new RegExp(query,"g"),"<span class='query_word'>"+query+"</span>")
                let answer = result[i].answer.replace(new RegExp(query,"g"),"<span class='query_word'>"+query+"</span>")
                let categories = result[i].category.split(':');
                let category = "";
                for(let i=0;i<categories.length;i++){
                    //カテゴリ要素を作成
                    category += "<span class='category-elements'>"
                    category += categories[i]
                    category += "</span><br>"
                }
                result_table += "<tr><td class='table_id'>"+ result[i].quiz_num +"</td><td class='table_sentense'>"+ sentense +"</td><td class='table_answer'>"+ answer +"</td><td>"+ category +"</td></tr>"
            }

            result_table += "</table>"

            let search_result = document.getElementById("search_result")
            search_result.innerHTML = result_table

        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })

    //検索したファイルの番号を記録
    searched_file_num = file_num
}

//カテゴリリスト取得
function get_category_list(file_num){

    //指定なしの場合
    if(Number(file_num) == -1){
        //ドロップダウンリストに「指定なし」のみ設定する
        let category_list = document.getElementById("category_list");
        category_list.innerHTML = "";

        let noselected = document.createElement('option');
        noselected.innerText = "指定なし";
        noselected.setAttribute('value',-1);
        category_list.appendChild(noselected);

        return true;
    }

    //JSONデータ作成
    var data = {
        "file_num": file_num
    }

    //外部APIへPOST通信、カテゴリを取得しにいく
    post_data(getCategoryListApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let results = resp.result

            // ドロップダウンリストにカテゴリのリストを定義する
            let category_list = document.getElementById("category_list");
            category_list.innerHTML = "";

            let noselected = document.createElement('option');
            noselected.innerText = "指定なし";
            noselected.setAttribute('value',-1);
            category_list.appendChild(noselected);

            for(let i=0;i<results.length;i++){
                var target = document.createElement('option');
                target.innerText = results[i];
                target.setAttribute('value',results[i]);
                category_list.appendChild(target);
            }

        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })
}

//問題検索・カテゴリ設定
function search_and_category(){
    //メッセージをクリア
    clear_all_message();

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }

    //入力された検索語句
    let query = document.getElementById("query").value

    //選択されたカテゴリ取得
    cl = document.getElementById("category_list")
    selected_category = cl.options[cl.selectedIndex].value

    //JSONデータ作成
    var data = {
        "file_num": file_num,
        "query": query,
        "condition" : {
            "question": document.getElementById('check_question').checked,
            "answer": document.getElementById('check_answer').checked
        },
        "category": selected_category == -1 ? "" : selected_category
    }

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getSearchQuizApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let result = resp.result

            let result_table = ""
            result_table += "<table id='search_result_table'>"
            result_table += "<thead><tr><th>チェック</th><th class='table_id'>番号</th><th class='table_sentense'>問題</th><th class='table_answer'>答え</th><th>カテゴリ</th></tr></thead>"

            for(let i=0;i<result.length;i++){
                let sentense = result[i].quiz_sentense.replace(new RegExp(query,"g"),"<span class='query_word'>"+query+"</span>")
                let answer = result[i].answer.replace(new RegExp(query,"g"),"<span class='query_word'>"+query+"</span>")
                let categories = result[i].category.split(':');
                let category = "";
                for(let i=0;i<categories.length;i++){
                    //カテゴリ要素を作成
                    category += "<span class='category-elements'>"
                    category += categories[i]
                    category += "</span><br>"
                }
                result_table += "<tr><td><input type='checkbox'></td><td class='table_id'>"+ result[i].quiz_num +"</td><td class='table_sentense'>"+ sentense +"</td><td class='table_answer'>"+ answer +"</td><td>"+ category +"</td></tr>"
            }

            result_table += "</table>"

            let search_result = document.getElementById("search_result")
            search_result.innerHTML = result_table

        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })

    //検索したファイルの番号を記録
    searched_file_num = file_num
}

// 問題のカテゴリを一括設定する
function update_category_to_checked_question(){
    //メッセージをクリア
    clear_all_message();

    //入力された検索語句
    let update_category = document.getElementById("update_category").value
    //空欄なら終了
    if(update_category == ""){
        set_error_message("カテゴリを入力して下さい");
        return false;
    }else if(!document.getElementById("search_result").hasChildNodes()){
        //テーブルにデータがないならエラー
        set_error_message("検索結果にデータがありません");
        return false;
    }

    //updateクエリを作成
    update_query = []

    //テーブルから入力データ取得
    let srt = document.getElementById("search_result_table")
    let srt_tbody = srt.lastChild
    let srt_tr = srt_tbody.childNodes
    for(let i=0;i<srt_tr.length;i++){
        let srt_td = srt_tr[i].childNodes
        //チェック確認
        if(!srt_td[0].firstChild.checked){
            continue
        }
        
        uqi={
            "file_num": searched_file_num,
            "quiz_num": srt_td[1].innerText,
            "category": update_category
        }
        update_query.push(uqi)
    }

    data = {
        "data": update_query
    }

    //外部APIへPOST通信、問題を取得しにいく
    post_data(getEditCategoryOfQuestionApi(),data,function(resp){
        if(resp['statusCode'] == 200){    

            let update_category_result = document.getElementById("update_category_result")
            update_category_result.innerHTML = resp['result']

        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })

    //検索したファイルの番号を記録
    searched_file_num = file_num
}


// カテゴリ別正解率表示
function display_accuracy_rate_by_category(){
    //メッセージをクリア
    clear_all_message();

    //エラーチェック、問題番号が範囲内か
    if(Number(file_num) == -1){
        set_error_message("問題ファイルを選択して下さい");
        return false;
    }

    //JSONデータ作成
    var data = {
        "file_num": file_num
    }

    //外部APIへPOST通信、カテゴリと正解率を取得しにいく
    post_data(getAccuracyRateByCategoryApi(),data,function(resp){
        if(resp['statusCode'] == 200){    
            let result = resp.result

            let visualized_data = [['Name', 'Accuracy_Rate', { role: 'style' } ]]
            for(let i=0;i<result.length;i++){
                visualized_data.push([result[i].c_category,parseFloat(result[i].accuracy_rate),'#76A7FA'])
            }
            // グラフ領域の縦の長さ（＝40 * データの個数）
            let graph_height = 40 * visualized_data.length
            visualized_data = google.visualization.arrayToDataTable(visualized_data)
            var view = new google.visualization.DataView(visualized_data);

            var options = {
                height: graph_height,
                legend: { position: "none" },
                chartArea: {
                    left: '15%',
                    top: 10,
                    width: '80%',
                    height: graph_height-50
                },
                hAxis: {
                    minValue: 0,
                    maxValue: 1
                }
            };

            var chart = new google.visualization.BarChart(document.getElementById("search_result"));
            chart.draw(view, options);

        }else{
            //内部エラー時
            set_error_message(resp['statusCode']
                                +" : "+resp['error']);
        }
    })

    //検索したファイルの番号を記録
    searched_file_num = file_num
}