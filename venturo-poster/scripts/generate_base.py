#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path

from curl_cffi import requests

MODEL_CHAIN = ["dreamina-4.5", "dreamina-4.1", "dreamina-4.0"]
POLL_INTERVAL = 3
POLL_TIMEOUT = 180

REGION_CONFIG = {
    "us": {
        "base_url": "https://mweb-api-sg.capcut.com",
        "aid": 513641, "region_code": "US", "store_region": "us",
    },
    "sg": {
        "base_url": "https://mweb-api-sg.capcut.com",
        "aid": 513641, "region_code": "SG", "store_region": "hk",
    },
    "hk": {
        "base_url": "https://mweb-api-sg.capcut.com",
        "aid": 513641, "region_code": "HK", "store_region": "hk",
    },
    "jp": {
        "base_url": "https://mweb-api-sg.capcut.com",
        "aid": 513641, "region_code": "JP", "store_region": "hk",
    },
}

MODEL_MAP = {
    "dreamina-4.5": "high_aes_general_v40l",
    "dreamina-4.1": "high_aes_general_v41",
    "dreamina-4.0": "high_aes_general_v40",
    "jimeng-4.5": "high_aes_general_v40l",
    "jimeng-4.1": "high_aes_general_v41",
    "jimeng-4.0": "high_aes_general_v40",
}

RESOLUTIONS = {
    "1k": {"1:1": (1024, 1024, 1)},
    "2k": {"1:1": (2048, 2048, 1)},
    "4k": {"1:1": (4096, 4096, 101)},
}

PLATFORM_CODE = "7"
VERSION_CODE = "5.8.0"
DRAFT_VERSION = "3.3.7"
DRAFT_MIN_VERSION = "3.0.2"

_sess = None


def get_plugin_root():
    return Path(__file__).resolve().parent.parent


def load_config():
    cfg_path = get_plugin_root() / "config" / "cookies.json"
    if not cfg_path.exists():
        return {"session_ids": [], "region": "sg"}
    try:
        with open(cfg_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"session_ids": [], "region": "sg"}


def new_uuid():
    return str(uuid.uuid4())


def md5(s):
    return hashlib.md5(s.encode()).hexdigest()


def build_prompt(base_prompt, tier, aesthetics, lighting, bg_tone):
    tier_hints = {
        "starter": "Clean, minimalist, modern, approachable. Bright teal/green accents.",
        "growth": "Professional, interconnected, data-driven dashboards. Corporate feel.",
        "enterprise": "High-tech, dark cyberpunk, data streams, cybersecurity, holographic.",
    }
    return (
        f"Background visual untuk katalog WhatsApp Business — jasa pengembangan software. "
        f"Service tier: {tier}. "
        f"Gaya visual: {tier_hints.get(tier.lower(), 'Modern, profesional')}. "
        f"Tema teknis: {aesthetics}. "
        f"Human elements: {lighting}. "
        f"Background tone: {bg_tone}. "
        f"CRITICAL: Hanya background visual — JANGAN ada teks, JANGAN ada logo, JANGAN ada tulisan apapun. "
        f"Area tengah 70% harus bersih/soft agar teks bisa dibaca ketika ditimpa. "
        f"Gunakan gradient halus, jangan terlalu ramai di bagian tengah. "
        f"Format kotak 1:1 untuk katalog WhatsApp. "
        f"Kualitas tinggi, resolusi 8K, lighting profesional."
    )


def resolve_resolution(resolution="2k", ratio="1:1"):
    rg = RESOLUTIONS.get(resolution)
    if not rg:
        return resolve_resolution("2k", ratio)
    r = rg.get(ratio)
    if not r:
        return resolve_resolution(resolution, "1:1")
    return {"width": r[0], "height": r[1], "image_ratio": r[2], "resolution_type": resolution}


