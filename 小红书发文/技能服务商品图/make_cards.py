from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = Path(r"D:\GitHub\MyWorks\小红书发文\技能服务商品图")
BASE.mkdir(parents=True, exist_ok=True)

BG = {
    "cover": Path(r"D:\GitHub\MyWorks\vibe_images\xhs-service-cover-bg_1794718266074_e8dd128b.png"),
    "scope": Path(r"D:\GitHub\MyWorks\vibe_images\xhs-service-scope-bg_1794718289249_24eed444.png"),
    "process": Path(r"D:\GitHub\MyWorks\vibe_images\xhs-service-process-bg_1794718306214_4a0aeb82.png"),
    "trust": Path(r"D:\GitHub\MyWorks\vibe_images\xhs-service-trust-bg_1794718327398_8a0419d7.png"),
}

FONT_B = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_R = r"C:\Windows\Fonts\msyh.ttc"
FONT_L = r"C:\Windows\Fonts\msyhl.ttc"

W = 1080
WHITE = (246, 249, 253)
MUTED = (160, 178, 200)
DIM = (118, 138, 164)
ACCENT = (62, 224, 196)
AMBER = (255, 184, 107)
CARD_TINT = (8, 16, 30, 208)
BORDER = (255, 255, 255, 36)


def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def text_size(d, s, f):
    b = d.textbbox((0, 0), s, font=f, anchor="lt")
    return b[2] - b[0], b[3] - b[1]


def rounded(img, box, radius, fill=None, outline=None, width=1):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def frost(img, box, radius=26, blur=18, tint=CARD_TINT):
    region = img.crop(box).filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
    region = Image.alpha_composite(region, Image.new("RGBA", region.size, tint))
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, region.width - 1, region.height - 1), radius=radius, fill=255
    )
    out = img.copy()
    out.paste(region, (box[0], box[1]), mask)
    return out


def scrim(img, stops, horizontal=True):
    g = Image.new("L", (W, 1))
    px = g.load()
    for i in range(W):
        t = i / (W - 1)
        val = 0
        for j in range(len(stops) - 1):
            p0, a0 = stops[j]
            p1, a1 = stops[j + 1]
            if p0 <= t <= p1:
                k = (t - p0) / (p1 - p0) if p1 > p0 else 0
                val = int(a0 + (a1 - a0) * k)
                break
        else:
            val = stops[-1][1] if t > stops[-1][0] else stops[0][1]
        px[i, 0] = val
    if horizontal:
        g = g.resize((W, W))
    else:
        g = g.rotate(90, expand=True).resize((W, W))
    black = Image.new("RGBA", (W, W), (0, 0, 0, 255))
    black.putalpha(g)
    return Image.alpha_composite(img.convert("RGBA"), black).convert("RGB")


