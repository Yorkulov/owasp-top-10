from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .flags import compute_flag
from .internal import INTERNAL_HEADER, INTERNAL_HEADER_VALUE
from .models import HintUnlock, Solve
from .vulnerabilities import CATEGORIES, HINTS_UZ


def progress(request):
    solved_ids = set(Solve.objects.values_list("vuln_id", flat=True))
    unlocked = {}
    for vuln_id, level in HintUnlock.objects.values_list("vuln_id", "level"):
        unlocked.setdefault(vuln_id, set()).add(level)

    rows = []
    for cat in CATEGORIES:
        vid = cat["vuln_id"]
        levels_unlocked = sorted(unlocked.get(vid, set()))
        hints = HINTS_UZ.get(vid, [])
        visible_hints = [hints[i - 1] for i in levels_unlocked if i <= len(hints)]
        rows.append({
            **cat,
            "solved": vid in solved_ids,
            "hints_unlocked": len(levels_unlocked),
            "hints_total": len(hints),
            "visible_hints": visible_hints,
        })

    return render(request, "lab/progress.html", {
        "rows": rows,
        "solved_count": len(solved_ids),
        "total_count": len(CATEGORIES),
    })


@require_POST
def unlock_hint(request, vuln_id):
    hints = HINTS_UZ.get(vuln_id, [])
    already = set(HintUnlock.objects.filter(vuln_id=vuln_id).values_list("level", flat=True))
    next_level = len(already) + 1
    if next_level <= len(hints):
        HintUnlock.objects.get_or_create(vuln_id=vuln_id, level=next_level)
        messages.success(request, f"{next_level}-darajali maslahat ochildi.")
    else:
        messages.info(request, "Bu vazifa uchun barcha maslahatlar allaqachon ochilgan.")
    return redirect("lab:progress")


@csrf_exempt
def internal_flag_vault(request):
    """
    === INTENTIONAL VULNERABILITY: A01:2025 - Broken Access Control (SSRF) ===
    See instructor_solutions/A01-BAC-SSRF.md

    "Internal-only" endpoint gated by a header a normal browser never sends.
    Reachable only through the seller panel's server-side URL-fetch feature
    (SSRF) - see sellerpanel/views.py.
    """
    header_key = f"HTTP_{INTERNAL_HEADER.upper().replace('-', '_')}"
    if request.META.get(header_key) != INTERNAL_HEADER_VALUE:
        return HttpResponseForbidden("internal service: forbidden")
    return JsonResponse({"service": "internal-metadata", "flag": compute_flag("A01-BAC-SSRF")})


@require_POST
def submit_flag(request):
    vuln_id = request.POST.get("vuln_id", "").strip()
    submitted = request.POST.get("flag", "").strip()

    valid_ids = {c["vuln_id"] for c in CATEGORIES}
    if vuln_id not in valid_ids:
        messages.error(request, "Noma'lum topshiriq ID.")
        return redirect("lab:progress")

    expected = compute_flag(vuln_id)
    if submitted == expected:
        _, created = Solve.objects.get_or_create(
            vuln_id=vuln_id, defaults={"submitted_flag": submitted}
        )
        if created:
            messages.success(request, "To'g'ri! Flag qabul qilindi.")
        else:
            messages.info(request, "Bu topshiriq allaqachon yechilgan.")
    else:
        messages.error(request, "Flag noto'g'ri. Qayta urinib ko'ring.")

    return redirect("lab:progress")
