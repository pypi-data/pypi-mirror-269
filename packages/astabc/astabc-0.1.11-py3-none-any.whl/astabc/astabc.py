import cv2
import argparse

def _read_image(filename):
    img = cv2.imread(filename)
    return img
def _automatic_brightness_and_contrast(image, clip_hist_percent=25):
    if isinstance(image, str):
        image = _read_image(image)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)
    
    accumulator = []
    accumulator.append(float(hist[0][0]))  # Extract single element from array
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index][0]))  # Extract single element from array
    
    maximum = accumulator[-1]
    clip_hist_percent *= maximum / 100.0
    clip_hist_percent /= 2.0
    
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha
    
    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

def correct(filename, abc=25, output_filename=None,qual = 100):
    img = _read_image(filename)
    img, alpha, beta = _automatic_brightness_and_contrast(img, abc)
    
    file_extension = filename.split(".")[-1].lower()
    abc_fn_suffix = str(abc).zfill(2)
    
    new_filename = output_filename if output_filename else filename.replace("." + file_extension, "_abc" + abc_fn_suffix + "." + file_extension)
    
    cv2.imwrite(new_filename, img, [int(cv2.IMWRITE_JPEG_QUALITY), qual])
    
    return img, alpha, beta, new_filename

def main():
    import sys
    #print process arguments with their id
    
    schema_one=True
    if sys.argv and sys.argv[1]:
        chk=sys.argv[1]
        #if chk is a number, set schema_one to False
        if chk.isdigit():
            schema_one=False
    
    descript = f"""
    
    Image Brightness and Contrast Correction\nby Guillaume D. Isabelle, 2024
    """
    parser = argparse.ArgumentParser(description=descript)
    #add quality argument
    if schema_one:
        parser.add_argument('filename', type=str, help='input image filename (or filenames as second arguments)')
        parser.add_argument('abc', type=int, nargs='?', default=15, help='automatic brightness and contrast percentage (default: 15).  You can pass it as first argument for multiple files.')
        parser.add_argument('-o','--output', type=str, help='output image filename.')
    else:
        parser.add_argument('abc', type=int, nargs='?', default=15, help='automatic brightness and contrast percentage (default: 15)')
        #parser.add_argument('filename', type=str, help='input image filename')
        parser.add_argument('files', type=str, nargs='+', help='input image filenames')
    #argument flag --feh to open the image with feh
    parser.add_argument('--feh', action='store_true', help='open the image with feh')
    parser.add_argument('-q','--quality', type=int, default=100, help='output image quality (default: 100)')
    #add --pipe so the outputs is the filename only
    parser.add_argument('-p','--pipe', action='store_true', help='output the filename only')

    
    args = parser.parse_args()
    
    
    qual=args.quality
    target_output = args.output if schema_one else ""
        
    
    if schema_one:
        filename = args.filename
        abc_value = args.abc
        img, alpha, beta, outfile=correct(filename, abc_value, target_output,qual=qual)
        print("Brightness and contrast corrected image saved as", outfile) if not args.pipe else print(outfile)
        if args.feh:
            import subprocess
            subprocess.run(['feh', outfile])
    else:
        abc_value = args.abc
        filenames = args.files
        for filename in filenames:
            img, alpha, beta, outfile = correct(filename, abc_value, target_output,qual=qual)
            print("Brightness and contrast corrected image saved as", outfile) if not args.pipe else print(outfile)
            if args.feh:
                subprocess.run(['feh', outfile])
        

    
if __name__ == '__main__':
    main()
