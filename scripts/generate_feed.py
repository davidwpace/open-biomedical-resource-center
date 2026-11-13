"""RSS includes approved, due-published stories only, never public review drafts."""
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
import json
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
from render_daily_spotlight import available_stories
ROOT=Path(__file__).resolve().parent.parent
def render(destination):
    today=datetime.now(ZoneInfo("America/Chicago")).date()
    stories=available_stories(json.loads((ROOT/"data/stories.json").read_text())["stories"],today)
    root=ET.Element("rss",version="2.0");channel=ET.SubElement(root,"channel")
    for k,v in {"title":"Open Biomedical Resource Center","link":"https://davidwpace.github.io/open-biomedical-resource-center/","description":"Published educational discovery stories with sources and explicit limits."}.items():ET.SubElement(channel,k).text=v
    for s in stories:
        item=ET.SubElement(channel,"item");url="https://davidwpace.github.io/open-biomedical-resource-center/stories/"+s["slug"]+".html"
        for k,v in {"title":s["title"],"link":url,"guid":url,"description":s["intro"],"pubDate":format_datetime(datetime.fromisoformat(s["published_on"]).replace(tzinfo=ZoneInfo("America/Chicago")))}.items():ET.SubElement(item,k).text=v
    ET.indent(root);(destination/"feed.xml").write_bytes(ET.tostring(root,encoding="utf-8",xml_declaration=True))
    return {"feed.xml"}
