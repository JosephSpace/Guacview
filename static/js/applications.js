document.addEventListener('DOMContentLoaded', function() {
    // Tüm başlatma butonlarını seçelim
    const startButtons = document.querySelectorAll('.start-app');
    const stopButtons = document.querySelectorAll('.stop-app');
    
    // Başlatma butonlarına tıklama olayı ekleyelim
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const appId = this.getAttribute('data-app-id');
            const appPath = this.getAttribute('data-app-path');
            
            // API'ye istek gönderelim
            fetch('/api/start-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    app_id: appId,
                    app_path: appPath
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Başarılı ise butonları güncelle
                    this.disabled = true;
                    const stopButton = document.querySelector(`.stop-app[data-app-id="${appId}"]`);
                    stopButton.disabled = false;
                    
                    // Durum göstergesini güncelle
                    const statusBadge = this.closest('.card-body').querySelector('.badge');
                    statusBadge.textContent = 'Çalışıyor';
                    statusBadge.classList.remove('badge-secondary');
                    statusBadge.classList.add('badge-success');
                    
                    // Eğer HTML dosyası varsa, otomatik olarak açalım
                    if (data.html_path) {
                        window.open(data.html_path, '_blank');
                    }
                    // Adres uyarısını kaldırdık, artık alert çıkmayacak
                } else {
                    alert('Uygulama başlatılamadı: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Hata:', error);
                alert('Bir hata oluştu. Lütfen tekrar deneyin.');
            });
        });
    });
    
    // Durdurma butonlarına tıklama olayı ekleyelim
    stopButtons.forEach(button => {
        button.addEventListener('click', function() {
            const appId = this.getAttribute('data-app-id');
            
            // API'ye istek gönderelim
            fetch('/api/stop-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    app_id: appId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Başarılı ise butonları güncelle
                    this.disabled = true;
                    const startButton = document.querySelector(`.start-app[data-app-id="${appId}"]`);
                    startButton.disabled = false;
                    
                    // Durum göstergesini güncelle
                    const statusBadge = this.closest('.card-body').querySelector('.badge');
                    statusBadge.textContent = 'Kapalı';
                    statusBadge.classList.remove('badge-success');
                    statusBadge.classList.add('badge-secondary');
                } else {
                    alert('Uygulama durdurulamadı: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Hata:', error);
                alert('Bir hata oluştu. Lütfen tekrar deneyin.');
            });
        });
    });
});