開發計畫 (Plan)
Phase 1: 後端 (Backend)

更新資料庫: 修改 db/init.sql，新增一個 orders 資料表來儲存訂單資訊。同時，我們可以建立一個 menu_items 表來儲存菜單，使其更具擴展性。
建立菜單 API: 在 backend/app.py 中新增一個 GET /api/menu 的 endpoint，用來回傳所有可用的餐點。
建立訂單 API:
POST /api/orders: 接收前端傳來的訂單資訊 (餐點 ID 和數量)，計算總價，並將訂單存入資料庫。
GET /api/orders: 回傳所有訂單的列表。
PUT /api/orders/<order_id>: 允許更新特定訂單的狀態。
Phase 2: 前端 (Frontend)

建立點餐介面: 修改 frontend/index.html 和 frontend/app.js。
使用 GET /api/menu 取得菜單並顯示在畫面上。
讓使用者可以點選餐點，並將其加入到一個 "購物車" 或 "當前訂單" 區域。
即時計算並顯示當前訂單的總金額。
新增一個 "送出訂單" 按鈕，點擊後會呼叫 POST /api/orders。
建立後台管理介面:
我們可以新增一個 kitchen.html 頁面 (或在原頁面新增一個區塊)。
此頁面會呼叫 GET /api/orders 來顯示所有訂單及其目前狀態。
提供按鈕或下拉選單，讓使用者可以呼叫 PUT /api/orders/<order_id> 來更新訂單狀態。
Phase 3: 專案設定

新增 LICENSE 檔案: 在專案的根目錄下建立一個 LICENSE 檔案，並填入 MIT License 的內容。