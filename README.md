# Vega Market — OWASP Top 10:2025 Black-Box Practice Lab

O'zbekcha | [English below](#english)

## Uzbekcha

Vega Market — bu **to'liq ishlaydigan, real ko'rinishdagi onlayn-do'kon**
qiyofasida yashiringan, **OWASP Top 10:2025** ro'yxatidagi barcha 10
zaiflik toifasini o'zida jamlagan, **qora quti (black-box)** uslubidagi
pentest mashq maydonchasi. Juice Shop yoki DVWA'dan farqli o'laroq, bu
yerda hech qanday sahifada "bu yerda SQL Injection bor!" kabi to'g'ridan-
to'g'ri ishoralar berilmaydi — talaba zaifliklarni **haqiqiy razvedka**
(recon) orqali: manba kodini ko'rish, tarmoq so'rovlarini kuzatish,
endpointlarni sanab chiqish, parametrlarni fuzzing qilish orqali topishi
kerak.

### Tezkor boshlash

```bash
git clone https://github.com/Yorkulov/owasp-top-10.git vega-market && cd vega-market && ./run.sh
```

Windows uchun (PowerShell / CMD):

```bat
git clone https://github.com/Yorkulov/owasp-top-10.git vega-market && cd vega-market && run.bat
```

Skript avtomatik ravishda: virtual muhit yaratadi, kutubxonalarni
o'rnatadi, ma'lumotlar bazasini tayyorlaydi, shu o'rnatish uchun **noyob
tasodifiy seed** yaratadi (`instance_config.env`, gitga tushmaydi) va
serverni ishga tushiradi. Keyin brauzerda oching:

```
http://localhost:8000/
```

Progressni kuzatish uchun: `http://localhost:8000/lab/progress/`

### Qoidalar (Rules of Engagement)

- Bu lab **faqat sizning kompyuteringizda, faqat siz uchun** ishlaydi.
  Hech qanday ma'lumot tashqariga yuborilmaydi.
- Flaglar **shu o'rnatishga xos** — internetdan qidirib topib bo'lmaydi va
  boshqa talaba bilan bo'lishib bo'lmaydi.
- **Manba kodini yoki `db.sqlite3` faylini to'g'ridan-to'g'ri o'qib
  javoblarni topish — mashqning maqsadiga zid.** Bu mahalliy, bir
  foydalanuvchili trener bo'lgani uchun texnik jihatdan buni to'xtatib
  bo'lmaydi (Juice Shop va shunga o'xshash boshqa laboratoriyalarda ham
  xuddi shunday), lekin bu "sharaf tamoyili" (honor system) asosida
  ishlaydi: brauzer, DevTools, `curl`/`Burp Suite` kabi vositalar orqali,
  haqiqiy qora quti pentest kabi harakat qiling.
- Har bir toifa uchun 3 darajali maslahat (hint) mavjud — progress
  sahifasida ochib boring.

### Talab qilinadigan dasturlar

- Python 3.10+ (`python3 --version` bilan tekshiring)
- Docker **shart emas**.

### Loyihaning tuzilishi

```
config/                 Django sozlamalari va marshrutlash
accounts/               Ro'yxatdan o'tish, kirish, profil
shop/                   Katalog, qidiruv
cart/                   Savatcha
orders/                 Buyurtmalar, checkout
sellerpanel/            Sotuvchi paneli
reviews/                Mahsulot sharhlari
support/                Yordam/aloqa bo'limi
lab/                    Flag/seed/progress/hint tizimi
templates/, static/     UI (navy/teal "quiet luxury" dizayn)
instructor_solutions/   FAQAT O'QITUVCHI UCHUN — talabalarga tarqatishdan oldin o'chiring
```

### O'qituvchilar uchun

`instructor_solutions/` papkasida har bir zaiflikning aniq joyi va
exploit yo'li tavsiflangan. **Talabalarga repo'ni tarqatishdan oldin bu
papkani albatta o'chiring** (yoki alohida, o'qituvchi-only branch/reponi
saqlang). Talabalarga tarqatishdan oldin platformaning o'zini (nazarda
tutilmagan zaifliklar bormi-yo'qmi) boshqa xavfsizlik mutaxassisi bilan
tekshirtirib chiqing.

---

## English

Vega Market is a **fully-functional, realistic-looking online
marketplace** that secretly contains one exploitable scenario for every
category of the **OWASP Top 10:2025**. Unlike Juice Shop/DVWA/WebGoat,
nothing on the UI names or hints at the vulnerability category — students
must find each flaw through genuine black-box reconnaissance (viewing
source, inspecting network traffic, enumerating endpoints, fuzzing
parameters).

### Quick start

```bash
git clone https://github.com/Yorkulov/owasp-top-10.git vega-market && cd vega-market && ./run.sh
```

Windows (PowerShell / CMD):

```bat
git clone https://github.com/Yorkulov/owasp-top-10.git vega-market && cd vega-market && run.bat
```

The script creates a venv, installs dependencies, runs migrations,
generates a unique per-install random seed (`instance_config.env`, never
committed), seeds demo data + flags, and starts the server at
`http://localhost:8000/`. No Docker required, no external services, no
telemetry.

### Rules of engagement

- Single local instance per student. Nothing leaves your machine.
- Flags are unique per install (`HMAC(seed, vuln_id)`) — they cannot be
  looked up online or shared between classmates.
- Reading the source or the SQLite database directly to find flags
  defeats the purpose (and, like Juice Shop, cannot be technically
  prevented in a single-player local trainer) — please play black-box,
  using only the browser, DevTools, and HTTP tooling, as in a real
  engagement.
- Tiered hints (3 levels per category) are available from the progress
  dashboard at `/lab/progress/`.

### Coverage

All 10 OWASP Top 10:2025 categories are implemented as real,
working features of the marketplace (not standalone checklist pages).
See `instructor_solutions/README.md` (instructor-only) for the full map.

### For instructors

Remove `instructor_solutions/` before distributing the repo to students.
Have the platform itself reviewed for *unintended* vulnerabilities before
release — every intentional one is marked in source with:

```
=== INTENTIONAL VULNERABILITY: <category> ===
```

License: MIT.
