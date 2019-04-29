import base64
import io
from imageio import imread
import numpy as np

rawb64image = ",iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAA" \
                   "BXAvmHAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZ" \
                   "VJlYWR5ccllPAAACk5JREFUeNrUmQlsW/Udx7/P933Edk" \
                   "qcO016xKXt2AohrNBWdKNQWi6BxKVtQKVs0ujEhiYBHamE" \
                   "JlhBZdU0qdI0iWNapQEdA1bGBgqMlgKZmjRx4vTK1eZyEif" \
                   "2e8/2O7zf/9m5tlISmgOe9PJ8PDuf3+///V1/c5lMBt/kw3" \
                   "C5X7Dm/ehlff5A/Trt+i97xcsr09E7uQy406a8hn6D45F7x" \
                   "lt6LvXZzQ3nwS31Ctjvf/zK/cnPjly/rC9YuMEDTsdh" \
                   "oHkc3Z/H8KZ95c9vTUSev5QBuqWEv3fPc3c8a+999xprdzB" \
                   "QZEa6T4QpmkRFtQOhzT7s4CP7/uZY+dilvkO3lPD5NuPeLY8+" \
                   "WWD51t1o/3AE0U4BsfE0hroTCDh1CF3r/lIjlkRCE/C7dnw/VF1" \
                   "dDVEUMdLSiOiRQ+A/PoyCSgssdj0CdgNGx2S0NsYvKqcliYEJ+B1" \
                   "XrwsFAgHk5+dDr9dr77Hr2Ad/Redvn4AvaITbr4fXokeSV9HaKv6" \
                   "fEYseAyxgGfzD27eG/H4/urq60NOTTTQ6nQ5GoxGO67dj+QuvgVt7" \
                   "Jwa70xgcScHIqQgtN11UTobFhF/ndzx93fKikMvlgslk0rzP" \
                   "cRw8Hg8SiYR2ssMYLIPv3p8iSuoYPfpnpB0SAlYdVgZ12HE+su" \
                   "8N5+qB2+JtryxaEDN4utRdWL/1jn8Yi/Dee++hubkZ8Xhce5/ne" \
                   "QwMDCASiSCVSkFRFKh6A1w33wdUXQ9+TMGFaAoGJY2gW0WxNPbUom" \
                   "WhCfjA5p11jsor8W9DAV5w1+ClqB6NjY2IxWKa5202G9jKn" \
                   "DhxAul0GqqqQpeXD8fm25Dg9UgLCrqH01DIwJp07" \
                   "4rDzlU/XHADJuB9m26ts1eGIA8PQBESkDkdzhasw" \
                   "kfrtuEPkSEcPXoUyWQSXq8XRUVFFLCtmhFsJZxXb" \
                   "UTgrl0QU3pIooSxBBkny3Co0g0LasAk/Mab6xzlqyE" \
                   "N9xM8k0wGeW47qpY58VlUwdvuNXhXV4Djx49r6ZTFA" \
                   "4uN/v5+LT7MZjNs2+6DrDNBSmUgiySvjA4JnbFh" \
                   "wQyYhL/uJoJfBXlkABmBB0cv5rkcWHGFC22DSfBpFU" \
                   "SDY741+MBahqamJsjkXbYS7HQ6nZq8ZMr0rtsfgsIZafW" \
                   "MaMmrOntbvP2PC2LABHzetVvr7KUrIBG8KiQ0z3vdBB90Ijw" \
                   "gIk7wGdJ5RpGRkSUcc63ABwigvb1dqwcszTIjWHplUrJuv" \
                   "BUZqw3dK2tGT6vmxxYkiCfhr9lSZy+pnAHvIdmsDLoQ" \
                   "7hcQT8nkeYUMIHhFIgNI11IKDfYKhCUzWHFlwd3X14dj" \
                   "x45pmal/LI53vrc78mbFlod3xtsPz6gDTU9wcwJd90zmC" \
                   "+G9GzbVWYuXE/wgMukkdZd6gnegKuhFSx8PXmYNDPkt" \
                   "1wFonUAmuxIeE5AsqtCy0+rVqzX5sGLHVuOtz062DaRR/" \
                   "5OPDrw+74VsAt5z1cY6KxUheXgavJfgC71ouzAOXtJK" \
                   "Lv0h4Cw+PczBWziUe2x4veM8oqKKPKoLLJjXr1+fhRf" \
                   "S9Y80vHho3geaCXj3+lqCL4U8OqTBg8F7nKgs8qHtPIN" \
                   "Xc55XkXN9zvMK3GaC99rREumioiaikbOjlgxgteDv/w" \
                   "l/IfxlGzAJv7amznpFMcEzz6c0eK+HPF/sQ/v5Uco2mZ" \
                   "znJ6Q35Xm3RYdyvwMt7Qxe0N7to9Dcd0bEpp4s/J/2Pk7" \
                   "wj8/43wcPHsTmyzFgAt61ZkOdJT+Y83wWnsmmssSP9p4R" \
                   "JCjbcMzz6pTnM2wVNHg9yvx2tIY7wSeEye9ORvvR0XPm" \
                   "YAfwe/6V507M+0zM4EPmCwd6KrbfYPEXQI5Fp+CZbErz" \
                   "Eeli8AqpRkf+Vic9z1InmGysepTm2xEOn5sBn6Lg53vPH" \
                   "cQs4L+SAQdGN91Raz2792TJ7SGLf1kWXkppEnG7PVhel" \
                   "o+O7igSKeWi2YZ53mU1oCRA9aD1LIQEPwU/GoVwoWvW8" \
                   "HM2gMF3Sb69zYU7Q2ZvPslmOAtPJd/tcRP8MnR0DoFPyl" \
                   "l4LpdtpgWsy2Ygz7vQHj4NPj4Fn44NQxjonRP8nArZBHxTw" \
                   "faQyeuDMjYMNclrgeh02lBeXoBT5/qRiAvZ6jqtSGmFijK" \
                   "Tk/J8KWsjWk8jERvL3kdniuJnrvA/+/D0nFbgCgZ/wndj" \
                   "yOzyaPAZKZ2NB4IvZfCnuiGQbDjq45HRa5VWcz/zPD12W" \
                   "I0oKfCgveUUhOmej8coaAfm7Pk5SegIH3rmuFodshIRa8" \
                   "wmg9lpR2lFIc60kZZZtqGRkGUYTkuZXFb3DN5mQhFV4kh" \
                   "LZAa8lBhHcmToK8PP1gD9Nkf4R0JRCPuaaD61OWF0u" \
                   "uAkzZdUFOEsg6cswhnN4Bi8njyu0+eSjgo7gy/04UxL" \
                   "B4TxxBQ8H0cqNnxZ8LONgVucfg/qa7ow9GADnv52M4T+" \
                   "XuqCJXS2n6Fxb1zTMYsHNSlATeXOtAibiaMBxU/wEfCj" \
                   "sUnNS/GxeYGfrQEPeANugFpem1HCbjKk95ef4E5vA6" \
                   "Kd52g6krTswk5VJPCkqJ1Wow6Fxfk4e5LgR2KT92ieH" \
                   "x+dF/jZSChPb9Df5aI+BSIFrUOvadtrSuL5bR1wmST85" \
                   "uNysMDWqi1TDXnYRrNtkME3hyFO07ycSjID5g1+Ngbc5" \
                   "c5z0jJRRlG0fTxtgqKxiJ5z+NXGCPQZGc8eXQGzw6nV" \
                   "AxtNXMVVJegOR2bCU6WWBH5e4WdjwA/yqMWFRH2wnssWJJ" \
                   "IBpKn54cmaMKiBxO+aVsGVH0CwqgxdrTPhFUq5frn/c" \
                   "B/c8wr/ZQZUmkyGa+0WukUkA5y5toDBK9Puopd+XdOEM" \
                   "1ErPjUUoid8CuK0bKNQjHxH1xb+RC6vn2/4LzPgAa/LS" \
                   "oByVjbIFSd52vSm5toEevmR5RG8834QJot1GryMDYZIW4E" \
                   "h9tRCwF/KACaYPXl2I3VY5H1TTj6s+DIDmD1aLLDn2etW" \
                   "SxceLOjAq4PV1JTqyVYFG4wdbWXG4frXUt993fvQnov+oz" \
                   "QF9kIYcIvTZoTJoEISFRj1uqx01NxMkoMGGxGlDBQaWNic" \
                   "/oD/JF7qW6FV4KtNpzT4v4i1hzDZTi/eCtR5mfZlRdtMM" \
                   "pIh2baS6T+jgasEnpSmPqDQipSpvXi1+BUcGKrNwgs1C" \
                   "wr/RQZYKRveZCQvCvEsYSoOmMWsaqZDs+c8DS1xOrW" \
                   "Zlya9Mu7Coc+lqvfpXJpfKW886N/141oR968XUGA" \
                   "3aLtpsqIV4slZXJBVjNMKsCs9f5leZgP3kdquX+Tyk" \
                   "7xovzkY/gf+UbPZvD9adDfe6nwDO8v6scySzTo86T5" \
                   "BXDxJiDz/Br30cg5aXMofCg3T4U0m0/61a9eira0Nn" \
                   "8YLER+P4Z41IotTJv23c55+k84xfE0OQw7eodPp9v" \
                   "t8Pm1XmG2wDg4O4kCnfffOarGRbonQOYSv4aH9yM" \
                   "e2FsmIervdvodtZ7N9SVVVd/9zV/TFr7LNuCQS0posno" \
                   "cgCHvIqFnBf61WYFosOAg+cTkbvYtuwDf50OEbfvxXgAEA" \
                   "FpyqPqutRYcAAAAASUVORK5CYII="


rawb64images = [rawb64image, rawb64image]

image_bytes = base64.b64decode(rawb64image)
img_io = imread(io.BytesIO(image_bytes))

img = np.asarray(img_io.astype('uint8'))