def build_core_param(model_internal, prompt, seed, ratio_res, negative_prompt=""):
    cp = {
        "type": "", "id": new_uuid(),
        "model": model_internal, "prompt": prompt, "seed": seed,
        "sample_strength": 0.5,
        "image_ratio": ratio_res["image_ratio"],
        "large_image_info": {
            "type": "", "id": new_uuid(),
            "min_version": DRAFT_MIN_VERSION,
            "height": ratio_res["height"],
            "width": ratio_res["width"],
            "resolution_type": ratio_res["resolution_type"],
        },
        "intelligent_ratio": False,
    }
    if negative_prompt:
        cp["negative_prompt"] = negative_prompt
    return cp


def build_metrics_extra(model_name, user_model, submit_id, ratio_res):
    scene = {
        "type": "image",
        "scene": "ImageBasicGenerate",
        "modelReqKey": user_model,
        "resolutionType": ratio_res["resolution_type"],
        "benefitCount": 4,
        "reportParams": {
            "enterSource": "generate",
            "vipSource": "generate",
            "extraVipFunctionKey": f"{user_model}-{ratio_res['resolution_type']}",
            "useVipFunctionDetailsReporterHoc": True,
        },
    }
    return json.dumps({
        "promptSource": "custom",
        "generateCount": 1,
        "enterFrom": "click",
        "sceneOptions": json.dumps([scene]),
        "generateId": submit_id,
        "isRegenerate": False,
    })


def build_draft_content(component_id, core_param):
    return json.dumps({
        "type": "draft",
        "id": new_uuid(),
        "min_version": DRAFT_MIN_VERSION,
        "min_features": [],
        "is_from_tsn": True,
        "version": DRAFT_VERSION,
        "main_component_id": component_id,
        "component_list": [
            {
                "type": "image_base_component",
                "id": component_id,
                "min_version": DRAFT_MIN_VERSION,
                "aigc_mode": "workbench",
                "metadata": {
                    "type": "", "id": new_uuid(),
                    "created_platform": 3,
                    "created_platform_version": "",
                    "created_time_in_ms": str(int(time.time() * 1000)),
                    "created_did": "",
                },
                "generate_type": "generate",
                "abilities": {
                    "type": "", "id": new_uuid(),
                    "generate": {
                        "type": "", "id": new_uuid(),
                        "core_param": core_param,
                    },
                    "gen_option": {
                        "type": "", "id": new_uuid(),
                        "generate_all": False,
                    },
                },
            },
        ],
    })


def parse_region(region_str):
    r = region_str.lower()
    for prefix, code in [("us-", "us"), ("sg-", "sg"), ("hk-", "hk"), ("jp-", "jp")]:
        if r.startswith(prefix):
            return code, region_str[3:]
    return "sg", region_str


