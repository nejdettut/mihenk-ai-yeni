-- EKSİK OLAN AYARLAR
-- Mevcut tablolarınıza eklenecek güvenlik ve politikalar

-- 1. ENUM TYPE (Eğer yoksa)
-- subscription_tier için enum oluştur
DO $$ BEGIN
  CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- 2. ROW LEVEL SECURITY (RLS) AKTIF ET
-- Güvenlik için mutlaka gerekli
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE exam_results ENABLE ROW LEVEL SECURITY;

-- 3. GÜVENLİK POLİTİKALARI

-- Profiles Policies
DROP POLICY IF EXISTS "Users can view own profile" ON profiles;
CREATE POLICY "Users can view own profile" 
  ON profiles FOR SELECT 
  USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
CREATE POLICY "Users can update own profile" 
  ON profiles FOR UPDATE 
  USING (auth.uid() = id);

DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;
CREATE POLICY "Users can insert own profile" 
  ON profiles FOR INSERT 
  WITH CHECK (auth.uid() = id);

-- Classes Policies
DROP POLICY IF EXISTS "Teachers can view own classes" ON classes;
CREATE POLICY "Teachers can view own classes" 
  ON classes FOR SELECT 
  USING (auth.uid() = teacher_id);

DROP POLICY IF EXISTS "Teachers can insert own classes" ON classes;
CREATE POLICY "Teachers can insert own classes" 
  ON classes FOR INSERT 
  WITH CHECK (auth.uid() = teacher_id);

DROP POLICY IF EXISTS "Teachers can update own classes" ON classes;
CREATE POLICY "Teachers can update own classes" 
  ON classes FOR UPDATE 
  USING (auth.uid() = teacher_id);

DROP POLICY IF EXISTS "Teachers can delete own classes" ON classes;
CREATE POLICY "Teachers can delete own classes" 
  ON classes FOR DELETE 
  USING (auth.uid() = teacher_id);

-- Students Policies
DROP POLICY IF EXISTS "Teachers can view class students" ON students;
CREATE POLICY "Teachers can view class students" 
  ON students FOR SELECT 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = students.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can insert class students" ON students;
CREATE POLICY "Teachers can insert class students" 
  ON students FOR INSERT 
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = students.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can update class students" ON students;
CREATE POLICY "Teachers can update class students" 
  ON students FOR UPDATE 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = students.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can delete class students" ON students;
CREATE POLICY "Teachers can delete class students" 
  ON students FOR DELETE 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = students.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

-- Exams Policies
DROP POLICY IF EXISTS "Teachers can view class exams" ON exams;
CREATE POLICY "Teachers can view class exams" 
  ON exams FOR SELECT 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = exams.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can insert class exams" ON exams;
CREATE POLICY "Teachers can insert class exams" 
  ON exams FOR INSERT 
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = exams.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can update class exams" ON exams;
CREATE POLICY "Teachers can update class exams" 
  ON exams FOR UPDATE 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = exams.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can delete class exams" ON exams;
CREATE POLICY "Teachers can delete class exams" 
  ON exams FOR DELETE 
  USING (
    EXISTS (
      SELECT 1 FROM classes 
      WHERE classes.id = exams.class_id 
      AND classes.teacher_id = auth.uid()
    )
  );

-- Exam Results Policies
DROP POLICY IF EXISTS "Teachers can view exam results" ON exam_results;
CREATE POLICY "Teachers can view exam results" 
  ON exam_results FOR SELECT 
  USING (
    EXISTS (
      SELECT 1 FROM exams 
      JOIN classes ON classes.id = exams.class_id 
      WHERE exams.id = exam_results.exam_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can insert exam results" ON exam_results;
CREATE POLICY "Teachers can insert exam results" 
  ON exam_results FOR INSERT 
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM exams 
      JOIN classes ON classes.id = exams.class_id 
      WHERE exams.id = exam_results.exam_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can update exam results" ON exam_results;
CREATE POLICY "Teachers can update exam results" 
  ON exam_results FOR UPDATE 
  USING (
    EXISTS (
      SELECT 1 FROM exams 
      JOIN classes ON classes.id = exams.class_id 
      WHERE exams.id = exam_results.exam_id 
      AND classes.teacher_id = auth.uid()
    )
  );

DROP POLICY IF EXISTS "Teachers can delete exam results" ON exam_results;
CREATE POLICY "Teachers can delete exam results" 
  ON exam_results FOR DELETE 
  USING (
    EXISTS (
      SELECT 1 FROM exams 
      JOIN classes ON classes.id = exams.class_id 
      WHERE exams.id = exam_results.exam_id 
      AND classes.teacher_id = auth.uid()
    )
  );

-- 4. STORAGE BUCKET (Sınav kağıtları için)
-- Supabase Storage'da bucket oluştur
INSERT INTO storage.buckets (id, name, public)
VALUES ('exam-papers', 'exam-papers', false)
ON CONFLICT (id) DO NOTHING;

-- Storage Policies
DROP POLICY IF EXISTS "Teachers can upload exam papers" ON storage.objects;
CREATE POLICY "Teachers can upload exam papers"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'exam-papers' 
    AND auth.role() = 'authenticated'
  );

DROP POLICY IF EXISTS "Teachers can view exam papers" ON storage.objects;
CREATE POLICY "Teachers can view exam papers"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'exam-papers' 
    AND auth.role() = 'authenticated'
  );

DROP POLICY IF EXISTS "Teachers can delete exam papers" ON storage.objects;
CREATE POLICY "Teachers can delete exam papers"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'exam-papers' 
    AND auth.role() = 'authenticated'
  );

-- 5. TRIGGER: Yeni kullanıcı kaydolduğunda otomatik profile oluştur
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, created_at)
  VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name', NOW());
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger'ı oluştur (eğer yoksa)
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 6. İNDEXLER (Performans için)
CREATE INDEX IF NOT EXISTS idx_classes_teacher_id ON classes(teacher_id);
CREATE INDEX IF NOT EXISTS idx_students_class_id ON students(class_id);
CREATE INDEX IF NOT EXISTS idx_exams_class_id ON exams(class_id);
CREATE INDEX IF NOT EXISTS idx_exam_results_exam_id ON exam_results(exam_id);
CREATE INDEX IF NOT EXISTS idx_exam_results_student_id ON exam_results(student_id);

-- TAMAMLANDI!
-- Bu SQL'i Supabase SQL Editor'de çalıştırın.
