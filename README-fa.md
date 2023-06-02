# مدیریت کننده کاربران مرزبان

## قابلیت ها
- چند برابر کردن حجم باقیمانده کاربران
- افزایش و کاهش حجم تمامی کاربران
- افزایش و کاهش زمان تمامی کاربران
- حذف کاربران بسته به روز انقضا

# نحوه استفاده 💡

ابتدا API مرزبان را فعال کنید ،
میتوانید با اضافه کردن  DOCS=True اون رو فعال کنید

```bash
wget -qO- https://github.com/M03ED/Marzban_User_Manager/blob/main/main.py
wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 -
python3 -m pip install -r requirements.txt
python3 main.py
```

در صورتی که میخواهید هر بار با اجرا اسکریپت نیازی به وارد کردن اطلاعات نداشته باشید میتونید اطلاعات واقعی خودتون رو در فایل جایگزین کنید
```bash
username = input('Enter Your Username:')
password = input('Enter Your Password:')
DOMAIN = input('Enter Your Panel Domain (without https):')
PORT = input('Enter Your Panel Port (1-65535):')
```

مثال:
```bash
username = 'username'
password = 'password'
DOMAIN = 'domain.com'
PORT = '12345'
```

# مشارکت
اگر اشکالی می بینید یا ایده ای برای بهتر کردن اسکریپت دارید، می توانید یک Pull Request باز کنید و تغییرات را Commit کنید.
