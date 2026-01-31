# 🚀 Deployment Guide - Vercel + Render

Bu rehber, **mihenk-ai** projesini **Vercel** (Frontend) ve **Render** (Backend) üzerinde deploy etmek için adım adım talimatlar içerir.

---

## 📋 Ön Hazırlık

### 1. Gerekli Hesaplar

Aşağıdaki platformlarda hesap oluşturun:

- ✅ **GitHub** - https://github.com (Kod repository)
- ✅ **Vercel** - https://vercel.com (Frontend hosting)
- ✅ **Render** - https://render.com (Backend hosting)
- ✅ **Supabase** - https://supabase.com (Database)
- ✅ **Google AI Studio** - https://aistudio.google.com (Gemini API)

### 2. Kod GitHub'a Yükleme

```bash
# Eğer henüz yüklemediyseniz:
git add .
git commit -m "Ready for deployment"
git push origin main
```

---

## 🗄️ ADIM 1: Supabase Kurulumu

### 1.1. Proje Oluşturma

1. https://supabase.com adresine gidin
2. **New Project** butonuna tıklayın
3. Proje bilgilerini doldurun:
   - **Name:** mihenk-ai
   - **Database Password:** Güçlü bir şifre seçin (kaydedin!)
   - **Region:** Europe (Frankfurt) veya en yakın bölge
4. **Create new project** butonuna tıklayın
5. Proje hazırlanana kadar bekleyin (~2 dakika)

### 1.2. Database Schema Yükleme

1. Sol menüden **SQL Editor**'e gidin
2. **New Query** butonuna tıklayın
3. `backend/supabase_schema.sql` dosyasının içeriğini kopyalayıp yapıştırın
4. **Run** butonuna tıklayın
5. Başarılı mesajını görmelisiniz

### 1.3. API Bilgilerini Alma

1. **Settings** → **API** bölümüne gidin
2. Aşağıdaki bilgileri kopyalayın (sonra kullanacağız):
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY` (güvenli)
   - veya **service_role** key → `SUPABASE_KEY` (tam yetki)

---

## 🔑 ADIM 2: API Keys Alma

### 2.1. Gemini API Key

1. https://aistudio.google.com/app/apikey adresine gidin
2. **Create API Key** butonuna tıklayın
3. Key'i kopyalayın → `GEMINI_API_KEY`

### 2.2. Groq API Key (Opsiyonel)

1. https://console.groq.com/keys adresine gidin
2. **Create API Key** butonuna tıklayın
3. Key'i kopyalayın → `GROQ_API_KEY`

---

## 🖥️ ADIM 3: Backend Deployment (Render)

### 3.1. Render'da Yeni Servis Oluşturma

1. https://render.com adresine gidin ve giriş yapın
2. **Dashboard** → **New +** → **Web Service** seçin
3. **Build and deploy from a Git repository** → **Next**
4. GitHub hesabınızı bağlayın (ilk kez ise)
5. **mihenk-ai-yeni** repository'sini seçin → **Connect**

### 3.2. Servis Ayarları

Aşağıdaki ayarları yapın:

```
Name: mihenk-ai-backend
Region: Frankfurt (EU Central) veya en yakın
Branch: main
Root Directory: backend
Runtime: Docker
```

**Docker Settings:**
```
Dockerfile Path: ./Dockerfile
Docker Context: ./
```

**Instance Type:**
```
Free (veya Starter - $7/month daha hızlı)
```

### 3.3. Environment Variables Ekleme

**Environment** sekmesine gidin ve aşağıdaki değişkenleri ekleyin:

```bash
# Zorunlu
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
TEST_MODE=0

