可用skill: https://github.com/lewislulu/html-ppt-skill


# GitHub Pages 網頁化討論紀錄

紀錄日期：2026-06-02
議題：將 DataGuard 期末簡報轉換為靜態 HTML 網頁並部署至 GitHub Pages

---

## 一、技術可行性評估

**結論：完全可行。**

- Repo：`github.com/Hayward5/DataGuard`
- 部署後 URL：`https://hayward5.github.io/DataGuard/`
- 現有 GitHub Actions CI 可直接延伸加入 Pages deploy workflow
- 靜態 HTML + CSS + JS 符合 GitHub Pages 限制，不需要伺服器

---

## 二、呈現方式選擇

### 選項 A：簡報模式（Reveal.js）
- 瀏覽器裡是投影片，按空白鍵換頁
- 可直接現場報告（接投影機）
- 支援 speaker notes、列印成 PDF
- 缺點：不適合瀏覽閱讀，ASCII art 需特殊處理

### 選項 B：滾動式單頁網站（Pure HTML/CSS）✅ 已選定
- 像 portfolio/文件頁面，從上往下滾動
- 分享連結體驗好，不需進入簡報模式
- 視覺設計自由度高
- 更像 project showcase，有加分效果
- 缺點：不適合現場報告

**決定：使用選項 B（滾動式單頁網站），PPTX 用於現場報告，HTML 版作為 GitHub Pages 永久展示頁。**

---

## 三、框架選擇評估

### 選項 1：Pure HTML + CSS + 輕量 JS 套件（全 CDN）
- AOS、GSAP、Prism.js
- 零 build step，直接 push HTML
- 無法做複雜互動（tab 切換、狀態管理）

### 選項 2：HTML + Alpine.js（全 CDN，無 build）✅ 已選定
- Alpine.js（15KB）加上 AOS、GSAP、Prism.js
- 仍是零 build step
- 可以做 tab 切換、展開收合、toggle 等互動
- 覆蓋所有需求，工程量合理

### 選項 3：React/Vue + Vite（需要 build pipeline）
- 最強動畫能力（Framer Motion）
- 需要 GitHub Actions 跑 npm run build
- 對一頁靜態展示頁工程量過重，不採用

---

## 四、最終技術組合

```
Alpine.js (15KB, CDN)   → 所有互動狀態管理（tab、toggle、展開收合）
GSAP (CDN)              → Transformer pipeline 動畫、複雜 timeline
AOS (CDN)               → Section 滾動進場動畫
CountUp.js (CDN)        → 測試數字計數動畫（82 → 178）
Typed.js (CDN)          → Demo 打字機 CLI 指令效果
Prism.js (CDN)          → 所有 code block 語法高亮
tsParticles (CDN)       → 標題 hero 背景粒子（可選，輕量）
```

全部使用 CDN，不需要 build step，部署維持最簡單。

---

## 五、互動元素規劃清單

### 層次 1：全頁通用元素

| 元素 | 說明 | 技術 |
|---|---|---|
| 頂部滾動進度條 | 頁面頂部細線隨滾動填滿 | Pure CSS + Intersection Observer |
| 固定側邊導覽點 | 右側 12 個圓點，當前 section 放大顯示名稱，可點擊跳頁 | Alpine.js + Intersection Observer |
| 深色/淺色模式切換 | 右上角切換鈕（☀/🌙） | Alpine.js + CSS custom properties |

### 層次 2：各 Slide 專屬互動

