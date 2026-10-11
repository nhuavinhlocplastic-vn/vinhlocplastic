# Vĩnh Lộc Plastic — website demo nhiều trang

Website tĩnh gồm 13 trang. Header, footer và menu dùng chung cho mọi trang; nội dung được sinh sẵn trong HTML, nên Google đọc được mà không cần chạy JavaScript.

## Các trang và đường dẫn

| Trang | URL |
|---|---|
| Trang chủ | `/` |
| Giới thiệu (Về chúng tôi, Hành trình, Khách hàng, Tầm nhìn & cam kết, Thông tin doanh nghiệp) | `/gioi-thieu/` |
| Tất cả sản phẩm | `/san-pham/` |
| Túi hút chân không PA/PE | `/san-pham/tui-hut-chan-khong-pa-pe/` |
| Bao bì thực phẩm | `/san-pham/bao-bi-thuc-pham/` |
| Bao bì nông sản | `/san-pham/bao-bi-nong-san/` |
| Bao bì công nghiệp | `/san-pham/bao-bi-cong-nghiep/` |
| Giải pháp (Nông sản, Thực phẩm, Đông lạnh, Công nghiệp, Quy trình) | `/giai-phap/` |
| Tin tức | `/tin-tuc/` |
| Túi PA/PE là gì? | `/tin-tuc/tui-pa-pe-la-gi/` |
| Chọn độ dày túi hút chân không | `/tin-tuc/chon-do-day-tui-hut-chan-khong/` |
| Bảo quản nông sản khô | `/tin-tuc/bao-quan-nong-san-kho/` |
| Liên hệ (thông tin, bản đồ, form báo giá) | `/lien-he/` |

Mọi mục menu đều mở trang riêng. Mỗi mục trong menu "Sản phẩm" mở trang danh mục của nó.

**Thêm bài viết:** thêm một mục vào `NEWS` trong `data.py` (slug, ngày, tiêu đề, tóm tắt, nội dung), chạy lại `python3 build.py`; trang bài viết, danh sách tin tức và sitemap tự cập nhật.

**Form liên hệ** hiện chỉ hiện thông báo, chưa gửi đi đâu. Khi lên WordPress, thay bằng Contact Form 7 hoặc WPForms.

## SEO có sẵn trên mỗi trang

- `<title>` và meta description riêng; một thẻ `<h1>` duy nhất.
- `canonical`, Open Graph (chia sẻ Facebook/Zalo hiện đúng tiêu đề, mô tả).
- Breadcrumb hiển thị và dữ liệu cấu trúc `BreadcrumbList`.
- JSON-LD: `Organization` (tên, địa chỉ, điện thoại, email, mã số thuế), `AboutPage`, `CollectionPage`, `BlogPosting` cho bài viết, `ContactPage` kèm `ContactPoint`.
- `sitemap.xml` và `robots.txt` (chỉ có trong bản `public/`).
- Liên kết nội bộ: thẻ sản phẩm trỏ về danh mục, mỗi trang danh mục trỏ sang các danh mục khác.

## Mở website

- **Xem nhanh trên máy:** mở `preview/index.html` bằng trình duyệt (bấm đúp). Các trang dùng tên file `.html` nên chuyển trang được mà không cần server.
- **Đưa lên hosting:** tải toàn bộ nội dung thư mục `public/` lên thư mục gốc của website (thường là `public_html`). Bản này dùng URL đẹp như `/gioi-thieu/`, `/san-pham/bao-bi-nong-san/`.
- **Chạy thử bản public trên máy:** `npm run dev` hoặc `cd public && python3 -m http.server 5173`, rồi mở http://localhost:5173.

Mọi đường dẫn CSS, JS, ảnh và link giữa các trang đều là đường dẫn tương đối, nên giao diện không bị vỡ dù mở từ máy hay đặt website trong thư mục con.

## Sửa nội dung và tạo lại trang

1. Sửa `data.py`: thông tin công ty, danh mục, sản phẩm, tin tức. Đổi `SITE["url"]` thành tên miền chính thức.
2. Chạy `python3 build.py` (tạo `public/`) và `python3 build.py preview` (tạo `preview/`).

## Cấu trúc

```
data.py          # nội dung (sửa ở đây)
build.py         # khuôn trang + sinh HTML, sitemap
assets/css       # tokens.css (hệ màu từ logo) + main.css
assets/js        # tương tác: slider, lọc sản phẩm, tìm kiếm, form, dark mode
assets/img       # logo màu, logo trắng, biểu tượng VL
public/          # website đã sinh, đưa lên hosting
preview/         # bản xem nhanh, mở thẳng file index.html
```

## Khi chuyển sang WordPress

Giữ nguyên đường dẫn để không mất SEO:
- Các trang: `gioi-thieu`, `giai-phap`, `tin-tuc`, `lien-he`. Bài viết: đặt Đường dẫn tĩnh dạng `/tin-tuc/%postname%/`.
- Nếu dùng WooCommerce: vào Cài đặt → Đường dẫn tĩnh, đặt "Cơ sở danh mục sản phẩm" là `san-pham`. Slug từng danh mục lấy theo bảng trên.
