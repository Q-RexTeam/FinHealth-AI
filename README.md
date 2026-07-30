FinHealth AI - Hệ thống AI phân tích sức khỏe tài chính doanh nghiệp



1. Tên và Logo dự án
Tên dự án: FinHealth AI (Financial Intelligence Platform)

Logo dự án: ![FinHealth AI Logo](images/logo.png) 
            
Thông điệp: Nền tảng trí tuệ nhân tạo hỗ trợ đánh giá sức khỏe tài chính và cảnh báo rủi ro doanh nghiệp tự động, minh bạch.

---

2. Mô tả bài toán
Hiện nay, việc phân tích báo cáo tài chính (BCTC) truyền thống tốn nhiều thời gian và dễ mang tính chủ quan. FinHealth AI được phát triển nhằm tự động hóa quá trình phân tích BCTC, chấm điểm sức khỏe tài chính chuẩn hóa và dự báo sớm khả năng xuất hiện sự kiện suy giảm hoặc cảnh báo tài chính trong 12 tháng tiếp theo.

Phạm vi doanh nghiệp: Tập trung vào các doanh nghiệp phi tài chính đang niêm yết hoặc có đăng ký giao dịch (không áp dụng cho Ngân hàng, Chứng khoán, Bảo hiểm do sự khác biệt về cấu trúc BCTC).

Kỳ dự báo: 12 tháng tiếp theo.

Phạm vi dữ liệu: Dữ liệu BCTC theo năm, thu thập trong giai đoạn 2017 – 2025 nhằm đảm bảo tính xu hướng và độ dày của tập huấn luyện.

---

3. Đối tượng sử dụng & Quyết định được hỗ trợ

Hệ thống hướng tới các chuyên gia tài chính với các quyết định hỗ trợ thực tiễn:

Chuyên viên tín dụng (Ngân hàng / Tổ chức tài chính) Phê duyệt hoặc từ chối cấp tín dụng mới. Điều chỉnh định mức tín dụng. Đưa doanh nghiệp vào danh sách kiểm soát/cảnh báo rủi ro định kỳ. 

Nhà đầu tư (Cá nhân / Tổ chức). Tối ưu quyết định mua, bán hoặc nắm giữ cổ phiếu. Cấu trúc lại danh mục đầu tư để hạn chế rủi ro từ doanh nghiệp suy yếu. 

Kiểm toán viên & Nhà quản trị. Sử dụng như công cụ tham khảo chéo và tự đánh giá sức khỏe tài chính nội bộ. 

---

4. Các chức năng chính
Phân tích toàn diện & Chấm điểm tự động: Đánh giá sức khỏe tài chính (*Financial Health Score*) theo chuẩn 5 nhóm tiêu chí (Thanh toán, Đòn bẩy, Sinh lời, Dòng tiền, Hiệu quả hoạt động).

Cảnh báo rủi ro sớm: Dự báo xác suất rủi ro trong 12 tháng tới, giúp phát hiện sớm dấu hiệu khủng hoảng.

Tính minh bạch (Explainable AI - XAI): Giải thích chi tiết các yếu tố ảnh hưởng đến kết quả dự báo (ví dụ: Dòng tiền âm, nợ tăng nhanh...).

Phân tích tương quan & Giả định (What-if): So sánh doanh nghiệp với vị thế trung vị cùng ngành và mô phỏng kịch bản giả định.

Trợ lý AI & Báo cáo tự động: Trợ lý thông minh hỗ trợ hỏi đáp trực tiếp trên dữ liệu doanh nghiệp và xuất báo cáo PDF tự động.

---

5. Sơ đồ giải pháp
![FinHealth AI Logo](images/SoDoGiaiPhap.png)

6. Ảnh chụp dashboard dự kiến
![FinHealth AI Logo](images/GiaoDien.png)

7. Link demo

GitHub: 

8. Nguồn dữ liệu dự kiến