| Slide | 互動設計 | 技術 |
|---|---|---|
| Slide 2（Before/After） | Toggle 撥動開關切換 Week 11 / Final 內容 | Alpine.js x-show + CSS transition |
| Slide 4（CLI Reference） | Validate / Clean / Convert 三個 Tab 切換 + Copy 按鈕 | Alpine.js tabs + Clipboard API |
| Slide 5（Architecture） | 七個模組卡片，懸停顯示說明和檔案路徑，點擊展開函式清單 | Alpine.js x-data + CSS hover |
| Slide 7（Transformer Pipeline） | **「▶ Run Pipeline」按鈕**：一筆髒資料逐步經過五個 transformer，每步高亮並顯示改變內容（詳見下方） | Alpine.js + GSAP timeline |
| Slide 8（Reporting） | JSON Report / Text Report Tab 切換，內容交叉淡入 | Alpine.js tabs |
| Slide 9（Testing）| 178 數字滾動進視野時從 0 計數到 178；97% 進度條從 0 填滿；時間軸逐步顯示 | CountUp.js + Intersection Observer |
| Slide 10（Demo） | 三個 Demo Tab 切換 + 打字機效果（指令逐字出現） | Typed.js + Alpine.js tabs |
| Slide 11（Lessons Learned） | 五張卡片 3D 翻轉（正面標題，翻轉後顯示詳細說明） | Pure CSS 3D transform |

### 層次 3：視覺動畫增強

| 效果 | 用在哪 | 技術 |
|---|---|---|
| 滾動進場 fade-up | 所有 section | AOS |
| 標題文字逐字浮現 | Slide 1 hero section | CSS animation `steps()` |
| 背景粒子（極淡） | Slide 1 標題背景 | tsParticles（可選） |
| 模組連線動態繪製 | Slide 5 架構圖 | SVG stroke-dashoffset animation |
| ✅ 打勾動畫 | Slide 3 Horizon 卡片 | CSS SVG checkmark animation |

---

## 六、Slide 7 Transformer Pipeline 動畫（重點設計）

這是工程量最大的互動元素（估計佔整體開發時間 30%），但也是最有說服力的展示。

**設計概念：**

一筆示範髒資料：
```json
{ "emp_id": "E001", "join_date": "2024/01/15", "age": "", "notes": "test" }
```

頁面上方顯示五個 transformer 步驟：
`field_map` → `dedup` → `date_format` → `fill_missing` → `type_cast`

點擊「▶ Run Pipeline」按鈕後，資料逐步通過每個步驟，每步高亮並顯示變化：

```
field_map    → emp_id 改名為 employee_id，notes 欄位消失
dedup        → （無重複，略過）
date_format  → join_date: "2024/01/15" → "2024-01-15"
fill_missing → age: "" → 填入前一筆值 "28"
type_cast    → age: "28" → 28 (integer)
```

最終輸出乾淨的 record。

**尚未決定**：這個動畫是否納入實作範圍（工程量最重）。

---

## 七、尚未決定的事項（下次討論需確認）

### 1. 設計風格方向（最重要）

| 風格 | 說明 | 適合情境 |
|---|---|---|
| 延續進度報告風格 | 淡藍白底色、優雅線條，與 NotebookLM 進度報告視覺一致 | 希望兩份報告風格統一 |
| CLI 工具風格 | 深色底、終端機配色、程式碼區塊為主視覺 | 強調「這是一個開發工具」，與進度報告有清楚視覺區隔 |

### 2. Slide 7 Transformer Pipeline 動畫

是否值得花 30% 開發時間做這個互動？
- 做：最有說服力的技術展示
- 不做：節省工程量，改用靜態 pipeline 圖加上動態進場動畫

### 3. 語言顯示策略

網頁內容是中英混合（技術術語英文、說明文字中文）或全中文或全英文？

---

## 八、GitHub Pages 部署方式

目前計畫：
- HTML 放在 `docs/` 資料夾或獨立的 `gh-pages` branch
- 在 GitHub Settings → Pages 開啟，選擇來源
- 現有 CI workflow (`ci.yml`) 不需修改，只需另外新增 `pages.yml`

---

## 九、待辦（下次討論時處理）

- [ ] 確認設計風格方向（深色 CLI 風 vs 淺色延續風）
- [ ] 確認 Transformer Pipeline 動畫是否納入範圍
- [ ] 確認語言顯示策略
- [ ] 確認上述三點後，開始規劃完整的實作計畫