def dreamina_headers(token, region, uri, ts, web_id):
    rc = REGION_CONFIG.get(region, REGION_CONFIG["sg"])
    last7 = uri[-7:]
    sign_input = f"9e2c|{last7}|{PLATFORM_CODE}|{VERSION_CODE}|{ts}||11ac"
    sign = md5(sign_input)
    user_id = md5(token)

    cookies = "; ".join([
        f"sid_guard={token}%7C{ts}%7C5184000%7CMon%2C+03-Feb-2025+08%3A17%3A09+GMT",
        f"sessionid={token}",
        f"sessionid_ss={token}",
        f"uid_tt={user_id}",
        f"uid_tt_ss={user_id}",
        f"sid_tt={token}",
        f"store-region={rc['store_region']}",
        f"store-region-src=uid",
        f"_tea_web_id={web_id}",
        "is_staff_user=false",
    ])

    return {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Cookie": cookies,
        "Device-Time": str(ts),
        "Sign": sign,
        "Sign-Ver": "1",
        "Appid": str(rc["aid"]),
        "Pf": PLATFORM_CODE,
        "Appvr": VERSION_CODE,
        "Origin": "https://dreamina.capcut.com",
        "Referer": "https://dreamina.capcut.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": '"Google Chrome";v="142", "Chromium";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }


def call_dreamina(prompt, output_path, token, model="dreamina-4.5", region="sg",
                  ratio="1:1", resolution="2k"):
    global _sess
    if _sess is None:
        _sess = requests.Session(impersonate="chrome")

    rc = REGION_CONFIG.get(region, REGION_CONFIG["sg"])
    model_internal = MODEL_MAP.get(model)
    if not model_internal:
        return False, f"unknown model: {model}"

    ratio_res = resolve_resolution(resolution, ratio)
    ts = int(time.time())
    submit_id = new_uuid()
    component_id = new_uuid()
    web_id = str(abs(hash(token)) % 999999999999999999 + 7000000000000000000)
    seed = int(time.time() * 1000000) % 100000000 + 2500000000

    core_param = build_core_param(model_internal, prompt, seed, ratio_res)
    draft_content = build_draft_content(component_id, core_param)
    metrics_extra = build_metrics_extra(model, model, submit_id, ratio_res)

    body_data = {
        "extend": {"root_model": model_internal},
        "submit_id": submit_id,
        "metrics_extra": metrics_extra,
        "draft_content": draft_content,
        "http_common_info": {"aid": rc["aid"]},
    }

    uri_path = "/mweb/v1/aigc_draft/generate"
    url = f"{rc['base_url']}{uri_path}?aid={rc['aid']}&device_platform=web&region={rc['region_code']}&webId={web_id}"
    headers = dreamina_headers(token, region, uri_path, ts, web_id)

    try:
        resp = _sess.post(url, json=body_data, headers=headers, timeout=60)
        result = resp.json()
    except Exception as e:
        return False, f"submit error: {e}"

    ret = result.get("ret", 0)
    if ret != 0 and ret != "0":
        msg = result.get("errmsg", "unknown")
        fc = result.get("data", {}).get("fail_code", "")
        if fc:
            fm = result.get("data", {}).get("fail_starling_message", "")
            return False, f"Dreamina error [{ret}]: {msg} (code={fc}, {fm})"
        return False, f"Dreamina error [{ret}]: {msg}"

    try:
        history_id = result["data"]["aigc_data"]["history_record_id"]
    except (KeyError, TypeError):
        return False, f"no history_record_id: {json.dumps(result, ensure_ascii=False)[:300]}"

    print(f"  task_id={history_id}")

    # ── Poll ────────────────────────────────────────────────────
    poll_uri = "/mweb/v1/get_history_by_ids"
    poll_url = f"{rc['base_url']}{poll_uri}?aid={rc['aid']}&device_platform=web&region={rc['region_code']}&webId={web_id}"
    deadline = time.time() + POLL_TIMEOUT

    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)

        poll_headers = dreamina_headers(token, region, poll_uri, int(time.time()), web_id)
        poll_body = {
            "data": {
                "history_ids": [history_id],
                "image_info": {
                    "width": 2048, "height": 2048, "format": "webp",
                    "image_scene_list": [
                        {"scene": "normal", "width": 1080, "height": 1080, "uniq_key": "1080", "format": "webp"},
                    ],
                },
            },
        }

        try:
            presp = _sess.post(poll_url, json=poll_body, headers=poll_headers, timeout=30)
            status = presp.json()
        except Exception as e:
            return False, f"poll error: {e}"

        task_info = status.get("data", {}).get(history_id, {})
        if not task_info:
            return False, f"task not found in poll response"

        s = task_info.get("status")
        total = max(task_info.get("total_image_count", 4), 1)
        finished = task_info.get("finished_image_count", 0)
        progress = int(finished / total * 100)
        print(f"  progress: {progress}%")

        if s in (10, 50):
            images = []
            for item in task_info.get("item_list", []):
                url = (item.get("image", {}).get("large_images", [{}])[0].get("image_url")
                       or item.get("common_attr", {}).get("cover_url")
                       or item.get("image_url") or item.get("url"))
                if url:
                    images.append(url)
            if not images:
                return False, "completed but no images"

            try:
                img_resp = _sess.get(images[0], timeout=30)
                img_resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                return True, f"OK (model={model})"
            except Exception as e:
                return False, f"download failed: {e}"

        elif s == 30:
            fail_code = task_info.get("fail_code", "?")
            return False, f"generation failed (code={fail_code})"

    return False, "timeout"


