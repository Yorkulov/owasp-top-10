from django.db import models


class Solve(models.Model):
    """
    A single-install progress record: which vuln_id has been solved and
    when. There is no FK to a marketplace User on purpose - this lab is a
    single local instance per student (see build spec section 1), so
    progress is tracked per-installation, not per marketplace account.
    """

    vuln_id = models.CharField(max_length=64, unique=True)
    solved_at = models.DateTimeField(auto_now_add=True)
    submitted_flag = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.vuln_id} @ {self.solved_at:%Y-%m-%d %H:%M}"


class FlagVault(models.Model):
    """
    A DB table intentionally reachable via UNION-based SQL injection in
    shop's product search (A05). Seeded with the A05 flag by the
    seed_lab management command.
    """

    label = models.CharField(max_length=64)
    secret = models.CharField(max_length=128)


class HintUnlock(models.Model):
    vuln_id = models.CharField(max_length=64)
    level = models.PositiveSmallIntegerField()
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("vuln_id", "level")
