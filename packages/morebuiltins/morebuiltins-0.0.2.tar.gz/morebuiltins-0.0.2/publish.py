import os
import time

import zipapps

zipapps.create_app(
    "./morebuiltins",
    main="morebuiltins",
    output="./morebuiltins.pyz",
    compressed=True,
)
os.system("flit publish")
time.sleep(3)
