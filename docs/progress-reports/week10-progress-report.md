# Week 10 Progress Report Draft

## Week 10 Progress Focus

Week 10 的核心目標，是把 Week 9 已完成的 transformer foundation 接進第一條真正會產生清理結果的 CLI 流程，也就是 `clean`。
如果說 Week 9 的重點是先把資料轉換邏輯從 CLI 與檔案 I/O 中切出來，Week 10 的重點就是驗證這個基礎模組是否能被實際流程重用，並與 parser、schema、reporter 組合成一條可執行的 end-to-end clean path。

本週的範圍刻意聚焦在第一個可用版本，而不是一次支援所有輸出格式或所有清理策略。
目前 `clean` 的主要責任是：讀入資料、載入 schema、載入 transforms、套用 transforms、重新驗證 transformed records、保留沒有 validation error 的 rows，最後輸出 clean CSV 與 JSON report。這讓 `clean` 成為繼 `validate` 之後第二條完整 CLI flow。

## Week 10 Completed Functionality

本週首先完成的是 transform configuration loader。
`src/dataguard/transformer/loader.py` 目前可從 YAML 檔案讀取 `transforms` 陣列，並在缺少 root key 時回傳空 list。這讓 transformation steps 不再只存在於測試資料或 Python 呼叫中，而是可以由外部設定檔驅動。

第二個完成的基礎能力是 CSV output writer。
`src/dataguard/output.py` 新增 `write_csv_output`，可依 records 欄位寫出 header 與 rows，也能在 records 為空時透過 fieldnames 寫出 header-only CSV。這是 `clean` flow 能產出實際清理檔案的必要前置功能。

在 CLI flow 本身，Week 10 已完成 `clean` command。
目前 `clean` 會使用既有 parser 讀取 CSV 或 JSONL input，使用 schema loader 載入 YAML schema，使用 transform loader 載入 YAML transform config，接著呼叫 `apply_transforms` 套用資料轉換。轉換完成後，流程會用既有 `validate_records` 檢查 transformed records，並只把沒有 `ERROR` 等級驗證結果的 rows 寫入 clean CSV output。

本週也延續 Week 8 的 reporting model。
`clean` 在輸出 clean CSV 的同時，也會組裝 validation report 並寫成 JSON。這份 report 反映 transformed records 的驗證結果，讓使用者不只拿到清理後的資料，也能看到哪些 rows 被排除以及原因。當 report 中仍有 error 時，CLI 會以 exit code `1` 結束，維持與 `validate` flow 類似的錯誤語意。

## Week 10 Development Method

Week 10 延續前幾週的節奏，以小切片、測試驅動、可驗證提交來推進。
提交順序大致反映了 `clean` flow 的建構路徑：先補 transform config loader，再補 CSV output writer，接著建立 clean CLI contract，最後才把 parser、schema、transformer、validator、reporter 與 output writer 串成完整流程。

本週的 commit 可以分成三段。
第一段是支援性基礎模組，包括 transformer config loader 與 CSV writer。第二段是 `clean` command contract 與 CSV clean flow 本體。第三段則是 integration coverage 的擴充，包括 invalid CSV filtering 與 JSONL input path。這樣的順序讓每一個新增責任都有對應測試，而不是把整條 CLI flow 一次寫完後再補測試。

## Software Testing Methods Used in Week 10

本週仍以測試驅動開發（TDD）作為主要方法。
transform loader 與 CSV output writer 都先由 unit tests 定義最小行為，再補上實作。`clean` command 則先以 CLI contract test 鎖定必要參數，之後再用 integration tests 驗證實際資料流程。

在測試設計上，本週使用了整合測試（Integration Testing）確認多個模組的協作。
`tests/integration/test_clean_flow.py` 覆蓋 valid CSV clean path、invalid CSV filtering path，以及 JSONL input 到 clean CSV output 的 path。這些測試不是只檢查單一函式，而是從 Click CLI 入口一路跑到 output file 與 report file。

本週也使用輸入空間切分（Input Space Partitioning）區分 valid、invalid 與 non-CSV input。
valid CSV 測試確認清理流程能成功產出 output/report；invalid CSV 測試確認含錯誤的 rows 會被排除且 exit code 為 `1`；JSONL 測試則確認 `clean` 不只綁定 CSV input，而能重用 parser factory 支援另一種 input format。

最後，回歸測試仍是固定步驟。
每完成 clean flow 的一個切片後，都重新執行 pytest，確認 Week 8 的 `validate` 與 Week 9 的 transformer foundation 沒有被新的 CLI orchestration 破壞。

## Week 10 Validation Results

本週在 Week 10 commit 快照上使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run --extra dev pytest -q`

測試結果為：
- `67 passed`
- Coverage `95%`

和 Week 9 的 `59 passed` 相比，Week 10 的新增測試主要來自 transform config loader、CSV output writer、clean CLI contract，以及 clean flow integration coverage。這表示專案的測試範圍已經從純 validation 與 transformation layer，進一步擴充到第二條完整 CLI workflow。

## Current Week 10 Status

就 Week 10 的目標而言，`clean` 已達到第一個可用的 end-to-end 版本。
目前專案已具備：
- transform YAML config loader
- CSV output writer
- `clean` CLI command
- CSV input 到 clean CSV output 的主要流程
- invalid rows filtering
- JSONL input 到 clean CSV output 的補充流程
- clean flow JSON report

Week 10 的成果可以視為把 Week 9 的 transformer foundation 正式接入產品流程。
到這一週為止，DataGuard 已不只是一個 validation CLI，也開始具備資料清理與資料輸出能力，為後續 Week 11 的格式轉換流程鋪好 output layer 與 CLI orchestration 經驗。
