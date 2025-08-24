import base64
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont

# Create a simple image with the text "2 + 2"
img_width, img_height = 400, 200
image = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))  # black background
draw = ImageDraw.Draw(image)

text = "2 + 2"
# Use default PIL font
font = ImageFont.load_default()
# Pillow 10+ removed textsize; use textbbox to measure
bbox = draw.textbbox((0, 0), text, font=font)
text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
position = ((img_width - text_width) // 2, (img_height - text_height) // 2)
draw.text(position, text, font=font, fill=(255, 255, 255))  # white text

# Convert image to base64 data URL
buffered = BytesIO()
image.save(buffered, format="PNG")
img_bytes = buffered.getvalue()
img_b64 = base64.b64encode(img_bytes).decode("utf-8")
data_url = f"data:image/png;base64,{img_b64}"

# Send request to backend
url = "http://localhost:8900/calculate"
payload = {"image": data_url, "dict_of_vars": {}}

print("Sending request to:", url)
resp = requests.post(url, json=payload, timeout=120)
print("Status:", resp.status_code)
print("Response:")
print(resp.text)