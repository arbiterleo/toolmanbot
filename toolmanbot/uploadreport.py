import pyimgur

def upload_img(img_path):
    CLIENT_ID = "e00f48cb1956755"
    PATH = img_path #A Filepath to an image on your computer"
    title = "Uploaded with PyImgur"

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type)
