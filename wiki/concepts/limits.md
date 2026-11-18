# RAG 的限制

- **檢索品質**。索引可能漏掉關鍵證據，或回傳錯誤、冗餘及互相矛盾的內容。 [S02 §§III-B、VII-B](../sources/S02.md)
- **生成忠實性**。檢索到片段後，仍需評估回答中的主張是否得到這些片段支持。 [S02 §VI-C.1](../sources/S02.md)
- **維護與權限**。更新文件後需要同步維護索引，私人文件的檢索須依使用者權限控制，並在速度與搜尋深度間取捨。 [S04「Update external data」](../sources/S04.md) · [S05「The challenges of RAG」](../sources/S05.md)

## 來源觀察差異

- [S02 §§IV-A、VII-B](../sources/S02.md) 提醒冗餘或矛盾資料可能有害，也轉述特定研究中加入無關資料意外提升準確率的結果。
- [S05「Solving token constraint challenges」](../sources/S05.md) 在其產品情境強調回傳少量高相關片段與限制結果數量。

## 延伸閱讀

- [回 Wiki 索引](../index.md)
- [LLM 的限制](llm-limits.md)
- [Retrieval（檢索）](retrieval.md)
- [Generation（生成）](generation.md)
