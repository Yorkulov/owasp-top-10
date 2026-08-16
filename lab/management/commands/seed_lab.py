import base64
import secrets
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Profile
from lab.flags import compute_flag
from lab.models import FlagVault
from orders.models import Order, OrderItem
from shop.models import Brand, Category, Product

CATEGORY_DATA = [
    ("Elektronika", "elektronika"),
    ("Uy va bog'", "uy-va-bog"),
    ("Kiyim-kechak", "kiyim-kechak"),
    ("Go'zallik", "gozallik"),
    ("Sport va dam olish", "sport-va-dam-olish"),
    ("Bolalar dunyosi", "bolalar-dunyosi"),
]

BRAND_NAMES = ["Nordic", "Vega Basics", "Tashkent Craft", "Orion", "Silk Line", "Zenith"]

PRODUCTS = [
    ("Simsiz quloqchin ANC Pro", "elektronika", "Nordic", 349000, 4.6, "Faol shovqin bosuvchi simsiz quloqchinlar, 30 soatgacha batareya."),
    ("Smart soat FitTrack 2", "elektronika", "Orion", 899000, 4.4, "Yurak urish tezligi, uyqu monitoringi va 14 kunlik batareya."),
    ("Mexanik klaviatura RGB", "elektronika", "Zenith", 620000, 4.7, "Hot-swap mexanik klaviatura, RGB yoritish."),
    ("Portativ quvvat banki 20000mAh", "elektronika", "Nordic", 210000, 4.3, "Tez zaryadlash qo'llab-quvvatlaydi, ikki port."),
    ("4K veb-kamera", "elektronika", "Orion", 480000, 4.1, "Video qo'ng'iroqlar uchun to'liq HD/4K veb-kamera."),
    ("Keramik gulxon to'plami", "uy-va-bog", "Tashkent Craft", 265000, 4.8, "Qo'lda ishlangan keramik gulxonlar, 3 dona to'plamda."),
    ("Aromoterapiya diffuzori", "uy-va-bog", "Silk Line", 175000, 4.2, "Ultratovushli efir moyi diffuzori, avto o'chirish funksiyasi."),
    ("Bambuk oshxona to'plami", "uy-va-bog", "Tashkent Craft", 145000, 4.5, "Ekologik toza bambukdan yasalgan 6 buyumlik to'plam."),
    ("LED stol lampasi", "uy-va-bog", "Zenith", 128000, 4.0, "Sozlanuvchi yorug'lik darajasi, USB-C zaryadlash."),
    ("Yumshoq mikrofibra ko'rpa", "uy-va-bog", "Silk Line", 210000, 4.6, "200x230 sm, barcha fasllar uchun mos."),
    ("Erkaklar kashmir sviteri", "kiyim-kechak", "Silk Line", 380000, 4.5, "100% yumshoq kashmir, klassik kesim."),
    ("Ayollar charm sumkasi", "kiyim-kechak", "Tashkent Craft", 540000, 4.7, "Qo'lda tikilgan tabiiy charm sumka."),
    ("Unisex denim kurtka", "kiyim-kechak", "Vega Basics", 295000, 4.3, "Vintage yuvilgan denim, barcha o'lchamlarda."),
    ("Yugurish krossovkalari Air", "sport-va-dam-olish", "Orion", 460000, 4.4, "Yengil, nafas oluvchi to'r material."),
    ("Yoga gilamchasi Pro", "sport-va-dam-olish", "Vega Basics", 165000, 4.6, "6mm qalinlik, kayishmaydigan yuza."),
    ("Fitness gantel to'plami 2x5kg", "sport-va-dam-olish", "Zenith", 220000, 4.2, "Neopren qoplamali, uy mashqlari uchun."),
    ("Vitamin C serum 30ml", "gozallik", "Silk Line", 132000, 4.5, "20% Vitamin C, teri tiniqligi uchun."),
    ("Organik shampun to'plami", "gozallik", "Tashkent Craft", 98000, 4.3, "Sulfatsiz, tabiiy tarkibiy qismlar."),
    ("Elektr tish cho'tkasi", "gozallik", "Orion", 245000, 4.4, "3 ta rejim, 2 haftalik batareya."),
    ("Yog'och qurilish bloklari", "bolalar-dunyosi", "Vega Basics", 156000, 4.7, "100 dona ekologik toza yog'och bloklar."),
    ("Interaktiv ta'lim planshetchasi", "bolalar-dunyosi", "Zenith", 310000, 4.1, "3-8 yosh bolalar uchun o'quv o'yinlari."),
    ("Yumshoq pluysh ayiqcha", "bolalar-dunyosi", "Tashkent Craft", 89000, 4.8, "Gipoallergen material, 40 sm."),
]