def call_dalle(api_key, prompt, output_path, width=1080, height=1080):
    try:
        import openai
    except ImportError:
        return False, "openai not installed"

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3", prompt=prompt,
            size="1024x1024", quality="hd", n=1,
        )
        img_resp = requests.get(response.data[0].url, impersonate="chrome", timeout=30)
        with open(output_path, "wb") as f:
            f.write(img_resp.content)
        try:
            from PIL import Image
            img = Image.open(output_path)
            if img.size != (width, height):
                img = img.resize((width, height), Image.LANCZOS)
                img.save(output_path, "PNG", quality=95)
        except ImportError:
            pass
        return True, "OK (DALL-E)"
    except Exception as e:
        return False, f"DALL-E error: {e}"


def generate_placeholder(output_path, width=1080, height=1080, tier="starter"):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow required. pip install Pillow")
        return False, "no pillow"

    img = Image.new("RGB", (width, height), "#0f172a")
    draw = ImageDraw.Draw(img)

    colors = {
        "starter": ("#06b6d4", "#10b981"),
        "growth": ("#3b82f6", "#8b5cf6"),
        "enterprise": ("#ef4444", "#f59e0b"),
    }
    c1, c2 = colors.get(tier.lower(), ("#06b6d4", "#10b981"))

    for y in range(height):
        ratio = y / height
        r = int(int(c1[1:3], 16) * (1 - ratio) + int(c2[1:3], 16) * ratio)
        g = int(int(c1[3:5], 16) * (1 - ratio) + int(c2[3:5], 16) * ratio)
        b = int(int(c1[5:7], 16) * (1 - ratio) + int(c2[5:7], 16) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    for y in range(int(height * 0.15)):
        a = int(80 * (1 - y / (height * 0.15)))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, a))
    for y in range(int(height * 0.85), height):
        ratio = (y - height * 0.85) / (height * 0.15)
        a = int(80 * ratio)
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, a))

    for i in range(2):
        cx = width // 4 + i * width // 2
        cy = height // 2
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for r in range(200, 0, -10):
            a = max(0, 12 - (200 - r) // 17)
            gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16), a))
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img)

    img.save(output_path, "PNG", quality=95)
    print(f"  placeholder fallback")
    return True, "OK (placeholder)"


def main():
    parser = argparse.ArgumentParser(description="Generate Venturo catalog background via Dreamina")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--tier", default="starter", choices=["starter", "growth", "enterprise"])
    parser.add_argument("--aesthetics", default="modern UI design")
    parser.add_argument("--lighting", default="professional studio lighting")
    parser.add_argument("--bg-tone", default="dark cybertech")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    enriched = build_prompt(args.prompt, args.tier, args.aesthetics, args.lighting, args.bg_tone)
    print(f"Prompt ({len(enriched)} chars)")
    print(f"Size: {args.width}x{args.height}")

    config = load_config()
    sessions = config.get("session_ids", [])
    region = config.get("region", "sg")

    ok = False
    reason = ""

    if sessions:
        print(f"\nRegion: {region}")
        print(f"Sessions: {len(sessions)} loaded")

        for session in sessions:
            sid = session.strip()
            if not sid:
                continue
            r, token = parse_region(sid)
            actual_region = region or r
            for model in MODEL_CHAIN:
                print(f"  trying model={model} token={token[:12]}... region={actual_region}")
                print(f"  calling Dreamina API (curl_cffi chrome)...")
                ok, reason = call_dreamina(enriched, str(output_path), token, model=model, region=actual_region)
                if ok:
                    print(f"  ✓ {reason}")
                    break
                print(f"  ✗ {reason}")
            if ok:
                break
    else:
        print("\nNo Dreamina config. config/cookies.json not found or empty.")

    if not ok:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("  fallback → DALL-E 3")
            ok, reason = call_dalle(api_key, enriched, str(output_path), args.width, args.height)
            if ok:
                print(f"  ✓ {reason}")

    if not ok:
        print("  fallback → placeholder gradient")
        ok, reason = generate_placeholder(str(output_path), args.width, args.height, args.tier)
        if ok:
            print(f"  ✓ {reason}")

    if ok:
        print(f"\nDone: {output_path}")
    else:
        print(f"\nFAILED: {reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()
