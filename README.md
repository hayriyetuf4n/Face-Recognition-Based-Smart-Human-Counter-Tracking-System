# Yuz Tanima Destekli Akilli İnsan Sayaci ve Takip Sistemi/Face Recognition Based Smart Human Counter & Tracking System
Bu proje, Python ve OpenCV kullanarak geliştirilmiş, güvenlik ve istatistik odaklı bir görüntü işleme çözümüdür. Sistem, sadece bir yüzü algılamakla kalmaz, aynı zamanda o yüzün "parmak izini" (encoding) çıkararak daha önce görülüp görülmediğini anlar.

Öne Çıkan Fonksiyonlar:

Benzersiz Kişi Sayma: Geleneksel sayaçların aksine, aynı kişinin kamera önünde beklemesi veya gidip gelmesi durumunda sayacı mükerrer artırmaz. Her benzersiz yüzü hafızasına alarak toplam "tekil" kişi sayısını tutur.

Gerçek Zamanlı Tanıma: face_recognition kütüphanesi sayesinde tanımlı personeli/kişileri anlık olarak teşhis eder.

Optimize Edilmiş Performans: Görüntü boyutlandırma ve işlemci dostu döngüler sayesinde düşük gecikme ile çalışır.

Hata Payı Yönetimi: Ayarlanabilir tolerans eşiği (Tolerance) ile farklı açılardan ve ışık koşullarından kaynaklanan hatalı sayımları minimize eder.
