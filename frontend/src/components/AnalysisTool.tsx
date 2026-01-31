'use client';
import { useState } from 'react';
import axios from 'axios';

export default function AnalysisTool({ examId, studentId }: { examId: string, studentId: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('exam_id', examId);
    formData.append('student_id', studentId);

    try {
      const baseUrl = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8001'
      const response = await axios.post(`${baseUrl}/api/v1/analyze/full-analysis`, formData);
      setResult(response.data);
    } catch (error: any) {
      console.error('Analiz hatası:', error);
      setError(error?.response?.data?.detail || error.message || 'Bilinmeyen hata');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg">
      <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} className="mb-4 block w-full text-sm text-gray-500" />
      <button
        onClick={handleUpload}
        disabled={loading}
        className={`w-full py-3 rounded-xl font-bold text-white ${loading ? 'bg-gray-400' : 'bg-indigo-600 hover:bg-indigo-700'}`}>
        {loading ? 'Yapay Zeka Analiz Ediyor...' : 'Sınavı Analiz Et'}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">{error}</div>
      )}

      {result && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <h3 className="text-green-800 font-bold">Analiz Başarılı!</h3>
          <p className="text-2xl font-black text-green-900">Puan: {result.score}</p>
          {result.report_url && (
            <div className="mt-2 text-sm">
              Rapor: <a href={`${(process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8001')}${result.report_url}`} target="_blank" rel="noreferrer" className="underline">Görüntüle</a>
              <button onClick={() => window.open(`${(process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8001')}${result.report_url}`)} className="ml-4 px-2 py-1 bg-indigo-600 text-white rounded">İndir</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
