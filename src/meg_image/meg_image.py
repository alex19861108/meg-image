import os
import sys
import base64
import urllib2
import cStringIO
from PIL import ImageDraw, Image, ImageFont


file_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(os.path.dirname(file_path))


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


def draw_big_points_core(draw, points, fill, outline):
    for point in points:
        ps = []
        if isinstance(point, dict):
            ps.append((point['x']-1, point['y']-1))
            ps.append((point['x']+1, point['y']+1))
        elif isinstance(point, tuple):
            ps.append((point[0]-1, point[1]-1))
            ps.append((point[0]+1, point[1]+1))
        draw.ellipse(ps, fill, outline)


def draw_texts_core(draw, contents, fill, fontsize=50):
    font = ImageFont.truetype(os.path.join(src_path, 'fonts', 'DejaVuSerif.ttf'), size=fontsize)
    for content in contents:
        axis = content['axis']
        content = content['text']
        if isinstance(axis, dict):
            draw.text((axis['x']+1, axis['y']+1), content, font=font, fill=fill)
        elif isinstance(axis, tuple):
            draw.text((axis[0] + 1, axis[0] + 1), content, font=font, fill=fill)


def image_discard_alpha(image):
    if image.mode in ('RGBA', 'LA'):
        background = Image.new(image.mode[:-1], image.size, default_fill_color(image))
        background.paste(image, image.split()[-1])
        image = background
    image = image.convert('RGB')
    return image


def default_fill_color(image):
    if image.mode in ('RGB', 'RGBA'):
        return (0, 0, 0)
    else:
        return 0


class MegImage(object):
    @staticmethod
    def draw_points(points, image_path, saved_path, fill=128):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        draw_points_core(draw, points, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_rects_and_points(rects_groups, points_groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        for g in rects_groups:
            rects = g['rects']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            draw_rects_core(draw, rects, fill=fill)
        for g in points_groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            outline = g['outline'] if 'outline' in g else None
            draw_big_points_core(draw, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_rects_and_texts(rects_groups, text_groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        fontsize = fd_image.width / 40 if fd_image.width > 200 else 20
        draw = ImageDraw.Draw(fd_image)
        for g in rects_groups:
            rects = g['rects']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            draw_rects_core(draw, rects, fill=fill)
        for g in text_groups:
            texts = g['texts']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            draw_texts_core(draw, texts, fill, fontsize=fontsize)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_points_groups(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            draw_points_core(draw, points, fill=fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_polygon(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            outline = g['outline'] if 'outline' in g else None
            draw_polygon_core(draw, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_big_points(groups, image_path, saved_path):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        for g in groups:
            points = g['points']
            fill = g['fill'] if 'fill' in g else default_fill_color(fd_image)
            outline = g['outline'] if 'outline' in g else None
            draw_big_points_core(draw, points, fill, outline)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def draw_rects(rects, image_path, saved_path, fill=(0, 0, 0)):
        fd_image = Image.open(image_path)
        fd_image = image_discard_alpha(fd_image)
        draw = ImageDraw.Draw(fd_image)
        draw_rects_core(draw, rects, fill)
        fd_image.save(saved_path, "JPEG")

    @staticmethod
    def download_from_net(image_url, local_path):
        response = urllib2.urlopen(image_url)
        cur_image = Image.open(cStringIO.StringIO(response.read()))
        cur_image = image_discard_alpha(cur_image)
        #import requests
        #response = requests.get(image_url)
        #cur_image = Image.open(cStringIO.StringIO(response.content))
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