Dữ liệu Báo cáo Tài chính kiểm toán hàng năm của các doanh nghiệp phi tài chính niêm yết trên các sàn HOSE, HNX và UPCoM.

Giai đoạn thu thập: 2017 – 2025.

9. Phương pháp Machine Learning

Dự báo rủi ro (Supervised Learning): Sử dụng các mô hình học máy phân lớp như XGBoost, Random Forest, LightGBM để tính xác suất rủi ro tài chính 12 tháng.

Giải thích mô hình (XAI): Áp dụng SHAP (SHapley Additive exPlanations) để minh bạch hóa các biến số đóng góp vào điểm rủi ro.

Trợ lý AI (LLM + RAG): Kết hợp mô hình ngôn ngữ lớn (LLM) và kỹ thuật RAG để truy xuất thông tin từ BCTC.

10. Công nghệ sử dụng 

Frontend Demo: HTML5, CSS3, JavaScript (Pure Native)

Thư viện UI/Icon: Lucide Icons, Google Fonts (Plus Jakarta Sans)

Biểu đồ: ApexCharts

Deployment: GitHub Pages

11. Trạng thái hiện tại

[x] Đã hoàn thành bản mockup tương tác của màn hình lựa chọn doanh nghiệp và Dashboard tổng quan.

[x] Đã xây dựng 15 hồ sơ doanh nghiệp giả lập được khai báo trong frontend để kiểm thử chức năng tìm kiếm, chuyển đổi doanh nghiệp và trực quan hóa giao diện. Các số liệu chỉ dùng để minh họa và chưa phải kết quả của mô hình học máy.

[x] Hoàn thiện các luồng tương tác: Tìm kiếm doanh nghiệp, Tải tệp BCTC, Biểu đồ xu hướng, Trợ lý AI mô phỏng.

12. Kế hoạch phát triển Vòng 2

Kết nối Frontend với Backend (FastAPI/Python).

Huấn luyện và tích hợp mô hình Machine Learning thực tế trên tập dữ liệu 2017–2025.

Mở rộng pipeline RAG để tự động đọc và phân tích file BCTC dạng PDF.

Hoàn thiện chức năng Xuất báo cáo đánh giá định dạng PDF.

13. Hướng dẫn chạy thử: [Xem hướng dẫn chạy thử (PDF)](./docs/Hướng dẫn chạy thử.pdf)

Truy cập đường link sau: .docs/Hướng dẫn chạy thử.pdf

14. Thành viên và phân công

| STT |    Họ và Tên      |        Vai trò         |          Nhiệm vụ chính    |

|   1    |     Trần Bảo Lan     | Trưởng nhóm / Product Owner | Quản lý tiến độ, chốt phạm vi, tổng hợp hồ sơ, điều phối và chuẩn bị pitching |
|   2    | Trần Thị Bảo Yến | Phụ trách Tài chính – Dữ liệu | Nghiên cứu nghiệp vụ, thu thập dữ liệu, chuẩn hóa chỉ tiêu, xây dựng nhãn rủi ro |
|   3    | Đỗ Quốc Khánh | Phụ trách Machine Learning | Xây dựng đặc trưng, huấn luyện mô hình, đánh giá, hiệu chỉnh và XAI |
|   4    | Lương Trung Dương | Phụ trách Backend – Dữ liệu | Xây dựng cơ sở dữ liệu, API, pipeline xử lý file và tích hợp mô hình |
|   5    | Đặng Hải Phi Trường | Phụ trách Frontend – Sản phẩm | Thiết kế giao diện, dashboard, trực quan hóa, kiểm thử trải nghiệm và hỗ trợ slide |

15. Miễn trừ trách nhiệm (Disclaimer)
⚠️ Lưu ý: Kết quả phân tích và dự báo từ hệ thống FinHealth AI chỉ đóng vai trò hỗ trợ thông tin và tham khảo chéo. Hệ thống không thay thế cho quyết định thẩm định chính thức của chuyên gia tài chính hay khuyến nghị đầu tư pháp lý.
