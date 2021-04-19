# pixelmon_image_prettyfier
A Script to reduce the size of Pixelmons Pokémon Textures and to create UV-Map Masks from your Mesh Files!

## Installing
[Lastest .exe Download](https://github.com/heinrich26/pixelmon_image_prettyfier/releases)\
Just Download the .exe Version and you're done, no installation needed!

Alternatively you can clone the Source Code with
```bash
$ git clone https://github.com/heinrich26/pixelmon_image_prettyfier.git
```
and run main.py (with Python3)\

`$ python main.py --options` ([see below](README.md#pixelmon_image_prettifier---help))\


## Running

The Script may be given a Pokemon Texture located in the proper Assets Structure as in the `Pixelmon.jar`:\
textures: `.../pixelmon/textures/pokemon/...`\
It is important that the models are in the same `pixelmon` Directory, to function\
models: `.../pixelmon/models/pokemon/\<named folders\>/...`\

If no inputs are Given, it'll run a GUI version!
  

The script has a weak searching algorithm, that locates the Model in the Folder Structure in most cases, however, if there are too many *Form-Extensions* like -normal_omega_whatever it will ask the user to select the Model folder! If for some reason, your texture was detected to another model, just rename it, so theres no Pokémon-Folder that can be associated with it, and you will be able to select by Hand!

### pixelmon_image_prettifier - help


Pixelmon-Image-Prettifier by heinrich27   © heinrich27 - 2021


**Run without Inputfile/-dir to select from the GUI!**


Define Inputs with:\
    `-i \<image\>` or `-ifile=\<image\>`   for a single Image, or\
    `--dir=\<directory\>` for a whole Directory\


Other Options:\
    `-h` or `--help`  Shows this info\
    `-m` or `--mask`  Additionally saves the calculated UV-Map\
    `--mask-only`  Only Saves the UV-Map, but no Image\
    `-f` or `--force`  Ignore Errors, doesn't ask for User Input\
    `-s` or `--smaller`  Only keeps the Image, if it was smaller than the original one!\
    `--self-select`  You will be asked to select all the PQC\'s for the Texture by Hand!\



### Running from Source
If you want to run this from source, you will need:
- **Python3**
  - pycairo
  - PIL
- **Java**


to install the Python dependancyies, run: (If you have both Python 2 & 3 installed you might need to run `pip3` or `python3 -m pip ...`)\
```bash
$ pip install pycairo, PIL
```
