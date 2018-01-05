import sys
import base64
import urllib2
import requests
import cStringIO
from PIL import ImageDraw, Image


def draw_rects_core(fd_image, rects, fill):
    draw = ImageDraw.Draw(fd_image)
    #Lw, Lh = fd_image.size
    for rect in rects:
        left, top, width, height = rect['left'], rect['top'], rect['width'], rect['height']
        draw.line((left, top, left+width, top), fill=fill)
        draw.line((left, top, left, top+height), fill=fill)
        draw.line((left+width, top, left+width, top+height), fill=fill)
        draw.line((left, top+height, left+width, top+height), fill=fill)


def draw_points_core(fd_image, points, fill):
    draw = ImageDraw.Draw(fd_image)
    ps = []
    for point in points:
        if isinstance(point, dict):
            ps.append((point['x'], point['y']))
        elif isinstance(point, tuple):
            ps.append(point)
    draw.point(ps, fill)


def draw_polygon_core(fd_image, points, fill, outline):
    draw = ImageDraw.Draw(fd_image)
    ps = []
    for point in points:
        if isinstance(point, dict):
            ps.append((point['x'], point['y']))
        elif isinstance(point, tuple):
            ps.append(point)
    draw.polygon(ps, fill, outline)


class MegImage(object):
    @staticmethod
    def draw_points(points, image_path, saved_path, fill=128):
        fd_image = Image.open(image_path)
        draw_points_core(fd_image, points, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_points_groups(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else 128
            draw_points_core(fd_image, points, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_polygon(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else 128
            outline = g['outline'] if 'outline' in g else 128
            draw_polygon_core(fd_image, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_rects(rects, image_path, saved_path, fill=128):
        fd_image = Image.open(image_path)
        draw_rects_core(fd_image, rects, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def download_from_net(image_url, local_path):
        #pic_f = urllib2.urlopen(image_url)
        response = requests.get(image_url)
        cur_image = Image.open(cStringIO.StringIO(response.content))
        cur_image.save(local_path, "JPEG")
        if cur_image:
            cur_image.close()

    @staticmethod
    def base64toimg(s, img):
        image_data = base64.b64decode(s)
        with open(img, 'wb') as fd:
            fd.write(image_data)

    @staticmethod
    def imgtobase64(img):
        with open(img, 'rb') as fd:
            content = fd.read()
            image_base64 = base64.b64encode(content)
            return image_base64


if __name__ == '__main__':
    mi = MegImage()
    b64 = MegImage.imgtobase64(sys.argv[1])
    MegImage.base64toimg(b64, sys.argv[2])