#!/usr/bin/env python3
import asyncio
import hashlib
import time
import uuid
import json
from playwright.async_api import async_playwright

TOKEN = "9b62ff68e1330e46d361a952ed31a683"
BASE = "https://mweb-api-sg.capcut.com"
AID = 513641
TS = int(time.time())

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
            locale="zh-CN",
        )

        await ctx.add_cookies([
            {"name": "sessionid", "value": TOKEN, "domain": ".capcut.com", "path": "/"},
            {"name": "sessionid_ss", "value": TOKEN, "domain": ".capcut.com", "path": "/"},
            {"name": "sid_tt", "value": TOKEN, "domain": ".capcut.com", "path": "/"},
            {"name": "store-region", "value": "hk", "domain": ".capcut.com", "path": "/"},
        ])

        page = await ctx.new_page()
        await page.goto("https://dreamina.capcut.com/", wait_until="networkidle")
        print(f"Page: {await page.title()}")

        uri = "/mweb/v1/aigc_draft/generate"
        sign = hashlib.md5(f"9e2c|{uri[-7:]}|7|5.8.0|{TS}||11ac".encode()).hexdigest()
        web_id = str(abs(hash(TOKEN)) % 999999999999999999 + 7000000000000000000)
        uid = hashlib.md5(TOKEN.encode()).hexdigest()

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Device-Time": str(TS), "Sign": sign, "Sign-Ver": "1",
            "Appid": str(AID), "Pf": "7", "Appvr": "5.8.0",
            "Origin": "https://dreamina.capcut.com",
            "Referer": "https://dreamina.capcut.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": '"Google Chrome";v="142", "Chromium";v="142", "Not_A Brand";v="99"',
        }

        cid, sid = str(uuid.uuid4()), str(uuid.uuid4())
        body = json.dumps({
            "extend": {"root_model": "high_aes_general_v40l"}, "submit_id": sid,
            "metrics_extra": json.dumps({
                "promptSource": "custom", "generateCount": 1, "enterFrom": "click",
                "sceneOptions": json.dumps([{
                    "type": "image", "scene": "ImageBasicGenerate", "modelReqKey": "dreamina-4.5",
                    "resolutionType": "2k", "benefitCount": 4,
                    "reportParams": {"enterSource": "generate", "vipSource": "generate",
                        "extraVipFunctionKey": "dreamina-4.5-2k",
                        "useVipFunctionDetailsReporterHoc": True},
                }]), "generateId": sid, "isRegenerate": False,
            }),
            "draft_content": json.dumps({
                "type": "draft", "id": str(uuid.uuid4()), "min_version": "3.0.2", "is_from_tsn": True,
                "version": "3.3.7", "main_component_id": cid,
                "component_list": [{
                    "type": "image_base_component", "id": cid, "min_version": "3.0.2",
                    "aigc_mode": "workbench",
                    "metadata": {"type": "", "id": str(uuid.uuid4()), "created_platform": 3,
                        "created_platform_version": "",
                        "created_time_in_ms": str(int(time.time() * 1000)), "created_did": ""},
                    "generate_type": "generate",
                    "abilities": {
                        "type": "", "id": str(uuid.uuid4()),
                        "generate": {
                            "type": "", "id": str(uuid.uuid4()),
                            "core_param": {
                                "type": "", "id": str(uuid.uuid4()),
                                "model": "high_aes_general_v40l", "prompt": "test",
                                "seed": int(time.time() * 1000000) % 100000000 + 2500000000,
                                "sample_strength": 0.5, "image_ratio": 1,
                                "large_image_info": {
                                    "type": "", "id": str(uuid.uuid4()),
                                    "min_version": "3.0.2", "height": 2048, "width": 2048,
                                    "resolution_type": "2k",
                                }, "intelligent_ratio": False,
                            },
                        },
                        "gen_option": {"type": "", "id": str(uuid.uuid4()), "generate_all": False},
                    },
                }],
            }),
            "http_common_info": {"aid": AID},
        })

        url = f"{BASE}{uri}?aid={AID}&device_platform=web&region=SG&webId={web_id}"

        # Use page.route to intercept and modify the fetch, or just use evaluate
        # with credentials: 'include' and proper mode
        result = await page.evaluate(f"""
            async () => {{
                try {{
                    const resp = await fetch("{url}", {{
                        method: "POST",
                        headers: {json.dumps(headers)},
                        body: {json.dumps(body)},
                        credentials: "include",
                        mode: "cors",
                    }});
                    return await resp.json();
                }} catch(e) {{
                    return {{error: e.message}};
                }}
            }}
        """)

        ret = result.get("ret")
        print(f"ret={ret}, errmsg={result.get('errmsg', '')}")
        if result.get("data", {}).get("aigc_data"):
            print(f"SUCCESS task_id={result['data']['aigc_data'].get('history_record_id')}")
        elif result.get("data", {}).get("fail_code"):
            print(f"fail_code={result['data']['fail_code']}")
            print(f"msg={result['data'].get('fail_starling_message', '')}")
        elif result.get("error"):
            print(f"FETCH ERROR: {result['error']}")

        await browser.close()

asyncio.run(main())
