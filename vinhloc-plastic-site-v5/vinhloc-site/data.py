"""Nội dung website Vĩnh Lộc Plastic.

Sửa thông tin công ty, danh mục, sản phẩm, tin tức ở file này rồi chạy:  python3 build.py
"""

SITE = {
    "url": "https://nhuavinhlocplastic.com",   # đổi thành tên miền chính thức
    "name": "Vĩnh Lộc Plastic",
    "legal_name": "Nhựa Vĩnh Lộc Plastic",
    "slogan": "Giải pháp bao bì cho công nghiệp và nông nghiệp",
    "field": "Bao bì PA/PE, túi hút chân không",
    "address": "252 ấp Nhơn Hòa 1, xã Mỹ Hạnh, Tây Ninh",
    "region": "Tây Ninh",
    "phone": "0919643000",
    "phone_display": "0919 643 000",
    "email": "nhuavinhlocplastic@gmail.com",
    "website": "nhuavinhlocplastic.com",
    "tax_id": "312323158",
    "founded": "2013-06-12",
}

# Mỗi danh mục = một trang riêng: /san-pham/<slug>/
CATEGORIES = [
    {
        "slug": "tui-hut-chan-khong-pa-pe",
        "name": "Túi hút chân không PA/PE",
        "short": "Túi hút chân không PA/PE",
        "color": "red",
        "title": "Túi hút chân không PA/PE – Sản xuất theo yêu cầu",
        "desc": "Túi hút chân không PA/PE trơn, in logo, một mặt nhám và dạng cuộn. Vĩnh Lộc Plastic sản xuất trực tiếp tại Tây Ninh, nhận đặt theo kích thước.",
        "lead": "Màng ghép PA/PE kết hợp lớp PA chống thấm khí với lớp PE dễ hàn kín, giữ sản phẩm tươi lâu khi hút chân không. Vĩnh Lộc Plastic nhận sản xuất theo kích thước, độ dày và in logo theo yêu cầu.",
        "uses": ["Thịt, cá, hải sản tươi và đông lạnh", "Giò chả, xúc xích, thực phẩm chế biến sẵn", "Gạo, hạt, nông sản khô cần chống ẩm", "Linh kiện, phụ tùng cần chống oxy hóa"],
        "specs": [("Cấu trúc màng", "PA/PE nhiều lớp"), ("Bề mặt", "Trơn hai mặt hoặc một mặt nhám"), ("Hình thức", "Túi cắt sẵn hoặc dạng cuộn"), ("In ấn", "Trơn hoặc in logo theo yêu cầu")],
    },
    {
        "slug": "bao-bi-thuc-pham",
        "name": "Bao bì thực phẩm",
        "short": "Bao bì thực phẩm",
        "color": "gold",
        "title": "Bao bì thực phẩm – Túi PA/PE cho thực phẩm chế biến",
        "desc": "Bao bì thực phẩm cho bánh tráng, muối tôm, giò chả, xúc xích, thịt và cá đông lạnh. Sản xuất theo kích thước và dây chuyền đóng gói của khách hàng.",
        "lead": "Bao bì cho cơ sở chế biến thực phẩm cần sạch, chắc mối hàn và phù hợp máy đóng gói. Vĩnh Lộc Plastic tư vấn vật liệu và kích thước theo từng mặt hàng, từ đặc sản Tây Ninh đến hàng đông lạnh.",
        "uses": ["Bánh tráng, muối tôm và đặc sản đóng gói", "Giò chả, xúc xích, lạp xưởng", "Thịt, cá cấp đông và vận chuyển lạnh", "Thực phẩm khô, gia vị"],
        "specs": [("Vật liệu", "PA/PE, PE"), ("Kiểu túi", "Túi hút chân không, túi đứng, túi dẹt"), ("Tương thích", "Máy hút chân không, máy hàn miệng túi"), ("In ấn", "Trơn hoặc in nhãn hiệu")],
    },
    {
        "slug": "bao-bi-nong-san",
        "name": "Bao bì nông sản",
        "short": "Bao bì nông sản",
        "color": "rice",
        "title": "Bao bì nông sản – Túi đựng gạo, cà phê, hạt điều",
        "desc": "Bao bì nông sản cho gạo, cà phê hạt, hạt điều và nông sản sấy. Chống ẩm, giữ hương vị, phù hợp đóng gói bán lẻ và xuất khẩu.",
        "lead": "Nông sản khô dễ hút ẩm và mất hương vị nếu bao bì không kín. Túi hút chân không và túi đứng của Vĩnh Lộc Plastic giúp gạo, cà phê, hạt điều giữ chất lượng lâu hơn trên kệ và khi vận chuyển xa.",
        "uses": ["Gạo đóng túi 1–5 kg", "Cà phê hạt và cà phê bột", "Hạt điều, đậu phộng, hạt dinh dưỡng", "Trái cây và nông sản sấy"],
        "specs": [("Vật liệu", "PA/PE, màng ghép"), ("Kiểu túi", "Túi hút chân không, túi đứng có cửa sổ"), ("Khối lượng đóng gói", "Theo yêu cầu, phổ biến 0,5–5 kg"), ("In ấn", "Trơn hoặc in nhãn hiệu")],
    },
    {
        "slug": "bao-bi-cong-nghiep",
        "name": "Bao bì công nghiệp",
        "short": "Bao bì công nghiệp",
        "color": "coal",
        "title": "Bao bì công nghiệp – Túi PE khổ lớn, màng PE cuộn",
        "desc": "Bao bì công nghiệp: túi PE khổ lớn, túi lót thùng carton, màng PE cuộn cho nhà máy và kho vận. Sản xuất số lượng lớn, giao toàn quốc.",
        "lead": "Nhà máy và kho vận cần bao bì bền, đồng đều và giao đúng hẹn. Vĩnh Lộc Plastic cung cấp túi PE khổ lớn, túi lót thùng và màng cuộn với kích thước, độ dày theo dây chuyền của từng khách hàng.",
        "uses": ["Lót thùng carton, bao bọc hàng xuất khẩu", "Đóng gói linh kiện, nguyên liệu", "Che phủ, chống bụi cho hàng lưu kho", "Đóng gói pallet trong kho vận"],
        "specs": [("Vật liệu", "PE"), ("Kiểu sản phẩm", "Túi khổ lớn, túi lót thùng, màng cuộn"), ("Kích thước", "Theo yêu cầu"), ("Số lượng", "Phù hợp đơn hàng nhà máy")],
    },
]

