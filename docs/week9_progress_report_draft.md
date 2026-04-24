# Week 9 Progress Report Draft

## Week 9 Progress Focus

Week 9 的核心目標，不是直接新增新的 CLI 命令，而是為後續 `clean` 與 `convert` 流程建立可重用的 `transformer` 基礎模組。  
如果說 Week 8 的工作重點是把 `validate` 做厚、做完整，那麼 Week 9 的重點就是先把資料轉換與資料清理的核心邏輯從 0 建立起來，並且用測試把這些操作的行為鎖定下來。

因此，Week 9 的範圍刻意聚焦在 transformer foundation，而不是同時把 CLI orchestration 也一起做完。這樣的安排可以讓這一週形成一個清楚的中間里程碑：先完成純 transformation layer，之後再把它接進 `clean` 或 `convert`。這和 Week 7、Week 8 的節奏一致，也就是先完成一個可被驗證、可被展示的核心模組，再往外擴充流程。

## Week 9 Completed Functionality

本週已完成的核心模組是 `src/dataguard/transformer/`。  
這個模組的定位是純 transformation layer，輸入為 `list[dict]` records 與 transforms array，輸出為新的 transformed records，不直接處理任何檔案 I/O，也不直接依賴 CLI。這樣的設計讓 transformation logic 可以單獨測試，也能在未來被 `clean` 或 `convert` 共用。

首先，專案已完成 ordered transformer engine。  
目前 `apply_transforms` 會依照 transforms 陣列順序逐步套用各個 operation，並在遇到 unknown operation 時回報明確錯誤。這表示 transformation 已不只是零散函式，而是具備一個統一的執行入口。

在操作類型方面，本週完成了三組具代表性的 transformation 功能。  
第一組是 `type_cast`，目前支援 `integer`、`float`、`string` 與 `boolean` 的最小型別轉換能力。對於轉換失敗的值，會保留原始值，而不是讓整體流程中斷。  
第二組是 `fill_missing`，本週先完成了 `default` 與 `drop_row` 兩種策略。前者可將空值補成預設值，後者則直接移除含缺值的 records。  
第三組是 `dedup`，目前支援以 `keys` 作為去重依據，並提供 `keep=first` 與 `keep=last` 兩種策略。這使 transformer 已具備最基本的資料清理能力。

整體來說，Week 9 已經不是只有單一 transformation function，而是已完成一個可排序、可組合、可驗證的 transformation foundation。這是後續擴充 `clean` 或 `convert` 的必要前置條件。

## Week 9 Development Method

Week 9 延續了前兩週的開發方式，也就是以小步驟、可驗證、測試驅動的節奏推進。  
本週的提交仍以一個功能切片對應一個明確 commit 為原則，並且盡量維持 `test -> feat` 的思考方式，即使某些最小骨架行為在 foundation commit 中已經先被建立，後續也會再用專屬測試把該行為明確補齊。

從本週新增的 commit 來看，提交內容大致可分成四個區塊。  
第一個區塊是 transformer package foundation，也就是 `transformer` module、engine 與最小 operation stubs。  
第二個區塊是 `type_cast` 與 `fill_missing` 的逐步擴充。  
第三個區塊是 `dedup` 行為的收斂，從 `keep=first` 到 `keep=last`。  
第四個區塊則是 integration coverage，也就是確認多個 transforms 可以依照順序一起工作，而不是只有單元函式各自正確。

這種提交方式的價值在於，GitHub 歷史本身就能作為開發證據。  
每一筆 commit 都對應一個小而明確的能力，能夠清楚展示本週成果不是一次性堆疊，而是逐步擴充出來的。

## Software Testing Methods Used in Week 9

本週仍然以軟體測試方法作為主要開發骨架，而不是先完成 transformation 再補測試。  
第一，測試驅動開發（TDD）仍是主要方法。每加入一個新操作或一個新策略，就先建立 failing tests，再補最小實作。  
第二，等價類別測試（Equivalence Class Testing）被用在 `type_cast`、`fill_missing` 與 `dedup`，例如區分可轉換與不可轉換、缺值與非缺值、重複與不重複 records。  
第三，整合測試（Integration Testing）則用於驗證 transformation 的順序性，也就是確認 `type_cast -> fill_missing -> dedup` 這樣的組合能得到正確結果。  
第四，回歸測試（Regression Testing）依然是固定步驟。每完成一組新功能後，都重新執行整套 pytest，確保 Week 7 與 Week 8 建立起來的 `validate` 功能沒有被破壞。

## Week 9 Validation Results

本週最新一次整體驗證使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`

測試結果為：
- `59 passed`
- Coverage `97%`

和 Week 8 相比，Week 9 的新增測試數量主要來自 transformer unit tests 與 integration coverage。這表示目前專案的測試範圍，已經不只涵蓋 parser、schema、validator、reporter 與 validate CLI，也開始正式涵蓋 transformation layer。

## Current Week 9 Status

就 Week 9 的目標而言，本週的 transformer foundation 已經達到一個可被視為完成的中間里程碑。  
目前專案已具備：
- ordered transformer engine
- `type_cast`
- `fill_missing(default, drop_row)`
- `dedup(keep=first, keep=last)`
- transformer integration coverage

這表示後續如果要進入 `clean` 或 `convert`，目前已經有一個可重用的 transformation layer 可以直接接入，而不需要從資料操作邏輯開始重寫。

因此，Week 9 的成果可以被視為在 Week 8 的 `validate` 基線之上，再建立一層新的核心能力。  
Week 8 的主要價值是完成一條更完整的資料驗證路徑；Week 9 的主要價值則是建立資料轉換與清理的基礎模組。兩者合起來，已經為後續更完整的資料處理流程鋪好主要地基。
