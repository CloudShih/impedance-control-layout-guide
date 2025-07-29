# GUI樣式問題 - PyQt5表格標頭顯示異常

## 問題敘述
在Windows系統下，PyQt5的QTableWidget表格標頭顯示為白底白字，無法辨識。同時出現"UpdateLayeredWindowIndirect failed"錯誤，表明存在Windows特定的渲染問題。

## 思考過程
1. **初步分析**：以為是單純的CSS樣式設定問題
2. **逐步嘗試**：從個別元件樣式設定到全域樣式
3. **深入調查**：發現主程式中有全域樣式覆蓋問題
4. **協作分析**：與GEMINI討論Windows PyQt5特殊問題
5. **實驗驗證**：嘗試QPalette方法但導致更嚴重問題

## 可能的解決方案列表
1. ✅ **修改個別QHeaderView樣式** - 無效，被全域樣式覆蓋
2. ✅ **設定QTableWidget::corner樣式** - 無效，Windows渲染問題
3. ✅ **在全域樣式中加入表格樣式** - 無效，樣式衝突
4. ❌ **使用QPalette程式化設定** - 反而導致更嚴重的白底白字
5. ⏳ **移除全域樣式衝突並使用精確選擇器** - 當前嘗試中

## 已完成驗證的方案
### 方案1：個別元件樣式設定
```python
header.setStyleSheet("QHeaderView::section { background-color: #404040; color: white; ... }")
```
**結果**：無效，被apply_dark_theme()的全域樣式覆蓋

### 方案2：全域樣式加入表格規則
```css
QTableWidget QHeaderView::section {
    background-color: #404040;
    color: white;
    font-weight: bold;
}
```
**結果**：CSS語法正確但在Windows上無效

### 方案3：QPalette程式化設定
```python
header_palette = QPalette()
header_palette.setColor(QPalette.Button, QColor(64, 64, 64))
header.setPalette(header_palette)
```
**結果**：導致整個信號規則區域變成白底白字，問題惡化

## 驗證成功與失敗代表的意義
- **CSS樣式失效**：表明Windows PyQt5對QHeaderView的CSS支援有限制
- **QPalette反效果**：說明調色盤設定會影響整個Widget樹，需要謹慎使用
- **全域樣式衝突**：證實了樣式優先級和繼承的複雜性

## 總結出的注意事項
1. **Windows PyQt5的限制**：某些Widget的樣式在Windows上可能無法通過CSS正常設定
2. **QPalette的副作用**：程式化調色盤設定可能影響父子Widget的顯示
3. **全域樣式的雙面性**：既能統一主題又可能覆蓋局部自定義
4. **UpdateLayeredWindowIndirect錯誤**：這是症狀不是根因，通常表示渲染衝突
5. **樣式設定的順序**：子元件樣式必須在父元件全域樣式之後設定才有效

## 後續建議
1. 考慮使用自定義Widget繼承QHeaderView並重寫paintEvent
2. 或者接受系統預設樣式，專注於功能實現
3. 在不同作業系統上測試樣式相容性
4. 建立樣式測試用例避免類似問題重複發生

## 時間記錄
- 問題發現：2025-07-29
- 調查時間：約2小時
- 嘗試方案：5種
- 當前狀態：尚未完全解決，但已排除多種無效方案