# (tên, slug danh mục, hình minh họa, bảng màu, nhãn, kiểu ruột túi)
PRODUCTS = [
    ("Túi hút chân không PA/PE trơn", "tui-hut-chan-khong-pa-pe", "vacuum", "clear", "Bán chạy", "block"),
    ("Túi hút chân không in logo", "tui-hut-chan-khong-pa-pe", "pouch", "red", "", ""),
    ("Túi PA/PE một mặt nhám", "tui-hut-chan-khong-pa-pe", "vacuum", "red", "", "block"),
    ("Túi PA/PE dạng cuộn", "tui-hut-chan-khong-pa-pe", "roll", "clear", "", ""),
    ("Túi đựng thịt, cá đông lạnh", "bao-bi-thuc-pham", "vacuum", "red", "", "block"),
    ("Túi đựng bánh tráng, muối tôm", "bao-bi-thuc-pham", "pouch", "gold", "Đặc sản Tây Ninh", ""),
    ("Túi đựng giò chả, xúc xích", "bao-bi-thuc-pham", "vacuum", "gold", "", "block"),
    ("Túi đựng gạo 1–5 kg", "bao-bi-nong-san", "vacuum", "rice", "Nông sản", "grain"),
    ("Túi đựng cà phê hạt", "bao-bi-nong-san", "pouch", "coal", "", ""),
    ("Túi đựng hạt điều, nông sản sấy", "bao-bi-nong-san", "vacuum", "gold", "Nông sản", "grain"),
    ("Túi PE công nghiệp khổ lớn", "bao-bi-cong-nghiep", "flat", "coal", "", ""),
    ("Màng PE cuộn đóng gói", "bao-bi-cong-nghiep", "roll", "coal", "", ""),
    ("Túi PE lót thùng carton", "bao-bi-cong-nghiep", "flat", "clear", "", ""),
]

