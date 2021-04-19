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

    cleanup = []
    old_size = os.path.getsize(texture)
    path = texture[:texture.find("/textures/")+1]
    name = texture.rsplit("/", 1)[1].rsplit(".")[0].rsplit("-normal", 1)[0].rsplit("-zombie", 1)[0].replace("shiny", "")

    meshdir = path + "models/pokemon/" + name.replace("-", "/")

    if not os.path.exists(meshdir):
        meshdir = path + "models/pokemon/" + name.rsplit("-", 1)[0].replace("-", "/").replace("female", "").replace("male", "")
        if not os.path.exists(meshdir) and user_confirmation:
            answer = messagebox.askyesno(message="Couldn't find directory, do you want to select a directory manually?", title="Directory not found!")
            if answer:
                meshdir = filedialog.askdirectory(mustexist=True, initialdir=path + "models/pokemon/" + name.replace("-", "/").rsplit("/", 1)[0], title="Select a Directory containing meshes for " + name)
            else:
                raise Exception("User canceled")
        elif not os.path.exists(meshdir):
            print("No SMD-Model located, skipping!")
            raise Exception("No SMD found")


    meshdir_contents = os.listdir(meshdir)
    mesh_files = []
    for file in meshdir_contents:
        if file.endswith(".pqc"):
            mesh_files.append([meshdir + "/" + line[6:] for line in open(meshdir + "/" + file, "r").read().split("\n") if line.startswith("$body")][0])
    for i in range(0, len(mesh_files)):
        if file.endswith(".bmd"):
            file = mesh_files[i]
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


        if save_mask:
            im.putalpha(mask)
            im.convert("RGBA")
            colors = im.getcolors(im.size[0] * im.size[1])
            sorted_colors = sorted(colors, key=lambda t: t[0])
            if sorted_colors[-1][1][3] == 0:
                bg_color = sorted_colors[-2][1]
            else:
                bg_color = sorted_colors[-1][1]

            im_out = Image.new("RGB", im.size, bg_color)
            im_out.paste(im, (0,0), mask)
    else:
        im.convert("RGBA")
        colors = im.getcolors(colorpicking_im.size[0] * colorpicking_im.size[1])
        sorted_colors = sorted(colors, key=lambda t: t[0])
        if sorted_colors[-1][1][3] == 0:
            bg_color = sorted_colors[-2][1]
        else:
            bg_color = sorted_colors[-1][1]
        im_out = Image.new("RGB", im.size, bg_color)
        im_out.paste(im, (0, 0), im)

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
        start_size += old_size
        end_size += new_size
        print("Old Texture size: " + str(old_size) + " New Texture size:" + str(new_size) + "\nTexture size was reduced by " + str(old_size - new_size) + " bytes! hurray")

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

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi:mf", ["ifile=", "help", "dir=", "mask-only", "mask"])
        except getopt.GetoptError:
            print('Usage: main.py <options>')
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', "--help"):
                print("pixelmon_image_prettifier - help\n\n  Pixelmon-Image-Prettifier by heinrich27 \u00A9 heinrich27 - 2021\n  Meant for internal use ONLY! Do not distibute!\n\nRun without Arguments to Select for a GUI!\n\nDefine Inputs with:\n    -i <image> / -ifile=<image>   for a single Image, or\n    --dir=<directory> for a whole Directory\n\nOther Options:\n    -h / --help  Shows this info\n    -m / --mask  Additionally saves the calculated UV-Map\n    --mask-only  Only Saves the UV-Map\n    -f / --force  Ignore Errors, doesn't ask for User Input")
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
        textures = filedialog.askopenfilenames(title='Choose image(s)')
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
