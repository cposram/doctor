import requests
import json
import datetime

def fetch_and_save():
    # 這是你抓到的高榮 API 網址
    url = "https://webreg.vghks.gov.tw/RSMKS/api/WWW7"
    
    # 這是你提供的 Payload 參數
    payload = {
        "hospitalID": "KSVGH",
        "apToken": "KSVGHAPP386",
        "language": "zh-TW",
        "userToken": "",
        "deptName": "胃腸肝膽科",
        "deptCode": "29"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        # 取得進度列表
        progress_list = data.get("body", {}).get("OPDProgressList", [])
        
        now = datetime.datetime.now() + datetime.timedelta(hours=8) # 轉成台灣時間
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # 產生一個給小白看的簡單網頁
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>高榮胃腸肝膽科進度</title>
            <style>
                body {{ font-family: -apple-system, sans-serif; background: #f0f2f5; padding: 15px; }}
                .container {{ max-width: 500px; margin: auto; }}
                .header {{ text-align: center; color: #1a73e8; }}
                .card {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .room {{ font-size: 1.1em; color: #5f6368; }}
                .doctor {{ font-size: 1.4em; font-weight: bold; margin: 10px 0; }}
                .number {{ font-size: 3em; color: #d93025; font-weight: bold; }}
                .update-time {{ text-align: center; color: #888; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="header">🏥 高榮看診進度</h2>
                <p class="update-time">最後更新：{time_str}</p>
        """
        
        for p in progress_list:
            html_content += f"""
                <div class="card">
                    <div class="room">診間 {p['roomName']}</div>
                    <div class="doctor">{p['drName']} 醫師</div>
                    <div class="number">{p['progNum']}</div>
                </div>
            """
            
        html_content += "</div></body></html>"
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"抓取失敗: {e}")

if __name__ == "__main__":
    fetch_and_save()
