import torchvision
import torch
import PIL.Image as Image

labels_dict = {1: 'rigid_plastic',
               2: 'cardboard', 3: 'metal', 4: 'soft_plastic'}
colors_dict = {1: (255, 0, 0), 2: (0, 255, 0), 3: (0, 0, 0), 4: (0, 0, 255)}


def inference(image):
    """
    takes in PIL image returns PIL image
    """
    model = get_model(r"./lifehack/weights/Model_2.pt")
    model.eval()
    image = torchvision.transforms.ToTensor()(image)
    image_output = (image.clone() * 255).to(torch.uint8)
    with torch.no_grad():
        output = model([image])[0]
    boxes = output['boxes']
    labels = output['labels']
    scores = output['scores']

    draw_boxes = []
    draw_labels = []
    draw_colors = []
    for box, label, score in zip(boxes, labels, scores):
        if score > 0.5:
            draw_boxes.append(box.tolist())
            draw_labels.append(labels_dict[int(label)])
            draw_colors.append(colors_dict[int(label)])
    if draw_boxes:
        image_output = torchvision.utils.draw_bounding_boxes(
            image_output, torch.tensor(draw_boxes), draw_labels, colors=draw_colors)
    image_output = torch.permute(image_output, (1, 2, 0)).numpy()
    image_output = Image.fromarray(image_output)
    return image_output


def get_model(path):
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
        num_classes=5)
    # model = torchvision.models.detection.ssdlite320_mobilenet_v3_large(
    #     num_classes=5)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model