def pill(img, x, y, s, f, fg=WHITE, bg=(255, 255, 255, 18), border=(255, 255, 255, 42), padx=22, h=None):
    d = ImageDraw.Draw(img)
    tw, _ = text_size(d, s, f)
    h = h or (f.size + 22)
    box = (x, y, x + tw + padx * 2, y + h)
    img = rounded(img, box, h // 2, bg, border, 1)
    d = ImageDraw.Draw(img)
    b = d.textbbox((0, 0), s, font=f, anchor="lt")
    th = b[3] - b[1]
    d.text((x + padx, y + (h - th) // 2 - b[1]), s, font=f, fill=fg)
    return img, box


def label(img, text, x=80, y=68, color=ACCENT, size=22):
    d = ImageDraw.Draw(img)
    d.ellipse((x, y + 8, x + 9, y + 17), fill=color)
    d.text((x + 20, y), text, font=font(size, False), fill=color)
    return img


def footer(img, n):
    img = rounded(img, (80, 998, 1000, 999), 0, (255, 255, 255, 20))
    d = ImageDraw.Draw(img)
    f = font(19, False)
    d.text((80, 1016), "软件定制开发 · 技能服务", font=f, fill=DIM)
    s = f"{n:02d} / 04"
    tw, _ = text_size(d, s, f)
    d.text((1000 - tw, 1016), s, font=f, fill=DIM)
    return img


def check(d, x, y, color):
    d.line([(x, y + 7), (x + 5, y + 12), (x + 14, y + 1)], fill=color, width=3, joint="curve")


def cross(d, x, y, color):
    d.line([(x, y), (x + 12, y + 12)], fill=color, width=3)
    d.line([(x + 12, y), (x, y + 12)], fill=color, width=3)


def base_image(key):
    return Image.open(BG[key]).convert("RGB").resize((W, W), Image.LANCZOS)


# ---------------------------------------------------------------- 01 cover
def card_cover():
    img = base_image("cover")
    img = scrim(img, [(0.0, 185), (0.42, 130), (0.72, 0), (1.0, 0)], horizontal=True)
    img = scrim(img, [(0.0, 0), (0.72, 0), (1.0, 120)], horizontal=False)

    img, _ = pill(img, 80, 66, "技能服务 · 软件开发", font(22, False))
    d = ImageDraw.Draw(img)
    d.text((80, 154), "软件定制开发", font=font(88), fill=WHITE)
    img = rounded(img, (82, 300, 182, 305), 2, ACCENT)
    d = ImageDraw.Draw(img)
    d.text((80, 326), "后台系统 / 自动化 / 部署运维", font=font(33, False), fill=WHITE)
    d.text((80, 384), "从需求到上线，一个人跟到底", font=font(26, False), fill=MUTED)

    img = frost(img, (80, 468, 636, 772), radius=28, blur=20)
    d = ImageDraw.Draw(img)
    d.text((112, 500), "为什么找我", font=font(23, False), fill=ACCENT)
    lines = [
        "企业级系统开发与部署经验",
        "需求清单先行，范围写清楚",
        "分阶段演示，验收后交付源码",
    ]
    for i, s in enumerate(lines):
        yy = 556 + i * 64
        d.ellipse((112, yy + 9, 119, yy + 16), fill=ACCENT)
        d.text((136, yy), s, font=font(25, False), fill=WHITE)

    x = 80
    img, box = pill(img, x, 872, "完整源码", font(25, False))
    img, box = pill(img, box[2] + 18, 872, "远程部署", font(25, False))
    img, box = pill(img, box[2] + 18, 872, "平台内交易", font(25, False))

    img = footer(img, 1)
    img.save(BASE / "01_封面.jpg", quality=94, subsampling=1)


# ---------------------------------------------------------------- 02 scope
def card_scope():
    img = base_image("scope")
    img = scrim(img, [(0.0, 95), (0.30, 0), (1.0, 0)], horizontal=False)
    img = scrim(img, [(0.0, 0), (0.86, 0), (1.0, 100)], horizontal=False)

    d = ImageDraw.Draw(img)
    lbl_f = font(22, False)
    lbl = "服务范围"
    lw, _ = text_size(d, lbl, lbl_f)
    lx = (W - (lw + 29)) // 2
    d.ellipse((lx, 76, lx + 9, 85), fill=ACCENT)
    d.text((lx + 20, 68), lbl, font=lbl_f, fill=ACCENT)
    d.text((W // 2, 106), "我能做什么", font=font(62), fill=WHITE, anchor="mt")
    d.text((W // 2, 194), "从一个小工具到一套系统", font=font(27, False), fill=MUTED, anchor="mt")

    items = [
        ("01", "后台系统", "客户、订单、库存", "审批、报表、数据看板"),
        ("02", "自动化工具", "Excel / Word / PDF", "批量处理与网页采集"),
        ("03", "AI 能力落地", "文档解析、知识库", "工作流与批量处理"),
        ("04", "部署与运维", "Windows / IIS、阿里云", "备份、监控、故障排查"),
    ]
    cw, ch, gap = 446, 238, 28
    for i, (num, title, l1, l2) in enumerate(items):
        col, row = i % 2, i // 2
        x = 80 + col * (cw + gap)
        y = 250 + row * (ch + gap)
        img = frost(img, (x, y, x + cw, y + ch), radius=24, blur=18)
        img = rounded(img, (x, y, x + cw, y + ch), 24, None, BORDER, 1)
        d = ImageDraw.Draw(img)
        d.text((x + 28, y + 24), num, font=font(22), fill=ACCENT)
        d.text((x + 28, y + 66), title, font=font(36), fill=WHITE)
        d.text((x + 28, y + 128), l1, font=font(23, False), fill=MUTED)
        d.text((x + 28, y + 164), l2, font=font(23, False), fill=MUTED)

    img = footer(img, 2)
    img.save(BASE / "02_服务范围.jpg", quality=94, subsampling=1)


# ---------------------------------------------------------------- 03 process
def card_process():
    img = base_image("process")
    img = scrim(img, [(0.0, 95), (0.28, 0), (1.0, 0)], horizontal=False)
    img = scrim(img, [(0.0, 0), (0.80, 0), (1.0, 190)], horizontal=False)

    img = label(img, "合作流程")
    d = ImageDraw.Draw(img)
    d.text((80, 106), "怎么合作", font=font(62), fill=WHITE)
    d.text((80, 194), "5 步，从一句话到能用的系统", font=font(27, False), fill=MUTED)

    # deliverables card
    img = frost(img, (80, 252, 320, 632), radius=24, blur=18)
    img = rounded(img, (80, 252, 320, 632), 24, None, BORDER, 1)
    d = ImageDraw.Draw(img)
    d.text((108, 280), "交付物", font=font(24, False), fill=ACCENT)
    for i, s in enumerate(["完整源码", "部署文档", "一次远程部署", "7 天缺陷修复"]):
        yy = 330 + i * 54
        check(d, 108, yy + 4, ACCENT)
        d.text((134, yy), s, font=font(23, False), fill=WHITE)
    d.text((108, 566), "按需求清单验收", font=font(20, False), fill=DIM)

    steps = [
        ("说清场景", "给谁用、解决什么问题、现在怎么做"),
        ("评估方案", "可行性、工期、费用，先给书面范围"),
        ("确认开工", "确认需求清单与首付款，锁定范围"),
        ("分阶段演示", "每步可确认，避免做完才发现不对"),
        ("验收交付", "源码、文档、远程部署，进入售后期"),
    ]
    d = ImageDraw.Draw(img)
    cx = 430
    d.line([(cx, 275), (cx, 748)], fill=(255, 255, 255, 26), width=2)
    for i, (title, desc) in enumerate(steps):
        y = 252 + i * 108
        d.ellipse((cx - 19, y + 4, cx + 19, y + 42), fill=(10, 26, 38), outline=ACCENT, width=2)
        s = str(i + 1)
        tw, th = text_size(d, s, font(20))
        d.text((cx - tw // 2, y + 23 - th // 2), s, font=font(20), fill=ACCENT)
        d.text((476, y), title, font=font(31), fill=WHITE)
        d.text((476, y + 44), desc, font=font(21, False), fill=MUTED)

    img, _ = pill(img, 430, 836, "全程小红书内沟通与下单", font(23, False))
    img = footer(img, 3)
    img.save(BASE / "03_合作流程.jpg", quality=94, subsampling=1)


# ---------------------------------------------------------------- 04 trust
def card_trust():
    img = base_image("trust")
    img = scrim(img, [(0.0, 95), (0.28, 0), (1.0, 0)], horizontal=False)
    img = scrim(img, [(0.0, 0), (0.84, 0), (1.0, 100)], horizontal=False)

    img = label(img, "边界与预期")
    d = ImageDraw.Draw(img)
    d.text((80, 106), "先说清楚", font=font(62), fill=WHITE)
    d.text((80, 194), "能做什么、不做什么，都写在前面", font=font(27, False), fill=MUTED)

    img = frost(img, (70, 244, 1010, 704), radius=28, blur=20)
    img = rounded(img, (70, 244, 1010, 704), 28, None, BORDER, 1)
    d = ImageDraw.Draw(img)

    d.text((108, 282), "适合找我", font=font(31), fill=ACCENT)
    left = [
        "个人或小团队的内部工具",
        "每天重复、想做成工具的事",
        "已有系统要增补或维护",
        "有明确场景和预算范围",
    ]
    for i, s in enumerate(left):
        yy = 340 + i * 62
        check(d, 108, yy + 5, ACCENT)
        d.text((136, yy), s, font=font(23, False), fill=WHITE)

    d.line([(540, 292), (540, 640)], fill=(255, 255, 255, 30), width=1)
    d.text((578, 282), "不接这些", font=font(31), fill=AMBER)
    right = [
        "外挂、破解、数据造假",
        "非公开或隐私数据采集",
        "违法业务、代写、伪造",
        "需要行业资质的合规系统",
    ]
    for i, s in enumerate(right):
        yy = 340 + i * 62
        cross(d, 578, yy + 5, AMBER)
        d.text((606, yy), s, font=font(23, False), fill=MUTED)

    d.line([(108, 574), (972, 574)], fill=(255, 255, 255, 26), width=1)
    d.text((108, 598), "范围写进需求清单，验收按清单来", font=font(21, False), fill=DIM)

    d.text((80, 744), "全程小红书内下单，不走站外交易", font=font(23, False), fill=MUTED)
    d.text((80, 792), "需求越具体，报价越准", font=font(29), fill=ACCENT)

    img = footer(img, 4)
    img.save(BASE / "04_边界说明.jpg", quality=94, subsampling=1)


card_cover()
card_scope()
card_process()
card_trust()
print("done")
for p in sorted(BASE.glob("*.jpg")):
    im = Image.open(p)
    print(p.name, im.size)
