"""
Human-facing metadata for the 10 OWASP Top 10:2025 categories covered by
this lab. Titles are deliberately generic ("A05 - Injection") so the
progress dashboard never spoils WHERE in the site the bug lives.
"""

CATEGORIES = [
    {
        "vuln_id": "A01-BAC-IDOR",
        "code": "A01:2025",
        "title_uz": "Buzilgan kirishni boshqarish - IDOR",
        "name": "Broken Access Control (IDOR)",
    },
    {
        "vuln_id": "A01-BAC-SSRF",
        "code": "A01:2025",
        "title_uz": "Buzilgan kirishni boshqarish - SSRF",
        "name": "Broken Access Control (SSRF)",
    },
    {
        "vuln_id": "A02-MISCONFIG",
        "code": "A02:2025",
        "title_uz": "Xavfsizlik konfiguratsiyasidagi xato",
        "name": "Security Misconfiguration",
    },
    {
        "vuln_id": "A03-SUPPLYCHAIN",
        "code": "A03:2025",
        "title_uz": "Dasturiy ta'minot yetkazib berish zanjiridagi nosozlik",
        "name": "Software Supply Chain Failures",
    },
    {
        "vuln_id": "A04-CRYPTO",
        "code": "A04:2025",
        "title_uz": "Kriptografik nosozlik",
        "name": "Cryptographic Failures",
    },
    {
        "vuln_id": "A05-INJECTION",
        "code": "A05:2025",
        "title_uz": "In'ektsiya (Injection)",
        "name": "Injection",
    },
    {
        "vuln_id": "A06-INSECURE-DESIGN",
        "code": "A06:2025",
        "title_uz": "Ishonchsiz dizayn (biznes-logika xatosi)",
        "name": "Insecure Design",
    },
    {
        "vuln_id": "A07-AUTH",
        "code": "A07:2025",
        "title_uz": "Autentifikatsiya nosozliklari",
        "name": "Authentication Failures",
    },
    {
        "vuln_id": "A08-INTEGRITY",
        "code": "A08:2025",
        "title_uz": "Dasturiy ta'minot yoki ma'lumot yaxlitligi nosozligi",
        "name": "Software or Data Integrity Failures",
    },
    {
        "vuln_id": "A09-LOGGING",
        "code": "A09:2025",
        "title_uz": "Xavfsizlik jurnali va ogohlantirish nosozligi",
        "name": "Security Logging & Alerting Failures",
    },
    {
        "vuln_id": "A10-EXCEPTIONS",
        "code": "A10:2025",
        "title_uz": "Favqulodda holatlarni noto'g'ri boshqarish",
        "name": "Mishandling of Exceptional Conditions",
    },
]

