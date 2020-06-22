import os
from PyPDF4 import PdfFileReader, PdfFileWriter
import argparse
from PIL import Image

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = '{}_page_{}.pdf'.format(
            fname, page + 1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

def pdf_deletepages(inpath, delete_list, outpath):
    fname = os.path.splitext(os.path.basename(inpath))[0]

    if not outpath:
        outpath = '{}_output.pdf'.format(fname)

    pdf = PdfFileReader(inpath)
    pdf_writer = PdfFileWriter()

    with open(outpath, 'wb') as out:
        for page in range(pdf.getNumPages()):
            if page+1 not in delete_list:
                pdf_writer.addPage(pdf.getPage(page))

        pdf_writer.write(out)

    print('Created: {}'.format(outpath))

def pdf_generate(inpath, generate_list, outpath):
    fname = os.path.splitext(os.path.basename(inpath))[0]

    if not outpath:
        outpath = '{}_output.pdf'.format(fname)


    pdf_writer = PdfFileWriter()

    with open(outpath, 'wb') as out:
        for file in generate_list:
            pdf = PdfFileReader(file)
            for page in range(pdf.getNumPages()):
                pdf_writer.addPage(pdf.getPage(page))

        pdf_writer.write(out)

    print('Created: {}'.format(outpath))


def pdf_appendfile(inpath:str, appendpath:str, page_no: int, outpath:str):
    fname = os.path.splitext(os.path.basename(inpath))[0]
    if not outpath:
        outpath = '{}_output.pdf'.format(fname)

    pdf = PdfFileReader(inpath)
    pdf_a = PdfFileReader(appendpath)
    pdf_writer = PdfFileWriter()

    with open(outpath, 'wb') as out:
        for page in range(pdf.getNumPages()):
            pdf_writer.addPage(pdf.getPage(page))
            if page+1 == int(page_no):
                for page_a in range(pdf_a.getNumPages()):
                    pdf_writer.addPage(pdf_a.getPage(page_a))

        pdf_writer.write(out)

    print('Created: {}'.format(outpath))


def pdf_replacepage(inpath:str, replacepath:str, page_no: int, outpath:str):
    fname = os.path.splitext(os.path.basename(inpath))[0]
    if not outpath:
        outpath = '{}_output.pdf'.format(fname)

    pdf = PdfFileReader(inpath)
    pdf_d = PdfFileReader(replacepath)
    pdf_writer = PdfFileWriter()

    with open(outpath, 'wb') as out:
        for page in range(pdf.getNumPages()):
            if page+1 == int(page_no):
                for page_d in range(pdf_d.getNumPages()):
                    pdf_writer.addPage(pdf_d.getPage(page_d))
            else:
                pdf_writer.addPage(pdf.getPage(page))

        pdf_writer.write(out)

    print('Created: {}'.format(outpath))

def pdf_convertfile(inpath:str, convertpaths, outpath:str):
    fname = os.path.splitext(os.path.basename(inpath))[0]
    if not outpath:
        outpath = '{}_output.pdf'.format(fname)

    images = []
    for file in convertpaths:
        image = Image.open(file)
        image.convert('RGB')
        images.append(image)

    image_1 = images.pop(0)
    image_1.save(outpath, save_all=True, append_images=images)

    print('Created: {}'.format(outpath))




if __name__ == '__main__':
    # Initialize parser
    parser = argparse.ArgumentParser(description="Update PdfFiles")

    # Adding optional argument
    parser.add_argument(type=str, metavar='input_file', dest="infile",
                        help="PDF Input file")
    parser.add_argument("-s", dest="split", action='store_true', default=False,
                        help="Split input PDF into files containing individual pages")
    parser.add_argument("-d", dest="delete_pages", type=int, action='append', default=[],
                        help="delete page_number")
    parser.add_argument("-o", dest="output_file", type=str, action='store',
                        help="output filename")
    parser.add_argument("-a", nargs=2, metavar=('page_no', 'filename'), dest=("append"),
                        help="Append filename after page_no")
    parser.add_argument("-r", nargs=2, metavar=('page_no', 'filename'), dest=("replace"),
                        help="Replace page_no with filename ")
    parser.add_argument("-c", dest="images", type=str, action='append', default=[],
                        help="Convert images to one pdf file")
    parser.add_argument("-g", dest="generate", metavar="filename", type=str, action='append', default=[],
                        help="Combine all files in order to form a single PDF file ")

    # Read arguments from command line
    args = parser.parse_args()


    if args.images:
        print('Converting images : {}'.format(args.images))
        pdf_convertfile(args.infile, args.images, args.output_file)


    if args.split:
        print("Splitting %s to files " % args.infile)
        pdf_splitter(args.infile)

    if args.delete_pages:
        print('Deleting pages : {}'.format(args.delete_pages))
        pdf_deletepages(args.infile, args.delete_pages, args.output_file)

    if args.generate:
        print('Combining : {}'.format(args.generate))
        pdf_generate(args.infile, args.generate, args.output_file)

    if args.append:
        after_page_no, append_filename = args.append
        print('Append {} after page {}'.format(append_filename, after_page_no))
        pdf_appendfile(args.infile, append_filename, after_page_no, args.output_file)

    if args.replace:
        page_no, replace_filename = args.replace
        print('Replace page {} with {}'.format(page_no, replace_filename))
        pdf_replacepage(args.infile, replace_filename, page_no, args.output_file)



