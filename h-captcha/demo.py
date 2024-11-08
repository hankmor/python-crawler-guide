from tesserocr import PyTessBaseAPI

with PyTessBaseAPI(path="/Users/hank/.tessdata", lang="eng") as api:
    api.SetImageFile("test.jpg")
    print(api.GetUTF8Text())  # text
    print(api.AllWordConfidences())  # confidence