HINTS_UZ = {
    "A01-BAC-IDOR": [
        "Buyurtmalar tarixi sahifasida har bir buyurtmaning o'ziga xos ID'si bor. Bu ID qayerda ko'rinadi?",
        "URL manzildagi buyurtma ID'sini o'zgartirib ko'ring. Server bu buyurtma sizga tegishli ekanligini tekshiryaptimi?",
        "/orders/1/, /orders/2/ ... ketma-ket raqamlarni sanab chiqing (IDOR). Boshqa foydalanuvchining buyurtmasini oching.",
    ],
    "A01-BAC-SSRF": [
        "Sotuvchi (seller) panelida mahsulot rasmini 'URL orqali import qilish' funksiyasi bor.",
        "Bu funksiya serverning o'zi tomonidan so'rov yuboradi. U tashqi URL o'rniga ichki (internal) manzillarga ham murojaat qila oladimi?",
        "http://127.0.0.1:<port>/internal/... kabi ichki endpointlarni URL maydoniga kiritib ko'ring.",
    ],
    "A02-MISCONFIG": [
        "Har doim robots.txt va umumiy statik fayllar papkasini tekshiring - ba'zan u yerda bo'lmasligi kerak bo'lgan narsalar qoladi.",
        "robots.txt faylida 'Disallow' qilingan, lekin baribir ochiladigan bir yo'l bor.",
        "/internal-backup/ papkasini to'g'ridan-to'g'ri brauzerda oching.",
    ],
    "A03-SUPPLYCHAIN": [
        "Sayt yuklaydigan barcha JavaScript fayllarni ko'zdan kechiring (Network yoki View Source orqali).",
        "'vendor' papkasidagi kutubxonalardan biri odatdagidek ko'rinmaydi - ichida shubhali, kodlashtirilgan (encoded) qism bor.",
        "static/js/vendor/analytics.js faylidagi base64 bilan kodlangan qatorni deshifrlang (decode qiling).",
    ],
    "A04-CRYPTO": [
        "Profilda 'Meni eslab qol' (remember me) funksiyasi cookie orqali ishlaydi. Bu cookie qanday tuzilgan?",
        "Cookie qiymati oddiy base64 - ichida imzo (signature) yo'q. Uni decode qilib tuzilishini o'rganing.",
        "Cookie'ni o'zingiz qo'lda tuzib, boshqa foydalanuvchi (masalan admin) nomidan cookie yasang.",
    ],
    "A05-INJECTION": [
        "Qidiruv paneli mahsulot nomi bo'yicha qidiradi. Maxsus belgilar (', \", --) bilan sinab ko'ring.",
        "Qidiruv so'rovi ma'lumotlar bazasiga to'g'ridan-to'g'ri qo'shilayotganga o'xshaydi (SQL Injection).",
        "UNION SELECT yordamida boshqa jadvaldagi ma'lumotni (masalan lab_flagvault) qidiruv natijasida chiqarishga harakat qiling.",
    ],
    "A06-INSECURE-DESIGN": [
        "Savatchada mahsulot sonini (quantity) o'zgartirish maydoni bor. Faqat musbat sonlar kutilgan bo'lishi mumkin.",
        "Manfiy son kiritsangiz nima bo'ladi? Umumiy summa (total) qanday hisoblanadi?",
        "Savatchaga narxi qimmat mahsulotni manfiy miqdorda qo'shib, umumiy summani nolga yoki minusga tushiring.",
    ],
    "A07-AUTH": [
        "Login formasida urinishlar sonini cheklovchi (rate limit) hech narsa yo'qday tuyuladi.",
        "Sotuvchi (seller) akkaunti standart, kuchsiz parol bilan yaratilgan bo'lishi mumkin.",
        "seller@market.uz akkauntiga keng tarqalgan zaif parollar bilan kirishga harakat qiling.",
    ],
    "A08-INTEGRITY": [
        "Sayt sozlamalari yoki 'tema' cookie sifatida brauzerda saqlanadi. Uning tuzilishini tekshiring.",
        "Bu ma'lumot base64(JSON) ko'rinishida, lekin imzosiz - server uni tekshirmasdan ishonadi.",
        "Cookie ichidagi 'role' maydonini 'admin' ga o'zgartirib, qayta base64 qilib joylashtiring.",
    ],
    "A09-LOGGING": [
        "Ba'zi tizimlar xato/nozik ma'lumotlarni log fayllariga yozib qo'yadi va bu fayl tashqi dunyoga ochiq qolib ketishi mumkin.",
        "media/ papkasi ostida log fayllar joylashishi mumkin bo'lgan yo'lni qidiring.",
        "/media/logs/app.log faylini to'g'ridan-to'g'ri oching va unda tasodifan yozilgan nozik tokenni toping.",
    ],
    "A10-EXCEPTIONS": [
        "Buyurtma hisob-fakturasi (invoice) sahifasi buyurtma ID'sini URL'dan oladi.",
        "ID o'rniga kutilmagan qiymat (masalan raqam emas, matn) yuborsangiz nima bo'ladi? Xatolik qanday ishlov beriladi?",
        "/orders/<ID>/invoice/ ga raqam o'rniga boshqa qiymat yuborib, ruxsat tekshiruvini chetlab o'tishga harakat qiling (fail-open).",
    ],
}