class Command(BaseCommand):
    help = "Seed the marketplace with demo data and plant the OWASP Top 10:2025 lab vulnerabilities."

    def handle(self, *args, **options):
        self.seed_catalog()
        self.seed_users_and_orders()
        self.seed_flag_vault()
        self.seed_supply_chain_js()
        self.seed_sensitive_log()
        self.stdout.write(self.style.SUCCESS("Lab seeded. Flags are unique to this installation."))

    def seed_catalog(self):
        if Product.objects.exists():
            return
        cats = {}
        for name, slug in CATEGORY_DATA:
            cats[slug], _ = Category.objects.get_or_create(name=name, slug=slug)
        brands = {}
        for name in BRAND_NAMES:
            brands[name], _ = Brand.objects.get_or_create(name=name)

        for name, cat_slug, brand_name, price, rating, desc in PRODUCTS:
            slug = self._slugify(name)
            Product.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    name=name, category=cats[cat_slug], brand=brands[brand_name],
                    description=desc, price=Decimal(price), stock=secrets.randbelow(80) + 5,
                    rating_avg=Decimal(str(rating)),
                    image_url=f"https://picsum.photos/seed/vega-{slug}/500/500",
                    image_note="",
                ),
            )

    def _slugify(self, name):
        s = name.lower().replace("'", "").replace("'", "").replace("`", "")
        s = "".join(c if c.isalnum() or c == " " else " " for c in s)
        return "-".join(s.split())[:180]

    def seed_users_and_orders(self):
        if not User.objects.filter(username="siteadmin").exists():
            admin = User.objects.create_user("siteadmin", "admin@vega.local", secrets.token_urlsafe(24))
            Profile.objects.create(user=admin, role="admin", address="Bosh ofis, Toshkent")
            Order.objects.create(
                user=admin, status="delivered", shipping_address="Bosh ofis, Toshkent",
                total=Decimal("0.00"), notes=compute_flag("A01-BAC-IDOR"),
            )

        if not User.objects.filter(username="seller_owner").exists():
            seller = User.objects.create_user("seller_owner", "seller@vega.local", secrets.token_urlsafe(24))
            Profile.objects.create(user=seller, role="seller", address="Chilonzor tumani, Toshkent")

        if not User.objects.filter(username="demo_customer").exists():
            demo = User.objects.create_user("demo_customer", "demo@vega.local", "password1")
            Profile.objects.create(
                user=demo, role="customer",
                address=f"Yunusobod, Toshkent - maxfiy eslatma: {compute_flag('A07-AUTH')}",
            )

        if not User.objects.filter(username="_exceptions_target").exists():
            target = User.objects.create_user("_exceptions_target", "", secrets.token_urlsafe(24))
            Profile.objects.create(user=target, role="customer")
            Order.objects.create(
                user=target, status="pending", shipping_address="N/A",
                total=Decimal("0.00"), notes=compute_flag("A10-EXCEPTIONS"),
            )

    def seed_flag_vault(self):
        FlagVault.objects.all().delete()
        FlagVault.objects.create(label="A05-INJECTION", secret=compute_flag("A05-INJECTION"))

    def seed_supply_chain_js(self):
        flag = compute_flag("A03-SUPPLYCHAIN")
        payload = base64.b64encode(f"SUPPLY-CHAIN-BACKDOOR: {flag}".encode()).decode()
        js_dir = settings.BASE_DIR / "static" / "js" / "vendor"
        js_dir.mkdir(parents=True, exist_ok=True)
        content = (
            "/*! analytics.min.js v2.4.1 | (c) VegaMetrics - CDN mirror, cached locally */\n"
            "(function(w,d){\n"
            "  var VegaAnalytics = { version: '2.4.1', queue: [] };\n"
            "  VegaAnalytics.track = function(evt){ this.queue.push(evt); };\n"
            "  // build artifact - do not edit, regenerated by CI\n"
            f"  var _p = \"{payload}\";\n"
            "  w.VegaAnalytics = VegaAnalytics;\n"
            "})(window, document);\n"
        )
        (js_dir / "analytics.js").write_text(content)

    def seed_sensitive_log(self):
        flag = compute_flag("A09-LOGGING")
        logs_dir = settings.MEDIA_ROOT / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        now = timezone.now()
        content = (
            f"[{now:%Y-%m-%d %H:%M:%S}] INFO  auth: admin session refreshed\n"
            f"[{now:%Y-%m-%d %H:%M:%S}] DEBUG payments: gateway handshake ok\n"
            f"[{now:%Y-%m-%d %H:%M:%S}] DEBUG payments: internal_recovery_token={flag} (TODO remove debug log before release)\n"
            f"[{now:%Y-%m-%d %H:%M:%S}] INFO  orders: nightly reconciliation complete\n"
        )
        (logs_dir / "app.log").write_text(content)
