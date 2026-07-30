// 1. TỰ ĐỘNG BỘ ĐỊNH TUYẾN ROUTER (SPA HASH ROUTING)
function handleRouter() {
  const hash = window.location.hash || '#welcome';

  const welcomeView = document.getElementById('welcomeView');
  const dashboardView = document.getElementById('dashboardView');

  // Chuyển đổi giữa Màn hình Chào mừng (#welcome) và Khung Dashboard chính
  if (hash === '#welcome') {
    welcomeView.style.display = 'flex';
    dashboardView.style.display = 'none';
  } else {
    welcomeView.style.display = 'none';
    dashboardView.style.display = 'grid';

    // Ẩn tất cả các trang nội dung
    document.querySelectorAll('.page-content').forEach(p => p.style.display = 'none');

    // Hiển thị Trang nội dung tương ứng theo Hash
    const route = hash.replace('#', '');
    const targetPage = document.getElementById('page-' + route);

    if (targetPage) {
      targetPage.style.display = 'block';
    } else if (route === 'dashboard') {
      document.getElementById('page-dashboard').style.display = 'block';
    } else {
      // Cho các trang đang phát triển khác (health, risks, trends...)
      const genericPage = document.getElementById('page-generic');
      const activeLink = document.querySelector(`.menu a[href="${hash}"]`);
      const titleText = activeLink ? activeLink.innerText.trim() : 'Chức năng';
      document.getElementById('genericTitle').innerText = titleText;
      genericPage.style.display = 'block';
    }

    // Highlight menu được chọn trên Sidebar
    document.querySelectorAll('.menu a').forEach(a => {
      a.classList.remove('active');
      if (a.getAttribute('href') === hash) {
        a.classList.add('active');
      }
    });
  }

  if (window.lucide) lucide.createIcons();
}

// Lắng nghe sự thay đổi của Hash trên đường dẫn
window.addEventListener('hashchange', handleRouter);

// 2. BẬT / TẮT GIAO DIỆN DARK MODE
function initTheme() {
  const savedTheme = localStorage.getItem('finhealth_theme');
  const darkModeToggle = document.getElementById('darkModeToggle');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    if (darkModeToggle) darkModeToggle.checked = true;
  }
}

function toggleDarkMode(isDark) {
  if (isDark) {
    document.body.classList.add('dark-mode');
    localStorage.setItem('finhealth_theme', 'dark');
  } else {
    document.body.classList.remove('dark-mode');
    localStorage.setItem('finhealth_theme', 'light');
  }
  // Re-render chart để tương thích với theme mới
  updateCompanyData(document.getElementById('companySelect').value || 'ABC');
}

// 3. KHỞI TẠO DANH SÁCH 15 DOANH NGHIỆP TRÊN GIAO DIỆN
function initCompanyList() {
  const listContainer = document.getElementById('companyList');
  const selectContainer = document.getElementById('companySelect');
  
  listContainer.innerHTML = '';
  selectContainer.innerHTML = '';

  Object.keys(companyData).forEach(code => {
    const comp = companyData[code];

    // Thêm vào Tùy chọn 2 ở màn hình Landing
    const itemDiv = document.createElement('div');
    itemDiv.className = 'company-item';
    itemDiv.onclick = () => selectAndStartOption2(code);
    itemDiv.innerHTML = `
      <div class="company-info">
        <strong>${comp.name}</strong>
        <span>${comp.industry} · Kỳ: 2025</span>
      </div>
      <span class="tag ${comp.tagScore[0]}">${comp.score} · ${comp.tagScore[1]}</span>
    `;
    listContainer.appendChild(itemDiv);

    // Thêm vào Dropdown chọn nhanh ở Dashboard
    const option = document.createElement('option');
    option.value = code;
    option.textContent = comp.name;
    selectContainer.appendChild(option);
  });
}

