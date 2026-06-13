import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    url=f"https://wttr.in/city?{format}=3"
    try:
        response=request.get(url,timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"weather unavailable({e})"

def get_quote():
    url=f"hhtps://zenquotes.io/api/random"
    try:
        response=request.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()
        quote=data[0]["q"]
        author=data[0]["a"]
        return f'"{quote}"-{author}'
    except Exception as e:
        return f"quote unavailable ({e})"

def build_summary():
    today=date.today().strftime("%A, %d %B %Y")
    weather=get_weather()
    quote=get_quote()
    summary=f"""
    ========================================================
      PULSE-Daily summary
      {today}
    ========================================================
      WEATHER
      {weather}

      QUOTE
      {quote}

    ========================================================
    """
    return summary

    def run():
        summary=build_summary()
        print(summary)
        with open("daily_summary.txt","w",encoding="utf-8") as f:
            f.write(summary)
        
        print("Pulse ran successfully")

        if _name_=="_main_":
            run()
