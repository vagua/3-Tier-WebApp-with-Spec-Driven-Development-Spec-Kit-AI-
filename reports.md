## 1. What changed (from HW3) and why (reference spec sections)

主要在功能的部分，多了一些模仿POS機的一些簡易點餐功能。
因為SPEC的要求，需要用SDD的流程去開發一個public的repo，多了很多除了自己開發的文件，例如contributing跟log的方式要有一定的規則寫給其他用戶看。
還要增添unit test的方法，讓增加功能之後原本的功能還是可以去正常的作用。

---

## 2. Key issues you ran into during this refactor and how you resolved them

在這次重構過程中，遇到了一些挑戰，以下是主要的幾個問題及其解決方法。

### 問題一：Vscode code assist error
* **問題描述：** Vscode code assist 的 agent mode不知道是吃太多資源還是某些優化問題會持續的卡死。
* **解決方法：**
    1.  **關閉agent mode：** 切換回正常模式，卡死的問題就減少了，但還是流失掉了一些log跟對話紀錄。
    2.  **使用其他的AI agent：** 可以看 .ai-log/ 內的chat_log，有一些code assist檢查不出來的問題，還是用一些其他的AI agent跟自己debug去看問題比較實際一點。

### 問題二：sql error
* **問題描述：** docker compose up 的時候 db一直沒有初始化內容。
* **解決方法：** 確保前端js與後端flask的內容都是正常的之後，就回去重看db 的init.sql，發現因為compose up要去檢查一下資料庫有沒有重複的內容，但相應的資料型態並沒有給unique導致一直報錯。給好正確的型態就OK了

---

## 3. How to reproduce results locally

詳情請看QUICKSTART.md