# Opsiyonel
OPENAI_API_KEY=sk-proj-...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
```

**Önemli:** Her bir değişken için **Add Environment Variable** butonuna tıklayın.

### 3.4. Deploy Başlatma

1. **Create Web Service** butonuna tıklayın
2. Render otomatik olarak build ve deploy işlemini başlatacak
3. Logs'ları izleyin (~5-10 dakika sürer)
4. Deploy tamamlandığında URL'iniz hazır olacak:
   ```
   https://mihenk-ai-backend.onrender.com
   ```

### 3.5. Backend Test

Tarayıcıda veya terminal'de test edin:

```bash
curl https://mihenk-ai-backend.onrender.com/health
```

Başarılı yanıt:
```json
{"status": "healthy"}
```

---

## 🌐 ADIM 4: Frontend Deployment (Vercel)

### 4.1. Vercel'de Yeni Proje Oluşturma

1. https://vercel.com adresine gidin ve giriş yapın
2. **Add New...** → **Project** seçin
3. GitHub hesabınızı bağlayın (ilk kez ise)
4. **mihenk-ai-yeni** repository'sini bulun
5. **Import** butonuna tıklayın

### 4.2. Proje Ayarları

```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build (otomatik)
Output Directory: .next (otomatik)
Install Command: npm install (otomatik)
```

### 4.3. Environment Variables

**Environment Variables** bölümüne aşağıdaki değişkeni ekleyin:

```bash
NEXT_PUBLIC_API_BASE=https://mihenk-ai-backend.onrender.com
```

**Önemli:** 
- Backend URL'inizi Render'dan kopyalayın
- Sonunda `/` olmamalı
- `NEXT_PUBLIC_` prefix'i zorunlu!

### 4.4. Deploy Başlatma

1. **Deploy** butonuna tıklayın
2. Vercel otomatik olarak build ve deploy işlemini başlatacak
3. Logs'ları izleyin (~2-3 dakika)
4. Deploy tamamlandığında URL'iniz hazır olacak:
   ```
   https://mihenk-ai-yeni.vercel.app
   ```

### 4.5. Frontend Test

Tarayıcıda açın:
```
https://mihenk-ai-yeni.vercel.app
```

Browser console'da (F12) hata olmamalı.

---

## ✅ ADIM 5: Son Kontroller

### 5.1. Backend Health Check

```bash
curl https://mihenk-ai-backend.onrender.com/health
```

### 5.2. Frontend API Bağlantısı

1. Frontend'i açın
2. F12 → Console
3. API isteklerinde hata olmamalı
4. Network sekmesinde backend'e yapılan istekleri kontrol edin

### 5.3. Database Bağlantısı

1. Supabase Dashboard → **Table Editor**
2. Tabloların oluştuğunu kontrol edin:
   - `users`
   - `schools`
   - `classes`
   - `students`
   - `exams`
   - `questions`
   - `student_answers`
   - `analysis_results`

---

## 🔄 ADIM 6: Otomatik Deployment Ayarları

### 6.1. Vercel Auto-Deploy

✅ Vercel otomatik olarak her `git push` sonrası deploy eder.

**Ayarlar:**
- **Settings** → **Git** → **Production Branch:** main
- Her commit otomatik deploy edilir
- Preview deployments her PR için oluşturulur

### 6.2. Render Auto-Deploy

✅ Render otomatik olarak her `git push` sonrası deploy eder.

**Ayarlar:**
- **Settings** → **Build & Deploy**
- **Auto-Deploy:** Yes
- **Branch:** main

---

## 🔧 Sorun Giderme

### Backend Deploy Hatası

**Hata:** `Build failed`
- **Çözüm:** Render logs'larını kontrol edin
- `requirements.txt` eksik paket var mı?
- Dockerfile doğru mu?

**Hata:** `Application failed to respond`
- **Çözüm:** Environment variables doğru mu?
- Supabase bağlantısı çalışıyor mu?
- PORT değişkeni doğru mu?

### Frontend Deploy Hatası

**Hata:** `Build failed`
- **Çözüm:** Vercel logs'larını kontrol edin
- `package.json` dependencies eksik mi?
- TypeScript hataları var mı?

**Hata:** `API calls failing`
- **Çözüm:** `NEXT_PUBLIC_API_BASE` doğru mu?
- Backend çalışıyor mu?
- CORS ayarları doğru mu?

### Supabase Bağlantı Hatası

**Hata:** `Invalid API key`
- **Çözüm:** SUPABASE_KEY doğru kopyalandı mı?
- Supabase projesi aktif mi?

**Hata:** `Table does not exist`
- **Çözüm:** SQL schema çalıştırıldı mı?
- Supabase SQL Editor'de hata var mı?

---

## 📊 Monitoring & Logs

### Render Logs

```
Dashboard → Your Service → Logs
```
- Real-time logs
- Error tracking
- Performance metrics

### Vercel Logs

```
Dashboard → Your Project → Deployments → View Function Logs
```
- Build logs
- Runtime logs
- Analytics

### Supabase Logs

```
Dashboard → Logs → API Logs
```
- Database queries
- API requests
- Errors

---

## 🎯 Production Checklist

Deployment öncesi kontrol listesi:

- [ ] Tüm environment variables doğru girildi
- [ ] `TEST_MODE=0` (production'da)
- [ ] Supabase schema yüklendi
- [ ] Backend health endpoint çalışıyor
- [ ] Frontend API'ye bağlanıyor
- [ ] CORS ayarları doğru
- [ ] SSL sertifikaları aktif (otomatik)
- [ ] Custom domain ayarlandı (opsiyonel)
- [ ] Analytics eklendi (opsiyonel)
- [ ] Error tracking eklendi (opsiyonel)

---

## 🚀 Gelişmiş Ayarlar

### Custom Domain (Vercel)

1. **Settings** → **Domains**
2. Domain adınızı girin
3. DNS ayarlarını yapın
4. SSL otomatik aktif olacak

### Custom Domain (Render)

1. **Settings** → **Custom Domains**
2. Domain adınızı girin
3. DNS ayarlarını yapın
4. SSL otomatik aktif olacak

### Environment Secrets (Güvenlik)

Render ve Vercel'de environment variables otomatik olarak şifrelenir.
Asla kod içine hard-code etmeyin!

---

## 📞 Destek

Sorun yaşarsanız:

1. **Render Docs:** https://render.com/docs
2. **Vercel Docs:** https://vercel.com/docs
3. **Supabase Docs:** https://supabase.com/docs
4. **GitHub Issues:** Repository'nizde issue açın

---

**Son Güncelleme:** 2026-01-31  
**Versiyon:** 1.0  
**Platform:** Vercel + Render + Supabase
