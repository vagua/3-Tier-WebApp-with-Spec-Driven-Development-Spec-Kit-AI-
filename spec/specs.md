規格 (Specifications)
菜單 (Menu):

系統需要提供一份可用的餐點列表。
每個餐點應包含 id, name, 和 price。
訂單 (Orders):

使用者可以將多個餐點加入一個訂單。
系統需要能計算訂單的總金額。
送出的訂單需要被儲存起來，並包含以下資訊：
id (訂單編號)
items (訂單內容，例如餐點列表)
total_price (總金額)
status (訂單狀態，例如：pending, in_progress, completed)
created_at (訂單建立時間)
後台管理 (Kitchen/Admin View):

需要有一個介面能看到所有已送出的訂單。
在此介面中，可以更改每個訂單的狀態。
授權 (License):

整個專案應使用 MIT License。