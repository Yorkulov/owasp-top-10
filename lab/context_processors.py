from .models import Solve
from .vulnerabilities import CATEGORIES


def lab_progress(request):
    solved_ids = set(Solve.objects.values_list("vuln_id", flat=True))
    return {
        "lab_solved_count": len(solved_ids),
        "lab_total_count": len(CATEGORIES),
    }
