// Chart.js kütüphanesini kullanarak grafikleri oluşturacak ve güncelleyecek script

// Grafik nesnelerini global olarak tanımlayalım
let cpuChart;
let nfsStorageChart;
let localStorageChart;

// Sayfa yüklendiğinde çalışacak fonksiyon
document.addEventListener('DOMContentLoaded', function() {
    // CPU kullanımı grafiği için canvas elementini alalım
    const cpuCtx = document.getElementById('myChart').getContext('2d');
    
    // CPU grafiği için veri yapısını oluşturalım
    const cpuData = {
        labels: Array(60).fill(''),  // 60 saniyelik veri için boş etiketler
        datasets: [{
            label: 'CPU Kullanımı (%)',
            data: Array(60).fill(0),  // Başlangıçta tüm değerler 0
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            fill: false
        }]
    };
    
    // CPU grafiğini oluşturalım
    cpuChart = new Chart(cpuCtx, {
        type: 'line',
        data: cpuData,
        options: {
            responsive: true,
            animation: false,  // Animasyonu kapatalım, daha hızlı güncelleme için
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,  // CPU kullanımı %0-100 arasında
                    title: {
                        display: true,
                        text: 'CPU Kullanımı (%)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Zaman (saniye)'
                    }
                }
            }
        }
    });
    
    // NFS Storage (Network) grafiği için canvas elementini alalım
    const nfsCtx = document.getElementById('myPieChart1').getContext('2d');
    
    // NFS Storage grafiğini oluşturalım - doughnut tipinde (depolama grafiğiyle aynı tasarımda)
    nfsStorageChart = new Chart(nfsCtx, {
        type: 'doughnut',
        data: {
            labels: ['Gönderilen Veri (MB)', 'Alınan Veri (MB)'],
            datasets: [{
                data: [0, 0],  // Başlangıçta değerler 0
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',  // Doughnut deliğinin boyutunu ayarlayalım
            plugins: {
                title: {
                    display: true,
                    text: 'Ağ Kullanımı (MB)'
                },
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((acc, data) => acc + data, 0);
                            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                            return `${label}: ${value.toFixed(2)} MB (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
    
    // Local Storage (Depolama) grafiği için canvas elementini alalım
    const localStorageCtx = document.getElementById('myPieChart2').getContext('2d');
    
    // Local Storage (Depolama) grafiğini oluşturalım - doughnut tipinde
    localStorageChart = new Chart(localStorageCtx, {
        type: 'doughnut',
        data: {
            labels: ['Kullanılan Depolama (GB)', 'Boş Depolama (GB)'],
            datasets: [{
                data: [0, 0],  // Başlangıçta değerler 0
                backgroundColor: [
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            cutout: '70%',  // Doughnut deliğinin boyutunu ayarlayalım
            plugins: {
                title: {
                    display: true,
                    text: 'Depolama Alanı Kullanımı (GB)'
                },
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((acc, data) => acc + data, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value.toFixed(2)} GB (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
    
    // Verileri güncellemek için fonksiyonu çağıralım
    updateSystemStats();
    
    // Aktif bağlantı sayısını güncelleyelim
    updateActiveConnections();
    
    // Her saniye verileri güncelleyelim
    setInterval(updateSystemStats, 1000);
    setInterval(updateActiveConnections, 1000);
}); // Close DOMContentLoaded event listener


// Sistem istatistiklerini güncelleyen fonksiyon
function updateSystemStats() {
    fetch('/api/system-stats')
        .then(response => response.json())
        .then(data => {
            // CPU grafiğini güncelleyelim
            const cpuAvg = data.cpu.average;
            cpuChart.data.datasets[0].data.shift();  // İlk elemanı çıkaralım
            cpuChart.data.datasets[0].data.push(cpuAvg);  // Yeni değeri ekleyelim
            cpuChart.update();
            
            // NFS Storage (Network) grafiğini güncelleyelim - doughnut chart formatında
            // Gönderilen ve alınan veri için toplam değerleri ayarlayalım
            nfsStorageChart.data.datasets[0].data = [data.network.sent, data.network.received];
            
            nfsStorageChart.update();
            
            // Local Storage (Depolama) grafiğini güncelleyelim
            const diskUsed = data.disk.used;
            const diskFree = data.disk.total - data.disk.used;
            localStorageChart.data.datasets[0].data = [diskUsed, diskFree];
            localStorageChart.update();
        })
        .catch(error => console.error('Sistem istatistikleri alınırken hata oluştu:', error));
}

// Aktif bağlantı sayısını güncelleyen fonksiyon
function updateActiveConnections() {
    fetch('/api/active-connections')
        .then(response => response.json())
        .then(data => {
            // Aktif bağlantı sayısını güncelleyelim
            document.getElementById('active_conns').textContent = data.active_connections;
        })
        .catch(error => console.error('Aktif bağlantı sayısı alınırken hata oluştu:', error));
}