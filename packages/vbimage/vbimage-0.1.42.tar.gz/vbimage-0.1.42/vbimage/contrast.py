from PIL import Image
from PIL import ImageEnhance

import click


@click.command(
    help="Pixelates any image."
)
@click.option(
    '-i',
    '--inputfile',
    type=click.Path(),
    default="./main.png",
    show_default=True,
    help="Input file"
)
@click.option(
    '-o',
    '--outputfile',
    type=click.Path(),
    default="./main_contrasted.png",
    show_default=True,
    help="Output file"
)
@click.option(
    '-c',
    '--contrast',
    type=click.FLOAT,
    default=1.25,
    show_default=True,
    help="Contrast factor"
)
def contrast(inputfile, outputfile, contrast):
    image = Image.open(inputfile)
    image = ImageEnhance.Contrast(image).enhance(contrast)

    image.save(outputfile, 'PNG')
