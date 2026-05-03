import cv2
import face_recognition
import os
import numpy as np
# --- 1. AŞAMA: ÖĞRETME (EĞİTİM) ---
yol = r'C:\PROJE\bilinen_kisiler'
print("Sistem eğitiliyor, lütfen bekleyin...")

bilinen_kodlar = []
isimler = []

# Klasör kontrolü
if not os.path.exists(yol):
    print(f"HATA: {yol} dizini bulunamadı!")
    exit()

for dosya in os.listdir(yol):
    if dosya.lower().endswith(('.jpg', '.jpeg', '.png')):
        tam_yol = os.path.join(yol, dosya)
        
        # Türkçe karakterli dosya yolları için güvenli okuma
        resim_verisi = np.fromfile(tam_yol, np.uint8)
        img = cv2.imdecode(resim_verisi, cv2.IMREAD_COLOR)
        
        if img is not None:
            # İsmi temizle (Örn: ali_1.jpg -> ALI)
            temiz_isim = os.path.splitext(dosya)[0].split('_')[0].upper()
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            kodlar = face_recognition.face_encodings(img_rgb)
            
            if len(kodlar) > 0:
                bilinen_kodlar.append(kodlar[0])
                isimler.append(temiz_isim)
                print(f"✓ {temiz_isim} sisteme tanımlandı.")

print(f"\nEğitim tamamlandı. Tanınacak kişiler: {list(set(isimler))}")
print("-" * 50)

# --- 2. AŞAMA: GERÇEK ZAMANLI TANIMA ---
toplam_gecenler = set()  # Aynı kişiyi tekrar tekrar saymamak için isimleri burada tutuyoruz.........
# --- SAYICI İÇİN HAFIZA ---
tum_gecen_yuz_kodlari = []  # Görülen her yeni yüzün imzasını buraya kaydedeceğiz
toplam_insan_sayisi = 0     # Ekrandan gelip geçen toplam kişi sayısı

# --- 2. AŞAMA: GERÇEK ZAMANLI TANIMA ---
cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)
islem_yapilsin_mi = True 

# Sonuçları saklamak için boş liste (Kasma önleme için kare atlandığında kullanılır)
display_names = []

while True:
    success, img = cap.read()
    if not success:
        break
    
    # 1. İşlemciyi yormamak için her 2 karede bir analiz yap
    if islem_yapilsin_mi:
        # Görüntüyü 1/4 oranında küçült (Hız için)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        yuz_konumlari = face_recognition.face_locations(imgS)
        yuz_kodlari = face_recognition.face_encodings(imgS, yuz_konumlari)

        display_names = []
        for encodeFace, faceLoc in zip(yuz_kodlari, yuz_konumlari):
            # --- GELİŞMİŞ YENİ KİŞİ KONTROLÜ ---
            yeni_mi = True
            
            if len(tum_gecen_yuz_kodlari) > 0:
                # Tolerance değerini 0.50'den 0.60'a çektik (Daha esnek olması için)
                # Bu, farklı açıları aynı kişi olarak görme şansını artırır.
                eslesmeler = face_recognition.compare_faces(tum_gecen_yuz_kodlari, encodeFace, tolerance=0.60)
                
                if True in eslesmeler:
                    yeni_mi = False
            
            if yeni_mi:
                # Yeni kişiyi kaydet ve sayacı artır
                tum_gecen_yuz_kodlari.append(encodeFace)
                toplam_insan_sayisi += 1
            
            # -----------------------------------------------

            mesafeler = face_recognition.face_distance(bilinen_kodlar, encodeFace)
            # ... (kodun geri kalanı buradan devam ediyor)
            # TOLERANS: 0.4 - 0.5 arası en güvenlisidir. 
            # 0.6 yaparsan yabancıları tanıdıklarına benzetme ihtimali artar.
            mesafeler = face_recognition.face_distance(bilinen_kodlar, encodeFace)
            
            name = "BILINMIYOR"
            if len(mesafeler) > 0:
                en_iyi_eslesme_index = np.argmin(mesafeler)
                # Mesafe 0.45'ten küçükse kişi "tanıdıktır"
                if mesafeler[en_iyi_eslesme_index] < 0.45:
                    name = isimler[en_iyi_eslesme_index]
                    if mesafeler[en_iyi_eslesme_index] < 0.45:
                        name = isimler[en_iyi_eslesme_index]
                        toplam_gecenler.add(name) # ........................
            
            display_names.append((name, faceLoc))

    islem_yapilsin_mi = not islem_yapilsin_mi 

    # 2. Ekrana Çizim Yapma
    for name, faceLoc in display_names:
        # Koordinatları 4 ile çarpıyoruz çünkü resmi 0.25 oranında küçültmüştük
        y1, x2, y2, x1 = [v * 4 for v in faceLoc]
        
        # Tanınıyorsa Yeşil, tanınmıyorsa Kırmızı çerçeve
        renk = (0, 255, 0) if name != "BILINMIYOR" else (0, 0, 255)
        
        # Dikdörtgen ve İsim Etiketi
        cv2.rectangle(img, (x1, y1), (x2, y2), renk, 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), renk, cv2.FILLED) # İsim arka planı
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # Bilgi notu
    cv2.putText(img, "Çıkmak için 'q' tuşuna basın", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 255), 1)
    
    # Anlık karede kaç yüz varsa say
    anlik_kisi_sayisi = len(display_names)

    # Sol üst köşeye bilgi kutusu (Siyah dikdörtgen üzerine beyaz yazı)
    cv2.rectangle(img, (0, 0), (350, 110), (0, 0, 0), cv2.FILLED)
    
    cv2.putText(img, f"TOPLAM GEÇEN: {toplam_insan_sayisi}", (15, 35), 
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 128), 2)
   
    cv2.putText(img, f"Toplam Taninan: {len(toplam_gecenler)}", (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 191, 0), 2)
   
    cv2.putText(img, "Cikis:'q'", (15, 95),
                cv2.FONT_HERSHEY_PLAIN, 1.0, (180, 105, 255), 1)
    

    
    cv2.imshow('Guvenli Yuz Tanima Sistemi', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
