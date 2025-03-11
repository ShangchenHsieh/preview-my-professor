from pyt2s.services import stream_elements
import os

template_path = "app/templets/index.html"

if os.path.exists(template_path):
    print("index.html FOUND")
else:
    print("index.html NOT FOUND")


# Custom Voice
data = stream_elements.requestTTS('Database Keys: UUIDs are often used as primary keys in databases, especially when data needs to be globally unique.', stream_elements.Voice.Russell.value)

with open('/Users/sean/Desktop/Code/preview-my-professor/app/output.mp3', '+wb') as file:
    file.write(data)


