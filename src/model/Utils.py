import colorsys


def same_color(color1, color2, offset=10    ):
    return color2[0] - offset < color1[0] < color2[0] + offset and \
           color2[1] - offset < color1[1] < color2[1] + offset and \
           color2[2] - offset < color1[2] < color2[2] + offset

def same_color_offset_rgb(color1, color2, offset_rgb):
    return color2[0] - offset_rgb[0] < color1[0] < color2[0] + offset_rgb[0] and \
           color2[1] - offset_rgb[1] < color1[1] < color2[1] + offset_rgb[1] and \
           color2[2] - offset_rgb[2] < color1[2] < color2[2] + offset_rgb[2]

def same_color_hsv(color1_rgb, color2_rgb, offset_h=4, offset_s=30, offset_v=30):
    color1_hsv = colorsys.rgb_to_hsv(color1_rgb[0], color1_rgb[1], color1_rgb[2])
    color2_hsv = colorsys.rgb_to_hsv(color2_rgb[0], color2_rgb[1], color2_rgb[2])
    print("rgb c1={0}, c2={1}".format(color1_rgb, color2_rgb))
    print("hsv c1={0}, c2={1}".format(color1_hsv, color2_hsv))

    return color2_hsv[0] - offset_h < color1_hsv[0] < color2_hsv[0] + offset_h and \
           color2_hsv[1] - offset_s < color1_hsv[1] < color2_hsv[1] + offset_s and \
           color2_hsv[2] - offset_v < color1_hsv[2] < color2_hsv[2] + offset_v
