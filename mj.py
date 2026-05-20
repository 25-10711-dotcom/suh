<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💪 나만의 오운완 일지</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 모바일 앱 같은 부드러운 글꼴 적용 */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 min-h-screen py-6 px-4">

    <div class="max-w-md mx-auto bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
        
        <div class="bg-gradient-to-r from-violet-600 to-indigo-600 p-8 text-center text-white">
            <h1 class="text-3xl font-extrabold tracking-tight">🏋️‍♂️ 오운완 일지</h1>
            <p class="text-indigo-100 text-sm mt-2 font-medium">오늘도 당신의 노력을 기록하세요!</p>
        </div>

        <form id="workoutForm" class="p-6 space-y-5 bg-white">
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">날짜</label>
                    <input type="date" id="workoutDate" class="w-full rounded-xl border border-slate-200 p-3 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">운동 부위</label>
                    <select id="workoutPart" class="w-full rounded-xl border border-slate-200 p-3 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
                        <option value="전신 🔥">전신 🔥</option>
                        <option value="상체(가슴/등) 📐">상체 (가슴/등) 📐</option>
                        <option value="하체(스쿼트) 🍗">하체 (스쿼트) 🍗</option>
                        <option value="코어/복근 🍫">코어/복근 🍫</option>
                        <option value="유산소 🏃">유산소 🏃</option>
                    </select>
                </div>
            </div>

            <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">운동 내용</label>
                <textarea id="workoutContent" rows="3" placeholder="예: 벤치프레스 5세트, 스쿼트 100개 완료!" class="w-full rounded-xl border border-slate-200 p-3 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"></textarea>
            </div>

            <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">인증샷 첨부</label>
                <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-slate-200 border-dashed rounded-xl hover:border-indigo-400 transition cursor-pointer relative">
                    <div class="space-y-1 text-center">
                        <svg class="mx-auto h-12 w-12 text-slate-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                            <path d="M28 8H12a4 4 0 00-4 4v20a4 4 0 004 4h24a4 4 0 004-4V20m-12-4h.01M24 28a4 4 0 110-8 4 4 0 010 8z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                        <div class="flex text-sm text-slate-600 justify-center">
                            <span class="font-semibold text-indigo-600">사진 업로드하기</span>
                        </div>
                        <p class="text-xs text-slate-400">PNG, JPG 파일 가능</p>
                    </div>
                    <input type="file" id="workoutPhoto" accept="image/*" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
                </div>
                <div id="photoPreviewContainer" class="mt-3 relative rounded-xl overflow-hidden shadow-inner hidden">
                    <img id="photoPreview" src="" alt="Preview" class="w-full h-40 object-cover">
                </div>
            </div>

            <button type="submit" class="w-full bg-indigo-600 text-white p-4 rounded-xl font-bold text-base hover:bg-indigo-700 active:scale-[0.99] transition shadow-lg shadow-indigo-100">
                오늘 운동 완료 스탬프 찍기 💥
            </button>
        </form>

        <div class="p-6 bg-slate-50/50 min-h-[300px]">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-bold text-slate-800">내 오운완 기록들</h2>
                <span id="totalCount" class="text-xs font-bold bg-indigo-100 text-indigo-700 px-2.5 py-1 rounded-full">총 0회 완료</span>
            </div>
            
            <div id="recordList" class="space-y-4"></div>
        </div>

    </div>

    <script>
        // 오늘 날짜 기본 지정
        document.getElementById('workoutDate').value = new Date().toISOString().split('T')[0];

        let records = JSON.parse(localStorage.getItem('html_workout_records')) || [];
        let base64Photo = null;

        // 사진 파일 읽기
        document.getElementById('workoutPhoto').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onloadend = function() {
                    base64Photo = reader.result;
                    document.getElementById('photoPreview').src = base64Photo;
                    document.getElementById('photoPreviewContainer').classList.remove('hidden');
                }
                reader.readAsDataURL(file);
            }
        });

        // 화면에 오운완 리스트 그리기 함수
        function renderRecords() {
            const recordList = document.getElementById('recordList');
            const totalCount = document.getElementById('totalCount');
            recordList.innerHTML = '';
            totalCount.innerText = `총 ${records.length}회 완료`;

            if (records.length === 0) {
                recordList.innerHTML = `
                    <div class="text-center py-12">
                        <p class="text-3xl mb-2">😴</p>
                        <p class="text-sm font-medium text-slate-400">아직 기록이 없어요. 운동을 시작해볼까요?</p>
                    </div>`;
                return;
            }

            records.forEach((rec, index) => {
                const card = document.createElement('div');
                card.className = "bg-white border border-slate-100 rounded-2xl p-4 shadow-sm relative";
                
                let photoHtml = rec.photo ? `<img src="${rec.photo}" class="w-full h-44 object-cover rounded-xl mt-3">` : '';
                
                card.innerHTML = `
                    <button onclick="deleteRecord(${rec.id})" class="absolute top-4 right-4 text-slate-300 hover:text-red-500 text-xs font-medium transition">삭제</button>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-xs font-bold bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg">${rec.part}</span>
                        <span class="text-xs font-medium text-slate-400">${rec.date}</span>
                    </div>
                    <p class="text-sm text-slate-600 font-normal whitespace-pre-line leading-relaxed">${rec.content}</p>
                    ${photoHtml}
                `;
                recordList.appendChild(card);
            });
        }

        // 등록 이벤트
        document.getElementById('workoutForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const date = document.getElementById('workoutDate').value;
            const part = document.getElementById('workoutPart').value;
            const content = document.getElementById('workoutContent').value;

            if (!content.trim()) return alert('오늘 어떤 운동을 했는지 적어주세요!');

            const newRecord = { id: Date.now(), date, part, content, photo: base64Photo };
            records.unshift(newRecord);
            localStorage.setItem('html_workout_records', JSON.stringify(records));

            // 폼 초기화
            document.getElementById('workoutContent').value = '';
            document.getElementById('workoutPhoto').value = '';
            document.getElementById('photoPreviewContainer').classList.add('hidden');
            base64Photo = null;

            renderRecords();
        });

        // 삭제 이벤트
        window.deleteRecord = function(id) {
            if (confirm('이 기록을 삭제하시겠습니까