// 4. TÌM KIẾM DOANH NGHIỆP TỰ ĐỘNG REAL-TIME
document.getElementById('companySearchInput').addEventListener('input', function() {
  const filter = this.value.toLowerCase().trim();
  const items = document.querySelectorAll('#companyList .company-item');
  let visibleCount = 0;

  items.forEach(item => {
    const text = item.innerText.toLowerCase();
    if (text.includes(filter)) {
      item.style.display = 'flex';
      visibleCount++;
    } else {
      item.style.display = 'none';
    }
  });

  const noResultMsg = document.getElementById('noCompanyResult');
  noResultMsg.style.display = (visibleCount === 0) ? 'block' : 'none';
});

// 5. CHART APEXCHARTS
let apexChart = null;
function initOrUpdateChart(healthSeries, riskSeries) {
  const isDark = document.body.classList.contains('dark-mode');
  const options = {
    series: [
      { name: 'Health Score', type: 'column', data: healthSeries },
      { name: 'Risk Probability (%)', type: 'line', data: riskSeries }
    ],
    chart: {
      height: 230,
      type: 'line',
      toolbar: { show: false },
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      background: 'transparent'
    },
    colors: ['#005c45', '#d98200'],
    stroke: { width: [0, 3], curve: 'smooth' },
    plotOptions: { bar: { borderRadius: 6, columnWidth: '42%' } },
    dataLabels: { enabled: false },
    labels: ['2021', '2022', '2023', '2024', '2025'],
    xaxis: { labels: { style: { colors: isDark ? '#8ca398' : '#53695e', fontSize: '12px' } } },
    yaxis: { max: 100, labels: { style: { colors: isDark ? '#8ca398' : '#53695e', fontSize: '12px' } } },
    legend: { position: 'bottom', horizontalAlign: 'center', fontSize: '12px', labels: { colors: isDark ? '#e3ece8' : '#0f2017' } },
    grid: { borderColor: isDark ? '#22382d' : '#e2eae6' }
  };

  if (apexChart) {
    apexChart.updateOptions(options);
  } else {
    apexChart = new ApexCharts(document.querySelector("#apexTrendChart"), options);
    apexChart.render();
  }
}

// 6. ĐIỀU HƯỚNG TỪ NÚT BẤM MÀN HÌNH WELCOME
function selectAndStartOption2(companyCode) {
  window.location.hash = '#dashboard';
  const companySelect = document.getElementById('companySelect');
  if (companySelect) {
    companySelect.style.display = 'inline-block';
    companySelect.value = companyCode;
  }
  updateCompanyData(companyCode);
}

document.getElementById('companySelect').onchange = function() {
  updateCompanyData(this.value);
};

function updateCompanyData(code) {
  const data = companyData[code] || companyData["ABC"];
  
  document.getElementById('topbarSub').innerText = data.sub;
  
  document.getElementById('kpiScore').innerText = data.score;
  updateTag('tagScore', data.tagScore);
  
  document.getElementById('kpiRisk').innerText = data.risk;
  updateTag('tagRisk', data.tagRisk);
  
  document.getElementById('kpiTrend').innerText = data.trend;
  updateTag('tagTrend', data.tagTrend);
  
  document.getElementById('kpiRank').innerText = data.rank;
  updateTag('tagRank', data.tagRank);

  initOrUpdateChart(data.healthSeries, data.riskSeries);

  document.getElementById('gaugeVal').innerText = data.gaugeVal;
  document.getElementById('peerScore').innerText = data.gaugeVal;
  document.getElementById('gaugeCircle').style.background = `conic-gradient(var(--aof-gold) 0 ${data.angle}, var(--line) ${data.angle} 100%)`;

  [1,2,3,4,5].forEach(i => {
    document.getElementById('s' + i).innerText = data.scores[i-1];
    document.getElementById('f' + i).style.width = data.scores[i-1] + '%';
  });

  document.getElementById('peerIndustryName').innerText = data.industry;
  document.getElementById('peerNet').innerText = data.peerNet;
  document.getElementById('peerDebt').innerText = data.peerDebt;
  document.getElementById('peerAvg').innerText = data.peerAvg || "60";
  document.getElementById('peerRankVal').innerText = data.peerRank;
  document.getElementById('peerRankFill').style.width = data.peerRank;
  document.getElementById('aiBubble').innerText = data.aiText;
}

