from aiohttp.web import Response
from aiohttp.web import View
from aiohttp_jinja2 import render_template

from lib.image import image_to_img_src
from lib.image import PolygonDrawer
from lib.image import open_image


class IndexView(View):
    async def get(self) -> Response:
        return render_template("index.html", self.request, {})

    async def post(self) -> Response:
        try:
            form = await self.request.post()
            image = open_image(form["image"].file)
            draw = PolygonDrawer(image)
            model = self.request.app["model"]
            words = []
            for coords, word, confidence in model.readtext(image):
                draw.highlight_word(coords, word)
                cropped_img = draw.crop(coords)
                cropped_img_b64 = image_to_img_src(cropped_img)
                try:
                    min_confidence = float(form["confidence"]) / 100
                except BaseException:
                    min_confidence = 0

                if confidence > min_confidence:
                    words.append(
                        {
                            "image": cropped_img_b64,
                            "word": word,
                            "confidence": confidence,
                        }
                    )
            image_b64 = image_to_img_src(draw.get_highlighted_image())
            ctx = {"image": image_b64, "words": words}
        except Exception as err:
            print(repr(err))
            ctx = {
                "error": {
                    "title": err.__class__.__name__,
                    "text": str(err)
                }
            }
        return render_template("index.html", self.request, ctx)