# Giải pháp theo ngành hàng — trang /giai-phap/ (mỗi mục có neo #slug)
SOLUTIONS = [
    {
        "slug": "nong-san", "tag": "Nông sản", "category": "bao-bi-nong-san",
        "title": "Bao bì cho nông sản khô",
        "for": "Gạo, cà phê, hạt điều, nông sản sấy",
        "short": "Túi hút chân không và túi đứng giữ hương vị, chống ẩm mốc cho nông sản khô.",
        "challenge": "Nông sản khô dễ hút ẩm, bị oxy hóa và mất hương vị khi vận chuyển xa hoặc trưng bày lâu trên kệ.",
        "approach": ["Túi hút chân không PA/PE chống ẩm, hạn chế oxy", "Túi đứng có cửa sổ cho hàng bán lẻ",
                     "Kích thước theo khối lượng đóng gói, phổ biến 0,5–5 kg"],
    },
    {
        "slug": "thuc-pham", "tag": "Thực phẩm", "category": "bao-bi-thuc-pham",
        "title": "Bao bì cho thực phẩm chế biến",
        "for": "Bánh tráng, muối tôm, giò chả, xúc xích",
        "short": "Túi PA/PE cho bánh tráng, muối tôm, giò chả, xúc xích và hàng đóng gói sẵn.",
        "challenge": "Thực phẩm chế biến cần bao bì sạch, mối hàn chắc và chạy ổn định trên máy đóng gói của cơ sở sản xuất.",
        "approach": ["Túi PA/PE và túi đứng in nhãn hiệu", "Kích thước tương thích máy hút chân không, máy hàn miệng túi",
                     "Chọn vật liệu theo cách bảo quản: nhiệt độ thường, mát hay đông lạnh"],
    },
    {
        "slug": "dong-lanh", "tag": "Đông lạnh", "category": "tui-hut-chan-khong-pa-pe",
        "title": "Bao bì cho thịt, thủy hải sản đông lạnh",
        "for": "Thịt, cá, tôm, mực cấp đông",
        "short": "Màng dai, chịu lạnh sâu, mối hàn chắc khi cấp đông và vận chuyển xa.",
        "challenge": "Cấp đông sâu làm màng giòn hơn; hàng có xương hoặc vỏ cứng dễ làm thủng túi khi xếp chồng và vận chuyển.",
        "approach": ["Túi hút chân không PA/PE với độ dày phù hợp hàng sắc cạnh", "Màng chịu lạnh, giữ chân không trong suốt quá trình cấp đông",
                     "Túi một mặt nhám cho máy hút miệng túi"],
    },
    {
        "slug": "cong-nghiep", "tag": "Công nghiệp", "category": "bao-bi-cong-nghiep",
        "title": "Bao bì cho nhà máy, kho vận",
        "for": "Linh kiện, nguyên liệu, hàng xuất khẩu",
        "short": "Túi PE khổ lớn, túi lót thùng và màng cuộn cho đóng gói, lưu kho hàng hóa.",
        "challenge": "Nhà máy cần bao bì đồng đều về kích thước, độ dày và giao đúng tiến độ sản xuất.",
        "approach": ["Túi PE khổ lớn, túi lót thùng carton theo kích thước thùng", "Màng PE cuộn cho đóng gói và bọc hàng",
                     "Sản xuất theo kế hoạch đặt hàng của nhà máy"],
    },
]

STEPS = [
    ("Tiếp nhận nhu cầu", "Tìm hiểu sản phẩm, sản lượng và phương pháp đóng gói."),
    ("Tư vấn vật liệu", "Chọn cấu trúc PA/PE, kích thước, độ dày phù hợp."),
    ("Sản xuất & kiểm tra", "Sản xuất tại xưởng, kiểm tra độ dày và mối hàn."),
    ("Giao hàng", "Đóng gói cẩn thận, giao đến nhà máy, kho của khách hàng."),
]

