import sys
import base64
import requests
import cStringIO
from PIL import ImageDraw, Image


def draw_rects_core(draw, rects, fill):
    #Lw, Lh = fd_image.size
    for rect in rects:
        left, top, width, height = rect['left'], rect['top'], rect['width'], rect['height']
        draw.line((left, top, left+width, top), fill=fill)
        draw.line((left, top, left, top+height), fill=fill)
        draw.line((left+width, top, left+width, top+height), fill=fill)
        draw.line((left, top+height, left+width, top+height), fill=fill)


def draw_points_core(draw, points, fill):
    ps = []
    for point in points:
        if isinstance(point, dict):
            ps.append((point['x'], point['y']))
        elif isinstance(point, tuple):
            ps.append(point)
    draw.point(ps, fill)


def draw_polygon_core(draw, points, fill, outline):
    ps = []
    for point in points:
        if isinstance(point, dict):
            ps.append((point['x'], point['y']))
        elif isinstance(point, tuple):
            ps.append(point)
    draw.polygon(ps, fill, outline)


def draw_ellipse_core(draw, points, fill, outline):
    ps = []
    for point in points:
        if isinstance(point, dict):
            ps.append((point['x']-1, point['y']-1))
            ps.append((point['x']+1, point['y']+1))
        elif isinstance(point, tuple):
            ps.append((point[0]-1, point[1]-1))
            ps.append((point[0]+1, point[1]+1))
        draw.ellipse(ps, fill, outline)


class MegImage(object):
    @staticmethod
    def draw_points(points, image_path, saved_path, fill=128):
        fd_image = Image.open(image_path)
        draw = ImageDraw.Draw(fd_image)
        draw_points_core(draw, points, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_points_groups(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else (0, 0, 0)
            draw_points_core(draw, points, fill=fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_polygon(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else (0, 0, 0)
            outline = g['outline'] if 'outline' in g else None
            draw_polygon_core(draw, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_ellipse(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else (0, 0, 0)
            outline = g['outline'] if 'outline' in g else None
            draw_ellipse_core(draw, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_rects(rects, image_path, saved_path, fill=(0, 0, 0)):
        fd_image = Image.open(image_path)
        draw = ImageDraw.Draw(fd_image)
        draw_rects_core(draw, rects, fill)
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