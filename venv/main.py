import requests
from IPython.display import HTML
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib import patches
from io import BytesIO

subscription_key = "9422b51e8b594256b54c1b1f4583c46d"
assert subscription_key
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'src/surprised.jpg'


headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}


def annotate_image(image_url):
    response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
    faces = response.json()

    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    plt.figure(figsize=(8,8))
    ax = plt.imshow(image, alpha=0.6)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        em = fa["emotion"]

        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(origin, fr["width"], \
                              fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %d, %s"%(fa["gender"].capitalize(), fa["age"],em) ,fontsize=20, weight="bold", va="bottom")
    plt.axis("off")
    plt.show()


annotate_image("https://how-old.net/Images/faces2/main001.jpg")
# annotate_image("https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1543734668&di=8e78b44935225bd4cf47f5310817c956&imgtype=jpg&er=1&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F962bd40735fae6cd40a7035d04b30f2442a70ffe.jpg")