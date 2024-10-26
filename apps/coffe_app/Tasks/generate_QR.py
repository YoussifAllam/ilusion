# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile

# from ..models import User_Qr_Code_image , User_model

# def Generate_QR(self, *args, **kwargs):
#         # Save the user first
#         super().save(*args, **kwargs)
        
#         # Generate QR code
#         qr_data = str(self.id)  # QR code data is the user's ID
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data)
#         qr.make(fit=True)
#         qr_image = qr.make_image(fill='black', back_color='white')

#         # Save QR code to a file-like object
#         qr_image_io = BytesIO()
#         qr_image.save(qr_image_io, format='PNG')
#         qr_image_file = ContentFile(qr_image_io.getvalue(), f'{self.id}.png')

#         # Check if QR code already exists
#         qr_code_image, created = User_Qr_Code_image.objects.get_or_create(
#             user_fk=self,
#             defaults={'qr_image': qr_image_file}
#         )
#         if not created:
#             # Update the QR code if it already exists
#             qr_code_image.qr_image.save(f'{self.id}.png', qr_image_file)
#             qr_code_image.save()