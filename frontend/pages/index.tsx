import AnalysisTool from '../src/components/AnalysisTool';

export default function Home() {
  return (
    <div style={{ padding: 32 }}>
      <h1 style={{ fontSize: 28, marginBottom: 16 }}>Mihenk.ai — Analiz Test</h1>
      <AnalysisTool examId="test-exam-id" studentId="test-student" />
    </div>
  );
}
