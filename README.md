# pixelmon_image_prettyfier
A Script to reduce the size of Pixelmons Pokémon Textures and to create UV-Map Masks from your Mesh Files!

## Installing
Lastest .exe Download: https://github.com/heinrich26/pixelmon_image_prettyfier/releases
Just Download the .exe Version and you're done, no installation needed!

Alternatively you can just clone the source code, and run python main.py --options (see below)
## Running

The Script may be given a Pokemon Texture located in the proper Assets Structure as in the Pixelmon.jar:\
textures: .../pixelmon/textures/pokemon/... \
It is important that the models are in the same *"pixelmon"* Directory, to function\
models: .../pixelmon/models/pokemon/\<named folders\>/...\

If no inputs are Given, it'll run a GUI version!
  

The script has a weak searching algorithm, that locates the Model in the Folder Structure in most cases, however, if there are too many *Form-Extensions* like -normal_omega_whatever it will ask the user to select the Model folder! If for some reason, your texture was detected to another model, just rename it, so theres no Pokémon-Folder that can be associated with it, and you will be able to select by Hand!

### pixelmon_image_prettifier - help


Pixelmon-Image-Prettifier by heinrich27   © heinrich27 - 2021
Meant for internal use ONLY! Do not distibute!


**Run without Inputfile/-dir to select from the GUI!**


Define Inputs with:\
    -i <image> / -ifile=<image>   for a single Image, or\
    --dir=<directory> for a whole Directory\


Other Options:\
    -h / --help  Shows this info\
    -m / --mask  Additionally saves the calculated UV-Map\
    --mask-only  Only Saves the UV-Map, but no Image\
    -f / --force  Ignore Errors, doesn't ask for User Input\
    -s / --smaller  Only keeps the Image, if it was smaller than the original one!\
    --self-select  You will be asked to select all the PQC\'s for the Texture by Hand!\



### Running from Source
If you want to run this from source, you will need:
- **Python3**
  - pycairo
  - PIL
- **Java**


to install the Python dependancyies, run: (If you have Python2 & 3 installed you might need to run pip3 oder python3 -m pip ...)\
**pip install pycairo, PIL**
