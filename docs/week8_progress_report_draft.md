# Week 8 Progress Report Draft

## Week 8 Progress Focus

Week 8 的核心目標不是新增新的 CLI 流程，而是延續 Week 7 已完成的 `validate` 最小垂直切片，進一步把這條流程做厚、做完整。  
如果說 Week 7 的成果是先把 `validate` 從 0 做到 1，證明 parser、schema、validator、reporter 與 CLI 可以形成一條可運作的端到端路徑，那麼 Week 8 的工作重點，就是把這條既有流程從「最小可跑」提升到「更完整、可展示、可驗證」的版本。

本週的主要工作可分成兩個層次。第一個層次是擴充驗證規則本身，讓 `validate` 不再只支援最小的 `string` 與 `integer` 驗證，而是開始具備更接近真實資料檢查需求的能力。第二個層次則是補足流程完整性，也就是不只驗證欄位規則，還要把 schema strictness、parse errors、CLI error handling 與 edge-case integration 一起納入，讓 `validate` 更接近一個可收斂、可交付的功能。

## Week 8 Completed Functionality

本週已完成的規則擴充包括四類 validator。  
首先，在字串驗證部分，專案新增了 `min_length` 與 `max_length`，使 `string` validator 不只檢查 pattern，也能檢查長度邊界。其次，新增了 `enum` validator，可使用 schema 中的 `values` 檢查欄位值是否落在允許集合內。第三，新增了 `boolean` validator，可依照 `true_values` 與 `false_values` 驗證常見布林表示法。第四，新增了 `date format` 驗證，目前先採固定日期格式的最小可用版本，用來檢查日期字串是否符合預期格式。

除了 validator 本身，本週也補強了 validation engine 的行為。  
現在 `required` 錯誤具有優先順序，當欄位缺失或值為空時，不會再重複產生次要型別錯誤。對 optional 欄位而言，若值為空，則直接略過型別驗證，不會因為沒有值而錯誤地被判定為 invalid。這些行為讓驗證結果更一致，也讓錯誤訊息更接近實際使用者對資料驗證的直覺。

更重要的是，本週也把 `validate` 的整體流程補得更完整。  
首先，`strict: true` 現在已經真正生效，當輸入資料出現 schema 未定義欄位時，系統會回報 `UNKNOWN_COLUMN`。其次，parser 在處理輸入時產生的 parse errors，現在不再只是內部資訊，而是會整合進最終 JSON report，讓使用者能同時看到 parse-level 與 validation-level 的問題。報告 summary 也因此新增了 `parse_error_count` 與 `validation_error_count` 等資訊，使報告本身更完整、更適合展示。

本週也補強了 CLI / schema / input error handling。  
目前 `validate` 已可對 unsupported input format、missing input file、missing schema file、invalid schema 與 invalid JSON input 提供較清楚的錯誤輸出，而不是只讓底層例外直接暴露。這一點雖然不屬於新的資料規則，但對整體功能完整性非常重要，因為它決定了這個命令列工具在異常情況下是否仍然具備可預期、可理解的行為。

## Week 8 Development Method

Week 8 延續了 Week 7 的開發模式，也就是以測試驅動開發（TDD）作為主要節奏，並維持小步、可驗證、可提交的 commit 風格。  
本週每一個功能切片都盡量遵守 `test -> feat` 的順序：先建立 failing tests，確認失敗原因正確，再補上最小實作，最後回跑整體測試確認沒有產生回歸。這使得本週的 GitHub 歷史不只是紀錄程式碼變化，而是能清楚反映每一個功能能力是如何被測試驅動出來的。

從本週新增的 commit 來看，提交內容大致可以分成三段。  
第一段是 validator 擴充，包括 string length、enum、boolean 與 date format。第二段是 engine 行為強化與 schema/fixture/integration coverage 的補足。第三段則是進一步收斂 `validate` 的完整性，也就是 strict schema、parse error reporting、CLI/schema/input error handling，以及 edge-case integration coverage。這樣的節奏與 Week 7 的模式一致，差別只在於 Week 7 是先建立骨架，而 Week 8 是在既有骨架上逐步做厚。

## Software Testing Methods Used in Week 8

本週實作仍以軟體測試方法為主軸，而不是先做功能再補測試。  
第一，測試驅動開發（TDD）仍然是最核心的方法。每當新增一個 validator 或補一個引擎行為，就先用 failing tests 明確定義預期行為，再撰寫最小實作通過測試。  
第二，等價類別測試（Equivalence Class Testing）被用在 enum、boolean、date format 等規則，將輸入區分為 valid、invalid 與 optional/empty 類別。  
第三，邊界值測試（Boundary Value Testing）被用在 `min_length` 與 `max_length`。  
第四，輸入空間切分（Input Space Partitioning）被用在 CSV、JSON、JSONL 三種輸入格式，以及 valid / invalid / edge fixtures 的安排。  
第五，整合測試（Integration Testing）則用來驗證 parser、schema、validator、engine、reporter 與 CLI 是否能協同工作，尤其是在 JSONL bad line、strict unknown column 等較複雜情境下仍能輸出正確報告。  
最後，每完成一組小功能後都重新執行整套 pytest，將回歸測試（Regression Testing）當作固定步驟，而不是開發最後才做的事情。

## Week 8 Validation Results

本週最新一次整體驗證使用：

`UV_CACHE_DIR=/tmp/uv-cache uv run pytest -q`

測試結果為：
- `46 passed`
- Coverage `98%`

與 Week 7 相比，Week 8 的測試數量與覆蓋的行為都明顯增加。這代表專案不只是多了幾個 validator，而是把 `validate` 這條流程的規則能力、錯誤處理與 edge-case 覆蓋都一起提升了。

## Current Week 8 Status

就 Week 8 的目標而言，本週的 `validate` 強化已經達到一個相對完整的里程碑。  
目前 `validate` 已不只支援最小輸入解析與最小 schema 驗證，而是已具備：
- 更完整的 validator 集合
- 更穩定的 engine 行為
- strict schema unknown-column 檢查
- parse errors 與 validation errors 的整合報表
- 更完整的 CLI / schema / input error handling
- 更完整的 edge-case integration coverage

因此，Week 8 的成果可以被視為把 Week 7 的基線進一步做厚。  
Week 7 的主要價值是建立最小可展示基線；Week 8 的主要價值則是讓這條既有流程更像一個真正可用、可驗證、可延伸的核心功能。這也表示後續如果要進入 `clean`、`convert` 或其他更完整流程時，專案已經有一條更穩定的 `validate` 路徑可作為基礎。
