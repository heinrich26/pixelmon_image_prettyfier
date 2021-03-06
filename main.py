from PIL import Image, ImageDraw, ImageOps
from tkinter import filedialog, messagebox
import sys, os, getopt, math, cairo
import tkinter as tk


program_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")


def mask_image(texture):
    global start_size
    global end_size
    global user_confirmation
    global save_mask
    global save_image
    global keep_bigger
    global user_select

    cleanup = []
    mesh_files = []

    old_size = os.path.getsize(texture)
    path = texture[:texture.find("/textures/")+1]
    name = texture.rsplit("/", 1)[1].rsplit(".")[0].rsplit("-normal", 1)[0].rsplit("-zombie", 1)[0].replace("shiny", "")

    meshdir = path + "models/pokemon/" + name.replace("-", "/")

    if user_select:
        askpath = path + "models/pokemon/" + name[:name.find("-")]
        if not os.path.exists(askpath):
            askpath = path + "models/pokemon/"
        pqcs = [file.replace("\\", "/") for file in filedialog.askopenfilenames(initialdir=askpath, filetypes=[("PQC Files", ".pqc")], title="Select all PQC\'s for " + name)]
        if len(pqcs) == 0:
            raise Exception("User canceled")
        else:
            meshdir = pqcs[0][:pqcs[0].rfind("/")]
            for file in pqcs:
                mesh_files.append([meshdir + "/" + line[6:] for line in open(file, "r").read().split("\n") if line.startswith("$body")][0])
    elif not os.path.exists(meshdir):
        meshdir = path + "models/pokemon/" + name.rsplit("-", 1)[0].replace("-", "/").replace("female", "").replace("male", "")
        if not os.path.exists(meshdir) and user_confirmation:
            answer = messagebox.askyesno(message="Couldn't find directory for " + name + ", do you want to select a directory manually?", title="Directory not found!")
            if answer:
                askpath = path + "models/pokemon/" + name[:name.find("-")]
                if not os.path.exists(askpath):
                    askpath = path + "models/pokemon/"
                print(askpath)
                pqcs = [file.replace("\\", "/") for file in filedialog.askopenfilenames(initialdir=askpath, filetypes=[("PQC Files", ".pqc")], title="Select all PQC\'s for " + name)]
                if len(pqcs) == 0:
                    raise Exception("User canceled")
                else:
                    meshdir = pqcs[0][:pqcs[0].rfind("/")]
                    for file in pqcs:
                        mesh_files.append([meshdir + "/" + line[6:] for line in open(file, "r").read().split("\n") if line.startswith("$body")][0])
            else:
                raise Exception("User canceled")
        elif not os.path.exists(meshdir):
            print("No PQC-File located, skipping!")
            raise Exception("No PQC found")


    if mesh_files == []:
        meshdir_contents = os.listdir(meshdir)
        for file in meshdir_contents:
            if file.endswith(".pqc"):
                mesh_files.append([meshdir + "/" + line[6:] for line in open(meshdir + "/" + file, "r").read().split("\n") if line.startswith("$body")][0])
    for i in range(0, len(mesh_files)):
        file = mesh_files[i]
        if file.endswith(".bmd"):
            os.system("java -classpath " + program_path + " ModelConverter " + file)
            mesh_files[i] = file[:file.rfind("/") + 1] + "export-" + file[file.rfind("/") + 1:-3] + "smd"
            cleanup.append(mesh_files[i])

    raw_triangles = []



    for mesh in mesh_files:
        mesh_data = open(mesh, "r").read()
        try:
            mesh_data = mesh_data[mesh_data.find("triangles"):mesh_data.rfind("end") - 1].replace(",", ".")

            raw_verts = mesh_data.split("\n")[1:]
            try:
                raw_verts.remove("")
            except:
                pass

            del raw_verts[0::4]


            for i in range(0,int(len(raw_verts)/3)):
                raw_triangles.append((raw_verts[i*3:i*3+3]))

        except:
            print("Shit file, skipping!")
            raise Exception("Bad SMD-File")


    # image editing part

    im = Image.open(texture).convert("RGBA")
    width, height = im.size

    if mesh_files != []:
        for tri in range(0, len(raw_triangles)):
            for i in range(0, 3):
                raw_triangles[tri][i] = raw_triangles[tri][i].replace("  ", " ").split(" ")[7:9]
                raw_triangles[tri][i] = (float(raw_triangles[tri][i][0]) * width, float(raw_triangles[tri][i][1]) * height)


        mask = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                     width,
                                     height)

        draw = cairo.Context(mask)
        draw.set_source_rgb(1, 1, 1)
        draw.set_line_width(1)

        # Drawing code
        for i in range(0, len(raw_triangles)):
            draw.move_to(*raw_triangles[i][0])
            draw.line_to(*raw_triangles[i][1])
            draw.line_to(*raw_triangles[i][2])
            draw.close_path()
            draw.stroke_preserve()
            draw.stroke_preserve()
            draw.stroke_preserve()
            draw.fill()
        # End of drawing code

        raw_mask = mask.get_data().tobytes()

        mask = Image.frombuffer("RGBA", im.size, mask.get_data().tobytes(), "raw", "RGBA", 0, 0).convert("1")


        if save_image:
            im.convert("RGBA")
            im.putalpha(mask)
            sorted_colors = sorted(im.getcolors(im.size[0] * im.size[1]), key=lambda t: t[0])
            if sorted_colors[-1][1][3] == 0:
                bg_color = sorted_colors[-2][1]
            else:
                bg_color = sorted_colors[-1][1]

            im_out = Image.new("RGB", im.size, bg_color)
            im_out.paste(im, (0,0), mask)
            if len(sorted_colors) <= 256:
                print(len(sorted_colors), "I think I can make you Palette Mode :)")
                im_out.convert("P")
    else:
        sorted_colors = sorted(im.getcolors(im.size[0] * im.size[1]), key=lambda t: t[0])
        if sorted_colors[-1][1][3] == 0:
            bg_color = sorted_colors[-2][1]
        else:
            bg_color = sorted_colors[-1][1]
        im_out = Image.new("RGB", im.size, bg_color)
        im_out.paste(im, (0, 0), im)
        if len(sorted_colors) <= 256:
            im_out.convert("P")

    # write the file
    new_texture = texture[:texture.rfind("/")] + "/bg_averaged" + texture[texture.rfind("/"):]
    try:
        os.mkdir(texture[:texture.rfind("/")] + "/bg_averaged")
    except:
        pass
    im_out = im_out.convert("RGB", Image.WEB)

    if mesh_files != [] and save_mask:
        mask.save(new_texture[:-4] + "_mask.png", optimize=True)

    if save_image:
        im_out.save(new_texture, optimize=True)
        new_size = os.path.getsize(new_texture)
        if new_size >= old_size and not keep_bigger:
            cleanup.append(new_texture)
            print("Output bigger than Input, skipping!")
        else:
            start_size += old_size
            end_size += new_size
            print("Old Texture size: " + str(old_size) + " New Texture size:" + str(new_size) + "\n" + name + "\'s Texture size was reduced by " + str(old_size - new_size) + " bytes! hurray")

    for file in cleanup:
        os.remove(file)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    inputfile = ""
    inputdirectory = ""
    save_mask = False
    save_image = True
    user_confirmation = True
    keep_bigger = True
    user_select = False

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:mfs", ["ifile=", "help", "dir=", "mask-only", "mask", "smaller", "self-select"])
        except getopt.GetoptError:
            print('Usage: main.py <options>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', "--help"):
                print("pixelmon_image_prettifier - help\n\n  Pixelmon-Image-Prettifier by heinrich27 \u00A9 heinrich27 - 2021\n  Meant for internal use ONLY! Do not distibute!\n\nRun without Inputfile/-dir to select from the GUI!\n\nDefine Inputs with:\n    -i <image> / -ifile=<image>   for a single Image, or\n    --dir=<directory> for a whole Directory\n\nOther Options:\n    -h / --help  Shows this info\n    -m / --mask  Additionally saves the calculated UV-Map\n    --mask-only  Only Saves the UV-Map\n    -f / --force  Ignore Errors, doesn't ask for User Input\n    -s/--smaller  Does only keep the image, if its smaller than the old one!\n    --self-select  You will be asked to select all the PQC\'s for the Texture by Hand!")
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg.strip("\"").replace("\\", "/")
            elif opt == "--dir":
                inputdirectory = os.path.abspath(arg.strip("\"").replace("\\", "/")).replace("\\", "/")

            if opt in ("-m", "--mask", "--mask-only"):
                save_mask = True
                if opt == "--mask-only":
                    save_image = False

            if opt in ("-f", "--force"):
                user_confirmation = False

            if opt in ("-s", "--smaller"):
                keep_bigger = False

            if opt == "--self-select":
                user_select = True


    start_size = 0
    end_size = 0

    if inputfile != "" and os.path.isfile(inputfile):
        if inputfile[-4:].lower().endswith(".png"):
            try:
                mask_image(inputfile)
            except:
                print("An Error occured during Image processing")
        else:
            print("The given file isn\'t a PNG!")
            sys.exit(2)

    elif inputdirectory != "" and os.path.isdir(inputdirectory):
        for file in os.listdir(inputdirectory):
            if file.endswith(".png"):
                try:
                    print(inputdirectory + "/" + file)
                    mask_image(inputdirectory + "/" + file)
                except:
                    print("An Error occured during Image processing! Skipping")

    # else - run GUI interface
    else:
        textures = filedialog.askopenfilenames(title='Choose image(s)', filetypes=[("PNG Images", ".png")])
        if textures == "":
            sys.exit()
        for texture in textures:
            if texture.endswith(".png"):
                try:
                    mask_image(texture)
                except:
                    pass

    root.destroy()
    print("Total start size: " + str(start_size) + "; Total end size: " + str(end_size) + " Total size reduced by " + str(start_size-end_size) + " bytes!")
