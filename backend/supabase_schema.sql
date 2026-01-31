-- Create Enum for Subscription Tier
CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');

-- A. Profiles (Linked to Supabase Auth)
-- This table mimics the Supabase 'profiles' pattern often used with auth.users
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  school_name TEXT,
  subscription_tier subscription_tier DEFAULT 'free',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- B. Classes
CREATE TABLE classes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  teacher_id UUID REFERENCES profiles(id) ON DELETE CASCADE NOT NULL,
  name TEXT NOT NULL, -- e.g. "11-A Bilişim"
  grade_level INTEGER NOT NULL, -- e.g. 11
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Students (Enrolled in classes)
CREATE TABLE students (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  class_id UUID REFERENCES classes(id) ON DELETE CASCADE NOT NULL,
  student_number TEXT,
  full_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- C. Exams
CREATE TABLE exams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  class_id UUID REFERENCES classes(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL, -- e.g. "Python 1. Dönem 1. Yazılı"
  answer_key JSONB, -- Structure: [{question_no: 1, correct_answer: "A", points: 10}, ...]
  max_score INTEGER DEFAULT 100,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Exam Results (AI Analysis)
CREATE TABLE exam_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  exam_id UUID REFERENCES exams(id) ON DELETE CASCADE NOT NULL,
  student_id UUID REFERENCES students(id) ON DELETE CASCADE NOT NULL,
  paper_image_url TEXT, -- URL from Supabase Storage
  raw_ai_response JSONB, -- The raw JSON response from Gemini
  total_score NUMERIC,
  teacher_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS) - Recommended
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE exams ENABLE ROW LEVEL SECURITY;
ALTER TABLE exam_results ENABLE ROW LEVEL SECURITY;

-- Basic Policies (Examples - adjust as needed)
-- Users can see their own profile
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id);
-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);

-- Teachers can see their own classes
CREATE POLICY "Teachers can view own classes" ON classes FOR SELECT USING (auth.uid() = teacher_id);
-- Teachers can insert their own classes
CREATE POLICY "Teachers can insert own classes" ON classes FOR INSERT WITH CHECK (auth.uid() = teacher_id);

-- (Policies would need to be expanded for all tables to ensure data isolation)
