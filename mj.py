import React, { useState, useEffect } from 'react';

export default function App() {
  // 1. 로컬 스토리지에서 기존 운동 데이터 불러오기
  const [records, setRecords] = useState(() => {
    const saved = localStorage.getItem('workout_records');
    return saved ? JSON.parse(saved) : [];
  });

  // 2. 입력 폼 상태 관리
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [part, setPart] = useState('전신 🔥');
  const [content, setContent] = useState('');
  const [photo, setPhoto] = useState(null);

  // 3. 데이터가 바뀔 때마다 로컬 스토리지에 자동 저장
  useEffect(() => {
    localStorage.setItem('workout_records', JSON.stringify(records));
  }, [records]);

  // 4. 이미지 파일을 Base64 문자열로 변환 (DB 없이 로컬에 저장하기 위함)
  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhoto(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // 5. 오운완 등록 버튼 클릭 시
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!content.trim()) return alert('오늘 어떤 운동을 했는지 적어주세요!');

    const newRecord = {
      id: Date.now(),
      date,
      part,
      content,
      photo,
    };

    // 최신 날짜가 맨 위로 오도록 정렬하여 저장
    setRecords([newRecord, ...records]);
    
    // 입력창 초기화
    setContent('');
    setPhoto(null);
  };

  // 6. 기록 삭제 기능
  const handleDelete = (id) => {
    if (confirm('이 오운완 기록을 삭제하시겠습니까?')) {
      setRecords(records.filter(rec => rec.id !== id));
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-6 px-4">
      <div className="max-w-md mx-auto bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
        
        {/* 상단 헤더 비주얼 */}
        <div className="bg-gradient-to-r from-violet-600 to-indigo-600 p-8 text-center text-white">
          <h1 className="text-3xl font-extrabold tracking-tight">🏋️‍♂️ 오운완 일지</h1>
          <p className="text-indigo-100 text-sm mt-2 font-medium">오늘도 당신의 노력을 기록하세요!</p>
        </div>

        {/* 운동 등록 폼 컴포넌트 */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5 bg-white">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">날짜</label>
              <input 
                type="date" 
                value={date} 
                onChange={(e) => setDate(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-3 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">운동 부위</label>
              <select 
                value={part} 
                onChange={(e) => setPart(e.target.value)}
                className="w-full rounded-xl border border-slate-200 p-3 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white"
              >
                <option value="전신 🔥">전신 🔥</option>
                <option value="상체(가슴/등) 📐">상체 (가슴/등) 📐</option>
                <option value="하체(스쿼트) 🍗">하체 (스쿼트) 🍗</option>
                <option value="코어/복근 🍫">코어/복근 🍫</option>
                <option value="유산소 🏃">유산소 🏃</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">운동 내용</label>
            <textarea 
              rows="3"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="예: 벤치프레스 5세트, 스쿼트 100개 완료!"
              className="w-full rounded-xl border border-slate-200 p-3 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">인증샷 첨부</label>
            <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-slate-200 border-dashed rounded-xl hover:border-indigo-400 transition cursor-pointer relative">
              <div className="space-y-1 text-center">
                <svg className="mx-auto h-12 w-12 text-slate-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                  <path d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-12-4h.01M24 28a4 4 0 110-8 4 4 0 010 8z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div className="flex text-sm text-slate-600">
                  <span className="font-semibold text-indigo-600 hover:text-indigo-500">사진 업로드하기</span>
                </div>
                <p className="text-xs text-slate-400">PNG, JPG 최대 1MB</p>
              </div>
              <input 
                type="file" 
                accept="image/*"
                onChange={handlePhotoChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>
            {photo && (
              <div className="mt-3 relative rounded-xl overflow-hidden shadow-inner">
                <img src={photo} alt="Preview" className="w-full h-40 object-cover" />
                <button 
                  type="button" 
                  onClick={() => setPhoto(null)}
                  className="absolute top-2 right-2 bg-black/60 text-white rounded-full p-1 text-xs px-2 hover:bg-black"
                >
                  취소
                </button>
              </div>
            )}
          </div>

          <button 
            type="submit"
            className="w-full bg-indigo-600 text-white p-4 rounded-xl font-bold text-base hover:bg-indigo-700 active:scale-[0.99] transition shadow-lg shadow-indigo-100"
          >
            오늘 운동 완료 스탬프 찍기 💥
          </button>
        </form>

        {/* 기록 리스트 (타임라인) */}
        <div className="p-6 bg-slate-50/50 min-h-[300px]">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-800">내 오운완 기록들</h2>
            <span className="text-xs font-bold bg-indigo-100 text-indigo-700 px-2.5 py-1 rounded-full">
              총 {records.length}회 완료
            </span>
          </div>
          
          {records.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-3xl mb-2">😴</p>
              <p className="text-sm font-medium text-slate-400">아직 기록이 없어요. 운동을 시작해볼까요?</p>
            </div>
          ) : (
            <div className="space-y-4">
              {records.map((rec) => (
                <div key={rec.id} className="bg-white border border-slate-100 rounded-2xl p-4 shadow-sm relative group">
                  <button 
                    onClick={() => handleDelete(rec.id)}
                    className="absolute top-4 right-4 text-slate-300 hover:text-red-500 text-xs font-medium transition"
                  >
                    삭제
                  </button>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs font-bold bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg">
                      {rec.part}
                    </span>
                    <span className="text-xs font-medium text-slate-400">{rec.date}</span>
                  </div>
                  <p className="text-sm text-slate-600 font-normal whitespace-pre-line leading-relaxed mb-3">
                    {rec.content}
                  </p>
                  {rec.photo && (
                    <img src={rec.photo} alt="Workout Certification" className="w-full h-44 object-cover rounded-xl mt-2" />
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
