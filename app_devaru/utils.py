import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

def generate_barcode(code):
    buffer = BytesIO()

    code128 = barcode.get_barcode_class("code128")
    barcode_obj = code128(code, writer=ImageWriter())

    # Bars only - the item code is printed separately on the label
    barcode_obj.write(
        buffer,
        {
            "write_text": False,
            "module_height": 10.0,
            "quiet_zone": 2.0,
        }
    )

    return base64.b64encode(buffer.getvalue()).decode()