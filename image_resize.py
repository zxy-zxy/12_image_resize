import os
import sys
import argparse
from PIL import Image

COMMANDS = {
    'scaling': 'scaling',
    'resizing': 'resizing'
}


def append_subparser_for_scaling(subparsers):
    parser_scale = subparsers.add_parser(
        COMMANDS.get('scaling'),
        help='Command to scale image by a single parameter.'
    )
    parser_scale.add_argument(
        '--scale',
        type=int,
        help='scale'
    )


def append_subparser_for_resizing(subparsers):
    parser_resize = subparsers.add_parser(
        COMMANDS.get('resizing'),
        help='Command to resize image by desired height & width.'
    )
    parser_resize.add_argument(
        '--width',
        type=int,
        help='Width of target image'
    )
    parser_resize.add_argument(
        '--height',
        type=int,
        help='Height of target image'
    )


def create_parser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        help='Help for scaling & resizing commands.',
        dest='command'
    )

    append_subparser_for_scaling(subparsers)
    append_subparser_for_resizing(subparsers)

    parser.add_argument(
        'input',
        help='File path to original image.'
    )
    parser.add_argument(
        '--output',
        help='File path to target image.'
    )

    return parser


def load_image(path_to_image):
    try:
        return Image.open(path_to_image)
    except FileNotFoundError:
        return None


def parse_target_img_size(args):
    if args.command == COMMANDS.get('scaling'):
        target_img_size = tuple(
            value * args.scale
            for value in original_img.size
        )
    else:
        if args.width is not None and args.height is not None:
            target_img_size = (
                args.width,
                args.height,
            )
        elif args.height is None:
            target_img_size = (
                args.width,
                calculate_target_height(
                    original_img_size=original_img.size,
                    target_width=args.width
                )
            )
        else:
            target_img_size = (
                calculate_target_width(
                    original_img_size=original_img.size,
                    target_height=args.height
                ),
                args.height,
            )
    return target_img_size


def calculate_target_height(original_img_size, target_width):
    division_of_width = (original_img_size[0] / float(target_width))
    return int(original_img_size[1] / division_of_width)


def calculate_target_width(original_img_size, target_height):
    division_of_height = (original_img_size[1] / float(target_height))
    return int(original_img_size[0] / division_of_height)


def resize_image(original_img, target_img_size):
    img = original_img.resize(target_img_size, Image.ANTIALIAS)
    return img


def get_target_img_name(original_img_name, target_img_size):
    filepath, extension = os.path.splitext(original_img_name)
    return "{}__{}x{}{}".format(
        filepath,
        target_img_size[0],
        target_img_size[1],
        extension
    )


if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()

    original_img = load_image(args.input)
    if original_img is None:
        sys.exit('Cannot open image: {}'.format(format(args.input)))

    target_img_size = parse_target_img_size(args)

    target_img = resize_image(original_img, target_img_size)

    if args.output is None:
        target_img_name = get_target_img_name(args.input, target_img_size)
    else:
        target_img_name = args.output

    target_img.save(target_img_name)
    print("Path to proceeded image: {}".format(target_img_name))
