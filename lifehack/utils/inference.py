import torchvision
import torch
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import PIL.ImageColor as ImageColor

labels_dict = {1: 'rigid_plastic',
               2: 'cardboard', 3: 'metal', 4: 'soft_plastic'}


def inference(image):
    """
    takes in PIL image returns PIL image
    """
    model = get_model(
        r'./lifehack/weights/Model_2.pt')
    model.eval()
    image_output = image.copy()
    image = torchvision.transforms.ToTensor()(image)
    with torch.no_grad():
        output = model([image])[0]
    boxes = output['boxes']
    labels = output['labels']
    scores = output['scores']
    for box, label, score in zip(boxes, labels, scores):
        if score > 0.2:
            box = box.tolist()
            draw_bounding_box_on_image(image_output, box[1], box[0], box[3], box[2], display_str_list=[
                                       labels_dict[int(label)], str(float(score))])
    return image_output


def get_model(path):
    model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(
        num_classes=5)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model


def draw_bounding_box_on_image(image,
                               xmin,
                               ymin,
                               xmax,
                               ymax,
                               color='red',
                               thickness=2,
                               display_str_list=(),
                               font_size=10,
                               use_normalized_coordinates=False):
    """
    Taken from tensorflow object_detection models/research/object_detection/utils/visualization_utils.py.
    Args:
        image: a PIL.Image object.
        ymin: ymin of bounding box.
        xmin: xmin of bounding box.
        ymax: ymax of bounding box.
        xmax: xmax of bounding box.
        color: color to draw bounding box. Default is red.
        thickness: line thickness. Default value is 4.
        display_str_list: list of strings to display in box
                        (each to be shown on its own line).
        use_normalized_coordinates: If True (default), treat coordinates
        ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat
        coordinates as absolute.
    """
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    if use_normalized_coordinates:
        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                      ymin * im_height, ymax * im_height)
    else:
        (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
    if thickness > 0:
        draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                   (left, top)],
                  width=thickness,
                  fill=color)
    try:
        font = ImageFont.truetype('arial.ttf', font_size)
    except IOError:
        font = ImageFont.load_default()

    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = bottom + total_display_str_height
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = 0
        draw.rectangle(
            [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                              text_bottom)],
            fill=color)
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill='black',
            font=font)
        text_bottom -= text_height - 2 * margin


# test_path = r"C:\Users\fongy\Documents\lifehack\zerowaste-f-final\splits_final_deblurred\val\data\01_frame_000245.PNG"
# test = Image.open(test_path)
# out = inference(test)
# out.show()
