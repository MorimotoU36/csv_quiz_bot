画面遷移図

```mermaid
flowchart LR
    トップ --> クイズ選択
    クイズ選択 <--> クイズ追加
    クイズ選択 <--> クイズ編集
    クイズ選択 <--> クイズ削除
    クイズ選択 <--> クイズ検索
    クイズ選択 <--> 画像アップロード
    クイズ追加 <--> クイズ編集
    クイズ追加 <--> クイズ削除
    クイズ追加 <--> クイズ検索
    クイズ追加 <--> 画像アップロード
    クイズ編集 <--> クイズ削除
    クイズ編集 <--> クイズ検索
    クイズ編集 <--> 画像アップロード
    クイズ削除 <--> クイズ検索
    クイズ削除 <--> 画像アップロード
    クイズ検索 <--> 画像アップロード
```