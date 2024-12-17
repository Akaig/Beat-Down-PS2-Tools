import sys
import psutil
import io
import os
from PIL import Image
from Lib.binariesLib import BinaryReader
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from UI.BD import Ui_MainWindow
from PyQt5.QtCore import QTimer

class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.update_memory_usage()

        self.XAF = None
        #self.texture = None
        #self.texture_name = None
        self.palette_dict = None
        self.palette_offset = None
        self.raw_data_offset = None
        self.entries = None
        self.path = None
        self.offsets = []
        self.sizes = []
        self.special_extract = []
        self.bulk_extract = []


        # Start a timer to update memory usage periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_memory_usage)
        self.timer.start(10000)  # Update every 10 seconds

        # Button Connects
        self.ui.open_button.clicked.connect(self.open_file)
        self.ui.memory_button.clicked.connect(self.update_memory_usage)
        self.ui.offsets_button.clicked.connect(self.populate_table_with_offsets)
        self.ui.section_button.clicked.connect(self.export_section)
        self.ui.export_button.clicked.connect(self.save_texture)
        self.ui.patchImage_button.clicked.connect(self.patch_image)
        self.ui.patchSection_button.clicked.connect(self.patch_section)
        self.ui.export_list.clicked.connect(self.bulk_export)

        # Table Connects
        self.ui.offsets_table.currentCellChanged.connect(self.show_image)

        self.ui.filter_input.textChanged.connect(self.start_filter_timer)

        self.filter_timer = QTimer()
        self.filter_timer.setSingleShot(True)
        self.filter_timer.timeout.connect(self.filter_table)

        self.create_folder()

    def create_folder(self):
        try:
            os.makedirs("Export", exist_ok=True)
        except Exception as e:
            print(f"Error creating folder: {e}")

    def start_filter_timer(self):
        self.filter_timer.start(300)  

    def pil2pixmap(self, image):
        bytes_img = io.BytesIO()
        image.save(bytes_img, format='PNG')

        qimg = QImage()
        qimg.loadFromData(bytes_img.getvalue())

        return QPixmap.fromImage(qimg)

    def update_memory_usage(self):
        # Get memory usage information for the current process
        process = psutil.Process()
        memory_info = process.memory_info()

        # Format memory usage information
        used_memory = memory_info.rss / (1024 * 1024)  # Convert to MB
        memory_usage_str = f"Memory Usage: {used_memory:.2f} MB"

        # Update the memory label
        self.ui.memory_label.setText(memory_usage_str)

    def open_file(self):
        xaf_file = QFileDialog.getOpenFileName(None, "Open", "", "XAF File (*.XAF)")
        file_path = xaf_file[0]
        self.path = file_path
        del(xaf_file)
        if file_path != '':
            self.XAF = BinaryReader(open(file_path, "rb+"))
            magicID = self.XAF.read(4)
            magicID = magicID.decode("utf-8").replace('\x00', "")
            if magicID == "XAF":
                self.ui.statusBar.showMessage("File " + file_path.split('/')[-1] + " Loaded.", 3000)
                self.ui.export_button.setEnabled(True)
                self.ui.offsets_button.setEnabled(True)
                self.ui.section_button.setEnabled(True)
                self.ui.patchImage_button.setEnabled(True)
                self.ui.patchSection_button.setEnabled(True)
            else:
                self.ui.statusBar.showMessage("Magic ID XAF not found.", 3000)

    def populate_table_with_offsets(self):
        """
        Populate the offsets table in the UI with entries from the XAF file

        This function reads the offsets, names, and sizes from the XAF file and
        populates the table in the UI with the information. The UI table is
        cleared before the new information is added.

        The information is read from the XAF file in the following order:

        1. The offsets table at 0x00000040
        2. The names table at the end of the offset table

        The total number of entries is stored in the self.entries variable.

        The UI table is set up with 3 columns: offset, name, and size.
        The number of rows in the table is set to the number of entries in the
        offsets table.

        The information is displayed in the UI table as follows:

        - Offset: The offset of the entry in the XAF file, displayed in hex.
        - Name: The name of the entry, displayed as a string.
        - Size: The size of the entry, displayed as an integer.

        At the end, the total number of entries is displayed in the status bar for 5 seconds.
        """

        # Clear the Offset Table
        self.ui.offsets_table.clear()
        # Create lists for offsets, sizes, and names
        offsets = []
        sizes = []
        self.offsets = []
        names = []
        # Skip XAF Header
        self.XAF.seek(0x00000040)
        # Save the offsets and sizes to their lists
        entries = 0
        while True:
            offset = self.XAF.i(1)[0]
            offsets.append(offset)
            self.offsets.append(offset)

            size = self.XAF.i(1)[0]
            sizes.append(size)
            entries += 1
            # The Value 16 means end of the list
            if size == 16:
                break

        # Get the path names of the files
        for _ in range(entries):
            # The maximum size is 260 characters
            name = self.XAF.read(0x104)
            name = name.decode('utf-8')
            name = name.replace('\x00', "")
            names.append(name)

        self.entries = entries
        self.ui.offsets_table.setColumnCount(3)
        self.ui.offsets_table.setRowCount(len(offsets))

        row = 0
        print(sizes[0])
        for i, o in enumerate(offsets):
            self.ui.offsets_table.setItem(row, 0, QTableWidgetItem(hex(o)))
            self.ui.offsets_table.setItem(row, 1, QTableWidgetItem(names[i]))
            self.ui.offsets_table.setItem(row, 2, QTableWidgetItem(str(sizes[i])))
            row += 1

        self.ui.statusBar.showMessage(f"Total entries: {entries}.", 5000)

    def generate_image(self, width, height):
        """
        Generates an image from the XAF file based on the given width and height.

        The image is generated by reading the raw data and palette from the XAF file
        and then using the palette to set the pixel colors in the image.

        :param width: The width of the image
        :param height: The height of the image
        :return: A QPixmap of the generated image
        """
        self.XAF.I(2)
        self.raw_data_offset = self.XAF.tell()
        image_data = self.XAF.B(width*height)
        self.palette_offset = self.XAF.tell()
        self.palette_dict = {i:(self.XAF.B(4)) for i in range(256)}
        img = Image.new("RGBA", (width, height))
        i = 0
        for y in range(height):
            for x in range(width):
                img.putpixel((x,y), self.palette_dict[image_data[i]])
                i += 1
        
        self.texture = img
        pixmap = self.pil2pixmap(img)
        return pixmap
    
    def show_image(self, row):
        """
        Show the image at the given row in the offsets table in the UI.

        The method first reads the offset and name of the image from the table.
        Then, it checks if the name ends with ".STX". If it does, it reads the
        width and height of the image from the XAF file, generates the image
        using the `generate_image` method, and sets the image in the UI label.
        Finally, it sets the file name in the UI label.

        :param row: The row index of the image in the offsets table
        """
        offset = self.ui.offsets_table.item(row, 0).text()
        file_name = self.ui.offsets_table.item(row, 1).text()
        self.texture_name = file_name.split("\\")[-1]
        #print(offset, file_name)
        if file_name.endswith(".STX"):
            self.XAF.seek(int(offset[2:], 16) + 0x18)
            width, height = self.XAF.I(2)
            image = self.generate_image(width, height)
            self.ui.image_label.setPixmap(image)
            self.ui.filename_label.setText(file_name)

    def save_texture(self):
        """
        Saves the current texture to a PNG file with the name of the
        corresponding section in the XAF file.

        If the texture is not set, the method does nothing.

        The file is saved in the same directory where the script is run.
        """
        if self.texture:
            self.texture.save(f"{self.texture_name}.png", "PNG")

    def open_image(self):
        """
        Opens a PNG file using a file dialog and returns the path to the selected file.

        The path of the file is displayed in the status bar for 3 seconds.

        If the file dialog is canceled, the method returns None.

        :return: The path to the selected file or None if the file dialog is canceled
        """
        image = QFileDialog.getOpenFileName(None, "Open", "", "PNG Image (*.png)")
        file_path = image[0]
        del(image)
        if file_path != '':
            self.ui.statusBar.showMessage(f"{file_path} opened", 3000)
            return file_path
        else:
            return None
        
    def open_section_file(self, file_name):
        """
        Opens a file dialog for the user to select a file with the given name
        and returns the path to the selected file.

        If the file dialog is canceled, the method returns None.

        :param file_name: The name of the file to open
        :return: The path to the selected file or None if the file dialog is canceled
        """
        file = QFileDialog.getOpenFileName(None, "Open", "", f".{file_name.split('.')[-1]} (.{file_name.split('.')[-1]})")
        file_path = file[0]
        del(file)
        if file_path != '':
            return file_path
        else:
            return None

    def export_section(self, file_name=None, offset=None, size=None):
        """
        Exports a section of data from the XAF file to a specified file.

        This method retrieves the file name, offset, and size of the section to be exported from the
        current row of the offsets table if not provided. It reads the specified section of data from
        the XAF file and writes it to a file in the "Export" directory.

        :param file_name: The name of the file to export the section to. If None, it is derived from the
                        offsets table.
        :param offset: The starting offset of the section in the XAF file. If None, it is derived from
                    the offsets table.
        :param size: The size of the section to be exported. If None, it is derived from the offsets table.
        """
        row = self.ui.offsets_table.currentRow()
        if not file_name:
            file_name = self.ui.offsets_table.item(row, 1).text().split("\\")[-1]
            offset = int(self.ui.offsets_table.item(row, 0).text()[2:], 16)
        if not size:
            size = int(self.ui.offsets_table.item(row, 2).text())
        
        self.XAF.seek(offset)
        raw_data = self.XAF.B(size)
        with open(f"Export//{file_name}", "wb") as f:
            f.write(bytes(raw_data))

        self.XAF.inputFile.close()
        self.XAF = BinaryReader(open(self.path, "rb+"))


    def patch_image(self):
        """
        Patches the image of the current texture with the one selected from a file dialog.

        The method first opens a file dialog for the user to select a PNG file. If the file dialog
        is canceled, the method returns without doing anything.

        Then, it reads the image from the selected file, converts it to RGBA, and reads the raw pixel
        data from the image.

        It then reads the colors of the image, sorts them, and checks if there are more than 256
        colors. If there are, the method shows a message in the status bar and returns without doing
        anything.

        Finally, it writes the raw pixel data and the palette to the XAF file at the offset of the
        raw data of the current texture.

        :return: None
        """
        edited_image = self.open_image()
        if edited_image:
            im = Image.open(edited_image)
            im = im.convert("RGBA")
            raw_pixels = []

            for y in range(im.height):
                for x in range(im.width):
                    pixel = im.getpixel((x, y))
                    raw_pixels.append(pixel)

            colors = im.getcolors(im.size[0]*im.size[1])
            if not colors:
                self.ui.statusBar.showMessage(f"Operation Failed. There are no colors.", 3000)
                return

            rgba_colors = [(r, g, b, a) for count, (r, g, b, a) in colors]
            rgba_colors = sorted(rgba_colors)
            print(len(rgba_colors))

            if len(rgba_colors) > 256:
                self.ui.statusBar.showMessage(f"Operation Failed. The size of the palette is {len(rgba_colors)}.", 3000)
                return
            
            palette_dict = {i:(rgba_colors[i]) for i in range(len(rgba_colors))}
            reverse_palette_dict = {v: k for k, v in palette_dict.items()}
            raw_data = [reverse_palette_dict[rp] for rp in raw_pixels]

            self.XAF.seek(self.raw_data_offset)
            self.XAF.inputFile.write(bytes(raw_data))
            for rgba in rgba_colors:
                self.XAF.inputFile.write(bytes(rgba))
                
    def patch_section(self):
        row = self.ui.offsets_table.currentRow()
        file = self.open_section_file(self.ui.offsets_table.item(row, 1).text())
        offset = int(self.ui.offsets_table.item(row, 0).text()[2:], 16)
        self.XAF.seek(offset)
        with open(file, "rb") as f:
            self.XAF.inputFile.write(f.read())

        

    def filter_table(self):
        # Get the filter list from the input box
        filter_list = [x.lower() for x in self.ui.filter_input.text().split(",")]
        # Show only rows that contain the filter text
        for row in range(self.ui.offsets_table.rowCount()):
            item = self.ui.offsets_table.item(row, 1)
            # Show result if filter list has any True value
            row_matches_any = any(filter_item in item.text().lower() for filter_item in filter_list)
            if row_matches_any:
                self.ui.offsets_table.setRowHidden(row, False)
                # Check what item returned True
                for filter_item in filter_list:
                    if filter_item.split("--")[-1] in item.text().lower():
                        # If negative filter is found, hide result
                        if '--' in filter_item:
                            self.ui.offsets_table.setRowHidden(row, True)
                # self.bulk_extract.append([self.ui.offsets_table.item(row, 1).text().split("\\")[-1], int(self.ui.offsets_table.item(row, 0).text()[2:], 16), int(self.ui.offsets_table.item(row, 2).text())])
            else:
                self.ui.offsets_table.setRowHidden(row, True)
        
    def bulk_export(self):
        for o in self.bulk_extract:
            self.export_section(o[0],o[1],o[2])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    sys.exit(app.exec_())
