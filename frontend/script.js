document.getElementById("btn-run").addEventListener("click", function() {
    const btn = this;
    const originalText = btn.innerText;
    
    // Ubah tampilan tombol saat proses berjalan
    btn.innerText = "Running All Scenarios...";
    btn.disabled = true;

    fetch("http://127.0.0.1:8000/run-test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(dataArray => {
        // dataArray sekarang berisi kumpulan banyak laporan (Array)
        
        const metricTotal = document.getElementById("metric-total");
        const metricPass = document.getElementById("metric-pass");
        const metricFail = document.getElementById("metric-fail");
        const tableBody = document.getElementById("table-body");

        // Membalik urutan array agar saat di-prepend, skenario pertama (Registrasi) 
        // tetap berada di bawah skenario kedua (Login) secara kronologis
        dataArray.reverse().forEach(data => {
            // 1. Update Angka Metrik
            metricTotal.innerText = parseInt(metricTotal.innerText) + 1;

            if (data.status === "PASS") {
                metricPass.innerText = parseInt(metricPass.innerText) + 1;
            } else if (data.status === "FAIL" || data.status === "ERROR") {
                metricFail.innerText = parseInt(metricFail.innerText) + 1;
            }
            // Jika status SKIPPED, kita hanya menambah Total, tidak menambah Pass/Fail

            // 2. Tambah Baris Baru ke Tabel (Sekaligus memperbaiki urutan kolom)
            const newRow = document.createElement("tr");
            const waktuSekarang = new Date().toLocaleTimeString('id-ID');
            
            let warnaStatus = "var(--text-color)"; // warna default
            if (data.status === "PASS") warnaStatus = "var(--pass)";
            if (data.status === "FAIL" || data.status === "ERROR") warnaStatus = "var(--fail)";
            if (data.status === "SKIPPED") warnaStatus = "gray";

            newRow.innerHTML = `
                <td>${data.id}</td>
                <td>${data.modul}</td>
                <td>${waktuSekarang}</td>
                <td style="color: ${warnaStatus}; font-weight: bold;">${data.status}</td>
                <td>${data.message}</td>
            `;
            
            tableBody.prepend(newRow);
        });
        
        // Kembalikan tombol ke keadaan semula
        btn.innerText = originalText;
        btn.disabled = false;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Gagal terhubung ke server. Pastikan terminal Uvicorn masih menyala.");
        btn.innerText = originalText;
        btn.disabled = false;
    });
});