function updateTag(id, [cls, text]) {
  const el = document.getElementById(id);
  el.className = 'tag ' + cls;
  el.innerText = text;
}

// 7. XỬ LÝ UPLOAD FILE Ở TÙY CHỌN 1
const wFileInput = document.getElementById('wFileInput');
wFileInput.onchange = function() {
  if(this.files.length > 0) {
    document.getElementById('wUploadTitle').innerText = "📁 " + this.files[0].name;
    document.getElementById('wUploadDesc').innerText = "Tệp đã sẵn sàng. Bấm nút bên dưới để tiến hành phân tích.";
    document.getElementById('wUploadDesc').style.color = "var(--blue)";
    document.getElementById('wUploadDesc').style.fontWeight = "bold";
  }
};

document.getElementById('wAnalyzeBtn').onclick = function() {
  if(wFileInput.files.length === 0) {
    alert('Vui lòng chọn tệp Báo cáo tài chính để phân tích!');
    return;
  }
  const uploadedFileName = wFileInput.files[0].name;
  this.innerText = "Đang xử lý dữ liệu...";
  setTimeout(() => {
    this.innerText = "Phân tích dữ liệu ngay";
    window.location.hash = '#dashboard';
    document.getElementById('topbarSub').innerText = `Báo cáo tài chính tự tải lên: ${uploadedFileName} · Kỳ phân tích: Tự động trích xuất`;
  }, 600);
};

// 8. MODAL UPLOAD BỔ SUNG
const modal = document.getElementById('uploadModal');
document.getElementById('uploadBtn').onclick = () => modal.classList.add('open');
document.getElementById('closeModal').onclick = () => modal.classList.remove('open');
modal.onclick = e => { if(e.target === modal) modal.classList.remove('open'); };

const fileInput = document.getElementById('fileInput');
fileInput.onchange = function() {
  if(this.files.length > 0) {
    document.getElementById('uploadLabel').innerText = "📁 " + this.files[0].name;
    document.getElementById('uploadDesc').innerText = "Tệp đã chọn thành công. Bấm Phân tích để tiếp tục.";
    document.getElementById('uploadDesc').style.color = "var(--blue)";
    document.getElementById('uploadDesc').style.fontWeight = "bold";
  }
};

document.getElementById('processBtn').onclick = function() {
  if(fileInput.files.length === 0) {
    alert('Vui lòng chọn tệp Excel/CSV báo cáo tài chính!');
    return;
  }
  const name = fileInput.files[0].name;
  this.innerText = "Đang xử lý...";
  setTimeout(() => {
    this.innerText = "Phân tích";
    modal.classList.remove('open');
    window.location.hash = '#dashboard';
    document.getElementById('topbarSub').innerText = `Báo cáo tài chính tự tải lên: ${name} · Kỳ phân tích: Tự động trích xuất`;
  }, 800);
};

// 9. TRỢ LÝ AI
document.getElementById('sendBtn').onclick = sendChatMessage;
document.getElementById('chatInput').onkeypress = e => { if(e.key === 'Enter') sendChatMessage(); };

function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if(!text) return;

  const chatBox = document.getElementById('chatBox');
  
  const userDiv = document.createElement('div');
  userDiv.className = 'bubble user';
  userDiv.innerText = text;
  chatBox.appendChild(userDiv);
  
  input.value = '';

  setTimeout(() => {
    const aiDiv = document.createElement('div');
    aiDiv.className = 'bubble ai';
    aiDiv.innerText = `Trợ lý AI mô phỏng – chưa kết nối LLM/RAG.`;
    chatBox.appendChild(aiDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }, 600);

  chatBox.scrollTop = chatBox.scrollHeight;
}

// RENDER LẦN ĐẦU KHI TRANG LOAD
window.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initCompanyList();
  initOrUpdateChart(companyData["ABC"].healthSeries, companyData["ABC"].riskSeries);
  handleRouter();
});