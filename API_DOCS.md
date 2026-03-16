EntropyHub API Documentation v2.1.0

This document outlines the available endpoints, authentication methods, and standard error codes for the EntropyHub Live Quantum-Seeded Hyperchaos API.

1. Authentication

Most endpoints are protected and require an API key. You must include the x-api-key in the header of your HTTP requests.

Header Key: x-api-key

Example Value: teknofest2026-secret

2. Endpoints

System Endpoints

GET /health

Description: Checks if the API and the Chaos engine are running.

Auth Required: No

Rate Limit: 5/min

GET /metrics

Description: Returns active algorithms and system status.

Auth Required: Yes

Rate Limit: None

GET /api/stats

Description: Returns general statistics for the frontend dashboard.

Auth Required: Yes

Rate Limit: None

Entropy Generation Endpoints

POST /random/bytes

Description: Generates a requested number of random bytes (0-255).

Auth Required: Yes

Rate Limit: 10/min

POST /random/integers

Description: Generates random integers within a specified range.

Auth Required: Yes

Rate Limit: 10/min

POST /chaos/reseed

Description: Restarts and reseeds the quantum hyperchaos engine.

Auth Required: Yes

Rate Limit: 2/min

Payload Structures (POST Requests)

/random/bytes

{
  "byte_count": 16 
}


Constraints: byte_count must be between 1 and 1024.

/random/integers

{
  "count": 5,
  "min_val": 10,
  "max_val": 50
}


Constraints: count (1-1000), min_val must be less than max_val.

3. Error Codes (HTTP Status)

200 OK: Request processed successfully.

400 Bad Request: Invalid payload parameters.

Troubleshooting: Check the JSON body limits.

401 Unauthorized: Missing or invalid API Key.

Troubleshooting: Ensure x-api-key header is set.

429 Too Many Requests: Rate limit exceeded.

Troubleshooting: Wait for the Retry-After duration.

500 Internal Error: Engine failure / exception.

Troubleshooting: Check logs/api_audit.log.

EntropyHub API Dokümantasyonu v2.1.0

Bu belge, EntropyHub Canlı Kuantum Tohumlu Hiperkaos API'si için mevcut uç noktaları (endpoints), kimlik doğrulama yöntemlerini ve standart hata kodlarını özetlemektedir.

1. Kimlik Doğrulama

Çoğu uç nokta korumalıdır ve bir API anahtarı gerektirir. HTTP isteklerinizin başlık (header) kısmına x-api-key değerini eklemelisiniz.

Header Anahtarı: x-api-key

Örnek Değer: teknofest2026-secret

2. Uç Noktalar (Endpoints)

Sistem Uç Noktaları

GET /health

Açıklama: API'nin ve Kaos motorunun çalışıp çalışmadığını kontrol eder.

Yetki: Hayır

Hız Sınırı: 5/dk

GET /metrics

Açıklama: Aktif algoritmaları ve sistem durumunu döndürür.

Yetki: Evet

Hız Sınırı: Yok

GET /api/stats

Açıklama: Frontend paneli için genel istatistikleri döndürür.

Yetki: Evet

Hız Sınırı: Yok

Entropi Üretim Uç Noktaları

POST /random/bytes

Açıklama: İstenilen sayıda rastgele byte (0-255) üretir.

Yetki: Evet

Hız Sınırı: 10/dk

POST /random/integers

Açıklama: Belirtilen aralıkta rastgele tam sayılar üretir.

Yetki: Evet

Hız Sınırı: 10/dk

POST /chaos/reseed

Açıklama: Kuantum hiperkaos motorunu yeniden başlatır ve tohumlar.

Yetki: Evet

Hız Sınırı: 2/dk

İstek Gövdesi Yapıları (POST İstekleri İçin)

/random/bytes

{
  "byte_count": 16 
}


Kısıtlamalar: byte_count 1 ile 1024 arasında olmalıdır.

/random/integers

{
  "count": 5,
  "min_val": 10,
  "max_val": 50
}


Kısıtlamalar: count (1-1000), min_val değeri max_val'den küçük olmalıdır.

3. Hata Kodları (HTTP Durumları)

200 OK: İstek başarıyla işlendi.

400 Bad Request: Geçersiz parametreler.

Çözüm Adımı: JSON gövdesindeki sınırları kontrol edin.

401 Unauthorized: Geçersiz API Anahtarı.

Çözüm Adımı: x-api-key başlığını kontrol edin.

429 Too Many Requests: Hız sınırı aşıldı.

Çözüm Adımı: Belirtilen süre kadar bekleyin.

500 Internal Error: Backend çökmesi.

Çözüm Adımı: logs/api_audit.log dosyasını inceleyin.