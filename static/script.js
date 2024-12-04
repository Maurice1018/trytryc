// 儲存目前排序狀態
let sortBy = '運動中心';
let ascending = true;

// 動態加載運動場地資料
async function loadSportsData() {
    try {
        const response = await fetch('/data/'); // 從 API 獲取 JSON 資料
        const result  = await response.json();
        const data = result.items; // 資料列表
        const lastUpdated = result.update_time; // 最後更新時間

        // 更新最後更新時間到頁面
        document.getElementById('last-updated').textContent = `最後資料更新時間：${lastUpdated}`;

	// 排序資料
        data.sort((a, b) => {
            if (a[sortBy] < b[sortBy]) return ascending ? -1 : 1;
            if (a[sortBy] > b[sortBy]) return ascending ? 1 : -1;
            return 0;
        });

        const tableBody = document.getElementById('sports-table');
        tableBody.innerHTML = ''; // 清空表格

        // 遍歷資料並插入到表格
        data.forEach(item => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${item.運動中心}</td>
                <td>${item.運動種類}</td>
                <td>${item.場地}</td>
                <td>${item.日期}</td>
                <td>${item.時間}</td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading sports data:', error);
    }
}

// 排序功能，當點擊欄位標題時觸發
function sortData(column) {
    // 如果點擊相同欄位，反轉排序方向
    if (sortBy === column) {
        ascending = !ascending;
    } else {
        sortBy = column;
        ascending = true;  // 默認為升冪
    }
    loadSportsData();
}

document.addEventListener('DOMContentLoaded', loadSportsData);

// 設定點擊表頭時觸發排序
document.querySelectorAll('th').forEach(th => {
    th.addEventListener('click', () => sortData(th.textContent.trim()));
});
