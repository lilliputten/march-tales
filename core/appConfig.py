# -*- coding:utf-8 -*-

from .appEnv import (
    appEnv,
)

# Timezone (set `TZ_HOURS` to hours value to adjust date representation to corresponding timezone)
TZ_HOURS = appEnv.int('TZ_HOURS_OFFSET', 0)
