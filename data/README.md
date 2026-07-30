# 📑 README - Báo Cáo Giải Thích Tập Dữ Liệu Tài Chính (`financial_statement_normalized.csv`)

Tập file `sample_financial_data.csv` chứa dữ liệu báo cáo tài chính đã được thu thập, làm sạch và chuẩn hóa quy tắc dấu (Sign Normalization) phục vụ cho các ứng dụng phân tích tài chính, đánh giá sức khỏe doanh nghiệp và tích hợp vào hệ thống AI/Dashboard.

---

## 1. 📌 Nguồn Dữ Liệu (Data Source)
* **Nguồn thu thập:** Dữ liệu được trích xuất từ **Báo cáo tài chính (BCTC)** công khai của các công ty niêm yết trên thị trường chứng khoán Việt Nam (HOSE/HNX).
* **Phương thức thu thập & xử lý:** Thu thập tự động/bán tự động qua bộ cào dữ liệu (web scraper), sau đó được xử lý qua đường ống chuẩn hóa (Data Pipeline) để quy đổi đơn vị, xử lý giá trị âm/dương và gắn nhãn mã chỉ tiêu quy chuẩn.

---

## 2. 📋 Ý Nghĩa Các Cột (Data Dictionary)

| Tên Cột (Field Name) | Kiểu Dữ Liệu | Ý Nghĩa / Giải Thích Detail |
| :--- | :--- | :--- |
| `ticker` | String | Mã cổ phiếu/Mã niêm yết của doanh nghiệp (vd: `HPG`, `FPT`, `VNM`, `BMP`...) |
| `fiscal_year` | Integer | Năm tài chính của báo cáo (2022, 2023, 2024, 2025) |
| `statement_type` | String | Loại báo cáo tài chính (`balance_sheet`: Bảng cân đối kế toán, `income_statement`: Kết quả kinh doanh, `cash_flow`: Lưu chuyển tiền tệ) |
| `item_id` | String | Mã định danh chuẩn hóa của chỉ tiêu tài chính (vd: `bsa1`, `isa10`...) |
| `item_name_vi` | String | Tên đầy đủ của chỉ tiêu tài chính bằng **Tiếng Việt** |
| `item_name_en` | String | Tên đầy đủ của chỉ tiêu tài chính bằng **Tiếng Anh** |
| `raw_value` | Float | Giá trị nguyên bản thu thập được từ báo cáo gốc |
| `currency` | String | Loại tiền tệ gốc ghi nhận trên báo cáo |
| `value_vnd` | Float | Giá trị đã được quy đổi chính thức về đơn vị **VND** |
| `audit_status` | String | Trạng thái kiểm toán của báo cáo (`audited`: Đã kiểm toán, `unaudited`: Chưa kiểm toán/Tự lập) |
| `collected_at` | String | Ngày/Giờ hệ thống thu thập và đưa dữ liệu vào kho |
| `sign_rule_x` / `sign_rule_y` | String | Quy tắc xử lý dấu tài chính áp dụng cho chỉ tiêu (`always_positive`, `contra_asset`, `signed`, `expense_negative`) |
| `value_processor` | Float | Giá trị số sau khi đã qua bộ xử lý chuẩn hóa dấu (dùng trực tiếp cho tính toán/mô hình toán) |
| `value_status` | String | Trạng thái của giá trị chỉ tiêu (`reported`: Có ghi nhận số liệu, `zero_reported`: Báo cáo bằng 0) |

---

## 3. 📏 Đơn Vị (Units of Measurement)
* **Đơn vị tiền tệ:** Đồng Việt Nam (**VND**). Tất cả các giá trị tại cột `value_vnd` và `value_processor` đều được tính theo mệnh giá VND tuyệt đối (không rút gọn theo triệu hay tỷ đồng để tránh sai số khi tính toán).
* **Đơn vị thời gian:** Năm tài chính (**Fiscal Year**).

---

## 4. 🌐 Phạm Vi (Scope & Coverage)
* **Quy mô doanh nghiệp:** Gồm **21 doanh nghiệp niêm yết lớn** đại diện cho nhiều ngành nghề tại Việt Nam (Thép, Bất động sản, Công nghệ, Bán lẻ, Hàng không, Dược phẩm...):  
  `BMP`, `CTD`, `DGC`, `DHG`, `DXG`, `FPT`, `GAS`, `HBC`, `HPG`, `HVN`, `KBC`, `MSN`, `MWG`, `NVL`, `PDR`, `POM`, `REE`, `SAB`, `TTF`, `VJC`, `VNM`.
* **Khung thời gian:** Từ năm **2022** đến năm **2025**.
* **Tổng số bản ghi:** `15,792` dòng dữ liệu chi tiết.

---

## 5. 🔍 Dữ Liệu Mẫu Hay Dữ Liệu Thật? (Data Authenticity)
* **Loại dữ liệu:** **DỮ LIỆU THẬT 100% (Real Financial Data)**.
* Số liệu được trích xuất trực tiếp từ các Báo cáo tài chính đã qua kiểm toán (`audited`) và báo cáo niêm yết chính thức của các doanh nghiệp trên sàn chứng khoán Việt Nam, không phải dữ liệu giả lập (mock data) hay ngẫu nhiên.

---

## 6. ⚠️ Điều Kiện Sử Dụng (Terms & Conditions of Use)
* **Mục đích sử dụng:**
  * Dữ liệu được phép sử dụng cho mục đích **nghiên cứu học thuật, phân tích tài chính, thử nghiệm mô hình AI/Machine Learning** và làm **dữ liệu đầu vào cho các ứng dụng Dashboard/Web App**.
* **Khuyến cáo rủi ro:**
  * Dữ liệu phục vụ mục đích tham khảo và phân tích kỹ thuật.
  * Không sử dụng dữ liệu này làm tư vấn đầu tư tài chính trực tiếp hoặc cam kết pháp lý mà không qua xác minh lại với BCTC gốc công bố trên SSC/HOSE/HNX.
* **Bản quyền & Truy xuất:**
  * Dữ liệu trích xuất từ thông tin công khai của các công ty đại chúng. Khi trích dẫn hoặc xuất bản lại, vui lòng ghi rõ nguồn dữ liệu gốc từ BCTC của doanh nghiệp.

# Thư mục Dữ liệu Mẫu (Data)
Dữ liệu demo là giả lập;
không dùng để đánh giá doanh nghiệp thật;
Dữ liệu huấn luyện chưa được công bố;
Bộ dữ liệu thực tế đang trong quá trình thu thập và chuẩn hóa.
- `demo_companies.json`: Dữ liệu thông tin và các chỉ số tài chính mẫu của một số doanh nghiệp phi tài chính.

