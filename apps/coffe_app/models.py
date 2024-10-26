from django.db import models
from uuid import uuid4
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings    
from django.core.mail import EmailMessage 
from django.db.models import Sum
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

class MemberShip_model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100 ,
        verbose_name='Membership Name'
    )

    id_card_image = models.FileField(
        upload_to='MemberShip_card_images',
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Memberships'
        verbose_name_plural = 'Memberships'


class User_model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100 ,
        verbose_name='User Name'
    )

    email = models.EmailField(
        max_length=100 ,
        verbose_name='User Email',
        unique=True,
    )

    phone = models.CharField(
        max_length=100 ,
        verbose_name='User Phone Number',
        unique=True,
    )

    profile_image = models.ImageField(
        upload_to='Members_profile_images',
        blank=True,
        null=True,
        verbose_name='User Profile Image',
        default='defualt_profile_image.jpg'

    )

    memberShip_fk = models.ForeignKey(
        'MemberShip_model', 
        on_delete=models.CASCADE ,
        related_name='User_MemberShip_Set',
        verbose_name='User MemberShip'
    )

    memberShip_number = models.IntegerField(
        auto_created=True,
        null=True,
        )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Members'
        verbose_name_plural = 'Members'

    def save(self, *args, **kwargs):
        if not self.pk or 'memberShip_fk' in kwargs.get('update_fields', []):
            super().save(*args, **kwargs)  # Save the object first to ensure 'self.pk' is set

            
            # Set the memberShip_number only if it's a new object
            max_number = User_model.objects.aggregate(models.Max('memberShip_number'))['memberShip_number__max'] or 999
            if max_number < 1000:
                max_number = 1000
            self.memberShip_number = max_number + 1
            super().save(update_fields=['memberShip_number'])

            # Image processing and QR code generation...
            card_image_path = self.memberShip_fk.id_card_image.path
            card_image = Image.open(card_image_path)

            draw = ImageDraw.Draw(card_image)
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
            #/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf

            text_elements = [
                {"text": self.name, "position": (250, 360)},
                {"text": str(self.memberShip_number), "position": (360, 400)},
            ]

            for element in text_elements:
                draw.text(element["position"], element["text"], fill="black", font=font)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=1,
            )
            qr.add_data(str(self.id))
            qr.make(fit=True)
            qr_image = qr.make_image(fill='black', back_color='white')

            qr_image = qr_image.resize((200, 200))
            card_image.paste(qr_image, (693, 295))

            final_image_io = BytesIO()
            card_image.save(final_image_io, format='JPEG')

            final_image_file = ContentFile(final_image_io.getvalue(), f'{self.id}_card.jpg')
            qr_code_image, created = User_Qr_Code_image.objects.get_or_create(
                        user_fk=self,
                        defaults={'qr_image': final_image_file}
                )
            if not created:
                # Update the QR code if it already exists
                qr_code_image.qr_image.save(f'{self.id}.png', final_image_file)
                qr_code_image.save()

            # super().save(update_fields=['profile_image'])  # Save the profile image only


            Send_email(self.name, self.memberShip_fk.name, self.email, final_image_io, self.id)
            
            # send_whatsapp_message(
            #     image_path = qr_code_image.qr_image.path, 
            #     number = self.phone, 
            #     name = self.name , 
            #     memberShip_name = self.memberShip_fk.name
            #     )

        else:
            super().save(*args, **kwargs)

        

        """super().save(*args, **kwargs)
        # Generate QR code
        qr_data = str(self.id)  # QR code data is the user's ID
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill='black', back_color='white')

        # Save QR code to a file-like object
        qr_image_io = BytesIO()
        qr_image.save(qr_image_io, format='PNG')
        qr_image_file = ContentFile(qr_image_io.getvalue(), f'{self.id}.png')

        # Check if QR code already exists
        qr_code_image, created = User_Qr_Code_image.objects.get_or_create(
            user_fk=self,
            defaults={'qr_image': qr_image_file}
        )
        if not created:
            # Update the QR code if it already exists
            qr_code_image.qr_image.save(f'{self.id}.png', qr_image_file)
            qr_code_image.save()

        if self.email:
            Send_email(self.name , self.memberShip_fk_name , self.email , qr_image_io , self.id)"""

    @property
    def bills_this_month(self):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        return self.User_Bills_Set.filter(date__gte=start_of_month).count()

    @property
    def total_bills(self):
        return self.User_Bills_Set.count()

    @property
    def total_amount_this_month(self):
        today = datetime.today()
        start_of_month = today.replace(day=1)
        return self.User_Bills_Set.filter(date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0

    @property
    def total_amount_all_time(self):
        return self.User_Bills_Set.aggregate(Sum('amount'))['amount__sum'] or 0
    
def Send_email(name, memberShip_fk_name, email, final_image_io, id):
    # Create email
    subject = "Welcome to Illusion Night Club"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Illusion Night Club - Welcome</title>
        <style>
            /* Your CSS styles */
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Illusion Night Club</h1>
            </div>
            <div class="content">
                <h2>Welcome, {name}!</h2>
                <p>We’re excited to welcome you to Illusion Night Club!</p>
                <p>
                    Attached to this email, you’ll find your personal QR code. 
                </p>
                <p>
                    This QR code is your key to exclusive access and special offers at our club.
                </p>
                <p>
                    Additionally, we’re pleased to inform you that you’re now part of our 
                    <strong>{memberShip_fk_name}</strong> membership. 
                </p>
                <p>
                    With this membership, 
                    you’ll enjoy a range of fantastic benefits and perks.
                </p>
                
                <p>
                    If you have any questions or need further assistance, feel free to reach out to us.
                </p>

                <p>Thank you for being a part of our vibrant community. 
                </p>

                <p>
                We look forward to seeing you at our next event!
                </p>

            </div>
            <div class="footer">
                <p>&copy; 2024 Illusion Night Club. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = strip_tags(html_content)  # Fallback to plain text if HTML isn't supported

    # Create email
    email_message = EmailMultiAlternatives(
        subject,
        plain_text,  # Plain text content
        settings.EMAIL_HOST_USER,
        [email],
    )

    email_message.attach_alternative(html_content, "text/html")

    # Attach QR code image
    final_image_io.seek(0)  # Reset IO stream position
    email_message.attach(f'{id}.png', final_image_io.read(), 'image/png')

    # Embed the image in the HTML email using Content-ID (cid)
    email_message.attach(f'{id}.png', final_image_io.read(), 'image/png')
    email_message.send()

# import time 
# import pywhatkit
# # import pyautogui
# # from pynput.keyboard import Key, Controller

# # keyboard = Controller()
# def send_whatsapp_message(image_path , number , name , memberShip_name):
#     print( image_path , '++++++++++++++++++++++')
#     try:
#         Message = f"""
# Dear {name},
# We’re excited to welcome you to Illusion Night Club!
# Attached to this Message, you’ll find your personal QR code.
# This QR code is your key to exclusive access and special offers at our club.
# Additionally, we’re pleased to inform you that you’re now part of our {memberShip_name} membership.
# With this membership, you’ll enjoy a range of fantastic benefits and perks.
# If you have any questions or need further assistance, feel free to reach out to us.
# Thank you for being a part of our vibrant community.
# We look forward to seeing you at our next event!
# Best regards,
# The Illusion Night Club Team
# © 2024 Illusion Night Club. All rights reserved.
#             """
#         pywhatkit.sendwhats_image(
#                 number,
#                 rf"{image_path}",
#                 Message,
#                 10,
#                 True
#             )
#         # time.sleep(10)
#         # pyautogui.click() 
#         # time.sleep(2)
#         # keyboard.press(Key.enter)
#         # keyboard.release(Key.enter)
#         print("Message sent!")
#     except Exception as e:
#         print( '>>>>>>>>>>>>>>>>>Error :', e)
    



class Bills_model(models.Model):

    user_fk = models.ForeignKey(
            'User_model',
            on_delete=models.CASCADE,
            related_name='User_Bills_Set',
            verbose_name='User Name'
        )
    
    serial_number = models.CharField(
        max_length=100 ,
        verbose_name='Bill Serial number' , 
        null=True,
        blank=True,
        unique=True
    )
    
    bill_image = models.ImageField(
        upload_to='Bill_images',
        blank=True,
        null=True,
        verbose_name='Bill Image'
    )

    amount = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Bill Amount'
    )

    date = models.DateField(
        null=True,
        blank=True, 
        auto_now=True , 
        verbose_name='Bill created Date'
    )

    notes = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'User Bills'
        verbose_name_plural = 'User Bills'

class User_Qr_Code_image(models.Model):
    user_fk = models.OneToOneField(
            'User_model',
            on_delete=models.CASCADE,
            related_name='User_Qr_Code_Set',
            verbose_name='User Qr Code'
        )

    qr_image = models.ImageField(
        upload_to='Qr_images',
        blank=True,
        null=True,
        verbose_name='Qr Image'
    )

    memberShip_number = models.AutoField(
        auto_created=True,
        primary_key=True,
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set the memberShip_number only if it's a new object
            user = User_model.objects.get(id=self.user_fk.id)
            self.memberShip_number = user.memberShip_number

        super().save(*args, **kwargs)

class Notes_model(models.Model):
    user_fk = models.ForeignKey(
            'User_model',
            on_delete=models.CASCADE,
            related_name='User_Notes_Set',
            verbose_name='User Notes'
        )
    
    note = models.TextField(
        null=True,
        blank=True, 
    )


