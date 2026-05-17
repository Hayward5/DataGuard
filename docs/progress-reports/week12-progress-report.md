# Week 12 Progress Report Draft

## Week 12 Progress Focus

Week 12 的核心目標分成兩個層面。
第一個層面是建立正式的 GitHub 開發工作流程：在 Week 11 已完成三條主要 CLI flow 的基礎上，這週的重點是讓後續開發能透過 Issue、branch、PR、CI、merge 的標準流程推進，而不是直接在功能分支上累積變更。第二個層面是在不改動現有 `validate`、`clean`、`convert` 核心架構的前提下，補上兩個相對獨立但有實際使用價值的功能缺口：文字格式報告輸出，以及欄位結構轉換。

這樣的安排讓 Week 12 同時做到流程正規化與功能補齊，而且兩者都有明確的完成條件，不會讓範圍膨脹。

---

## Week 12 Completed Functionality

### GitHub 工作流程正規化

本週首先建立 `main` 作為正式整合分支，並將 GitHub 預設分支從 `week11-convert-flow` 改為 `main`。
在此之上，新增了兩份 GitHub 模板：`.github/pull_request_template.md` 要求每個 PR 填寫 summary、files changed、testing steps 與 linked issue；`.github/ISSUE_TEMPLATE/feature.md` 要求每個 Issue 填寫 goal、current behavior、expected behavior 與 acceptance criteria。
`README.md` 也同步補上 Contributing 區段，說明 `Issue → branch → PR → CI → merge` 的標準流程。

從本週開始，所有功能開發都走 issue-based 分支，PR 合併前必須通過 GitHub Actions CI，`main` 永遠維持可通過測試的狀態。

### Text Report 輸出格式

本週在 reporter 層新增了純文字格式的報告輸出能力。
`src/dataguard/reporter/text_report.py` 新增 `render_text_report()`，接收現有 `Report` dataclass，輸出包含 header、summary 計數、parse error 列表與 validation error 列表的可讀純文字字串。函式介面與既有 `render_json_report()` 刻意保持一致：同樣接受 `report` 與 `limit` 參數，差別只在回傳型別為 `str` 而非 `dict`。

為了讓 CLI 能根據 `--format` 參數選擇渲染器，`src/dataguard/reporter/__init__.py` 新增 `get_report_renderer()` factory 函式。factory 接受 `"json"` 或 `"text"` 字串，回傳對應的渲染函式，未來若需新增其他輸出格式，只需在 factory 中新增一個分支，不需修改 CLI。

在 CLI 端，`validate` 與 `clean` 的 `--format` 選項從只接受 `"json"` 擴充為 `click.Choice(["json", "text"])`，`json` 維持為預設值，確保現有行為不變。兩個 command 的渲染邏輯也改由 factory 統一分派，JSON 格式的報告透過 `json.dumps()` 序列化後寫檔，text 格式則直接寫入純文字字串。

### Field Mapping Transformer

本週在 transformer 層新增了 `field_map` 操作，補上了目前 transformer 唯一缺少的欄位結構控制能力。
`src/dataguard/transformer/field_map.py` 的 `field_map()` 函式支援兩個子操作：`rename` 依照 key-value 對應把欄位名稱改為目標名稱；`drop` 依照列表把指定欄位從每筆 record 中移除。兩者可以在同一個 transform step 中一起使用。設計上，`field_map` 延續現有 transformer 的純函式、record-based 風格，不產生 side effect，也不修改傳入的原始 records。

在 engine 端，`src/dataguard/transformer/engine.py` 的 registry 新增 `"field_map": field_map` 一行，讓 `clean` 可以直接在 YAML transforms config 中使用 `field_map` 操作，與 `type_cast`、`fill_missing`、`dedup` 排列組合。

---

## Week 12 Development Method

Week 12 的所有功能開發都遵循本週建立的 GitHub 工作流程：先開 Issue 描述需求，建立 `issue-<number>-<description>` 格式的分支，完成後開 PR 並使用 PR template 填寫說明，CI 通過後 merge 回 `main`。

在開發節奏上，本週延續測試驅動的小步提交。
Text report 的開發路徑是：先寫 6 個失敗的 unit tests 確認 `render_text_report()` 尚不存在，再實作最小版本使其通過，接著新增 factory、修改 CLI，最後補整合測試。Field map 的開發路徑是：先寫 9 個失敗的 unit tests 涵蓋 rename、drop、兩者組合、邊界情況與 engine 整合，再實作 `field_map.py`、更新 registry，最後以整合測試從 CLI 入口驗證完整 clean flow。

兩個功能都在 unit tests 轉為 green 後才修改 CLI 或整合測試，確保每一步都有可觀察的進展標誌。

---

## Software Testing Methods Used in Week 12

本週仍以測試驅動開發（TDD）作為主要方法。
`render_text_report()` 與 `field_map()` 都在實作存在之前先由測試描述預期行為，並確認測試在 module 缺失時以 `ModuleNotFoundError` 或 `ImportError` 正確失敗，再完成最小實作使其通過。

在單元測試設計上，`test_text_report.py` 以六個獨立測試分別確認輸出包含 source 與 schema 資訊、summary 計數、parse error 詳細內容、validation error 詳細內容，以及回傳型別為 `str`。`test_field_map.py` 則以九個測試覆蓋 rename 單欄位、rename 多欄位、drop 單欄位、drop 多欄位、rename 與 drop 同時使用、來源欄位不存在時的靜默略過、drop 欄位不存在時的靜默略過、不修改原始 records，以及透過 engine 的 end-to-end 行為。

整合測試方面，本週新增四個案例：`validate` 的 `--format text` 輸出與含錯誤時的文字報告，`clean` 的 `--format text` 輸出，以及 `clean` 使用 `field_map` 對欄位重命名與刪除的完整流程。整合測試使用專用 fixture（`csv_field_map_valid.csv` 與 `field_map_transforms.yaml`）確認從 CLI 入口到 output file 的完整路徑。

最後，Week 12 Regression Check 執行完整 pytest 確認本週所有新功能沒有破壞 Week 8 到 Week 11 已建立的任何能力。

---

## Week 12 Validation Results

本週 Regression Check 使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`

測試結果為：
- `100 passed`
- Coverage `95%`

和 Week 11 的 `82 passed` 相比，Week 12 新增了 18 個測試：6 個 text report unit tests、9 個 field map unit tests（含 1 個 engine 整合），以及 3 個 CLI integration tests（validate text format × 2、clean text format × 1）與 1 個 clean field map integration test。所有既有測試維持通過，無 regression。

---

## Current Week 12 Status

就 Week 12 的目標而言，計畫中的四個 task 全部完成。

目前專案已具備：
- `main` 為預設整合分支，CI 在 PR 時自動執行
- PR template 與 Issue template
- 標準化的 `Issue → branch → PR → CI → merge` 開發流程
- `validate` 與 `clean` 支援 `--format json|text` 報告輸出
- `get_report_renderer()` factory 可依格式選擇 reporter
- `field_map` transformer 操作，支援欄位 rename 與 drop
- 100 個自動化測試，覆蓋率 95%

Week 12 的成果可以分兩個角度來看。從流程角度，這是第一週正式走完完整 GitHub 工作流程的開發，Issue 追蹤需求、PR 追蹤變更、CI 保護 `main`，這套流程在本週已確立。從功能角度，text report 讓使用者可以在 terminal 直接閱讀驗證結果，field map 讓 `clean` 能在驗證前先修正欄位名稱不符的問題，兩者都在不改動核心架構的前提下擴充了既有能力。
