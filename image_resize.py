import os
import sys
import fractions
import argparse
from PIL import Image

COMMANDS = {
    'scale': 'scale',
    'resize': 'resize'
}


def append_subparser_for_scaling(subparsers):
    parser_scale = subparsers.add_parser(
        COMMANDS.get('scale'),
        help='Command to scale image by a single parameter.'
    )
    parser_scale.add_argument(
        'scale',
        type=int,
        help='Scale coefficient.'
    )


def append_subparser_for_resizing(subparsers):
    parser_resize = subparsers.add_parser(
        COMMANDS.get('resize'),
        help='Command to resize image by desired height & width.'
    )
    parser_resize.add_argument(
        '--width',
        type=int,
        help='Width of target image.'
    )
    parser_resize.add_argument(
        '--height',
        type=int,
        help='Height of target image.'
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


def get_target_size_by_scale(original_img_size, scale):
    target_img_size = tuple(
        dimension_value * scale
        for dimension_value in original_img_size
    )
    return target_img_size


def get_target_size_by_dimensions(original_img_size, width, height):
    if width is not None and height is not None:
        target_img_size = (
            width,
            height,
        )
    elif height is None:
        target_img_size = (
            width,
            calculate_target_height(
                original_img_size=original_img_size,
                target_width=width
            )
        )
    else:
        target_img_size = (
            calculate_target_width(
                original_img_size,
                height,
            ),
            height
        )
    return target_img_size


def calculate_target_height(original_img_size, target_width):
    division_of_width = (original_img_size[0] / float(target_width))
    return int(original_img_size[1] / division_of_width)


def calculate_target_width(original_img_size, target_height):
    division_of_height = (original_img_size[1] / float(target_height))
    return int(original_img_size[0] / division_of_height)


def verify_aspect_ratio(original_img_size, target_img_size):
    original = fractions.Fraction(original_img_size[0], original_img_size[1])
    target = fractions.Fraction(target_img_size[0], target_img_size[1])
    if original == target:
        return True
    return False


def resize_image(original_img, target_img_size):
    img = original_img.resize(target_img_size, Image.ANTIALIAS)
    return img


def get_target_img_name(original_img_name, target_img_size):
    filepath, extension = os.path.splitext(original_img_name)
    return '{}__{}x{}{}'.format(
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

    if args.command == COMMANDS.get('scale'):
        target_img_size = get_target_size_by_scale(original_img.size, args.scale)
    elif args.command == COMMANDS.get('resize'):
        target_img_size = get_target_size_by_dimensions(original_img.size, args.width, args.height)
    else:
        sys.exit('Cannot parse operation type.')

    if not verify_aspect_ratio(original_img.size, target_img_size):
        print('Aspect ratio is collapsed.')

    target_img = resize_image(original_img, target_img_size)

    if args.output is None:
        target_img_name = get_target_img_name(args.input, target_img_size)
    else:
        target_img_name = args.output

    target_img.save(target_img_name)
    print('Image has been saved at: {}'.format(target_img_name))
