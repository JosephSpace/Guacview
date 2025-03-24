![Guacomole View - Google Chrome 2025-03-24 19-04-53](https://github.com/user-attachments/assets/d082aec1-2485-4f0d-9eea-fbf3c5e78e13)

The primary goal of this application is to retrieve data from users connected to the same Active Directory server as you, streamlining IT-related tasks and eliminating file clutter. Instead of manually searching for specific files or information, the application provides an efficient and organized way to access and manage user data.

Its main objective is to simplify your workflow by automating processes, allowing you to run tasks effortlessly. If you have a relevant file, you can easily import it and let the system handle the rest, ensuring a smooth and hassle-free experience.

* CPU %
* Memory %
* User Files
* AD Server
* RAM Used/Total
* Disk Used/Total
* User Control

## Setup

installs the Flask framework, allowing you to develop web applications and APIs in Python.

```
pip install flask
```

When you import this file, all libraries will be downloaded.

```
pip install -r requirements.txt
```

``` 
Guacview/                      # Ana proje dizini
├── app.py                     # Ana Flask uygulaması, route'lar ve kimlik doğrulama işlemleri
├── api.py                     # Sistem istatistikleri için API fonksiyonları
├── requirements.txt           # Proje bağımlılıkları
│
├── __pycache__/               # Python derleme dosyaları
│   ├── api.cpython-312.pyc
│   └── auth.cpython-312.pyc
│
├── static/                    # Statik dosyalar dizini
│   ├── css/                   # CSS stil dosyaları
│   │   ├── dashboard.css      # Dashboard sayfası için stil
│   │   ├── login_style.css    # Giriş sayfası için stil
│   │   ├── main.css           # Ana sayfa için stil
│   │   ├── navbar.css         # Navigasyon çubuğu için stil
│   │   └── style.css          # Genel stil dosyası
│   │
│   └── js/                    # JavaScript dosyaları
│       ├── applications.js    # Uygulamalar sayfası için script
│       ├── dashboard.js       # Dashboard sayfası için script
│       ├── navbar.js          # Navigasyon çubuğu için script
│       └── script.js          # Genel script dosyası
│
└── templates/                 # HTML şablon dosyaları
    ├── applications.html      # Uygulamalar sayfası
    ├── dashboard.html         # Dashboard sayfası
    ├── home.html              # Ana sayfa
    ├── login.html             # Giriş sayfası
    └── table.html             # Tablo görünümü sayfası
``` 
## Maintainer

https://github.com/JosephSpace

## Credits

https://github.com/JosephSpace/Guacview

## Contact

- İnstagram: https://www.instagram.com/joseph.ddf/
- LinkedIn: https://www.linkedin.com/in/yusuf-aşkın-56015b232/
- Mail: yusufaliaskin@gmail.com

---
## License

MIT

The included Freeboard code is redistributed per its MIT License.
