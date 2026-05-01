# Week 11 Progress Report Draft

## Week 11 Progress Focus

Week 11 的核心目標，是在 Week 10 已建立 output layer 與 CLI orchestration 經驗之後，完成第一個可用的 `convert` flow。
和 `clean` 不同，`convert` 的責任刻意保持很薄：它只做 structured-data format conversion，也就是依 input 副檔名解析 records，再依 output 副檔名序列化 records，不載入 schema、不套用 transforms、不過濾 rows，也不產生 validation report。

這個範圍安排的重點，是把 DataGuard 的第三條 CLI flow 補齊，同時維持每條 command 的責任邊界清楚。
`validate` 負責 schema validation 與 report，`clean` 負責 transforms、validation、filtered output 與 report，`convert` 則只負責 CSV、JSON、JSONL 之間的格式轉換。

## Week 11 Completed Functionality

本週首先擴充了 output writer。
在 Week 10 的 `write_csv_output` 基礎上，`src/dataguard/output.py` 新增 `write_json_output` 與 `write_jsonl_output`。JSON writer 會輸出格式化的 array payload；JSONL writer 則會將每一筆 record 寫成一行 JSON object。這讓 output layer 從只支援 clean CSV，擴充為支援 CSV、JSON、JSONL 三種輸出格式。

第二個完成的基礎能力是 output writer factory。
`src/dataguard/output_factory.py` 會依 output path 的副檔名選擇對應 writer，支援 `.csv`、`.json` 與 `.jsonl`，並在遇到不支援的副檔名時回報 `Unsupported output format`。這讓 `convert` command 不需要直接知道每種格式的 writer 細節，也讓輸出格式選擇與 parser factory 的 input format 選擇形成對稱。

在 CLI flow 本身，Week 11 已完成 `convert` command。
目前 `convert` 會先透過 `get_parser(Path(input_path))` 根據 input 副檔名選 parser，再透過 `get_output_writer(Path(output_path))` 根據 output 副檔名選 writer。成功 parse 後，流程直接把 `parse_result.records` 寫到 output file。整個流程不會呼叫 schema loader、transform loader、validation engine 或 reporter，符合 pure conversion 的設計目標。

本週也補強了 convert 的錯誤處理。
目前 `convert` 可對 missing input file、unsupported input format、unsupported output format 與 invalid JSON input 回報清楚的 CLI error。這讓 `convert` 雖然是最薄的 flow，但在異常情況下仍保持可預期的 command-line 行為。

## Week 11 Development Method

Week 11 延續小步提交與測試驅動的開發方式。
本週先用 unit tests 鎖定 JSON/JSONL writer 行為，再新增 output writer factory 的 unit tests。之後才加入 `convert` CLI contract，最後用 integration tests 驗證跨格式轉換與錯誤路徑。

從本週新增的 commit 來看，提交內容可分成四個區塊。
第一個區塊是 output writer 擴充，讓 output layer 支援 JSON 與 JSONL。第二個區塊是 output writer factory，讓 CLI 可依副檔名選擇 writer。第三個區塊是 `convert` command 本體，完成 parser-to-writer 的薄 orchestration。第四個區塊則是 integration coverage，涵蓋多組格式轉換與 CLI error handling。

這種切分讓 Week 11 的進度能清楚對應到功能邊界。
`convert` 並不是把邏輯堆進 CLI，而是重用 parser factory 與 output writer factory，讓 command 本身維持簡單、可讀、可測。

## Software Testing Methods Used in Week 11

本週仍以測試驅動開發（TDD）作為主要方法。
JSON/JSONL output writer、output writer factory、convert CLI contract 與 convert integration cases 都先以測試描述預期行為，再完成最小實作。

本週也大量使用整合測試（Integration Testing）驗證完整 CLI flow。
`tests/integration/test_convert_flow.py` 覆蓋 CSV 到 JSON、JSON 到 JSONL、JSONL 到 CSV，以及 JSON 到 CSV。這些測試從 Click CLI 入口執行，檢查實際 output file 是否被寫出並包含預期資料。

在輸入空間切分（Input Space Partitioning）方面，本週將 convert 測試切成支援格式與錯誤格式。
支援格式測試確認 CSV、JSON、JSONL 能互相轉換到目前支援的 output；錯誤格式測試則確認 unsupported input、unsupported output、missing input 與 invalid JSON 都會以 CLI error 呈現。

最後，回歸測試仍用於確認 Week 11 沒有破壞既有能力。
完整 pytest 不只跑 convert tests，也同時跑 Week 8 的 validate flow、Week 9 的 transformer tests 與 Week 10 的 clean flow tests。

## Week 11 Validation Results

本週最新一次整體驗證使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`

測試結果為：
- `82 passed`
- Coverage `95%`

和 Week 10 的 `67 passed` 相比，Week 11 的新增測試主要來自 JSON/JSONL output writer、output writer factory、convert CLI contract，以及 convert integration/error handling coverage。這表示專案目前已經同時具備三條主要 CLI workflow 的自動化測試。

## Current Week 11 Status

就 Week 11 的目標而言，`convert` 已達到第一個可用版本。
目前專案已具備：
- JSON output writer
- JSONL output writer
- output writer factory
- `convert` CLI command
- CSV / JSON / JSONL input parsing reuse
- CSV / JSON / JSONL output writing
- convert flow integration coverage
- convert CLI error handling coverage

Week 11 的成果可以視為補齊 DataGuard 的第三條核心 CLI flow。
到目前為止，專案已具備 `validate`、`clean` 與 `convert` 三種主要使用路徑，而且三者的責任邊界清楚：validation、cleaning、conversion 分別由不同 command 承擔，並由測試覆蓋主要成功與錯誤情境。