# Tin tức — trang /tin-tuc/ và mỗi bài /tin-tuc/<slug>/
# Khối nội dung: ("p", chữ) ("h2", chữ) ("ul", [..]) ("ol", [..]) ("table", [tiêu đề], [[hàng]..]) ("note", chữ)
NEWS = [
    {
        "slug": "tui-pa-pe-la-gi", "date": "2026-10-05", "color": "red",
        "title": "Túi PA/PE là gì? Cấu tạo và ưu điểm khi hút chân không",
        "excerpt": "Lớp PA chống thấm khí, lớp PE giúp hàn kín: vì sao kết hợp này phổ biến trong đóng gói thực phẩm.",
        "body": [
            ("p", "Túi PA/PE là loại túi làm từ màng ghép gồm lớp PA (polyamide, còn gọi là nylon) và lớp PE (polyethylene). Đây là vật liệu phổ biến nhất cho túi hút chân không đựng thực phẩm nhờ cân bằng giữa độ bền, khả năng chắn khí và giá thành."),
            ("h2", "Cấu tạo của màng PA/PE"),
            ("ul", ["Lớp PA bên ngoài: dai, chống đâm thủng tốt, hạn chế oxy và mùi đi qua, giúp giữ trạng thái chân không lâu.",
                    "Lớp PE bên trong: mềm, dễ hàn nhiệt, chắn hơi ẩm và là lớp tiếp xúc trực tiếp với thực phẩm.",
                    "Hai lớp được liên kết bằng phương pháp ghép hoặc đùn đồng thời nhiều lớp, tạo thành một màng thống nhất."]),
            ("h2", "Vì sao PA/PE phù hợp để hút chân không"),
            ("p", "Khi hút chân không, không khí trong túi được rút ra và miệng túi được hàn kín. Nếu màng cho khí lọt qua, túi sẽ dần phồng lại và thực phẩm bị oxy hóa. Lớp PA làm chậm quá trình này, còn lớp PE giữ cho mối hàn kín và chắc."),
            ("ul", ["Kéo dài thời gian bảo quản, hạn chế ôi dầu và đổi màu.",
                    "Chịu được nhiệt độ cấp đông, phù hợp hàng đông lạnh.",
                    "Trong suốt, người mua nhìn rõ sản phẩm bên trong.",
                    "In được logo và thông tin sản phẩm lên bề mặt."]),
            ("h2", "Ứng dụng phổ biến"),
            ("ul", ["Thịt, cá, hải sản tươi và đông lạnh.", "Giò chả, xúc xích, lạp xưởng.",
                    "Gạo, hạt điều, nông sản khô.", "Linh kiện, phụ tùng cần chống oxy hóa."]),
            ("h2", "Lưu ý khi chọn túi PA/PE"),
            ("p", "Không phải loại túi PA/PE nào cũng dùng được cho mọi cách chế biến. Hàng cần luộc, hấp hoặc tiệt trùng ở nhiệt độ cao cần cấu trúc màng chịu nhiệt chuyên dụng. Hãy cho nhà cung cấp biết sản phẩm, cách bảo quản và loại máy hút bạn dùng để được tư vấn đúng loại màng và độ dày."),
        ],
    },
    {
        "slug": "chon-do-day-tui-hut-chan-khong", "date": "2026-09-28", "color": "gold",
        "title": "Chọn độ dày túi hút chân không theo từng loại hàng",
        "excerpt": "Thịt có xương, hàng khô hay hàng mềm cần độ dày khác nhau. Cách chọn để tránh thủng túi mà không tốn chi phí thừa.",
        "body": [
            ("p", "Độ dày quyết định túi hút chân không có bị thủng, rách hay xì khí khi đóng gói và vận chuyển hay không. Túi quá mỏng dễ thủng với hàng sắc cạnh; túi quá dày làm tăng chi phí mà không cần thiết."),
            ("h2", "Đơn vị đo độ dày"),
            ("p", "Độ dày màng thường tính bằng micromet (µm, còn gọi là micron). Trong ngành bao bì ở Việt Nam, nhiều nơi dùng đơn vị \"zem\": 1 zem bằng 10 µm, nên túi 80 µm tương đương 8 zem."),
            ("h2", "Độ dày tham khảo theo loại hàng"),
            ("table", ["Loại hàng", "Độ dày tham khảo", "Ghi chú"], [
                ["Hàng nhẹ, mềm: bánh, giò chả, trái cây sấy", "60–80 µm", "Đủ dai cho đóng gói bán lẻ"],
                ["Thịt, cá phi lê, hàng đông lạnh thông thường", "80–100 µm", "Mức phổ biến nhất"],
                ["Gạo, hạt, nông sản khô khối lượng lớn", "90–120 µm", "Hạt nhỏ tạo áp lực lên màng khi hút"],
                ["Hàng có xương, vỏ cứng, sắc cạnh", "120–150 µm trở lên", "Có thể lồng thêm một lớp túi"],
            ]),
            ("note", "Các mức trên chỉ để tham khảo. Độ dày phù hợp nên được xác định bằng mẫu thử với chính sản phẩm và máy hút của bạn."),
            ("h2", "Các yếu tố khác cần cân nhắc"),
            ("ul", ["Khối lượng mỗi túi: túi càng nặng càng cần màng dày.",
                    "Điều kiện bảo quản: cấp đông sâu làm màng giòn hơn, nên tăng độ dày.",
                    "Quãng đường vận chuyển: đi xa, xếp chồng nhiều lớp cần màng dai hơn.",
                    "Loại máy hút: máy hút buồng dùng túi trơn; máy hút miệng túi cần túi một mặt nhám để khí thoát ra."]),
        ],
    },
    {
        "slug": "bao-quan-nong-san-kho", "date": "2026-09-15", "color": "coal",
        "title": "Bảo quản nông sản khô bằng túi hút chân không",
        "excerpt": "Gạo, hạt điều, cà phê giữ hương vị lâu hơn khi được làm khô và hút chân không đúng cách.",
        "body": [
            ("p", "Gạo, hạt điều, đậu phộng hay trái cây sấy đều có thể giảm chất lượng nhanh nếu tiếp xúc với không khí và hơi ẩm. Hút chân không là cách đơn giản để giữ hương vị và kéo dài thời gian bảo quản."),
            ("h2", "Nông sản khô hỏng vì đâu"),
            ("ul", ["Hơi ẩm: làm nông sản mềm, dễ mốc.", "Oxy: làm chất béo trong hạt bị ôi, sinh mùi khó chịu.",
                    "Côn trùng: mọt, sâu phát triển khi còn không khí trong bao bì."]),
            ("h2", "Các bước đóng gói hút chân không"),
            ("ol", ["Làm khô sản phẩm đạt độ ẩm phù hợp trước khi đóng gói.",
                    "Để nguội hoàn toàn, tránh đóng gói khi còn nóng gây đọng hơi nước.",
                    "Chọn túi PA/PE có kích thước và độ dày phù hợp khối lượng.",
                    "Hút chân không và hàn miệng túi; kiểm tra mối hàn không nhăn, không hở.",
                    "Bảo quản nơi khô, mát, tránh ánh nắng trực tiếp."]),
            ("h2", "Lưu ý với cà phê rang"),
            ("p", "Cà phê mới rang tiếp tục thoát khí CO₂ trong nhiều ngày. Nếu hút chân không hoàn toàn, túi có thể phồng lại. Vì vậy nhiều cơ sở dùng túi có van một chiều: khí bên trong thoát ra được, không khí bên ngoài không lọt vào."),
            ("h2", "Hút chân không không thay thế sấy khô"),
            ("p", "Hút chân không làm chậm quá trình hư hỏng nhưng không xử lý được sản phẩm còn ẩm hoặc đã nhiễm mốc. Chất lượng đầu vào vẫn là yếu tố quan trọng nhất."),
        ],
    },
]

INDUSTRIES = ["Gạo", "Cà phê", "Hạt điều", "Bánh tráng", "Muối tôm", "Thịt đông lạnh",
              "Thủy hải sản", "Giò chả, xúc xích", "Nông sản sấy", "Linh kiện công nghiệp", "Kho vận"]

PALETTE = {
    "red":   ("#9E1815", "#C9443B", "#F8E3E0"),
    "gold":  ("#9E6A12", "#E2B867", "#F7EBD3"),
    "coal":  ("#2B2422", "#6B5F5A", "#EEE8E2"),
    "clear": ("#A8928A", "#EFE7DD", "#FFFFFF"),
    "rice":  ("#55702F", "#B9C98F", "#EEF2E1"),
}
